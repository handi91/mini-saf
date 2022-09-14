from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = 'minisaf.student'
    _description = 'An active student of the faculty'

    name = fields.Char(string='Name', required=True)
    nim = fields.Char(string='NIM', required=True)

    @api.model
    def generate_year_selection(self):
        '''This is a static method that generate year selection based on current year'''
        curr_year = fields.Date.today().year
        return [(str(i),str(i)) for i in range(curr_year-5, curr_year+1)]

    generation = fields.Selection(
        selection=generate_year_selection,
        string='Generation',
        required=True)
    active_term = fields.Integer(
        compute='_compute_active_term',
        string='Active Term')
    total_credit_passed = fields.Integer(
        string='Total Credits',
        compute='_compute_total_credits')
    gpa = fields.Float(
        string='GPA',
        digits=(12,2),
        compute='_compute_gpa')
    academic_lecturer_id = fields.Many2one(
        comodel_name='minisaf.lecturer',
        string='Academic advisor lecturer')
    courseplan_ids = fields.One2many(
        comodel_name='minisaf.courseplan',
        inverse_name='student_id', 
        string='Course Plan History')
    
    _sql_constraints = [
        ('unique_nim', 'unique(nim)', 'NIM must be unique')
    ]
    @api.depends('generation')
    def _compute_active_term(self):
        curr_year = fields.Date.today().year
        curr_month = fields.Date.today().month
        for rec in self:
            rec.active_term = 0
            if rec.generation:
                term_diff = (curr_year - int(rec.generation))*2
                rec.active_term = term_diff if curr_month < 7 else term_diff + 1    

    @api.depends('courseplan_ids')
    def _compute_total_credits(self):
        for rec in self:
            credits_sum = 0
            hist = self.env['minisaf.courseplan'].search([('student_id','=',rec.id)])
            for cp in hist:
                credits_sum += cp.total_credits
            rec.total_credit_passed = credits_sum
    
    @api.depends('courseplan_ids', 'total_credit_passed')
    def _compute_gpa(self):
        for rec in self:
            rec.gpa = 0
            if rec.total_credit_passed:
                hist = self.env['minisaf.courseplan'].search([('student_id','=',rec.id)])
                grade_sum = 0
                for cp in hist:
                    grade_sum += sum(self.env['minisaf.coursegrade']\
                                        .search([('courseplan_id','=',cp.id)])\
                                        .mapped('total_grade'))
                rec.gpa = grade_sum / rec.total_credit_passed

    @api.constrains('nim')
    def validate_nim(self):
        for rec in self:
            if rec.nim[0:2] != str(rec.generation)[-2:]:
                raise ValidationError(
                    f"{rec.generation}'s generation must have nim start with \"{str(rec.generation)[-2:]}\""
                    )
            try:
                nim_num = int(rec.nim)
            except:
                raise ValidationError('NIM must contains only numbers')
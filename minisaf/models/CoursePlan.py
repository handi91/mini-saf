from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CoursePlan(models.Model):
    _name = 'minisaf.courseplan'
    _description = 'Course plan history for specific student in a term'
    _rec_name = 'student_id'

    term = fields.Integer(string="Term", required=True, readonly=True, default=0)
    total_credits = fields.Integer(
        compute='_compute_total_credits',
        string='Total Credits')
    gpap = fields.Float(
        compute='_compute_gpap',
        digits=(12,2),
        string='GPA Period')
    student_id = fields.Many2one(
        comodel_name='minisaf.student',
        string='Student',
        required=True,
        ondelete='cascade')
    coursegrade_ids = fields.One2many(
        comodel_name='minisaf.coursegrade',
        inverse_name='courseplan_id',
        string='Grade Detail')
    state = fields.Selection(
        string='Status', 
        selection=[
            ('draft', 'Draft'),
            ('accepted', 'Accepted'),
            ],
        required=True,
        readonly=True,
        default='draft')
    
    def accept_draft(self):
        self.write({'state': 'accepted'})
    
    @api.onchange('student_id')
    def _onchange_term(self):
        if self.student_id:
            student_obj = self.env['minisaf.student']\
                            .search([('id','=', self.student_id.id)])
            t = len(self.env['minisaf.courseplan']\
                        .search([('student_id','=',student_obj.id)])\
                        .mapped('term'))
            self.term = t+1
        
    @api.depends('coursegrade_ids','total_credits')
    def _compute_gpap(self):
        for rec in self:
            rec.gpap = 0
            if rec.total_credits:
                grade_sum = sum(self.env['minisaf.coursegrade']\
                            .search([('courseplan_id','=',rec.id)])\
                            .mapped('total_grade'))
                rec.gpap = grade_sum / rec.total_credits

    @api.depends('coursegrade_ids')
    def _compute_total_credits(self):
        for rec in self:
            credits_sum = sum(self.env['minisaf.coursegrade']\
                            .search([('courseplan_id', '=', rec.id)])\
                            .mapped('course_credits'))
            rec.total_credits = credits_sum

    @api.model
    def create(self, vals):
        obj = super(CoursePlan, self).create(vals)
        student_obj = self.env['minisaf.student']\
                        .search([('id','=', obj.student_id.id)])
        t = len(self.env['minisaf.courseplan']\
                    .search([('student_id','=',student_obj.id)])\
                    .mapped('term'))
        obj.write({'term': t})
        return obj
    
    def unlink(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise ValidationError("You can't delete this record cause the status is accepted")
        if self.coursegrade_ids:
            for rec in self:
                grd = self.env['minisaf.coursegrade']\
                        .search([('courseplan_id', '=', rec.id)])
                grd.unlink()
        return super().unlink()


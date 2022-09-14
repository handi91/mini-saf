from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Course(models.Model):
    _name = 'minisaf.course'
    _description = 'An available course of the faculty'

    name = fields.Char(string='Course Name', required=True)
    code = fields.Char(string='Course Code', required=True)
    credits = fields.Integer(string='Credits', required=True)
    courseclass_ids = fields.One2many(
        comodel_name='minisaf.courseclass',
        inverse_name='course_id',
        string='Opened Classes')


class CourseClass(models.Model):
    _name = 'minisaf.courseclass'
    _description = 'An available class of a course that students can enroll'

    name = fields.Char(compute='_compute_name', string='Name')
    class_code = fields.Char(string='Class Code', required=True)
    course_id = fields.Many2one(
        comodel_name='minisaf.course',
        string='Course',
        required=True,
        ondelete='cascade')
    lecturer_id = fields.Many2one(
        comodel_name='minisaf.lecturer',
        string='Teaching Lecturer')
    participant_number = fields.Integer(
        string='Number of Participant',
        required=True,
        readonly=True,
        default=0)
    
    _sql_constraints = [
        ('unique_classcode', 'unique(course_id, class_code)', 'This class not available')
    ]

    @api.onchange('course_id')
    def _onchange_class_code(self):
        available_class = ['A','B','C','D','E','F']
        for record in self:
            tmp = record.course_id.courseclass_ids
            print(len(tmp))
            try:
                record.class_code = available_class[len(tmp)]
            except:
                raise ValidationError("There are already 6 classes of this course, you can't add more")
        
    @api.depends('course_id', 'class_code')
    def _compute_name(self):
        for rec in self:
            rec.name = ""
            if rec.course_id:
                rec.name = str(rec.course_id.name) + ' - ' + str(rec.class_code)
    
    @api.model
    def get_course_credits(self):
        return self.course_id.credits
    
    
from odoo import api, fields, models


class Lecturer(models.Model):
    _name = 'minisaf.lecturer'
    _description = 'A lecturer of the Faculty'

    name = fields.Char(string='Name', required=True)
    nip = fields.Char(string='NIP', required=True)
    email = fields.Char(string='Email')
    advised_student_ids = fields.One2many(
        comodel_name='minisaf.student',
        inverse_name='academic_lecturer_id',
        string='Advised students')
    courseclass_ids = fields.One2many(
        comodel_name='minisaf.courseclass',
        inverse_name='lecturer_id',
        string='Course Classes')
    
    _sql_constraints = [
        ('unique_nip', 'unique(nip)', 'NIP must be unique')
    ]

from odoo import api, fields, models


class AddStudent(models.TransientModel):
    _name = 'minisaf.addstudent'

    def get_default_lecturer(self):
        active_ids = self.env.context.get("active_ids")
        if active_ids:
            return self.env["minisaf.lecturer"].browse(active_ids[0])
        return self.env["minisaf.lecturer"]

    lecturer_id = fields.Many2one(
        comodel_name='minisaf.lecturer',
        string='Lecturer',
        required=True,
        default=get_default_lecturer)
    student_id = fields.Many2one(
        comodel_name='minisaf.student',
        string='Student', 
        domain=[('academic_lecturer_id','=',False)],
        required=True)
    
    
    def add_student_action(self):
        for rec in self:
            self.env['minisaf.student']\
                .search([('id','=',rec.student_id.id)])\
                .write({'academic_lecturer_id': rec.lecturer_id})
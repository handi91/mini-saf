from odoo import api, fields, models


class AddClass(models.TransientModel):
    _name = 'minisaf.addclass'

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
    courseclass_id = fields.Many2one(
        comodel_name='minisaf.courseclass',
        string='Class', 
        domain=[('lecturer_id','=',False)],
        required=True)
    
    
    def add_class_action(self):
        for rec in self:
            self.env['minisaf.courseclass']\
                .search([('id','=',rec.courseclass_id.id)])\
                .write({'lecturer_id': rec.lecturer_id})
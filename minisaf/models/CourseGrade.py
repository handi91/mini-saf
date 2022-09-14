from odoo import api, fields, models


class CourseGrade(models.Model):
    _name = 'minisaf.coursegrade'
    _description = 'A detail of the grade of a course taken.'

    name = fields.Char(string='Name')
    num_grade = fields.Float(string="Number Grade", required=True)
    letter_grade = fields.Char(compute='_compute_letter_grade', string="Letter Grade")
    total_grade = fields.Float(
        compute='_compute_total_grade',
        string="Total",
        digits=(12,2))
    courseclass_id = fields.Many2one(
        comodel_name='minisaf.courseclass',
        string='Course Class',
        ondelete='cascade')
    courseplan_id = fields.Many2one(
        comodel_name='minisaf.courseplan',
        string='minisaf.courseplan',
        ondelete='cascade')
    course_credits = fields.Integer(compute='_compute_course_credits', string='Credits')
    
    @api.depends('courseclass_id')
    def _compute_course_credits(self):
        for rec in self:
            rec.course_credits = 0
            if rec.courseclass_id:
                rec.course_credits = rec.courseclass_id.get_course_credits()

    @api.depends('num_grade')
    def _compute_letter_grade(self):
        for rec in self:
            rec.letter_grade = 'E'
            if rec.num_grade:
                if rec.num_grade >= 85:
                    rec.letter_grade = 'A'
                elif rec.num_grade >= 80:
                    rec.letter_grade = 'A-'
                elif rec.num_grade >= 75:
                    rec.letter_grade = 'B+'
                elif rec.num_grade >= 70:
                    rec.letter_grade = 'B'
                elif rec.num_grade >= 65:
                    rec.letter_grade = 'B-'
                elif rec.num_grade >= 60:
                    rec.letter_grade = 'C+'
                elif rec.num_grade >= 55:
                    rec.letter_grade = 'C'
                elif rec.num_grade >= 40:
                    rec.letter_grade = 'D'

    @api.depends('courseclass_id', 'num_grade')
    def _compute_total_grade(self):
        for rec in self:
            rec.total_grade = 0
            if rec.num_grade and rec.courseclass_id:
                credits = rec.courseclass_id.get_course_credits()
                if rec.num_grade >= 85:
                    rec.total_grade = 4.0 * credits
                elif rec.num_grade >= 80:
                    rec.total_grade = 3.7 * credits
                elif rec.num_grade >= 75:
                    rec.total_grade = 3.3 * credits
                elif rec.num_grade >= 70:
                    rec.total_grade = 3.0 * credits
                elif rec.num_grade >= 65:
                    rec.total_grade = 2.7 * credits
                elif rec.num_grade >= 60:
                    rec.total_grade = 2.3 * credits
                elif rec.num_grade >= 55:
                    rec.total_grade = 2.0 * credits
                elif rec.num_grade >= 40:
                    rec.total_grade = 1.0 * credits
    
    @api.model
    def create(self, vals):
        obj = super(CourseGrade, self).create(vals)
        if obj.courseclass_id:
            self.env['minisaf.courseclass']\
                .search([('id', '=', obj.courseclass_id.id)])\
                .write({'participant_number': obj.courseclass_id.participant_number + 1})
        return obj

    def unlink(self):
        for rec in self:
            if rec.courseclass_id:
                self.env['minisaf.courseclass']\
                    .search([('id', '=', rec.courseclass_id.id)])\
                    .write({'participant_number': rec.courseclass_id.participant_number - 1})
        return super(CourseGrade, self).unlink()
    

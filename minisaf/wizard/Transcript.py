from odoo import api, fields, models


class Transcript(models.TransientModel):
    _name = 'minisaf.transcript'

    student_id = fields.Many2one(
        comodel_name='minisaf.student', 
        string='Student',
        required=True)

    def get_transcript(self):
        student_id = self.student_id
        filter = [('student_id', '=', student_id.id)]
        # print(filter)
        course_plans = self.env['minisaf.courseplan'].search_read(filter)
        # print(course_plans)
        for plan in course_plans:
            course_grade = self.env['minisaf.coursegrade']\
                            .search_read([('courseplan_id','=',plan['id'])])
            plan['course_grade'] = course_grade

        # print(course_plans)
        student_info = self.env['minisaf.student'].search_read([('id', '=', student_id.id)])
        print(student_info)
        data = {
            'student': student_info[0],
            'courseplans': course_plans,
        }
        print(data)
        return self.env.ref('minisaf.wizard_report_transcript_pdf').report_action(self, data=data)

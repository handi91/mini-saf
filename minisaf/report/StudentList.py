from odoo import models, fields


class LecturerList(models.AbstractModel):
    _name = 'report.minisaf.report_student_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_lap = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, lecturers):
        sheet = workbook.add_worksheet('Lecturers')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'Retrieve Date:', bold)
        sheet.write(0, 1, str(self.tgl_lap))
        sheet.write(2, 0, 'NIM', bold)
        sheet.write(2, 1, 'Name', bold)
        sheet.write(2, 2, 'Generation', bold)
        sheet.write(2, 3, 'Academic Advisor Lecturer', bold)
        sheet.write(2, 4, 'Active Term', bold)
        sheet.write(2, 5, 'Total Credits', bold)
        sheet.write(2, 6, 'GPA', bold)
        row = 3
        max = 0
        for obj in lecturers:
            sheet.write(row, 0, obj.nim)
            sheet.write(row, 1, obj.name)
            sheet.write(row, 2, obj.generation)
            sheet.write(row, 3, obj.academic_lecturer_id.name)
            sheet.write(row, 4, obj.active_term)
            sheet.write(row, 5, obj.total_credit_passed)
            sheet.write(row, 6, obj.gpa)
            row += 1
            
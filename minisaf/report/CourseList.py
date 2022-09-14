from odoo import models, fields


class CourseList(models.AbstractModel):
    _name = 'report.minisaf.report_course_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_lap = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, courses):
        sheet = workbook.add_worksheet('Courses')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'Retrieve Date:', bold)
        sheet.write(0, 1, str(self.tgl_lap))
        sheet.write(2, 0, 'Course Name', bold)
        sheet.write(2, 1, 'Course Code', bold)
        sheet.write(2, 2, 'Credits(SKS)', bold)
        row = 3
        max = 0
        for obj in courses:
            sheet.write(row, 0, obj.name)
            sheet.write(row, 1, obj.code)
            sheet.write(row, 2, obj.credits)
            row += 1
            
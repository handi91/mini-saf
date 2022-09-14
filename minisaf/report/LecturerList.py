from odoo import models, fields


class LecturerList(models.AbstractModel):
    _name = 'report.minisaf.report_lecturer_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_lap = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, lecturers):
        sheet = workbook.add_worksheet('Lecturers')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'Retrieve Date:', bold)
        sheet.write(0, 1, str(self.tgl_lap))
        sheet.write(2, 0, 'Name', bold)
        sheet.write(2, 1, 'NIP', bold)
        sheet.write(2, 2, 'Email', bold)
        row = 3
        max = 0
        for obj in lecturers:
            sheet.write(row, 0, obj.name)
            sheet.write(row, 1, obj.nip)
            sheet.write(row, 2, obj.email)
            row += 1
            
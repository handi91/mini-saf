# -*- coding: utf-8 -*-
# from odoo import http


# class Minisaf(http.Controller):
#     @http.route('/minisaf/minisaf', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/minisaf/minisaf/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('minisaf.listing', {
#             'root': '/minisaf/minisaf',
#             'objects': http.request.env['minisaf.minisaf'].search([]),
#         })

#     @http.route('/minisaf/minisaf/objects/<model("minisaf.minisaf"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('minisaf.object', {
#             'object': obj
#         })

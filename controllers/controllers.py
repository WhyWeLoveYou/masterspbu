# -*- coding: utf-8 -*-
# from odoo import http


# class MasterSpbu(http.Controller):
#     @http.route('/master_spbu/master_spbu', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/master_spbu/master_spbu/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('master_spbu.listing', {
#             'root': '/master_spbu/master_spbu',
#             'objects': http.request.env['master_spbu.master_spbu'].search([]),
#         })

#     @http.route('/master_spbu/master_spbu/objects/<model("master_spbu.master_spbu"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('master_spbu.object', {
#             'object': obj
#         })

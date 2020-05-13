# -*- coding: utf-8 -*-
# from odoo import http


# class My-fact(http.Controller):
#     @http.route('/my-fact/my-fact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my-fact/my-fact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('my-fact.listing', {
#             'root': '/my-fact/my-fact',
#             'objects': http.request.env['my-fact.my-fact'].search([]),
#         })

#     @http.route('/my-fact/my-fact/objects/<model("my-fact.my-fact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my-fact.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Course(models.Model):
      _name = 'openacademy.course'
      _description = 'Model to store course'

      name = fields.Char(String="Title", required=True)
      description = fields.Text()
      responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True)
      session_ids = fields.One2many('openacademy.session', 'course_id')
      
class Session(models.Model):
      _name = 'openacademy.session'
      _description = 'Model to store sessions'

      name = fields.Char(required=True)
      start_date = fields.Date()
      duration = fields.Float(digits=(6, 2), help="Duration in days")
      seats = fields.Integer(string="Number of seats")
      instructor_id = fields.Many2one('res.partner', string="Instructor", domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'Teacher')])
      course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
      attendee_ids = fields.Many2many('res.partner', string="Attendees")
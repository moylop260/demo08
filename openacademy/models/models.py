# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import time

def get_uid(self, *a):
    return self.env.uid
   #return self.env.user.name      NO
   #return self.env.user.uid    Funcionan
   #return self.env.user.id    no se porque

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Clase o modulo para definir cursos'
        
    name = fields.Char(string="Title-F", required=True)
    description = fields.Text()
   #responsible_id = fields.Many2one('res.users', string="Responsible", index=True, ondelete='set null')
    responsible_id = fields.Many2one('res.users', string="Responsible", index=True, ondelete='set null', 
       #default= lambda self, *a: self.env.uid)
       default= get_uid)
    session_ids = fields.One2many('openacademy.session', 'course_id')

    #@api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]

    def copy(self, default=None):
        if default is None:
            default = {}
        copied_count = self.search_count([
            ('name', 'ilike', "Copy of %s%%" % (self.name))])
        if not copied_count:
            new_name = "Copy of %s" % (self.name)
        else:
            new_name = "Copy of %s (%s)"% (self.name, copied_count)
       #default['name'] = self.name + ' otro'
        default['name'] = new_name
        return super(Course, self).copy(default)


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Clase o modulo para definir Sessions'   
       
    name = fields.Char(required=True)
   #start_date = fields.Date()
    start_date = fields.Date(default=fields.Date.today)
    #datetime_test = fields.Datetime(default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    datetime_test = fields.Datetime(default=fields.Datetime.now)
    duration = fields.Float(digits=(6,2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)

    instructor_id = fields.Many2one('res.partner', string='Instructor', domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    #taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    taken_seats = fields.Float(compute='_taken_seats')
    active = fields.Boolean(default=True)

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        #import pdb; pdb.set_trace()
        #for r in self.filtered(lambda r: r.seats):
        #        r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
       #if self.seats < 0:
        if self.filtered(lambda r: r.seats < 0):
            self.active = False
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            self.active = False
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }
        self.active = True


    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
       #for r in self:
        for r in self.filtered("instructor_id"):
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")            
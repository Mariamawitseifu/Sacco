# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.

# import base64
# from pytz import timezone, UTC
# from datetime import datetime, time
# from random import choice
# from string import digits
# from werkzeug.urls import url_encode
# from dateutil.relativedelta import relativedelta
# from markupsafe import Markup

# from odoo import api, fields, models, _
# from odoo.exceptions import ValidationError, AccessError
# from odoo.osv import expression
# from odoo.tools import format_date
from datetime import timedelta, datetime
from odoo import api, fields, models, _

class SaccoEmployee(models.Model):
    _name = "sacco.employee.registration"
    _description = "Employee"
    _rec_name= 'employee'
    

    # name = fields.Char(string="Employee Name", store=True, readonly=False, tracking=True)
    employee=fields.Many2one(comodel_name="hr.employee",string="Employee Name", required=True)
    father_fullname=fields.Char(string="Fathers full name")
    age = fields.Char(string=" Age")
    place_of_birth = fields.Char('Place of Birth', tracking=True)
    image = fields.Binary(string="Image")
    id_card = fields.Binary(string="ID Card Copy")
    driving_license = fields.Binary(string="Driving License")
    region = fields.Selection([
                            ('addisababa', 'Addis Ababa'),
                            ('amhara', 'Amhara'),
                            ('oromia', 'Oromia'),
                            ('tigray', 'Tigray'),
                            ('amhara', 'Amhara'),
                            ('amhara', 'Amhara'),
                            ('amhara', 'Amhara'),
                            ('amhara', 'Amhara'),
                            ('amhara', 'Amhara')
                            ])
    zone= fields.Char(string="Zone")
    wereda=fields.Char(string="Wereda")
    akababi=fields.Char(string="Akababi")
    kebele=fields.Char(string="Kebele")
    house_no=fields.Char(string="House Number")
    full_date = fields.Datetime(string="Registration Date")
    city=fields.Char(string="City",tracking=True)
    kifle_ketema=fields.Char(string="Kifle Ketema")
    current_kebele=fields.Char(string="Kebele")
    current_house_no=fields.Char(string="House Number")
    # models.PhoneNumberField(_("phone number"))
    zip=fields.Char("Postal Code")
    phone_number=fields.Integer("Phone")
    kebele_id_number=fields.Integer("Kebele Id Number")
    mahber_id_number=fields.Integer("Mahber Id Number")
    date_of_membership=fields.Datetime("Date Of Members")
    fee_amount=fields.Integer("Fee Amount")
    lotto_number=fields.Integer("Lotto Number")
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', default='single', tracking=True)
    spouse_fullname=fields.Char("Spouse Full Name")
    emergency_contact = fields.Char("Contact Name", groups="hr.group_hr_user", tracking=True)
    emergency_phone = fields.Char("Contact Phone", groups="hr.group_hr_user", tracking=True)
    children = fields.Integer(string='Number of Children', tracking=True)
    # In your model

    
    child_ids = fields.One2many('sacco.employee.child', 'parent_id', string='Children')
    child_count = fields.Integer(compute='_compute_child_count')
   
    @api.depends('child_ids')
    def _compute_child_count(self):
        for record in self:
            record.child_count = len(record.child_ids)

    children_list_ids = fields.One2many('parent.children', 'children_list_id', string='Children list')
    inheriters_list_ids = fields.One2many('parentinheritence.children', 'inheriters_list_id', string='inheriters')
    emergency_list_ids = fields.One2many('parentemergency.children', 'emergency_list_id', string='emergency')
    spouse_complete_name = fields.Char(string="Spouse Complete Name", groups="hr.group_hr_user", tracking=True)
    private_phone = fields.Char(string="Private Phone", groups="hr.group_hr_user")
    birthday = fields.Date('Date of Birth', groups="hr.group_hr_user", tracking=True)
    saving_ids = fields.One2many(
        comodel_name="saving.for",
        inverse_name="employee_id",
        string="Savings"
    )
    # savings_model_ids = fields.One2many(
    #     comodel_name="savings.model",
    #     # inverse_name="employees_id",
    #     string="Savings"
    # )
    
class SaccoEmployeeChild(models.Model):
    _name = 'sacco.employee.child'

    # This is the Many2one field in the target model
    parent_id = fields.Many2one('sacco.employee.registration', string='Parent Employee')

class parent (models.Model):
  
    _name='parent.children'
    _description ='list of the children'
    
    children_list_id = fields.Many2one(
        'sacco.employee.registration',
        string='Childrens',
        )
    child_name = fields.Char(string='Child Name')
    child_age = fields.Integer(string='Age')
    child_sex = fields.Selection([('female', 'Female'),
                                  ('male', 'Male')
                                  ], string="Sex")
    
    
class parentinheritence (models.Model):
  
    _name='parentinheritence.children'
    _description ='list of the children'
    inheriters_list_id = fields.Many2one(
        'sacco.employee.registration',
        )
    inheriters_fullname = fields.Char(string='Inheriter Name')
    inheriters_ketema = fields.Char(string='Ketema')
    inheriters_zone=fields.Char(string='Zone')
    inheriters_wereda=fields.Integer(string='K/Ketema')
    inheriters_kebele=fields.Integer(string='Kebele')
    inheriters_house_no=fields.Integer(string='House_No')
    inheriters_job_position=fields.Char(string='Job Position')
    inheriters_phone_no=fields.Integer(string='Phone No')
    
class parentemergency (models.Model):
  
    _name='parentemergency.children'
    _description ='list of the children'
    emergency_list_id = fields.Many2one(
        'sacco.employee.registration',
        )
    emergency_fullname = fields.Char(string='Name')
    emergency_ketema = fields.Char(string='Ketema')
    emergency_zone=fields.Char(string='Zone')
    emergency_wereda=fields.Integer(string='K/Ketema')
    emergency_kebele=fields.Integer(string='Kebele')
    emergency_house_no=fields.Integer(string='House_No')
    emergency_job_position=fields.Char(string='Job Position')
    emergency_phone_no=fields.Integer(string='Phone No')
    
    
    
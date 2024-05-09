from odoo import api, fields, models, _

class SelfService (models.Model):
    _name = "guarantee.request"
    _description = "Requesting to be guarantee"
    
    
    for_employee = fields.Char(string="Employee")
    guarantee = fields.Char(string="Guarantee For")
    request_date = fields.Datetime(string="Request Date")
    reason = fields.Char(string="Reason")


class LoanRequest (models.Model):
    _name = "loan.request"
    _description = "Requesting for loan"
    

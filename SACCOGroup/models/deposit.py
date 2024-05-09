from odoo import api, fields, models

class Saccodeposit (models.Model):
    _name =  "sacco.deposit"
    _description = " Deposit for SACCO"
    
    
    customer_name= fields.Char(string="Employee Name")
    date = fields.Datetime(string="Date of Deposit")
    amount = fields.Integer(string="Amount")
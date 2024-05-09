from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Savings(models.Model):
    _name = "savings.model"
    _inherit = "sacco.employee.registration"
    _description = "savings info"
    _rec_name= 'customer_name'
    
    customer_name = fields.Many2one( comodel_name="share.member.inherit",string="Savings")
    # customer_name = fields.Many2one(string="Customer Name")
    cumulative_amount = fields.Float(string="Cumulative amount", compute='_compute_cumulative_amount')
    savings_child_ids = fields.One2many('savings.child.model', 'savings_member_id', string="Saving Model Records")
    employees_id = fields.Many2one(
        comodel_name="sacco.employee.registration",
        string="Employee"
    )
    
    @api.depends('savings_child_ids.amount')
    def _compute_cumulative_amount(self):
        for record in self:
            record.cumulative_amount = sum(record.savings_child_ids.mapped('amount'))

class ChildModel(models.Model):
    _name = 'savings.child.model'
    _description = 'Child Model of savings'
    
    date = fields.Datetime(string="Date")
    amount = fields.Integer(string="Amount")
    saving_type = fields.Selection([('regular', 'Regular'),('willing','By Will')])
    savings_member_id = fields.Many2one('savings.model', string='Savings')


class Savingfor(models.Model):
    _name = "saving.for"
    _description = "saving for what? the interest compound and tax"
    
    name = fields.Char(string="Name", required=True)
    savingneed = fields.Selection([('deposit', 'Deposit'),('loan','Loan')], string="Saving For", required=True)
    interest = fields.Integer(string="Interest")
    compound = fields.Boolean(string="Compound")
    with_interest = fields.Boolean(string="With Interest")
    tax_interest = fields.Integer(string="Tax Interest")
    employee_id = fields.Many2one(
        comodel_name="sacco.employee.registration",
        string="Employee"
    )
    
    @api.constrains('savingneed')
    def _check_savingneed(self):
        # Check if 'Deposit' has already been selected
        if self.savingneed == 'deposit':
            # Check if there's another record with 'Deposit' already selected
            existing_deposit = self.search([('savingneed', '=', 'deposit'), ('id', '!=', self.id)])
            if existing_deposit:
                raise ValidationError("Deposit has already been selected. Please choose another option.")
class Contractual(models.Model):
    _name = "contractual.customer"
    _description = "contractual customers"
    
    # open and closed 
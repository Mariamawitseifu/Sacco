
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class Loan (models.Model):
    _name="loan"
    _description="loan managment"
    
    loan_amount=fields.Integer(string="Loan Amount")
    loan_statment_number = fields.Integer(string="Loan Statment Number")
    loan_type = fields.Selection([('merchandise term loan', 'Merchandise Term Loan')])
    contract_date =fields.Datetime(string='Contract Date')
    loan_date=fields.Datetime(string='Loan Date')
    payment_start=fields.Datetime(string='Payment Start Date')
    
    payment_years = fields.Float(string='Period in Years')
    repayment_amount=fields.Float(string='Repayment Amount')
    repayment_interval=fields.Integer(string='Repayment Interval')
    annual_interest=fields.Float(string='Annual Interest Rate %')
    total_num_payment=fields.Float(string='Total Number of Payments')
    payment_per_year=fields.Float(string='Payments Per Year')
    overdue=fields.Float(string='Overdue')
    payment_date=fields.Datetime(string='Payment Date')
    next_payments=fields.Datetime(string='Next Payments')
    daily_interest_rate=fields.Float(string='Daily Interest Rate %')
    outstanding_balance=fields.Float(string='Start Outstanding Balance')
    outstanding_interest=fields.Float(string='Start Outstanding Interest')
    opening_date=fields.Datetime(string="Opening Date")
    payment_start_opening = fields.Datetime(string='Payment Start Date', compute='_compute_payment_start_opening')
    member_id = fields.Many2one('share.member.inherit')
    is_running =fields.Boolean(string='is running', compute='_compute_payment_start_opening')
        
    
    
    @api.onchange('repayment_interval', 'loan_date') 
    def _compute_payment_start_opening(self):
        for record in self:
            record.payment_start_opening=datetime.today()
            dt=datetime.today()
            if record.loan_date:
                dt=record.loan_date + relativedelta(months=record.repayment_interval)-relativedelta(days=1)
            record.payment_start_opening = dt
            record.is_running=True 
           
class Chartpost(models.Model):
    _name = 'chart.post'
    _description = 'the loan post field'

    accrued_interest_payable = fields.Float(string='Accrued Interest Payable')
    accrued_interest_recievable=fields.Float(string="Accrued Interest Recievable")
    journal_interest=fields.Float(string='Journal Interest')
    bank=fields.Float(string='Bank')
    disbursment=fields.Float(string='Disbursment')
    journal = fields.Float(string='Journal')
    post=fields.Many2one(string='Post',comodel_name='account.move')
    share_chart_ids = fields.Many2many('child.model', string='Share')
    
    
    def open_post_form(self):
        """Open the form view of the related account.move record."""
        self.ensure_one()  # Ensure we're working with a single record
        if self.post:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Account Move',
                'res_model': 'account.move',
                'res_id': self.post.id,
                'view_mode': 'form',
                'target': 'current',
            }
        else:
            raise ValidationError("No related account.move record found.")

    def compute_postt(self):
        for record in self:
            current_date = datetime.today()

            cday = current_date.date()
            pday=cday
            t=0
            account_recipt = self.env['loan'].search([('id', '=', record.total_number_share.id)])
              
            journal=record.total_number_share
            # account_bank=record.acount_loan_id.account_bank.id
            cash=record.bought_share
            bank=record.total_saving
            lines_vals_list = []

            if  record.value_date:
                pday=record.value_date
            receipt = self.env['account.move'].create(
                                    {'date':pday,'journal_id':journal
                                    ,'ref':record.reference,
                                     })                                    
            if receipt and not record.post:
                t=receipt.id
                lines_vals_list.append({
                    'move_id': t,                   
                    'credit':record.receipt,
                    'account_id': cash                   
                 })
                
                lines_vals_list.append({  
                    'move_id': t,
                    'debit':record.receipt,
                    'account_id': bank 
                 })
                self.env['account.move.line'].create(lines_vals_list)
                record.post=t
    


class ClosingDate(models.Model):
    _name='closing.date'
    _description='closing dates fiscal year'
    
    name=fields.Char(string='Name')
    start_date=fields.Datetime(string='Start Date')
    end_date=fields.Datetime(string='End Date')
    child_period_ids = fields.One2many('child.period', 'closing_id', string="Child Period")

class Period(models.Model):
    _name='child.period'
    _description='Period'
    
    
    name_period=fields.Char(string='Name')
    description=fields.Char(string='Description')
    date_from=fields.Datetime(string='Date From')
    date_to=fields.Datetime(string='Date To')
    closing_id = fields.Many2one('closing.date',string='closing date')
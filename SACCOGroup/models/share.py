from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Share(models.Model):
    _name = 'share.member.inherit'
    _inherit = 'sacco.employee.registration'

    share_name = fields.Char(string="Share Name")
    total_saving = fields.Float(string='Total Saving', compute='_compute_total_saving')
    # cumulative_amount = fields.Float(string="Total Bought Share", default=0.0, compute='_compute_cumulative_amount')
    bought_share = fields.Float(string="Total Bought Share", compute='_compute_bought_share')  # Corrected field name
    percentage = fields.Float(string="Percentage")
    is_employee = fields.Boolean(string="Is Employee")
    is_member = fields.Boolean(string="Is Member")
    total_number_share = fields.Float(string="Total Share Amount", compute='_compute_total_number_share', store=True, default=0.0)

    child_model_ids = fields.One2many('child.model', 'share_member_id', string="Child Model Records")
    child_loan_ids = fields.One2many('loan', 'member_id', string="Loan")
    share_amounts = fields.One2many('share', 'share_id', string="Share Amounts")

    # @api.depends('child_model_ids.bought_share')
    # def _compute_cumulative_amount(self):
    #     for record in self:
    #         cumulative_amount_from_children = sum(record.child_model_ids.bought_share)
    #         record.cumulative_amount = cumulative_amount_from_children

    @api.depends('child_model_ids.number_of_share')
    def _compute_bought_share(self):
        for record in self:
            bought_share = sum(record.child_model_ids.mapped('number_of_share'))
            record.bought_share = bought_share
    @api.depends('child_model_ids.amount')
    def _compute_total_saving(self):
        for record in self:
            total_saving = sum(record.child_model_ids.mapped('amount'))
            record.total_saving = total_saving

    @api.depends('child_model_ids')
    def _compute_total_number_share(self):
        for record in self:
            total_bought_share = sum(record.child_model_ids.mapped('number_of_share'))
            active_share_amount = self.env['share'].search([('state', '=', 'active')], limit=1).share_amount
            record.total_number_share = total_bought_share * active_share_amount if active_share_amount else 0.0

class ChildModel(models.Model):
    _name = 'child.model'
    _description = 'Child Model'

    date = fields.Datetime(string="Date", required=True)
    willing_saving = fields.Float(string="Willing Savings")
    regular_saving = fields.Float(string="Regular Savings")
    share_amount_child = fields.Float(string="Share Amount")
    amount = fields.Integer(string="Savings amount", readonly=True)
    number_of_share = fields.Integer(string="Bought No. of Share")
    share_member_id = fields.Many2one('share.member.inherit', string='Share Member')
    related_share_state = fields.Char(string="Related Share State")
    child_chart_ids = fields.Many2many('chart.post', 'share_chart_ids', string="Child")
    post_chart = fields.Char(compute='_compute_post_chart')

    @api.depends('child_chart_ids')
    def _compute_post_chart(self):
        for record in self:
            # Assuming 'post' is a field on the 'chart.post' model
            # and you want to get the value of 'post' for the first related record
            if record.child_chart_ids:
                record.post_chart = record.child_chart_ids[0].post
            else:
                record.post_chart = False
    # related_post = fields.Many2Many(related='child_chart_ids.post', string='Related Post')
    
    
    # def get_related_post(self):
    #     for record in self:
    #         related_posts = record.child_chart_ids.mapped('post')
    #         if related_posts:
    #             return related_posts[0]
    #     return None
    

    @api.onchange('willing_saving', 'regular_saving', 'share_amount_child')
    def _onchange_share_amount_child(self):
        if self.willing_saving and self.regular_saving:
            self.amount = int(self.willing_saving + self.regular_saving)
            child_records = self.env['child.model'].search([
                ('share_member_id', '=', self.share_member_id.id),
                ('related_share_state', '=', 'active')
            ])
            active_amounts = child_records.mapped('amount')
            if active_amounts:
                remainder = self.share_amount_child % sum(active_amounts)
                self.willing_saving += remainder

            if self.share_amount_child != 0 and self.amount != 0:
                self.number_of_share = self.amount / self.share_amount_child

            if self.share_amount_child != 0:
                active_shares = self.env['share'].search([('state', '=', 'active')])
                if active_shares:
                    active_share_amount = active_shares[0].share_amount
                    number_of_share, remainder = divmod(self.share_amount_child, active_share_amount)
                    self.share_amount_child -= remainder
                    self.number_of_share = int(number_of_share)
                    self.willing_saving += remainder

            self.amount = int(self.willing_saving + self.regular_saving)

        if self.share_member_id:
            share_record = self.env['share.member.inherit'].browse(self.share_member_id.id)
            if share_record and self.amount:
                share_record.cumulative_amount += self.amount
        # return child_record


class Shareamount(models.Model):
    _name = "share"
    _description = "share registered here"

    share_id = fields.Many2one('share.member.inherit', string="Share Amount")
    share_date = fields.Datetime(string="Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], default='draft', string='State')
    share_amount = fields.Integer(string="Share amount")

    @api.constrains('state')
    def _check_active_share_on_write(self):
        """
        Check if there's already an active share before allowing a state change to 'active'.
        """
        if self.state == 'active':
            active_share_exists = self.search_count([('state', '=', 'active')])
            if active_share_exists > 1:
                raise ValidationError("Only one active share is allowed.")
            
 
            
    # @api.depends('repayment_interval', 'loan_date')
    # def _compute_payment_start_opening(self):
    #     for record in self:
    #         if record.repayment_interval and record.loan_date:
    #             loan_date = fields.Datetime.from_string(record.loan_date)
    #             interval = int(record.repayment_interval)
    #             months = interval % 12
    #             years = interval // 12

    #             # Calculate the total number of days
    #             total_days = years * 365 + months * 30
    #             payment_start_opening = contract_date + timedelta(days=total_days)
    #             record.payment_start_opening = payment_start_opening
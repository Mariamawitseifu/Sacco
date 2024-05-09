# from odoo import api, fields, models

# class Saccointerest(models.Model):
#     _name = "sacco.interest"
#     _description = "Interest calculation for savings, loan, and payment"
    
#     yearly_interest = fields.Float(string="Yearly Interest")
#     daily_interest = fields.Float(string="Daily Interest")
#     saving_for_id = fields.Many2one(
#         comodel_name="saving.for",
#         string="Saving For",
#         required=True  # Assuming you want to enforce this relationship
#     )
#     # total_saving = fields.Float(string="Total Savings")  # Assuming this field exists
#     share_id = fields.Many2one(
#         comodel_name="share.member.inherit",
#         string="Share",
#         required=True  # Assuming you want to enforce this relationship
#     )

#     @api.depends('total_saving', 'saving_for_id', 'share_id')
#     def _compute_yearly_interest(self):
#         for record in self:
#             if record.saving_for_id and record.share_id:
#                 interest_rate = record.saving_for_id.interest / 100  # Convert interest to decimal
#                 record.yearly_interest = record.total_saving * interest_rate
#             else:
#                 record.yearly_interest = 0.0

#     def _compute_daily_interest(self):
#         for record in self:
#             record.daily_interest = record.yearly_interest / 365

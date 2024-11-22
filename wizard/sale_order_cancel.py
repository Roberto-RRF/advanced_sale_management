# -*- coding: utf-8 -*-
from odoo import models, api, exceptions, _, fields

class SaleOrderCancel(models.TransientModel):
    _inherit = 'sale.order.cancel'

    def action_cancel(self):
        for inv in self.order_id.invoice_ids:
            if inv.l10n_mx_edi_cfdi_state:
                # Launch the wizard
                return {
                    'name': _('Confirmation'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'sale.order.cancel.confirm.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {
                        'default_order_id': self.order_id.id,
                    }
                }
        # If no invoice has l10n_mx_edi_cfdi_state, proceed with cancellation
        for inv in self.order_id.invoice_ids:
            inv.button_draft()
            inv.button_cancel()
        return self.order_id.with_context(disable_cancel_warning=True).action_cancel()

class SaleOrderCancelConfirmWizard(models.TransientModel):
    _name = 'sale.order.cancel.confirm.wizard'
    _description = 'Wizard to Confirm Sale Order Cancellation'
    
    order_id = fields.Many2one('sale.order', string='Sale Order')

    def confirm_cancellation(self):
        """Executes the cancellation logic after user confirmation."""
        order = self.env['sale.order'].browse(self.order_id.id)
        for inv in order.invoice_ids:
            inv.button_draft()
            inv.button_cancel()
        return order.with_context(disable_cancel_warning=True).action_cancel()

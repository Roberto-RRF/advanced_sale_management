import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_cancel(self):
        if self.env.context.get('force_cancel'):
            _logger.info("Force cancel triggered for Sale Order %s", self.name)
            for inv in order.invoice_ids:
                if not inv.l10n_mx_edi_cfdi_state:
                    inv.button_draft()
                    inv.button_cancel()
            result = super(SaleOrder, self)._action_cancel()

            _logger.info("Sale Order %s state after cancellation attempt: %s", self.name, self.state)
            return result

        for order in self:
            for inv in order.invoice_ids:
                if inv.l10n_mx_edi_cfdi_state == 'sent':
                    return {
                        'name': 'Invoice Warning',
                        'type': 'ir.actions.act_window',
                        'res_model': 'sale.order.invoice.warning',
                        'view_mode': 'form',
                        'target': 'new',
                        'context': {
                            'default_message': _("Esta orden de venta tiene una factura asociada que esta timbrada. ¿Quiere cancelar la orden de venta?"),
                            'active_id': order.id,
                        }
                    }
            for inv in order.invoice_ids:
                if not inv.l10n_mx_edi_cfdi_state:
                    inv.button_draft()
                    inv.button_cancel()
        return super(SaleOrder, self).action_cancel()

from odoo import models, fields, api, _

class SaleOrderInvoiceWarning(models.TransientModel):
    _name = 'sale.order.invoice.warning'
    _description = 'Warning on Cancelling Sale Order with Valid Invoice'

    message = fields.Text(
        string="Message",
        readonly=True,
        default=_("Esta orden de venta tiene una factura asociada que esta timbrada. ¿Quiere cancelar la orden de venta?")
    )

    def action_confirm_cancel(self):
        """Proceed with sale order cancellation."""
        sale_order_id = self.env.context.get('active_id')
        sale_order = self.env['sale.order'].browse(sale_order_id)
        if sale_order:
            # Cancel with force_cancel context to bypass warning
            sale_order.with_context(force_cancel=True).sudo().action_cancel()

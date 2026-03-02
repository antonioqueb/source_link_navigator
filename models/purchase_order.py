from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    source_sale_order_id = fields.Many2one(
        'sale.order',
        string='Orden de Venta Origen',
        compute='_compute_source_sale_order',
        store=True,
    )

    @api.depends('origin')
    def _compute_source_sale_order(self):
        for record in self:
            sale_order = False
            if record.origin:
                # origin puede contener múltiples referencias separadas por coma
                refs = [ref.strip() for ref in record.origin.split(',')]
                for ref in refs:
                    so = self.env['sale.order'].search([('name', '=', ref)], limit=1)
                    if so:
                        sale_order = so.id
                        break
            record.source_sale_order_id = sale_order

    source_purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Orden de Compra Origen',
        compute='_compute_source_purchase_order',
        store=True,
    )

    @api.depends('origin')
    def _compute_source_purchase_order(self):
        """Para casos donde una PO referencia a otra PO."""
        for record in self:
            purchase_order = False
            if record.origin and not record.source_sale_order_id:
                refs = [ref.strip() for ref in record.origin.split(',')]
                for ref in refs:
                    po = self.env['purchase.order'].search(
                        [('name', '=', ref), ('id', '!=', record.id)], limit=1
                    )
                    if po:
                        purchase_order = po.id
                        break
            record.source_purchase_order_id = purchase_order

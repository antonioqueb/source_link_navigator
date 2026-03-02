from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    source_sale_order_ids = fields.Many2many(
        'sale.order',
        string='Órdenes de Venta Origen',
        compute='_compute_source_documents',
        store=True,
    )
    source_purchase_order_ids = fields.Many2many(
        'purchase.order',
        string='Órdenes de Compra Origen',
        compute='_compute_source_documents',
        store=True,
    )

    @api.depends('invoice_origin', 'line_ids.sale_line_ids', 'line_ids.purchase_line_id')
    def _compute_source_documents(self):
        for record in self:
            sale_orders = self.env['sale.order']
            purchase_orders = self.env['purchase.order']

            # Método 1: desde las líneas de factura
            for line in record.line_ids:
                if line.sale_line_ids:
                    sale_orders |= line.sale_line_ids.mapped('order_id')
                if line.purchase_line_id:
                    purchase_orders |= line.purchase_line_id.order_id

            # Método 2: buscar por invoice_origin
            if record.invoice_origin:
                refs = [ref.strip() for ref in record.invoice_origin.split(',')]
                for ref in refs:
                    if not sale_orders:
                        so = self.env['sale.order'].search(
                            [('name', '=', ref)], limit=1
                        )
                        if so:
                            sale_orders |= so
                    if not purchase_orders:
                        po = self.env['purchase.order'].search(
                            [('name', '=', ref)], limit=1
                        )
                        if po:
                            purchase_orders |= po

            record.source_sale_order_ids = sale_orders
            record.source_purchase_order_ids = purchase_orders

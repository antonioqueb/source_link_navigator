from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    source_sale_order_id = fields.Many2one(
        'sale.order',
        string='Orden de Venta Origen',
        compute='_compute_source_documents',
        store=True,
    )
    source_purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Orden de Compra Origen',
        compute='_compute_source_documents',
        store=True,
    )

    @api.depends('origin', 'move_ids.sale_line_id', 'move_ids.purchase_line_id')
    def _compute_source_documents(self):
        for record in self:
            sale_order = False
            purchase_order = False

            # Método 1: desde las líneas de movimiento (más confiable)
            for move in record.move_ids:
                if not sale_order and move.sale_line_id:
                    sale_order = move.sale_line_id.order_id.id
                if not purchase_order and move.purchase_line_id:
                    purchase_order = move.purchase_line_id.order_id.id
                if sale_order and purchase_order:
                    break

            # Método 2: buscar por campo origin
            if record.origin and (not sale_order or not purchase_order):
                refs = [ref.strip() for ref in record.origin.split(',')]
                for ref in refs:
                    if not sale_order:
                        so = self.env['sale.order'].search(
                            [('name', '=', ref)], limit=1
                        )
                        if so:
                            sale_order = so.id
                    if not purchase_order:
                        po = self.env['purchase.order'].search(
                            [('name', '=', ref)], limit=1
                        )
                        if po:
                            purchase_order = po.id

            record.source_sale_order_id = sale_order
            record.source_purchase_order_id = purchase_order
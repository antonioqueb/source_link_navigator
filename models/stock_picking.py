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

    @api.depends('origin', 'group_id')
    def _compute_source_documents(self):
        for record in self:
            sale_order = False
            purchase_order = False

            # Método 1: buscar por grupo de abastecimiento (más confiable)
            if record.group_id:
                so = self.env['sale.order'].search(
                    [('procurement_group_id', '=', record.group_id.id)], limit=1
                )
                if so:
                    sale_order = so.id
                po = self.env['purchase.order'].search(
                    [('group_id', '=', record.group_id.id)], limit=1
                )
                if po:
                    purchase_order = po.id

            # Método 2: buscar por campo origin
            if record.origin and not sale_order and not purchase_order:
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

            # Método 3: buscar por sale_id en las líneas del move
            if not sale_order:
                for move in record.move_ids:
                    if move.sale_line_id:
                        sale_order = move.sale_line_id.order_id.id
                        break

            # Método 4: buscar por purchase_line_id en las líneas del move
            if not purchase_order:
                for move in record.move_ids:
                    if move.purchase_line_id:
                        purchase_order = move.purchase_line_id.order_id.id
                        break

            record.source_sale_order_id = sale_order
            record.source_purchase_order_id = purchase_order

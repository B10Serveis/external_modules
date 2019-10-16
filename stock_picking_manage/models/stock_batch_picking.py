# -*- coding: utf-8 -*-
# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# © 2019 Comunitea - Vicente Ángel Gutiérrez <vicente@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, models, fields
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class StockBatchPicking(models.Model):
    _inherit = "stock.batch.picking"

    reserved_availability = fields.Float(
        'Quantity Reserved', compute='compute_picking_qties',
        digits=dp.get_precision('Product Unit of Measure'))
    quantity_done = fields.Float(
        'Quantity Done', compute='compute_picking_qties',
        digits=dp.get_precision('Product Unit of Measure'))
    product_uom_qty = fields.Float(
        'Quantity Ordered', compute='compute_picking_qties',
        digits=dp.get_precision('Product Unit of Measure'))
    all_assigned = fields.Boolean('All assigned', compute='get_all_assigned')

    @api.multi
    def get_all_assigned(self):
        for pick in self.mapped('picking_ids'):
            pick.all_assigned = not any(x.state in ('partially_available', 'confirmed') for x in pick.move_lines)

    @api.multi
    def compute_picking_qties(self):
        for batch in self:
            batch.quantity_done = sum(x.quantity_done for x in batch.picking_ids)
            batch.reserved_availability = sum(x.reserved_availability for x in batch.picking_ids)
            batch.product_uom_qty = sum(x.product_uom_qty for x in batch.picking_ids)

    @api.multi
    def force_set_qty_done(self):
        model = self._context.get('model_dest', 'stock.move')
        for batch in self:
            for picking in batch:
                if model == 'move.line':
                    picking.move_lines.force_set_qty_done()
                else:
                    picking.move_line_ids.force_set_qty_done()

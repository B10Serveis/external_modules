# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2019 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _name = 'stock.move'
    _inherit = ['stock.move', 'info.apk']

    tracking = fields.Selection(related='product_id.tracking')

    @api.model
    def force_set_qty_done_apk(self, vals):
        move = self.browse(vals.get('id', False))
        if not move:
            return {'err': True, 'error': "No se ha encontrado el movimiento."}
        for move_line in move.move_line_ids:
            move_line.qty_done = move_line.product_uom_qty
        return True
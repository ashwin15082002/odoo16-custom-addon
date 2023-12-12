# -*- coding: utf-8 -*-

from odoo import models


class StockReturnPicking(models.TransientModel):
	"""Inheriting stock_return_picking model for creating returns"""
	_inherit = 'stock.return.picking'

	def _create_returns(self):
		"""create returns"""
		new_picking, pick_type_id = (super(StockReturnPicking, self).
		                             _create_returns())
		picking = self.env['stock.picking'].browse(new_picking)
		if self.picking_id.return_order_id:
			picking.write({'return_order_picking': False,
			               'return_order_id': False,
			               'return_order_pick_id': self.picking_id.return_order_id.id})
			self.picking_id.return_order_id.write({'state': 'confirm'})
		return new_picking, pick_type_id

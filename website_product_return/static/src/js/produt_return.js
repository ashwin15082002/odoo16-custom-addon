odoo.define('website_product_return.return', function (require) {
    "use strict";
    var publicWidget = require('web.public.widget');
//    var rpc = require('web.rpc');

    publicWidget.registry.SaleReturn = publicWidget.Widget.extend({
    selector: '#sale_return_form',
    events: {
        'click .js_add_json': '_ReturnQuantity',
        'click #create': '_SubmitReturn',
    },

     _ReturnQuantity: function (ev) {
        var $link = $(ev.currentTarget);
        var $input = $link.closest('.input-group').find("input");
        var min = parseFloat($input.data("min") || 0);
        var max = parseFloat($input.data("max") || Infinity);
        var previousQty = parseFloat($input.val() || 0, 10);
        var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
        var newQty = quantity > min ? (quantity < max ? quantity : max) : min;
        if (newQty !== previousQty) {
            $input.val(newQty).trigger('change');
        }
        return false;
    },

    _SubmitReturn: function(ev){
        console.log('hiiiii')
        var val = []
        var products = []
        var qty = []
        var order_id = $(this).find(".quantity").data("order-id")
        $("tr.order_line").each(function(){
            qty.push($(this).find(".quantity").val()),
            products.push($(this).find(".quantity").data("product-id"))
        });
        val.push({'order_id': order_id,
                  'products':products,
                  'qty':qty,})
        console.log(val)
        this._rpc({
                model: 'stock.picking',
                method: 'create_picking',
                args: [val],
                })
    }

    });
});
//receipt = self.env['stock.picking'].create({
//            'picking_type_id': in_type.id,
//            'location_id': customer_location.id,
//            'location_dest_id': stock_location.id,
//            'move_ids': [(0, 0, {
//                'name': product.name,
//                'product_id': product.id,
//                'product_uom_qty': 1,
//                'product_uom': product.uom_id.id,
//                'location_id': customer_location.id,
//                'location_dest_id': stock_location.id,
//            })]
//        })
//        receipt.action_confirm()
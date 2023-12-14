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

        var val = []
        var order = []
        var delivered_qty = []
        $("tr.order_line").each(function(){
            var el = $(this)
            order = el.find(".quantity").data("order-id"),
            delivered_qty.push({'delivered': el.find(".quantity").data("delivered_qty"),
                                'line_id': el.find(".quantity").data("product-id"),})
            val.push({'product_id': el.find(".quantity").data("product-id"),
                      'quantity': el.find(".quantity").val(),})

        });

        this._rpc({
                model: 'stock.picking',
                method: 'create_picking',
                args: [val,order],
                }).then(function(result){
                    console.log(result)
                    if (result){
                        location.reload();
                    }
                })
    }

    });
});

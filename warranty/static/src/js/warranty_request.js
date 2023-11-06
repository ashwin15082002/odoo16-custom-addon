odoo.define('warranty.warranty_request_template', function (require) {


var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');


publicWidget.registry.warrantyRequest = publicWidget.Widget.extend({
    selector: '#warranty_form',
    events: {
        'change #invoice_id': '_onInvoiceChange',
        'change #product_ids': '_onProductChange',
    },

    _onInvoiceChange: function () {
        $('#product_ids').val('Select Product');
        $('#purchase_date').val('')
        $('#customer').val('')

        submit_request.setAttribute('disabled','disabled')
        var invoice = $('#invoice_id').val();

        ajax.jsonRpc('/getdata', 'call', {
                       'invoice' : invoice,
                      })
        .then(function (data) {
            $("#expiry_date").val("");
            var productDropdown = $("#product_ids");
                productDropdown.empty();
            $('#product_ids').prepend($('<option> Select Product </option>'));
            $.each(data.products, function (index, product) {
                    productDropdown.append($('<option>', {
                        value: product.id,
                        text: product.name,

                    }));
                });

            $("#customer").val(data.customer.name);
            $("#customer_id").val(data.customer.id);
            $("#purchase_date").val(data.purchase_date);
        });
    },

    _onProductChange: function() {
        var product = $('#product_ids').val();
        var invoice = $('#invoice_id').val();
        $('#expiry_date').val("")
        if (product != 'Select Product' && invoice){
            submit_request.removeAttribute('disabled')
        }
        else{
            submit_request.setAttribute('disabled','disabled')
        }

        ajax.jsonRpc('/getproductdata', 'call', {
                       'product' : product,
                       'invoice': invoice,
                      })
        .then(function (data) {
            $("#expiry_date").val(data.warranty_expiry);

        });

    },
    })
})

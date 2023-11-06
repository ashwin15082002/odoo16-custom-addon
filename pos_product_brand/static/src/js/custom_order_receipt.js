odoo.define('pos_product_brand.models', function (require) {
'use strict';


    var { Orderline } = require('point_of_sale.models');
    var Registries = require('point_of_sale.Registries');

    const CustomOrderline = (Orderline) => class CustomOrderline extends Orderline {
        export_for_printing(){
            var result = super.export_for_printing();
            result.brand = this.get_product().brand;
            console.log('result=',result.brand)
            return result

        }
    }
    Registries.Model.extend(Orderline, CustomOrderline);
});

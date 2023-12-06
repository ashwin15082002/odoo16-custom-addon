odoo.define('pos_button.Custom', function(require) {
'use strict';
    const { Gui } = require('point_of_sale.Gui');
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');

    class ProductButton extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }
        async onClick() {
            var self = this;
            await this.rpc({
                model: 'product.product',
                method: 'search_read',
                domain: [['available_in_pos','=',true]],
                fields: ['name','default_code','pos_categ_id','lst_price'],

            }).then(function (result) {
                self.showScreen('CategoryScreen', {
                    products: result,
                });
            });
        }

    }
    ProductButton.template = 'ProductButton';
    ProductScreen.addControlButton({component: ProductButton});
    Registries.Component.add(ProductButton);
});

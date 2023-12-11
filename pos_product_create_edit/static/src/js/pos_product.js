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
            console.log(this.env.pos)
            var self = this;
            var result = Object.values(this.env.pos.db.product_by_id)
                self.showScreen('CategoryScreen', {
                    products: result,
                });
        }
    }
    ProductButton.template = 'ProductButton';
    ProductScreen.addControlButton({component: ProductButton});
    Registries.Component.add(ProductButton);
});

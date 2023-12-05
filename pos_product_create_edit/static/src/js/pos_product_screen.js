odoo.define('pos_product_create_edit.CategoryScreen', function(require) {
    'use strict';
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } =require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var Qweb = core.qweb;
    const { onMounted, onWillUnmount, useState } = owl;
    class CategoryScreen extends PosComponent {
        setup(){
            super.setup();
            useListener('click_createProduct', this.onClick);
        }
        back() {
            this.showScreen('ProductScreen');
        }
        async onClick() {
            var self = this;
            await this.rpc({
                model: 'pos.category',
                method: 'search_read',
                fields: ['name'],

            }).then(function (result) {
                self.showPopup('CreateProduct', {
                    category: result,
                });
            });
        }

    };
    CategoryScreen.template= 'CategoryScreen';
    Registries.Component.add(CategoryScreen);

});

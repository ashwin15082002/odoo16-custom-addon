odoo.define('pos_product_create_edit.CategoryScreen', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } =require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');

    var rpc = require('web.rpc');
    var core = require('web.core');

    const { useState, useRef } = owl;
    class CategoryScreen extends PosComponent {
        setup(){
            super.setup();
            this.state = useState({
                searchWord:null,
                product_list : this.env.pos.db.product_by_id,
            });
            this.searchWordInputRef = useRef('search-word-input-product');

            useListener('click_createProduct', this.onClick);
            useListener('click_editProduct', this.editClick);

        }
        back() {
            this.env.pos.db.product_by_id = this.state.product_list;
            this.showScreen('ProductScreen');
        }

        async updateSearch(event){
            this.state.searchWord = event.target.value;
            var self = this;

            this.env.pos.db.product_by_id = await this.rpc({
                model: 'product.product',
                method: 'search_read',
                domain: [['available_in_pos', '=', true],
                        ['name', 'ilike', this.state.searchWord]],
                fields: ['display_name','default_code','pos_categ_id','lst_price','image_1920'],
                })

            self.showScreen('CategoryScreen', {
                products: this.env.pos.db.product_by_id,})
        }

        async onClick() {
            var self = this;
            const category = await this.rpc({
                model: 'pos.category',
                method: 'search_read',
                fields: ['name'],
            })
            self.showPopup('CreateProduct', {
                category,
            });
        }

        async editClick(details) {
            var self = this;
            const product = await this.rpc({
                model: 'product.product',
                method: 'search_read',
                domain: [['id','=',details.detail.details]],
                fields: ['name','standard_price','pos_categ_id','lst_price','image_1920'],
            })

            const category = await this.rpc({
                model: 'pos.category',
                method: 'search_read',
                fields: ['name'],

            })
            self.showPopup('CreateProduct', {
                category, product,
            });
        }

    };
    CategoryScreen.template= 'CategoryScreen';
    Registries.Component.add(CategoryScreen);

});

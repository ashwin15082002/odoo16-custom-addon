odoo.define('pos_product_create_edit.CreateProduct', function(require) {
    'use strict';
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } =require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var Qweb = core.qweb;
    const { onMounted, onWillUnmount, useState ,useRef } = owl;
    class CreateProduct extends PosComponent {
        setup(){
            super.setup();
            this.state = useState({
                product_name:'',
                product_price:'',
                product_cost:'',
                product_image: '',
                product_categ: 3,

            });
        }
        cancel(){
            this.showScreen('CategoryScreen');
            this.env.posbus.trigger('close-popup', {
                popupId: this.props.id,
            });
        }

        confirm(){
            console.log(this.state)
            this.rpc({
                model: 'pos.product.create',
                method: 'custom',
                args: [this.state],

                }).then(function (result) {

            });
        }

    };
    CreateProduct.template= 'CreateProduct';
    Registries.Component.add(CreateProduct);

});

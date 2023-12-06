odoo.define('pos_product_create_edit.CreateProduct', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } =require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const { getDataURLFromFile } = require("web.utils");

    var rpc = require('web.rpc');
    var core = require('web.core');

    const { useState ,useRef } = owl;
    class CreateProduct extends PosComponent {
        setup(){
            super.setup();
            this.state = useState({
                image:'',
                create_data :{
                    product_name:'',
                    product_price:'',
                    product_cost:'',
                    product_categ: 3,},
                edit_data :{
                    }
            });
            this.editName = useRef('editName');
            this.editPrice = useRef('editPrice');
            this.editName = useRef('editCateg');
            this.editImage = useRef('editImage');
        }
        cancel(){
            this.showScreen('CategoryScreen');
            this.env.posbus.trigger('close-popup', {
                popupId: this.props.id,
            });
        }
        updateData(ev){
            const field = ev.target.name;
            this.state.edit_data[field] = ev.target.value;
        }

        async uploadImage(event){
            const file = event.target.files[0];
            const imageUrl = getDataURLFromFile(file);
            console.log(imageUrl)
            const res = await this.processImage(imageUrl)

        }
        processImage(url){
            url.then((a)=>{
                this.state.image = a.split(',')[1];
            });
        }

        confirm(){
            console.log(this.state)
            this.rpc({
                model: 'pos.product.create',
                method: 'custom',
                args: [this.state.create_data,this.state.image],
                }).then((result)=> {
                if(result){
                    this.showScreen('ProductScreen');
                    this.env.posbus.trigger('close-popup', {
                        popupId: this.props.id,
                    });
                }else{
                    this.showPopup('ErrorPopup',{
                        title : "Failed ",
                        body : "Creation Of Product Failed! Enter valid Details. ",
                    });
                }
            });
        }
        edit(){
            this.rpc({
                model: 'pos.product.create',
                method: 'edit_product',
                args: [this.state.edit_data,this.props.product[0]['id'],this.state.image ],
                }).then((data)=> {
                console.log(data)
                if(data){
                    this.showScreen('ProductScreen');
                    this.env.posbus.trigger('close-popup', {
                    popupId: this.props.id,
                    });
                }else{
                    this.showPopup('ErrorPopup',{
                        title : "No Changes ",
                        body : "Change values and Click Edit . ",
                    });
                }
            });
        }

    };
    CreateProduct.template= 'CreateProduct';
    Registries.Component.add(CreateProduct);

});

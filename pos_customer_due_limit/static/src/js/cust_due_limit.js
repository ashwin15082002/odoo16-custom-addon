odoo.define('pos_customer_customer_due_limit.models', function (require) {
    'use strict';

    var Registries = require('point_of_sale.Registries')
    var ProductScreen = require('point_of_sale.ProductScreen')

    const CustomerDueLimit = (ProductScreen) => class CustomerDueLimit extends ProductScreen {
        async _onClickPay(){
            var partner = this.currentOrder.get_partner()

            console.log(partner)
            if (partner){
                var active_limit = partner.active_limit
                if (active_limit) {
                    var limit = partner.limit
                    var due = partner.credit

                    if (due >= limit){
                        console.log('limit reached')
                        this.showPopup('ErrorPopup', {
                            title : "Limit Reached",
                            body  : "The limit for this customer is already reached .",
                        });
                    }
                    else {
                    console.log('entered payment')
                        return super._onClickPay();
                    }
                }
                else {
                    console.log('active limit is not active')
                    return super._onClickPay();
                }
            }
            else {
                this.showPopup('ErrorPopup',{
                title : "No Customer ",
                body : "Customer is not selected . ",
                });
            }
        }
    }
    Registries.Component.extend(ProductScreen, CustomerDueLimit);
});

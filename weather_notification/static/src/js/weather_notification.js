/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
var Model = require('web.Model')
var rpc = require('web.rpc');

class SystrayIcon extends Component{

    _onClick() {
    console.log('function')
    rpc.query({
                    'model': 'res.config.settings',
                    'method': 'custom_method',
                    'domain': [],

            });
    console.log('function')


    }
}
SystrayIcon.template = "systray_icon";
export const systrayItem = { Component: SystrayIcon,};
registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });

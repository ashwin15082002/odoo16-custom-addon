/** @odoo-module */

import { registry } from "@web/core/registry"
import { ChartRendered } from "./chart_rendered"
import { useService } from "@web/core/utils/hooks"
const { Component, useRef, onWillStart, onMounted ,useState } = owl

export class OwlSalesDashboard extends Component {
    setup(){
        this.state = useState({
            quotations:{value:0},
            order:{value:0},

        })
        this.orm = useService("orm")
        onWillStart(async()=>{
            await this.getSaleCounts();
        })

    }
    async onPeriodChange(){
        this.state.date = moment().subtract(this.state.period, 'days').format('MM/DD/YYYY')
        this.state.date = this.state.date + ' 00:00:00'
        console.log(this.state.date)
        await this.getSaleCounts()
    }

    async getSaleCounts(){
        const quot = await this.orm.searchCount("sale.order",[['state','in',['draft','sent']], ['date_order', '>=', this.state.date ]])
        this.state.quotations.value = quot
        const order = await this.orm.searchCount("sale.order",[['state','in',['sale']], ['date_order', '>=', this.state.date ]])
        this.state.order.value = order
    }

}

OwlSalesDashboard.template = "OwlSalesDashboard"
OwlSalesDashboard.components = { ChartRendered }
registry.category("actions").add('custom_dashboard_tags', OwlSalesDashboard)

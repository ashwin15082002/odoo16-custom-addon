/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
const { Component, useRef, onMounted ,useState } = owl

export class OwlSalesDashboard extends Component {
    setup(){
        this.state = useState({
            data:{},
            period: 7,
            chart:[],
        })

        this.SalesPerson = useRef("SalesPerson"),
        this.SalesTeam = useRef("SalesTeam"),
        this.TopCustomers = useRef("TopCustomers"),
        this.LowProducts = useRef("LowProducts"),
        this.HighProducts = useRef("HighProducts"),
        this.OrderStatus = useRef("OrderStatus"),
        this.InvoiceStatus = useRef("InvoiceStatus"),

        this.orm = useService("orm")

        onMounted(async()=> {
            await this.FetchData();
        })

    }
    async onPeriodChange(){
        if (this.state.chart.length !=0) {
            this.state.chart.forEach((chart)=> {
                chart.destroy()
            })
            this.FetchData()
        }
    }
    async FetchData(){
        const date = this.state.period
        this.state.data = await this.orm.call("sale.dashboard", "get_sale_counts", [date]);

        this.charts(this.SalesPerson.el,'bar',this.state.data.sales_person,'Sales Person',this.state.data.data_sales_person)
        this.charts(this.SalesTeam.el,'line',this.state.data.team,'Sales Team', this.state.data.data_sales_team)
        this.charts(this.TopCustomers.el,'pie',this.state.data.partner_name,'Top Customers', this.state.data.count_records)
        this.charts(this.LowProducts.el,'doughnut',this.state.data.low_product,'Sale Order Count', this.state.data.low_count)
        this.charts(this.HighProducts.el,'pie',this.state.data.top_product,'Top Products', this.state.data.top_count)
        this.charts(this.OrderStatus.el,'polarArea',this.state.data.state_name,'Order Status', this.state.data.state_count)
        this.charts(this.InvoiceStatus.el,'radar',this.state.data.invoice_state_name,'Invoice Status', this.state.data.invoice_state_count)

    }


    charts(canvas,type,labels,label,data){
        this.state.chart.push(new Chart(
            canvas,
            {
                type:type,
                data: {
                    labels: labels,
                    datasets: [
                        {
                        label: label,
                        data: data,
                        }
                    ]
                },
            }
        ))
    }

}
OwlSalesDashboard.template = "OwlSalesDashboard"
registry.category("actions").add('custom_dashboard_tags', OwlSalesDashboard)

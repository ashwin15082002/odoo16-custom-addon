/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
const { Component, useRef, onWillStart, onMounted ,useState ,onPatched } = owl

export class OwlSalesDashboard extends Component {
    setup(){
        this.state = useState({
        data:{},
        period: 7,
        })

        this.SalesPerson = useRef("SalesPerson"),
        this.SalesTeam = useRef("SalesTeam"),
        this.TopCustomers = useRef("TopCustomers"),
        this.LowProducts = useRef("LowProducts"),
        this.HighProducts = useRef("HighProducts"),
        this.OrderStatus = useRef("OrderStatus"),
        this.InvoiceStatus = useRef("InvoiceStatus"),

        this.orm = useService("orm")
            onWillStart(async()=>{
                await this.onPeriodChange();
            })

        onMounted(()=> {
            var sale_person_chart = new Chart(this.SalesPerson.el,
                {
                    type:'bar',
                    data: {
                        labels: this.state.data.sales_person,
                        datasets: [{
                                label: 'Sales Person',
                                data: this.state.data.data_sales_person,
                            }]
                    },

                },
            );
        })
        onMounted(()=> {
            new Chart(this.SalesTeam.el,
                {
                    type:'line',
                    data: {
                        labels: this.state.data.team,
                        datasets: [{
                                label: 'Sales Team',
                                data: this.state.data.data_sales_team,
                            }]
                    },

                },
            );
        })
        onMounted(()=> {
            new Chart(this.TopCustomers.el,
                {
                    type:'pie',
                    data: {
                        labels: this.state.data.partner_name,
                        datasets: [{
                                label: 'Top Customers',
                                data: this.state.data.count_records,
                            }]
                    },

                },
            );
        })
        onMounted(()=> {
            new Chart(this.LowProducts.el,
                {
                    type:'bar',
                    data: {
                        labels: ['Red','Blue','Yellow'],
                        datasets: [{
                                label: 'Acquisitions by year',
                                data: [300, 50, 100]
                            }]
                    },

                },
            );
        })
        onMounted(()=> {
            new Chart(this.HighProducts.el,
                {
                    type:'bar',
                    data: {
                        labels: ['Red','Blue','Yellow'],
                        datasets: [{
                                label: 'Acquisitions by year',
                                data: [300, 50, 100]
                            }]
                    },

                },
            );
        })
        onMounted(()=> {
            new Chart(this.OrderStatus.el,
                {
                    type:'bar',
                    data: {
                        labels: ['Red','Blue','Yellow'],
                        datasets: [{
                                label: 'Acquisitions by year',
                                data: [300, 50, 100]
                            }]
                    },

                },
            );
        })
        onMounted(()=> {
            new Chart(this.InvoiceStatus.el,
                {
                    type:'bar',
                    data: {
                        labels: ['Red','Blue','Yellow'],
                        datasets: [{
                                label: 'Acquisitions by year',
                                data: [300, 50, 100]
                            }]
                    },

                },
            );
        })
    }
    async onPeriodChange(){
        const date = this.state.period
        this.state.data = await this.orm.call("sale.dashboard", "get_sale_counts", [date]);
        console.log(this.state.data)
    }

//    charts(canvas,type,label,labels,data){
//        this.state.chart.push(new Chart(
//            canvas,
//            {
//                type,
//                data: {
//                    labels,
//                    datasets: [
//                        {
//                        label,
//                        data,
//                        }
//                    ]
//                },
//                options: {
//                    plugins: {
//                        legend: {
//                            position: 'bottom',
//                        },
//                        title: {
//                            display: true,
//                        }
//                    }
//                }
//            }
//        ))
//    }

}
OwlSalesDashboard.template = "OwlSalesDashboard"
//OwlSalesDashboard.components = { ChartRendered }
registry.category("actions").add('custom_dashboard_tags', OwlSalesDashboard)

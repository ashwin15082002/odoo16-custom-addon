/** @odoo-module */

import { registry } from "@web/core/registry"
import { loadJS } from "@web/core/assets"
const { Component, useRef, onMounted } = owl

export class ChartRendered extends Component {
    setup(){
        this.chartRef = useRef("chart")
        onMounted(()=> this.renderChart())
    }
    renderChart(){
        new Chart(this.chartRef.el,
            {
                type:this.props.type,
                data: {
                    labels: ['Red','Blue','Yellow'],
                    datasets: [
                        {
                            label: 'Acquisitions by year',
                            data: [300, 50, 100]
                        }
                    ]
                },
                options:{
                responsive:true,
                plugins:{
                    legend:{
                        position:'bottom',
                    },
                    title:{
                        display:true,
                        text:this.props.title,
                        position:'bottom',
                    }
                }
            }
            },
        );
    }
}

ChartRendered.template = "ChartRendered"

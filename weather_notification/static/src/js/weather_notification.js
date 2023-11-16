/** @odoo-module **/

import { registry} from "@web/core/registry"
const { Component,useState } = owl
const rpc = require('web.rpc')

class SystrayIcon extends Component{

    async setup() {

        this.state = useState({
            is_option_enabled: false,
            dict: false,
        });

    var setting = await rpc.query({
            model: "res.config.settings",
            method: "custom",
        });
        this.api_key = setting['api_key']
        this.city = setting['city']
        this.state.is_option_enabled = setting['is_active']

    }

    onClick(ev) {
        if (ev.city && ev.api_key){
            fetch(`https://api.openweathermap.org/data/2.5/weather?q=${ev.city}&appid=${ev.api_key}`)
            .then(response => response.json())
            .then(function(data) {
                 var datas = data
                 ev_values(datas)
            })
        }
        else{
            alert('Provide API Key and City')
        }
        function ev_values(data){
            if (data['cod']==401){
                alert('Provide correct API Key')

            }
            else if(data['cod']==404){
                alert('Please provide Correct City')
            }
            else{

                var name = data['name']
                var temp_max = data['main']['temp_max']
                var temp_min = data['main']['temp_min']
                var feels_like = data['main']['feels_like']
                var type = data['weather'][0]['main']
                var weather_type = data['weather'][0]['description']
                var icon = data['weather'][0]['icon']

                var datas = {
                    'name': name,
                    'temp_max': temp_max,
                    'temp_min': temp_min,
                    'feels_like': feels_like,
                    'weather_type': weather_type,
                    'type': type,
                    'icon': icon,
                }
            }
            ev.state.dict = datas
        }
    }
}
SystrayIcon.template = "systray_icon";
const systrayItem = { Component: SystrayIcon, };
registry.category("systray").add("SystrayIcon", systrayItem);

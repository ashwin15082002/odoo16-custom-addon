/** @odoo-module **/
import { registry} from "@web/core/registry"
const { Component,useState} = owl
const rpc = require('web.rpc')

class SystrayIcon extends Component{

    async setup() {

        this.state = useState({
        is_option_enabled: false,

    });

    var setting = await rpc.query({
        model: "res.config.settings",
        method: "custom",
        });
        console.log(setting)
        this.api_key = setting['api_key']
        this.city = setting['city']
        this.state.is_option_enabled = setting['is_active']
        fetch(`https://api.geoapify.com/v1/geocode/autocomplete?text=${this.city}&apiKey=2fef58d064e5431c88fbb8c2e4a59e09`)
        .then(response => response.json())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));

    }


    onClick(ev) {
        console.log(ev)

        if (ev.city && ev.api_key){

            fetch(`https://api.openweathermap.org/data/2.5/weather?q=${ev.city}&appid=${ev.api_key}`)
            .then(response => response.json())
            .then(function(data) {
                 var datas = data
                 console.log(datas)
                 ev_values(datas)
            })
        }
        else{
            $('#body').empty()
            alert('Provide API Key and City')
        }
        function ev_values(data){
            console.log('function called')
            if (data['cod']==401){
                $('#body').empty()
                alert('Provide correct API Key')

            }
            else if(data['cod']==404){
                $('#body').empty()
                alert('Please provide Correct City')
            }
            else{

                var icon = data['weather'][0]['icon']

                $('#loc').text(data['name'])
                $('#max').text(data['main']['temp_max'])
                $('#min').text(data['main']['temp_min'])
                $('#temp').text(data['main']['feels_like'])
                $('#type').text(data['weather'][0]['main'])
                $('#weather_type').text(data['weather'][0]['description'])

            }
            ev.state.icon = icon

        }
    }

}
SystrayIcon.template = "systray_icon";
const systrayItem = { Component: SystrayIcon, };
registry.category("systray").add("SystrayIcon", systrayItem);

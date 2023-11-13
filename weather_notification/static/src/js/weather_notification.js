/** @odoo-module **/
import { registry} from "@web/core/registry"
const { Component,useState} = owl
const rpc = require('web.rpc')

class SystrayIcon extends Component{
    async setup() {
    this.state = useState({
      is_option_enabled: false,
      values: {},
    });

    var setting = await rpc.query({
        model: "res.config.settings",
        method: "custom",
      });
      console.log(setting)
      this.api_key = setting['api_key']
      this.city = setting['city']
      this.is_active = setting['is_active']

    }

    _onClick(ev) {
            console.log(ev)

            if (this.city && this.api_key){

                fetch(`https://api.openweathermap.org/data/2.5/weather?q=${this.city}&appid=${this.api_key}`)
                .then(response => response.json())
                .then(function(data) {
                     var datas = data
                     console.log(datas)
                     ev_values(datas)
                })
            }
            else{
                $('#body').text('')
                alert('Provide API Key and City')
            }
        function ev_values(data){
            console.log('function called')

            if (data['cod']==401){
                $('#body').text('')
                alert('Provide correct API Key')

            }
            else if(data['cod']==404){
                $('#body').text('')
                alert('Please provide Correct City')
            }
            else{

                $('#loc').text(data['name'])
                $('#max').text(data['main']['temp_max'])
                $('#min').text(data['main']['temp_min'])
                $('#temp').text(data['main']['feels_like'])
                $('#type').text(data['weather'][0]['main'])
                $('#weather_type').text(data['weather'][0]['description'])

            }

        }

    }
}
SystrayIcon.template = "systray_icon";
const systrayItem = { Component: SystrayIcon, };
registry.category("systray").add("SystrayIcon", systrayItem);

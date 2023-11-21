odoo.define('idle_timer.custom_time', function (require) {

    console.log('aaaaaa')
    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');

    publicWidget.registry.custom_time = publicWidget.Widget.extend({
    selector: '.o_survey_form',

    start: function() {
        this._rpc({
           model: 'ir.config_parameter',
           method: 'get_param',
           args:['idle_timer.idle_timer'],
        }).then(function(result){
           time = result;
           currentSec = time;
        })
        let begin_in = 5
        let timer = setInterval(startIdleTimer,1000);

        window.onmousemove = ResetTimer;
        window.onclick = ResetTimer;
        window.onkeydown = ResetTimer;

        function ResetTimer(){
            currentSec = time;
            begin_in = 5
            $('#timer').text('');
        }

        function startIdleTimer(){
            begin_in--;
            if (begin_in <=0 && currentSec > 0){
                currentSec--;
                $('#timer').text(currentSec);
                console.log('currentSec-- ',currentSec)
            }
            if (currentSec == 0){
                $('.btn-primary').click();
                $('#timer').text('');
            }
        }

    }
    })
});
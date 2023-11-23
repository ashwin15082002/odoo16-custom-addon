odoo.define('idle_timer.custom_time', function (require) {

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
           console.log(result)
           time = result;
           currentSec = time;
        })
        let begin_in = 5;
        var idle = setInterval(startIdleTimer,1000);

        window.onmousemove = ResetTimer;
        window.onclick = ResetTimer;
        window.onkeydown = ResetTimer;

        function ResetTimer(){
            currentSec = time;
            begin_in = 5
            $('#timer').empty();
        }

        function startIdleTimer(){
            begin_in--;
            if (begin_in <=0 && currentSec > 0){
                currentSec--;

                var element = $('.o_survey_review')
                if(! element['length']){
                    $('#timer').text(currentSec);
                }
                if (currentSec == 0){
                    $('.btn-primary').click();
                }
            }
        }

    }
    })
});

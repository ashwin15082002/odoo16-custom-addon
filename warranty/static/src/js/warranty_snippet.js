odoo.define('warranty.warranty_snippet', function (require) {
   var PublicWidget = require('web.public.widget');
   var rpc = require('web.rpc');
   var core = require('web.core');
   var qweb = core.qweb;
   console.log('snippet')

      var Dynamic = PublicWidget.Widget.extend({
       selector: '.dynamic_snippet_blog',
       start: function () {
           var self = this;
           rpc.query({
               route: '/snippet',
           }).then((data) => {
               console.log(data)
               var chunks = _.chunk(data, 4)

               chunks[0].is_active = true
               var snippet = qweb.render('warranty.carousel_temp', {'chunks': chunks,'new_id': Date.now()} )
               self.$('#courosel').html(snippet)
           });
       },
   });
   PublicWidget.registry.dynamic_snippet_blog = Dynamic;
   return Dynamic;
});

odoo.define('warranty.warranty_snippet', function (require) {
   var PublicWidget = require('web.public.widget');
   var rpc = require('web.rpc');
   var core = require('web.core');
   var qweb = core.qweb;
   console.log('snippet')

      var Dynamic = PublicWidget.Widget.extend({
       selector: '#dynamic_snippet',
       start: function () {
       console.log('working')
           var self = this;
           rpc.query({
               route: '/product_snippet',
           }).then((data) => {
           console.log('data=', data)
               var chunks = _.chunk(data[0], 4 )
               console.log( 'sold', chunks)
               chunks[0].is_active = true
               var snippet = qweb.render('most_sold_product.carousel_temp', {'chunks': chunks,'new_id': Date.now()} )
               self.$('#courosel').html(snippet)

               var view_chunks = _.chunk(data[1], 4)
               console.log( 'view', view_chunks)
               view_chunks[0].is_active = true
               var view_snippet = qweb.render('most_sold_product.view_temp', {'view_chunks':view_chunks })
               self.$('#most_view').html(view_snippet)

           });
       },
   });
   PublicWidget.registry.dynamic_snippet_blog = Dynamic;
   return Dynamic;
});


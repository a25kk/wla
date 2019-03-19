(function($) {
     $(document).ready(function() {

     	$("#formfield-form-widgets-publications").hide(); 
     	if ($("#form-widgets-publications").text()) {
     		var result = $("#form-widgets-publications").text().split(","); 

     		for (var i =0; i < result.length; i++) {
     			var data = result[i].split(":"); 
     			if (data.length > 1) {
     				var id = data[0];
     				var qty = data[1];
     				alert("input [data-id = '"+id+"']");

     				$("input[data-id = '"+id+"']").val(qty); 
     			}
     		}
     	}


	 	$(".publications-list .qty").on('change', function() {

 			var result = []; 
 			$(".publications-list .qty").each(function(){
 			    var qty = $(this).val(); 
 				if ($.isNumeric(qty) && qty > 0) {
 					result.push($(this).attr("data-id") + ":" + $(this).val()); 
 				}
 			})
 			$("#form-widgets-publications").text(result.join()); 

	 	})

     })
})(jQuery);


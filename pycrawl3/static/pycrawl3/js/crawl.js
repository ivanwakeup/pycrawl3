$("#crawl-form").submit(function(e) {
    var url = "/crawl"

    $.ajax({
        type: "POST",
        url: url,
        data: $("#crawl-form").serialize(),
        success: function(data){
            if(data.success) {
                toastr.success(data.message);
                setTimeout(function() {
		            window.location.href = '/';
	            }, 2000);
            }
            else {
                toastr.error(data.message);
            }
        }
    });

    e.preventDefault();
});

$("#urls-form").submit(function(e) {
    var url = "/crawl"

    $.ajax({
        type: "POST",
        url: url,
        data: $("#urls-form").serialize(),
        success: function(data){
            if(data.success) {
                toastr.success(data.message);
                setTimeout(function() {
		            window.location.href = '/';
	            }, 2000);
            }
            else {
                toastr.error(data.message);
            }
        }
    });

    e.preventDefault();
});

$("#seed-form").submit(function(e) {
    var url = "/add-seed"

    $.ajax({
        type: "POST",
        url: url,
        data: $("#seed-form").serialize(),
        success: function(data){
            if(data.success) {
                toastr.success(data.message);
                setTimeout(function() {
		            window.location.href = '/';
	            }, 2000);
            }
            else {
                toastr.error(data.message);
            }
        }
    });

    e.preventDefault();
});
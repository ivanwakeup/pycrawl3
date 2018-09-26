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

$("#start-crawls").click(function() {
    var url = "/start-crawl"

    $.ajax({
        type: "GET",
        url: url,
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

});


$("#get-csv").click(function() {
    var url = "/get-emails-csv"

    $.ajax({
        type: "GET",
        url: url,
        success: function(data){
            if(data.success) {
                toastr.success(data.message);
                console.log(data);
                setTimeout(function() {
		            window.location.href = '/';
	            }, 2000);
            }
            else {
                toastr.error(data.message);
            }
        }
    });
});


$("#google-form").submit(function(e) {
    var url = "/search-google"

    $.ajax({
        type: "POST",
        url: url,
        data: $("#google-form").serialize(),
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
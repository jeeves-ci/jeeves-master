$( document ).ready(function() {
    var url = window.location.href;
    var arr_url = url.split("/");
    var webUiPublicIp = arr_url[2];
    var arrIp = webUiPublicIp.split(":");
    var restfulPublicIp = arrIp[0] + ":8080";

    $("#login-btn").click( function()
       {
           var url = `http://${restfulPublicIp}/api/v1.0/login`;
         var data = {"email": $("#email").val(),
                     "password": $("#psw").val()};
         $.ajax({
             url,
             type: "POST",
             data: JSON.stringify(data),
             headers: {
                 "Content-Type": "application/json",
             },
             dataType: "json",
             success: onLoginReceived.bind(this)
         });
       }
    );

    function onLoginReceived(data) {
        if ($("#remember").is(":checked")) {
            window.localStorage.setItem("access_token", data.access_token);
        } else {
            window.sessionStorage.setItem("access_token", data.access_token);
        }

        $.ajaxSetup({
            beforeSend: function (xhr)
            {
               xhr.setRequestHeader("Authorization","Bearer " + data.access_token);
            }
        });
        var body = $('body');
        body.empty().load('#');
    }
});

$(document).ready(function() {
    $("#btn1").click(function () {
        $.ajax({
            url: "http://127.0.0.1:5000/record",
            type: "POST",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                movie: $("#movie").val(),
                actor: $("#actor").val(),
                country: $("#country").val(),
                popularity: $("#popularity").val()
            }),
            success: function (result) {
                $("#res_mo").text(result.movie);
                $("#res_ac").val(result.actor);
                $("#response").val(JSON.stringify(result));
                alert("Success! Please check the output!")
            }, error: function (error, response) {
                alert("Failed! Please check if the server is running and the endpoint is correct!")
            }
        });
        return false;
    });
});



$("#btn2").click(function () {
    $.ajax({
        url: $("#api2-url").val(),
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            title: $("#title").val(),
            text: $("#text").val()
        }),
        success: function (result) {
            console.log(result)
            $("#title").val(result.title);
            $("#text").val(result.text);
            $("#keywords").val(result.keywords);
            $("#response").val(JSON.stringify(result));
            alert("Success! Please check the output!")
        }, error:function (error, response) {
            alert("Failed! Please check if the server is running and the endpoint is correct!")
        }
    });
    return false;
});


$("#btn3").click(function () {


    $.ajax({
        url: 'http://api.interpreter.caiyunai.com/v1/translator',
        method: 'post',
        headers: {
            'Content-type': 'application/json',
            "x-authorization": "token bic0luupe3xdi0qa7fjq",
        },
        data: JSON.stringify({
            "source" : [$("#title").val(), $("#text").val(), $("#keywords").val()],
            "trans_type" : "zh2en",
            "request_id" : "demo",
        }),
        responseType: 'json',
        success: function(response){
            $("#response").val(JSON.stringify(response));
            console.log(response.target)
            $("#title").val(response.target[0]);
            $("#text").val(response.target[1]);
            $("#keywords").val(response.target[2]);
        }
    })

    return false;
});
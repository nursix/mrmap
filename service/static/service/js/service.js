function toggleOverlay(html){
    var overlay = $("#overlay");
    if(overlay.is(":visible")){
        overlay.html(html);
    }
    overlay.toggleClass("show");
}

function replaceButtonWithSpinner(button){
}

function changeOverlayContent(html){
    var overlay = $("#overlay");
    overlay.html(html);
}

function removeService(id, confirmed){
    $.ajax({
        url: "/service/remove",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        data:{
            "id": id,
            "confirmed": confirmed
        },
        type: 'get',
        dataType: 'json',
        success: function(data){
            var html = data["html"];
            toggleOverlay(html);
            if(data["redirect"] !== null){
                window.open(data["redirect"], "_self");
            }
        }
    })
}

function toggleServiceActiveStatus(id, active){
    $.ajax({
        url: "/service/activate",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        data:{
            "id": id,
            "active": active
        },
        type: 'post',
        dataType: 'json',
        success: function(data){
            location.reload();
        }
    })
}

function startServiceRegistration(uri, button){
    var oldHtml = button.html();
    button.html("Please wait...");
    $.ajax({
        url: "/service/new/",
        headers:{
            "X-CSRFToken": getCookie("csrftoken")
        },
        data: {
            "uri": uri
        },
        type: 'post',
        dataType: 'json',
        success: function(data){
            changeOverlayContent(data["html"]);
            button.html(oldHtml);
        },
        always: function(data){
            $(".loading-spinner").toggleClass("hide");
        }
    });

}

function checkServiceRequestURI(){
    var uri = $("#request-uri input").val().trim();
    if (uri.length == 0){
        return
    }
    if (!uri.startsWith("http")){
        uri = "http://" + uri; // use http by default
    }
    $.ajax({
        url: "/service/new/register-form",
        headers:{
            "X-CSRFToken": getCookie("csrftoken")
        },
        data: {
            "uri": uri
        },
        type: 'post',
        dataType: 'json',
        success: function(data){
            changeOverlayContent(data["html"]);
        }
    });
}

function toggleCollapsibleSymbol(elem){
    var src = elem.attr("src");
    var toggle = elem.attr("data-toggle");
    elem.attr("src", toggle);
    elem.attr("data-toggle", src);
}

$(document).ready(function(){
    $(".remove-service-container").click(function(){
        var id = $(this).attr("data-parent");
        // call remove form, but indicate that the remove process was not confirmed yet by the user
        removeService(id, false);
    });

    $(".deactivate-service-container, .activate-service-container").click(function(){
        var id = $(this).attr("data-parent");
        var elem = $(this);
        var active = false;
        if(elem.hasClass("activate-service-container")){
            var active = true;
        }
        toggleServiceActiveStatus(id, active)
    });



    $("#service-display-selector").change(function(){
        var val = $(this).val();
        $.ajax({
            url: "/service/session",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            data:{
                "session": JSON.stringify({
                    "displayServices": val
                })
            },
            type: 'get',
            dataType: 'json',
            success: function(data){
                location.reload();
            }

        });


    });

    $(".action-button").click(function(){
        $.ajax({
            url: "/service/new/register-form",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            data: {},
            type: 'get',
            dataType: 'json',
            success: function(data) {
                var html = data["html"];
                toggleOverlay(html);
            }
        });
    });

    $(".layer-title").click(function(){
        var elem = $(this);
        var table = elem.siblings(".layer-content");
        table.toggle("fast");
        var img = elem.find("img");
        toggleCollapsibleSymbol(img);
    });

    $(".sublayer-headline").click(function(){
        var elem = $(this);
        var table = elem.siblings(".sublayer");
        table.toggle("fast");
        var img = elem.find("img");
        toggleCollapsibleSymbol(img);
    });

});
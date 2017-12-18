var datastamp = Date.parse(new Date());
$.getScript("http://static.geetest.com/static/tools/gt.js?v=" + datastamp, function () {
    $.ajax({
        url: "/SearchItemCaptcha?v=" + datastamp,
        type: "get",
        dataType: "json",
        success: function (a) {
            initGeetest({
                gt: a.gt,
                challenge: a.challenge,
                product: "popup",
                offline: !a.success
            }, handlerPopup)
        }
    })
});
var handlerPopup = function (a) {
    $("#pop-captcha-submit").click(function () {
        var b = a.getValidate();
        if (!b) {
            return
        }
        $("#search_form").submit()
    });
    a.bindOn("#pop-captcha-submit");
    a.appendTo("#popup-captcha");
    a.onReady(function () {
        var b = $("#keywords_para").val();
        if (b != null && b != "") {
            b = decodeURI($("#keywords_para").val());
            $("#keyword").val(b);
            setTimeout(function () {
                $("#btn_query").click()
            }, 100)
        }
    })
};
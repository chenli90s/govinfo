var location_info = 0;
var browser_version;
var hasValid = false;
if (!Array.prototype.map) {
    Array.prototype.map = function (i, h) {
        var b, a, c;
        if (this == null) {
            throw new TypeError(" this is null or not defined")
        }
        var e = Object(this);
        var f = e.length >>> 0;
        if (typeof i !== "function") {
            throw new TypeError(i + " is not a function")
        }
        if (h) {
            b = h
        }
        a = new Array(f);
        c = 0;
        while (c < f) {
            var d, g;
            if (c in e) {
                d = e[c];
                g = i.call(b, d, c, e);
                a[c] = g
            }
            c++
        }
        return a
    }
}
window.console = window.console || (function () {
    var a = {};
    a.log = a.warn = a.debug = a.info = a.error = a.time = a.dir = a.profile = a.clear = a.exception = a.trace = a.assert = function () {
    };
    return a
})();
window.alert = function (c) {
    var b = document.createElement("DIV");
    b.id = "shield";
    b.style.position = "absolute";
    b.style.left = "0px";
    b.style.top = "0px";
    b.style.width = "100%";
    b.style.height = document.body.scrollHeight + "px";
    b.style.textAlign = "center";
    b.style.zIndex = "25";
    b.style.backgroundColor = "black";
    b.style.opacity = 0.6;
    b.style.filter = "alpha(opacity=60)";
    var a = document.createElement("DIV");
    a.id = "alertFram";
    a.style.position = "absolute";
    a.style.left = "50%";
    a.style.top = "50%";
    a.style.marginLeft = "-225px";
    a.style.marginTop = "-75px";
    a.style.width = "350px";
    a.style.height = "100px";
    a.style.background = "#ff0000";
    a.style.textAlign = "center";
    a.style.lineHeight = "100px";
    a.style.zIndex = "300";
    strHtml = '<ul style="list-style:none;margin:0px;padding:0px;width:100%">\n';
    strHtml += '<li style="background:#d1ab62;text-align:left;padding-left:10px;font-size:14px;font-weight:bold;height:40px;line-height:40px;color:#FCFCFC;font-family:Microsoft YaHei;">提示框<div style="width:20px;height:20px;background:#fff;border-radius:100%;display:inline-block;color:#000;line-height:20px;text-align:center;position:absolute;right:10px;top:10px;cursor:pointer;"  onclick="doOk()">X</div></li>\n';
    strHtml += ' <li style="background:#ffffff;text-align:center;font-size:12px;height:100px;line-height:24px;padding-top:34px;border-left:1px solid #F0F0F0;border-right:1px solid #F0F0F0;font-family:Microsoft YaHei;">' + c + "</li>\n";
    strHtml += ' <li style="background:#F7F7F7;text-align:center;height:50px;line-height:50px; border:1px solid #F0F0F0;color:#FCFCFC;"><input  style="background:#d1ab62;text-align:center;width:75px;height:25px;color:#F0F0F0;font-family:Microsoft YaHei;display: inline-block;    margin-bottom: 0;font-weight: normal;text-align: center;vertical-align: middle;-ms-touch-action: manipulation;touch-action: manipulation;cursor: pointer;background-image: none;border: 1px solid transparent;white-space: nowrap;padding: 6px 12px;font-size: 14px;line-height: 1;border-radius: 4px;-webkit-user-select: none;" type="button" value="确定" onclick="doOk()" /></li>\n';
    strHtml += "</ul>\n";
    a.innerHTML = strHtml;
    document.body.appendChild(a);
    document.body.appendChild(b);
    this.doOk = function () {
        a.style.display = "none";
        b.style.display = "none"
    };
    a.focus();
    document.body.onselectstart = function () {
        return false
    }
};

function stripscript(c) {
    var d = new RegExp("[`~!@#$^&*=|{}':;',\\[\\].<>/?~！ @#￥……&*——|{}【】‘；：”“'。，、？]");
    var a = "";
    for (var b = 0; b < c.length; b++) {
        a = a + c.substr(b, 1).replace(d, "")
    }
    return a
}

function checkRate(b) {
    number_2 = b.replace(/[(|)|（|）]/g, "");
    number_2 = number_2.replace(/(^\s*)|(\s*$)/g, "");
    var a = /^[0-9a-zA-Z]*$/g;
    if (!a.test(number_2)) {
        return false
    } else {
        return true
    }
}

function chechSingleWord(b) {
    b = stripscript(b);
    if (b == "") {
        alert("请输入企业名称、统一社会信用代码或注册号！");
        return false
    }
    var c = b.split(" ");
    for (var a = 0; a < c.length; a++) {
        if (c[a].length > 1) {
            return true
        }
    }
    alert("请输入更详细的查询条件");
    return false
}

function load(b) {
    str_2 = b.replace(/[(|)|（|）]/g, "");
    str_2 = str_2.replace(/(^\s*)|(\s*$)/g, "");
    var a = /^[\u4E00-\u9FA5]+$/;
    if (!a.test(str_2)) {
        return false
    } else {
        return true
    }
}

var data1 = false;

function check() {
    var xhr = new XMLHttpRequest();
    var val = document.getElementById("keyword");
    var testStr = val.value;
    if (!chechSingleWord(testStr)) {
        return false
    }
    testStr = testStr.replace(/ /g, "");
    var flag = checkRate(testStr);
    if (flag) {
        if (val.value.length > 18) {
            alert("您输入的长度超过规定长度，请输入不超过50个汉字或18个数字和字母！");
            return false
        }
    } else {
        var isChinese = load(testStr);
        if (isChinese) {
            if (testStr.length > 50) {
                alert("您输入的长度超过规定长度，请输入不超过50个汉字或18个数字和字母！");
                return false
            }
        } else {
            if (testStr.length > 50) {
                alert("您输入的长度超过规定长度，请输入不超过50个字符！");
                return false
            }
        }
    }
    $.ajax({
        type: "get",
        async: false,
        url: "/corp-query-geetest-validate-input.html?token=" + location_info,
        dataType: "json",
        success: function (json) {
            eval(json.map(function (item) {
                return String.fromCharCode(item)
            }).join(""));
            var token = document.getElementById("token");
            token.value = location_info
        },
        error: function () {
        }
    });
    $.ajax({
        type: "get",
        async: false,
        url: "/corp-query-search-test.html",
        data: {searchword: val.value},
        dataType: "json",
        success: function (data) {
            if (data) {
                data1 = true;
                $("#pop-captcha-submit").trigger("click")
            } else {
                if (val.value.length != 0) {
                    alert("请输入更为详细的查询条件！")
                } else {
                    alert("请输入企业名称、统一社会信用代码或注册号！")
                }
            }
            console.log(data1 + "neibu")
        }
    });
    return data1
}

$(function () {
    $("#btn_query").on("click", function () {
        if ($("#keyword").val() == "请输入企业名称、注册号或统一社会信用代码") {
            $("#keyword").val("")
        }
        if (check()) {
            $("#pop-captcha-submit").trigger("click")
        }
    });
    $("#keyword").on("keypress", function (event) {
        if (event.keyCode === 13) {
            $("#keyword").blur();
            if ($("#keyword").val() == "请输入企业名称、注册号或统一社会信用代码") {
                $("#keyword").val("")
            }
            check();
            return false
        }
    });
    $("#submitButton").click(function () {
        $("#mainForm").submit()
    });
    $(".content label").click(function () {
        switch ($(".content").find(".tab-on").prev().attr("src")) {
            case"images/iconfont-shujutianbao2.png":
                $(".tab-on").prev().attr("src", "images/iconfont-shujutianbao.png");
                break;
            case"images/iconfont-rest2.png":
                $(".tab-on").prev().attr("src", "images/iconfont-rest.png");
                break
        }
        $(".content").find(".tab-on").removeClass("tab-on");
        $(this).addClass("tab-on");
        switch ($(this).prev().attr("src")) {
            case"images/iconfont-shujutianbao.png":
                $(this).prev().attr("src", "images/iconfont-shujutianbao2.png");
                break;
            case"images/iconfont-rest.png":
                $(this).prev().attr("src", "images/iconfont-rest2.png");
                break
        }
    });
    $(".tabs label").click(function () {
        $(".tabs").find(".tab-in").next().hide();
        $(".tabs").find(".tab-in").removeClass("tab-in");
        $(this).addClass("tab-in");
        $(this).next().show()
    });
    $(".choosetabs span").click(function () {
        $(".choosetabs").find(".tab2in").removeClass("tab2in");
        $(this).addClass("tab2in");
        switch ($(this).attr("name")) {
            case"tab1":
                $(".span1").css("background", "#4164a7");
                $(".span2").css("background", "#fff");
                break;
            case"tab2":
                $(".span2").css("background", "#4164a7");
                $(".span1").css("background", "#fff");
                break
        }
    });
    $(".search_items > span").click(function () {
        $(".search_items").find(".selected").removeClass("selected");
        switch ($(this).attr("class")) {
            case"entInfo":
                $("input[name=tab]").val("ent_tab");
                break;
            case"abnormal":
                $("input[name=tab]").val("excep_tab");
                break;
            case"serious":
                $("input[name=tab]").val("ill_tab");
                break
        }
        $(this).addClass("selected")
    });
    var date = new Date();
    var timestamp = date.getMinutes() + date.getSeconds();
    $.ajax({
        type: "get",
        async: false,
        url: "/corp-query-custom-geetest-image.gif?v=" + timestamp,
        dataType: "json",
        success: function (json) {
            eval(json.map(function (item) {
                return String.fromCharCode(item)
            }).join(""));
            browser_version = check_browser
        },
        error: function () {
        }
    })
});
var provinceTonum = {
    "北京": 110000,
    "天津": 120000,
    "河北": 130000,
    "山西": 140000,
    "内蒙古": 150000,
    "辽宁": 210000,
    "吉林": 220000,
    "黑龙江": 230000,
    "上海": 310000,
    "江苏": 320000,
    "浙江": 330000,
    "安徽": 340000,
    "福建": 350000,
    "江西": 360000,
    "山东": 370000,
    "广东": 440000,
    "广西": 450000,
    "海南": 460000,
    "河南": 410000,
    "湖北": 420000,
    "湖南": 430000,
    "重庆": 500000,
    "四川": 510000,
    "贵州": 520000,
    "云南": 530000,
    "西藏": 540000,
    "陕西": 610000,
    "甘肃": 620000,
    "青海": 630000,
    "宁夏": 640000,
    "新疆": 650000
};
var teladdr = {
    "100000": "tel.html",
    "110000": "http://bj.gsxt.gov.cn/sydq/loginSydqAction!jszc.dhtml",
    "120000": "http://www.tjxy.gov.cn/gsnb/jsp/saic/dianhua.jsp",
    "310000": "http://sh.gsxt.gov.cn/notice/search/search_telephone",
    "500000": "http://cq.gsxt.gov.cn/common/jslxzc.html",
    "130000": "http://he.gsxt.gov.cn/notice/search/search_telephone",
    "140000": "http://sx.gsxt.gov.cn/zxPhone.jspx",
    "210000": "http://ln.gsxt.gov.cn/saicpub/entPublicitySC/entPublicityDC/include/zxfwNew.jsp",
    "220000": "http://jl.gsxt.gov.cn/Contact.html",
    "230000": "http://hl.gsxt.gov.cn/zxPhone.jspx",
    "320000": "http://www.jsgsj.gov.cn:58888/province/system/tel.jsp",
    "330000": "http://zj.gsxt.gov.cn/client/entsearch/contact",
    "340000": "http://ah.gsxt.gov.cn/zxPhone.jspx",
    "350000": "http://fj.gsxt.gov.cn/notice/search/search_telephone",
    "360000": "http://jx.gsxt.gov.cn/pages/contact.jsp",
    "370000": "http://sd.gsxt.gov.cn/pub/hotphone",
    "410000": "http://ha.gsxt.gov.cn/zxPhone.jspx",
    "420000": "http://hb.gsxt.gov.cn/zxPhone.jspx",
    "430000": "http://hn.gsxt.gov.cn/notice/search/search_telephone",
    "440000": "http://gd.gsxt.gov.cn/aiccips//main/consult.html",
    "460000": "http://hi.gsxt.gov.cn/zxPhone.jspx",
    "510000": "http://sc.gsxt.gov.cn/ztxy.do?method=changeTel&random=2110095111",
    "520000": "http://gz.gsxt.gov.cn/2016/frame/services.jsp",
    "530000": "http://gsxt.ynaic.gov.cn/notice/search/search_telephone",
    "610000": "http://sn.gsxt.gov.cn/ztxy.do?method=shanxiTel&random=2110095111",
    "620000": "http://gs.gsxt.gov.cn/gsxygs/pubSearch/footerLink",
    "630000": "http://qh.gsxt.gov.cn/zxPhone.jspx",
    "150000": "http://nm.gsxt.gov.cn:58888/main/consult.html",
    "450000": "http://gx.gsxt.gov.cn/sydq/loginSydqAction!gxjszc.dhtml",
    "540000": "http://xz.gsxt.gov.cn/zxPhone.jspx",
    "640000": "http://nx.gsxt.gov.cn/indexAction_phoneList.action",
    "650000": "http://xj.gsxt.gov.cn/sydq/loginSydqAction!xj_jszc.dhtml"
};

function addLinks() {
    $("#choose_state").hover(function () {
        if (!$(".loadingView").html()) {
            $(".state_box").show();
            return false
        }
        $(this).addClass("activing");
        $.ajax({
            type: "post", url: "index/getLinks", dataType: "json", success: function (b) {
                $(".loadingView").remove();
                var a = $(".state_box").find("a");
                a.each(function () {
                    if (b[provinceTonum[$(this).html()]] == undefined || b[provinceTonum[$(this).html()]].length == 0) {
                        $(this).css("color", "#999")
                    } else {
                        if ($(this).html().length < 4) {
                            $(this).attr("href", b[provinceTonum[$(this).html()]]).attr("target", "_blank")
                        }
                    }
                });
                if (!$("#choose_state").hasClass("activing")) {
                    return
                }
                $(".state_box").show();
                $("#zj_link").attr("href", b["100000"])
            }
        })
    }, function () {
        $(".state_box").hide();
        $(this).removeClass("activing")
    })
}

function inputPlaceholder() {
    var a = $("#keyword");
    a.css({color: "#999"}).val("请输入企业名称、注册号或统一社会信用代码");
    a.on("focus", function () {
        if ($(this).val() == "请输入企业名称、注册号或统一社会信用代码") {
            $(this).removeAttr("style").val("")
        }
    });
    a.on("blur", function () {
        if ($(this).val() == "请输入企业名称、注册号或统一社会信用代码" || $(this).val() == "") {
            $(this).css({color: "#999"}).val("请输入企业名称、注册号或统一社会信用代码")
        }
    })
}

function addTelLinks() {
    if ($("#subsite").val() == 120000) {
        $("#subsite").next().attr("href", teladdr[$("#subsite").val()])
    }
}

$(document).ready(function () {
    if (navigator.appName == "Microsoft Internet Explorer" && navigator.appVersion.match(/8./i) == "8.") {
        inputPlaceholder();
        var a = $(window).width();
        if (a <= 1160) {
            $(".body_layout").css({"min-width": 960});
            $(".body-1140").css({width: 960, "margin-left": -480});
            $(".body-min1400-df").css({"min-width": 960});
            $(".main-layout").css({width: 960});
            $(".body-min1400").css({"min-width": 960});
            $(".footer2").css({"min-width": 960})
        } else {
            $(".body_layout").removeAttr("style");
            $(".body-1140").removeAttr("style");
            $(".body-min1400-df").removeAttr("style");
            $(".main-layout").removeAttr("style");
            $(".body-min1400").removeAttr("style");
            $(".footer2").removeAttr("style")
        }
    } else {
        if (navigator.appName == "Microsoft Internet Explorer" && navigator.appVersion.match(/9./i) == "9.") {
            inputPlaceholder()
        }
    }
    $(".search_items").find("span").removeClass("selected");
    switch ($("input[name=tab]").val()) {
        case"ent_tab":
            $(".search_items").find(".entInfo").addClass("selected");
            break;
        case"excep_tab":
            $(".search_items").find(".abnormal").addClass("selected");
            break;
        case"ill_tab":
            $(".search_items").find(".serious").addClass("selected");
            break
    }
    addLinks();
    addTelLinks()
});
$(window).resize(function () {
    if (navigator.appName == "Microsoft Internet Explorer" && navigator.appVersion.match(/8./i) == "8.") {
        var a = $(window).width();
        if (a <= 1160) {
            $(".body_layout").css({"min-width": 960});
            $(".body-1140").css({width: 960, "margin-left": -480});
            $(".body-min1400-df").css({"min-width": 960});
            $(".main-layout").css({width: 960});
            $(".body-min1400").css({"min-width": 960});
            $(".footer2").css({"min-width": 960})
        } else {
            $(".body_layout").removeAttr("style");
            $(".body-1140").removeAttr("style");
            $(".body-min1400-df").removeAttr("style");
            $(".main-layout").removeAttr("style");
            $(".body-min1400").removeAttr("style");
            $(".footer2").removeAttr("style")
        }
    }
});

function Link(b) {
    var a = getCurrUrl();
    window.open("http://121.43.68.40/exposure/jiucuo.html?site_code=" + b + "&url=" + encodeURIComponent(a))
}

function getCurrUrl() {
    var a = "";
    if (parent !== window) {
        try {
            a = window.top.location.href
        } catch (b) {
            a = window.top.document.referrer
        }
    }
    if (a.length == 0) {
        a = document.location.href
    }
    return a
};
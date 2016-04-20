/**
 * Created by qiqi on 16/2/23.
 */
var login = function() {
    $("#loginBtn").click(function() {
        var username = $("#InputUser1").val();
        var password = $("#InputPassword1").val();
        var remember_me = $("#remember_me").is(":checked");
        if (username == "" || username.length > 16) {
            loginAlert(4);
            return;
        }
        if (password == "" || password.length > 16) {
            loginAlert(5);
            return;
        }
        var data = {'username':username,'password':password,'remember_me':remember_me};
        $.ajax({
            'url':'/user/login',
            'type':'post',
            'datatype':'json',
            'data':data,
            success: function(res) {
                loginAlert(res.code);
            }
        });
    });

    $(".msgBtn").click(function() {
        $(this).parent().fadeOut();
    });
};

function loginAlert(code) {
    if(code == 0) {
        widget = $("#successMsg");
        txt = '正在跳转到先前页面···';
        setTimeout(function() {
            window.location.href = "/";
        },1000)
    } else {
        widget = $("#alertMsg");
        switch (code) {
            case 1:
                txt = '账户被禁用！';
                break;
            case 2:
                txt = '密码错误！';
                break;
            case 3:
                txt = '未找到该账户！';
                break;
            case 4:
                txt = "账号不能为空或超过16位！";
                break;
            case 5:
                txt = "密码不能为空或超过16位！";
                break;
            default:
                txt = '未知错误！';
                break;
        }
    }
    if(widget.css("display") == "block") {
        return;
    }
    widget.children('text').text(txt);
    widget.fadeIn();
    setTimeout(function() {
        widget.fadeOut();
    },2000);
};

login();


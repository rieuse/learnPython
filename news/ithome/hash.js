document.domain = "ithome.com";
$(document).ready(function () {
    $("#btnComment").click(function () {
        $(this).attr({"disabled": "disabled"});
        postdata();
        $(this).removeAttr("disabled");
    });
    $("#btnReplyComment").click(function () {
        $(this).attr({"disabled": "disabled"});
        postdata();
        $(this).attr({"disabled": "disabled"});
    });


    var oremarkbtn = "";
    $("body").delegate(".comment_co", "click", function () {
        oremarkbtn = $(this);
        var commentID = oremarkbtn.parents("li").attr("cid");
        var newsID = oremarkbtn.parents("li").attr("nid");
        oremarkbtn.parents("li").replaceWith($("<div/>").load("/ithome/getajaxdata.aspx", {
            "commentid": commentID,
            "newsid": newsID,
            "type": "getsinglecomment"
        }, function () {
            AutoifHeight();
        }));
    });

    $(".post_comment").delegate(".comm-con .tg a", "click", function () {
        //$("#commentContent").insertAtCaret("@投稿 ");
    });

    $(".post_comment").delegate(".ywz", "click", function () {
        oremarkbtn = $(this);
        var biaoqing = oremarkbtn.parents(".add_comm").find(".biaoqing_box");
        if (biaoqing.is(':hidden')) {
            biaoqing.show();
        } else {
            biaoqing.hide();
        }
    });


    $("body").delegate(".biaoqing_box a", "click", function () {
        oremarkbtn = $(this);
        oremarkbtn.parents(".add_comm").find("textarea").insertAtCaret(oremarkbtn.text());
        $(".biaoqing_box").hide();
    });

    $(".comm_list").delegate("h3 .refresh", "click", function () {
        commentpage = 1;
        $('#ulcommentlist').fadeOut('fast', function () {
            $('#ulcommentlist li').remove();
        });
        $('#ulcommentlist').fadeIn('slow', function () {
            $("<div/>").load("/ithome/getajaxdata.aspx", {
                "newsID": $("#newsid").val(),
                "hash": $("#hash").val(),
                "type": "commentpage",
                "page": 1,
                "order": false
            }, function () {
            }).appendTo($("#ulcommentlist")).fadeIn('slow');
        });
    });

    $('#entered_passwordInput').focus(function () {
        $('#entered_passwordLabel').hide();
    }).blur(function () {
        if ($(this).val() == '') $('#entered_passwordLabel').show();
    });

    $("#btn_loginbtn").click(function () {
        CommentLogin($("#entered_UsernameInput").val(), $("#entered_passwordInput").val());
    });

    $("#btn_logoutbtn").click(function () {
        LogOut();
    });


    $("#commentnew").click(function () {
        $("#divLatest").hide();
        $("#ulcommentlistLatest").html('');
        InitfHeight();
        pagecomment(1, 0, false);
        $("#divcommentlist").show('slow', function () {
            AutoifHeight();
        });
    });
    $("#commentlatest").click(function () {
        $("#ulcommentlist").html('');
        InitfHeight();
        pagecomment(1, 0, true);
        $("#divLatest").show('slow', function () {
            AutoifHeight();
        });
        $("#divcommentlist").hide();
    });

    $("#commentnew").attr("checked", 'checked');

});

function postdata() {
    $.ajax({
        type: "POST",
        url: "/ithome/postComment.aspx",
        data: "newsid=" + $("#newsid").val() + "&commentNick=" + escape($("#commentNick").val()) + "&commentContent=" + encodeURIComponent($("#commentContent").val()).replace(/\+/g, '%2B') + "&parentCommentID=" + $("#parentCommentID").val() + "&txtCode=" + $("#txtCode").val() + "&type=comment",
        success: function (msg) {
            var messageobj = GetObj('commentMessage');
            messageobj.innerHTML = '<span style="color:red">' + msg + '</span>';
            if (msg.indexOf("评论成功") >= 0) {
                LoadData();
                var comment = GetObj("commentContent");
                comment.value = '';
            } else if (msg.indexOf("验证手机") >= 0) {
                PopVerifyMobile();
            } else if (msg.indexOf("被禁言") >= 0) {
                messageobj.innerHTML = '';
                jQuery.getScript("http://img.ithome.com/file/js/jquery/confirm.js").done(function () {
                    var msgStr = msg.replace("\r\n", "").replace('”', "");
                    var pos = msgStr.indexOf('，');
                    var msg1 = msgStr.substring(0, pos);
                    var msg2 = msgStr.substring(pos + 7);
                    var txt = '<div><img src=http://img.ithome.com/images/v2.3/cry.png width=50></div><div style="font-size:16px;margin:10px 0;font-weight:700">' + msg1 + "</div><div style='color:#d22222;text-align:left'>违规内容：</div><div style=text-align:left>" + msg2 + "</div><div style=text-align:right><a target='_blank' href='http://quan.ithome.com/helpcenter/'>我要申诉</a></div>";
                    var option = {
                        title: "",
                        btn: parseInt("0011", 2),
                        onOk: function () {
                        }
                    }
                    window.wxc.xcConfirm(txt, "custom", option);

                });
            }
        }
    });
}

function GetObj(objName) {
    if (document.getElementById) {
        return eval('document.getElementById("' + objName + '")');
    } else if (document.layers) {
        return eval("document.layers['" + objName + "']");
    } else {
        return eval('document.all.' + objName);
    }
}


function CloseReply(commentid) {
    var ReplyDiv = $('[id=Reply' + commentid + ']');
    ReplyDiv.hide();
}

function ShowReply(commentid, newsid, lou, parentcommentID) {
    var ReplyDiv = $('[id=Reply' + commentid + ']');
    ReplyDiv.show();
    JsonStr = "\{ \"commentid\":\"" + commentid + "\", \"newsid\":\"" + newsid + "\"  , \"iLou\":\"" + lou + "\"  , \"ppCID\":\"" + parentcommentID + "\" \}";
    $.ajax({
        type: "POST",
        url: "/ithome/getajaxdata.aspx/ShowReplyLogin",
        data: JsonStr,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        async: true,
        success: function (msg) {
            ReplyDiv.html(msg.d);
            var t = $("#commentContent" + commentid).val();
            $("#commentContent" + commentid).val("").focus().val(t);
        }
    });
}

function ShowReply(commentid, newsid, lou, parentcommentID, nickname) {
    var ReplyDiv = $('[id=Reply' + commentid + ']');
    ReplyDiv.show();
    JsonStr = "\{ \"commentid\":\"" + commentid + "\", \"newsid\":\"" + newsid + "\"  , \"iLou\":\"" + lou + "\"  , \"ppCID\":\"" + parentcommentID + "\" , \"nickName\": \"" + nickname + "\" \}";
    $.ajax({
        type: "POST",
        url: "/ithome/getajaxdata.aspx/ShowReplyLogin",
        data: JsonStr,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        async: true,
        success: function (msg) {
            ReplyDiv.html(msg.d);
            var t = $("#commentContent" + commentid).val();
            $("#commentContent" + commentid).val("").focus().val(t);
            AutoifHeight();
        }
    });
}

function displayCommentLouMore(commentid, obj) {
    $("<div/>").load("/ithome/getajaxdata.aspx", {
        "commentid": commentid,
        "type": "getmorelou"
    }, function () {
        AutoifHeight();
    }).appendTo($(obj).parent().parent());
    $('[id=liGetMore' + commentid + ']').hide();

}

function PostQuickComment(commentid, newsid, ppCID) {
    $.ajax({
        type: "POST",
        url: "/ithome/postComment.aspx",
        data: "newsid=" + newsid + "&commentNick=" + escape($("#commentNick" + commentid).val()) + "&commentContent=" + encodeURIComponent($("#commentContent" + commentid).val()).replace(/\+/g, '%2B') + "&parentCommentID=" + commentid + "&ppCID=" + ppCID + "&txtCode=" + $("#txtCode" + commentid).val() + "&type=comment",
        success: function (msg) {

            var messageObj = GetObj('commentMessage' + commentid);
            messageObj.innerHTML = '<span id="commentMessage" style="color:red">' + msg + '</span>';
            if (msg.indexOf("评论成功") >= 0) {
                QuickCommentLoadData(commentid);
            } else if (msg.indexOf("验证手机") >= 0) {
                PopVerifyMobile();
            }
        }
    });
}

function QuickCommentLoadData(commentid) {
    $("#lou" + commentid).show();
    $("<div/>").load("/ithome/getajaxdata.aspx", {
        "commentid": commentid,
        "type": "getloucomment"
    }, function () {
    }).appendTo($("#lou" + commentid));
    //  $("#lou" + commentid).append('   <li class="gh"><div class="re_info"><strong class="p_floor"></strong>新回复</div><div class="re_comm"><p class="p_1">' + $("#commentContent" + commentid).val() + '</p><p class="p_2"><span class="comm_reply"><a  href="javascript:;">支持(0)</a><span class="v">|</span><a id="against877904" href="javascript:;">反对(0)</a><span class="v">|</span><a href="javascript:;">回复</a></span></p></li>');
    var ReplyDiv = GetObj('Reply' + commentid);
    ReplyDiv.style.display = 'none';
    ReplyDiv.innerHTML = "";
}

function commentVote(commentid, typeid) {
    var attr;
    if (typeid == 1) {
        attr = $("#agree" + commentid).attr('href');
        $("#agree" + commentid).attr('href', 'javascript:;');
    } else {
        attr = $("#against" + commentid).attr('href');
        $("#against" + commentid).attr('href', 'javascript:;');
    }

    $.ajax({
        type: "POST",
        url: "/ithome/postComment.aspx",
        data: "commentid=" + commentid + "&type=loginReplyVote&typeid=" + typeid,
        success: function (msg) {

            if (msg.indexOf("通行证") >= 0) {
                {
                    var width = "450";
                    if ((navigator.userAgent.match(/(iPhone|iPod|Android|Windows Phone)/i)))
                        width = "320";
                    PopLogin();
                }


                if (typeid == 1) {
                    $("#agree" + commentid).attr('href', attr);
                } else {
                    $("#against" + commentid).attr('href', attr);
                }
                return;
            }
            if (msg.indexOf("验证手机") >= 0) {
                PopVerifyMobile();
                if (typeid == 1) {
                    $("#agree" + commentid).attr('href', attr);
                } else {
                    $("#against" + commentid).attr('href', attr);
                }
                return;
            }
            if (msg.indexOf("禁言") >= 0) {
                jQuery.getScript("http://img.ithome.com/file/js/jquery/confirm.js").done(function () {
                    var msgStr = msg.replace("\r\n", "").replace('”', "");
                    var pos = msgStr.indexOf('，');
                    var msg1 = msgStr.substring(0, pos);
                    var msg2 = msgStr;
                    var txt = '<div><img src=http://img.ithome.com/images/v2.3/cry.png width=50></div><div style="font-size:16px;margin:10px 0;font-weight:700">' + msg1 + "</div><div style='color:#d22222;text-align:left'>违规内容：</div><div style=text-align:left>" + msg2 + "</div><div style=text-align:right><a target='_blank' href='http://quan.ithome.com/helpcenter/'>我要申诉</a></div>";
                    var option = {
                        title: "",
                        btn: parseInt("0011", 2),
                        onOk: function () {
                        }
                    }
                    window.wxc.xcConfirm(txt, "custom", option);
                });
                return;
            }
            if (msg.indexOf("您") >= 0) {
                alert(msg);
            } else {
                if (typeid == 1) {
                    $("#agree" + commentid).text('取消支持(' + msg + ')');
                    $("#agree" + commentid).attr('href', 'javascript:cancleCommentVote(' + commentid + ', 1)');

                    $("#agree" + commentid).css({
                        "position": "relative"
                    });
                    $("#agree" + commentid).append("<span class='flower'></span>");
                    $("#agree" + commentid).find(".flower").css({
                        "position": "absolute",
                        "text-align": "center",
                        "left": "6px",
                        "top": "-10px",
                        "display": "block",
                        "width": "30px",
                        "height": "30px",
                        "background": "url(http://img.ithome.com/file/images/agree.gif) left center no-repeat",
                        "opacity": "0"
                    }).animate({
                        top: '-30px',
                        opacity: '1'
                    }, 300, function () {
                        $(this).delay(300).animate({
                            top: '-35px',
                            opacity: '0'
                        }, 300)
                    });
                    $("#agree" + commentid).find(".flower").removeClass();

                } else {
                    $("#against" + commentid).text('取消反对(' + msg + ')');
                    $("#against" + commentid).attr('href', 'javascript:cancleCommentVote(' + commentid + ', 2)');

                    $("#against" + commentid).css({
                        "position": "relative"
                    });
                    $("#against" + commentid).append("<span class='shit'></span>");
                    $("#against" + commentid).find(".shit").css({
                        "position": "absolute",
                        "text-align": "center",
                        "left": "6px",
                        "top": "-60px",
                        "display": "block",
                        "width": "30px",
                        "height": "30px",
                        "background": "url(http://img.ithome.com/file/images/against.gif) left center no-repeat",
                        "opacity": "0"
                    }).animate({
                        top: '-30px',
                        opacity: '1'
                    }, 300, function () {
                        $(this).delay(300).animate({
                            top: '-5px',
                            opacity: '0'
                        }, 300)
                    });
                    $("#against" + commentid).find(".shit").removeClass();
                }
            }
        }
    });
}

function cancleCommentVote(commentid, typeid) {
    $.ajax({
        type: "POST",
        url: "/ithome/postComment.aspx",
        data: "commentid=" + commentid + "&type=loginCancleReplyVote&typeid=" + typeid,
        success: function (msg) {
            if (msg.indexOf("您") >= 0) {
                alert(msg);
            } else {
                if (typeid == 1) {
                    $("#agree" + commentid).text('支持(' + msg + ')');
                    $("#agree" + commentid).attr('href', 'javascript:commentVote(' + commentid + ', 1)');

                } else {
                    $("#against" + commentid).text('反对(' + msg + ')');
                    $("#against" + commentid).attr('href', 'javascript:commentVote(' + commentid + ', 2)');
                }
            }
        }
    });
}

function commentComplain(commentid) {
    if (confirm("感谢您对评论内容的监督，多人举报后该评论将被隐藏，注意恶意举报会被处罚。是否举报？")) {
        $.ajax({
            type: "POST",
            url: "/ithome/postComment.aspx",
            data: "commentid=" + commentid + "&type=complain",
            success: function (message) {
                if (message.indexOf("需登录软媒通行证") >= 0) {
                    {
                        var width = "450";
                        if ((navigator.userAgent.match(/(iPhone|iPod|Android|Windows Phone)/i)))
                            width = "320";
                        PopLogin();
                    }
                }
                else if (message.indexOf("手机") >= 0) {
                    PopVerifyMobile();
                }
                else {
                    $("#complainmessage" + commentid).html("<span style=\"color:red;display:none;border:1px #fcbb90 solid;background:#fefcf4;position:absolute;padding:4px;right:0;top:0px;width:225px;text-align:center;\" class=\"jubao" + commentid + "\">" + message + "&nbsp;&nbsp;</span>");
                    $(".jubao" + commentid).css({
                        "display": "block",
                        "opacity": "0"
                    }).animate({
                        top: '-22px',
                        opacity: '1'
                    }, 300, function () {
                        $(this).delay(1000).animate({
                            top: '-30px',
                            opacity: '0'
                        }, 300, function () {
                            $(this).remove();
                        })
                    });
                }
            }
        });
    }
}

function appCommentComplain(commentid, u, p) {
    if (confirm("感谢您对评论内容的监督，多人举报后该评论将被隐藏，注意恶意举报会被处罚。是否举报？")) {
        wp7Complain(commentid, u, p);
    }
}

function wp7Complain(commentid, u, p) {
    $.ajax({
        type: "POST",
        url: "/ithome/postComment.aspx",
        data: "commentid=" + commentid + "&type=complain&u=" + u + "&p=" + p,
        success: function (message) {
            $("#complainmessage" + commentid).html("<span style=\"color:red;\" class=\"jubao\">" + message + "&nbsp;&nbsp;</span>");
            $(".jubao").delay(1500).fadeOut("slow");
        }
    });
}

function hotCommentVote(commentid, typeid) {
    var attr;
    $.ajax({
        type: "POST",
        url: "/ithome/postComment.aspx",
        data: "commentid=" + commentid + "&type=loginReplyVote&typeid=" + typeid,
        success: function (msg) {

            if (msg.indexOf("通行证") >= 0) {
                PopLogin();
                if (typeid == 1) {
                    $("#agree" + commentid).attr('href', attr);
                } else {
                    $("#against" + commentid).attr('href', attr);
                }
                return;
            }
            if (msg.indexOf("操作") >= 0 || msg.indexOf("金币") >= 0) {
                alert(msg);
                if (typeid == 1) {
                    $("#agree" + commentid).attr('href', attr);
                } else {
                    $("#against" + commentid).attr('href', attr);
                }
                return;
            }
            if (msg.indexOf("禁言") >= 0) {
                jQuery.getScript("http://img.ithome.com/file/js/jquery/confirm.js").done(function () {
                    var txt = msg.replace("\r\n", "<br>") + "<br><a href='http://quan.ithome.com/0/003/116.htm'>禁言和解封规则请点这里 >></a>";

                    window.wxc.xcConfirm(txt, window.wxc.xcConfirm.typeEnum.error);
                });
                return;
            }

            if (msg.indexOf("您") >= 0) {
                alert(msg);
            } else {
                if (typeid == 1) {
                    $("#hotagree" + commentid).text('取消支持(' + msg + ')');
                    $("#hotagree" + commentid).attr('href', 'javascript:cancleHotCommentVote(' + commentid + ', 1)');

                    $("#hotagree" + commentid).css({
                        "position": "relative"
                    });
                    $("#hotagree" + commentid).append("<span class='flower'></span>");
                    $("#hotagree" + commentid).find(".flower").css({
                        "position": "absolute",
                        "text-align": "center",
                        "left": "6px",
                        "top": "-10px",
                        "display": "block",
                        "width": "30px",
                        "height": "30px",
                        "background": "url(http://img.ithome.com/file/images/agree.gif) left center no-repeat",
                        "opacity": "0"
                    }).animate({
                        top: '-30px',
                        opacity: '1'
                    }, 300, function () {
                        $(this).delay(300).animate({
                            top: '-35px',
                            opacity: '0'
                        }, 300)
                    });
                    $("#hotagree" + commentid).find(".flower").removeClass();

                } else {

                    $("#hotagainst" + commentid).text('取消反对(' + msg + ')');
                    $("#hotagainst" + commentid).attr('href', 'javascript:cancleHotCommentVote(' + commentid + ', 2)');

                    $("#hotagainst" + commentid).css({
                        "position": "relative"
                    });
                    $("#hotagainst" + commentid).append("<span class='shit'></span>");
                    $("#hotagainst" + commentid).find(".shit").css({
                        "position": "absolute",
                        "text-align": "center",
                        "left": "6px",
                        "top": "-60px",
                        "display": "block",
                        "width": "30px",
                        "height": "30px",
                        "background": "url(http://img.ithome.com/file/images/against.gif) left center no-repeat",
                        "opacity": "0"
                    }).animate({
                        top: '-30px',
                        opacity: '1'
                    }, 300, function () {
                        $(this).delay(300).animate({
                            top: '-5px',
                            opacity: '0'
                        }, 300)
                    });
                    $("#hotagainst" + commentid).find(".shit").removeClass();
                }
            }
        }
    });
}

function cancleHotCommentVote(commentid, typeid) {
    $.ajax({
        type: "POST",
        url: "/ithome/postComment.aspx",
        data: "commentid=" + commentid + "&type=loginCancleReplyVote&typeid=" + typeid,
        success: function (msg) {
            if (msg.indexOf("您") >= 0) {
                alert(msg);
            } else {
                if (typeid == 1) {
                    $("#hotagree" + commentid).text('支持(' + msg + ')');
                    $("#hotagree" + commentid).attr('href', 'javascript:hotCommentVote(' + commentid + ', 1)');

                } else {
                    $("#hotagainst" + commentid).text('反对(' + msg + ')');
                    $("#hotagainst" + commentid).attr('href', 'javascript:hotCommentVote(' + commentid + ', 2)');
                }
            }
        }
    });
}

function clearComment() {
    var comment = document.getElementById("commentContent");

    if (comment.value == "IT之家有您参与更精彩！") {
        comment.value = '';
        comment.onclick = function () {
        }
    }
}

function showValidate() {
    var comment = GetObj('commentContent');
    if (comment.value == "IT之家有您参与更精彩！") comment.value = '';

}

function LoadData() {
    var insertObj;
    if ($('#commentlatest').is(':checked')) insertObj = $("#LoadArticleReplyLatest");
    else insertObj = $("#LoadArticleReply");
    var new_item = $("<div/>").load("/ithome/getajaxdata.aspx", {
        "newsID": $("#newsid").val(),
        "type": "comment"
    }, function () {
    }).hide();
    insertObj.append(new_item);
    new_item.fadeIn("slow");
}

function loadhotcomment() {
    $("<div/>").load("/ithome/getajaxdata.aspx", {
        "newsID": $("#newsid").val(),
        "type": "hotcomment",
    }, function () {
    }).appendTo($("#HotList")).fadeIn('slow');
}

function pagecomment(page, commentcount, order) {
    if (order) {
        $("<div/>").load("/ithome/getajaxdata.aspx", {
            "newsID": $("#newsid").val(),
            "hash": $("#hash").val(),
            "type": "commentpage",
            "page": page,
            "order": order
        }, function () {
        }).appendTo($("#ulcommentlistLatest")).fadeIn('slow', function () {
            AutoifHeight();
        });
        if (page != 1 && page * 50 > commentcount) $("#latestmorecomm").hide();
    } else {
        var new_item = $("<div/>").load("/ithome/getajaxdata.aspx", {
            "newsID": $("#newsid").val(),
            "hash": $("#hash").val(),
            "type": "commentpage",
            "page": page,
            "order": order
        }, function () {
        }).hide();
        $("#ulcommentlist").append(new_item);
        new_item.fadeIn('slow', function () {
            AutoifHeight();
        });
        if (page != 1 && page * 50 > commentcount) $("#morecomm").hide();
    }


}

$('.mobile a').attr('title', '下载IT之家客户端，炫耀我的尾巴！');
$('.qiyu a').attr('title', '旗鱼浏览器，绿色极速清爽！');


/* Ctrl+Enter回复 */
$('textarea').attr('onkeydown', 'if(event.ctrlKey&&event.keyCode==13){document.getElementById("btnComment").click();return false}');

var txt = $('#entered_UsernameInput').val();
$('#entered_UsernameInput').focus(function () {
    if (txt === $(this).val()) $(this).val('').css({
        'color': '#272a30'
    });
}).blur(function () {
    if ($(this).val() == '') $(this).val(txt).css({
        'color': '#888'
    });
});


function CommentLogin(username, pwd) {
    $("#btn_loginbtn").addClass("disable").attr({
        disabled: true
    });
    $("#returnMsg").text('');
    var JsonStr = "\{ \"username\":\"" + username + "\", \"password\":\"" + pwd + "\"  \}";
    $.ajax({
        type: "POST",
        url: "/ithome/login.aspx/btnLogin_Click",
        data: JsonStr,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        async: true,
        success: function (msg) {
            if (msg.d.indexOf('ok') < 0) {
                $("#btn_loginbtn").attr('disabled', false);
                $("#returnMsg").text(msg.d);
            } else {
                $(".comm_login").hide();
                $(".quickcommentlogined").show();
            }
        }
    });
}

function LogOut() {
    var JsonStr = "";
    $.ajax({
        type: "POST",
        url: "/ithome/login.aspx/btnLogout_Click",
        data: JsonStr,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        async: true,
        success: function (msg) {
            location.reload();
        }
    });
}


$("#displayAnonymous").click(function () {
    $("#commentLoginPanel").hide();
    $("#commentAnonymousPanel").show();
    $("#commentMessage").html('');
});
$("#displayLogin").click(function () {
    $("#commentLoginPanel").show();
    $("#commentAnonymousPanel").hide();
    $("#commentMessage").html('');
});


(function ($) {
    $.fn.extend({
        insertAtCaret: function (myValue) {
            var $t = $(this)[0];
            if (document.selection) {
                this.focus();
                sel = document.selection.createRange();
                sel.text = myValue;
                this.focus();
            } else if ($t.selectionStart || $t.selectionStart == '0') {
                var startPos = $t.selectionStart;
                var endPos = $t.selectionEnd;
                var scrollTop = $t.scrollTop;
                $t.value = $t.value.substring(0, startPos) + myValue + $t.value.substring(endPos, $t.value.length);
                this.focus();
                $t.selectionStart = startPos + myValue.length;
                $t.selectionEnd = startPos + myValue.length;
                $t.scrollTop = scrollTop;
            } else {
                this.value += myValue;
                this.focus();
            }
        }
    })
})(jQuery);


function InitfHeight() {
    var t, i;
    try {
        window != parent && (t = parent.document.getElementById("ifcomment"), $(t).removeAttr("height"), i = $("#post_comm").height(), t.style.height = i + "px" )
    } catch (r) {
    }
    ;

}

function AutoifHeight(n) {
    var t, i;
    try {
        window != parent && (t = parent.document.getElementById("ifcomment"), $(t).removeAttr("height"), i = $(document).height(), t.style.height = n == 0 ? "0px" : i + "px")
    } catch (r) {
    }
    ;
}

function PopLogin() {
    try {
        window != parent && (parent.popWin.showWin("400", "568", "软媒通行证登录", "https://my.ruanmei.com/?source=ithome"))
    } catch (r) {
    }
    ;

}

function PopVerifyMobile() {
    try {
        window != parent && (parent.popWin.showWin("310", "255", "验证手机", "/ithome/verifymobile.aspx"))
    } catch (r) {
    }
    ;

}

function connectLogin(type) {
    var url = "",
        name = "",
        width = "",
        height = "";
    var clienttime = parseInt((new Date).getTime() / 1000)

    switch (type) {
        case "Sina":
            url = "http://www.ithome.com/ithome/openplat/sina/login.aspx";
            name = "SinaLogin";
            width = 562;
            height = 380;
            break;
        case "QQ":
            url = "http://www.ithome.com/openplat/qq/login";
            name = "qq";
            width = 600;
            height = 380;
            break;
        case "WX":
            url = "http://www.ithome.com/ithome/openplat/wx/login.aspx";
            name = "wx";
            width = 580;
            height = 660;
            break;

    }
    if (url) {
        url += "?clienttime=" + clienttime
        var l = (window.screen.width - width) / 2,
            t = (window.screen.height - height) / 2;
        window.open(url, name, "width=" + width + ",height=" + height + ",left=" + l + ",top=" + t + ",menubar=0,scrollbars=0,resizable=0,status=0,titlebar=0,toolbar=0,location=1");
    }

}

/**
 * Created by Shinelon on 2017/9/28.
 */

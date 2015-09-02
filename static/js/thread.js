window.thiuff = window.thiuff || {};

// Posts a reply via AJAX. Also puts the message locally but with
// a sending indicator.
thiuff.postReply = function (event) {
    var form = $(this).parent("form");
    // Get content
    var data = {
        body: form.find("textarea").val(),
        csrfmiddlewaretoken: form.find("input[name=csrfmiddlewaretoken]").val()
    }
    // Post to backend handler
    $.ajax(form.attr("action"), {
        data: data,
        method: "POST"
    }).done(function (data) {
        alert(data);
    }).fail(function () {
        alert("fail");
    });
    // Don't do anything
    event.preventDefault();
    return false;
}

// Opens or closes replies
thiuff.toggleReplies = function (event) {
    var expander = $(this);
    var replies = expander.parent().children(".replies.main");
    var preview = expander.parent().children(".replies.preview");
    if (replies.filter(":visible").length) {
        replies.hide();
        preview.show();
        expander.removeClass("expanded");
    } else {
        preview.hide();
        replies.show();
        expander.addClass("expanded");
    }
}

$(function () {
    // Reply form handler
    $(".reply-form button").click(thiuff.postReply);
    // Reply expand/contracter
    $(".discussion .expander").click(thiuff.toggleReplies);
    // Contract all replies on page load
    $(".discussion .expander").removeClass("expanded");
    $(".discussion .replies.main").hide();
    $(".discussion .replies.preview").show();
});

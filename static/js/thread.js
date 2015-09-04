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
        form.find("textarea").val("");
    }).fail(function () {
        alert("Failed to post message.");
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

// Adds a reply to the reply div for the parent message given by
// the ID. Expects the parent message ID and full HTML for the reply.
thiuff.addReplyHtml = function (discussionId, replyHtml) {
    $(".discussion[data-discussion-id='" + discussionId + "']").find(".reply-form").before(replyHtml);
    $(".discussion[data-discussion-id='" + discussionId + "']").find(".replies.preview").html(replyHtml);
}

// Adds a reply to the reply div for the parent message given by
// the ID. Expects the parent message ID and full HTML for the reply.
thiuff.addDiscussionHtml = function (discussionId, discussionHtml) {
    var div = $(".discussion[data-discussion-id='" + discussionId + "']");
    if (div.length) {
        // Extract the HTML from the incoming chunk for the message.
        var content = $(discussionHtml);
        window.c = content;
        div.children(".js-body").html(content.children(".js-body").html());
    } else {
        $(document.body).append(discussionHtml);
    }
}

// Handles "reply" type messages
thiuff.handleReply = function (data) {
    thiuff.addReplyHtml(data.discussion_id, data.html);
}

// Handles "reply" type messages
thiuff.handleDiscussion = function (data) {
    thiuff.addDiscussionHtml(data.id, data.html);
}

// Listen on the streamer for new replies
thiuff.mainStreamer.addStream("thread-" + document.body.dataset.threadId);
thiuff.mainStreamer.addHandler("reply", thiuff.handleReply);
thiuff.mainStreamer.addHandler("discussion", thiuff.handleDiscussion);

$(function () {
    // Reply form handler
    $(".reply-form button").click(thiuff.postReply);
    $('.reply-form textarea').keydown(function (event) {
        if ((event.keyCode == 10 || event.keyCode == 13) && event.ctrlKey) {
            thiuff.postReply(event);
        }
    });
    // Reply expand/contracter
    $(".discussion .expander").click(thiuff.toggleReplies);
    // Contract all replies on page load
    $(".discussion .expander").removeClass("expanded");
    $(".discussion .replies.main").hide();
    $(".discussion .replies.preview").show();
});

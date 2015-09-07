window.thiuff = window.thiuff || {};


// Handles "reply" type messages
thiuff.handleThread = function (data) {
    var div = $(".thread[data-thread-id='" + data.id + "']");
    var top_level_messages_noun = data.num_top_level_messages_noun != 1 ? "discussions" : "discussions";
    var messages_noun = data.num_messages != 1 ? "replies" : "reply";
    window.d = data;
    div.find(".js-num-messages").text(data.num_messages + " " + messages_noun);
    div.find(".js-num-top-level-messages").text(data.num_top_level_messages + " " + top_level_messages_noun);
}

// Listen on the streamer for new replies
thiuff.mainStreamer.addStream("group-" + document.body.dataset.groupId);
thiuff.mainStreamer.addHandler("thread", thiuff.handleThread);

$(function () {
});

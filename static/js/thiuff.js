window.thiuff = window.thiuff || {};
window.console = window.console || {log: function () {}};

// Streamer - abstraction for telling the server what we want and
// handling responses from it.
thiuff.Streamer = function (url, streams) {
    // Check we even have websockets
    if (!window.WebSocket) {
        console.log("No websocket functionality.")
        return;
    }
    // Add streams
    if (streams) {
        this.streams = streams;
    }
    // Connect
    this.url = url;
    this.connect();
}
thiuff.Streamer.prototype = {
    url: null,
    streams: [],
    handlers: {},
    sentStreams: false,
    connectFailures: 0,
    connect: function () {
        var self = this;
        this.sentStreams = false;
        this.socket = new WebSocket(this.url);
        this.socket.onopen = function () {
            if (self.streams) {
                var packet = {
                    "type": "streams",
                    "streams": self.streams,
                }
                this.send(JSON.stringify(packet));
            }
            this.sentStreams = true;
            self.connectFailures = 0;
            console.log("Streamer open for " + self.streams.join(" "));
        }
        this.socket.onclose = function () {
            // When a close happens, perform an auto-backing-off reconnect.
            self.connectFailures += 1;
            var retryTime = Math.min(120, 5 * self.connectFailures);
            window.setTimeout(self.connect.bind(self), retryTime * 1000);
            console.log("Streamer closed; retrying in " + retryTime + " seconds");
        }
        this.socket.onmessage = function (msg) {
            console.log("Streamer message:" + msg.data);
            var data = JSON.parse(msg.data);
            // Error handling
            if (data.error) throw "Streamer error: " + data.error;
            // Find a handler by type key
            var handler = self.handlers[data.type];
            if (!handler) throw "No handler for " + data.type;
            handler(data);
        }
    },
    // Adds a stream to subscribe to. Works if the socket is open or not.
    addStream: function (stream) {
        this.streams.push(stream);
        // If the socket is already open, send an extra stream request with this.
        if (this.sentStreams) {
            this.socket.send("streams " + stream);
            console.log("Added additional stream " + stream);
        }
    },
    // Adds a handler for a message type, by type name.
    addHandler: function (type, func) {
        // Make sure we won't overwrite something.
        if (this.handlers[type]) throw "Handler already exists for " + type;
        // We just store handlers in an object.
        this.handlers[type] = func;
    }
}

// Runs content binding stuff (called on body on load, and content as it
// lightboxes in)
thiuff.bindContent = function (content) {
    content = $(content);
    // Hook up any optional-lightbox links
    content.find(".opt-lightbox").click(function (e) {
        // If it wasn't left mouse click, don't do anything (middle mouse
        // should still open in new tab)
        if (e.button != 0) return true;
        // Fire up featherlight lightbox
        $.featherlight(this.href + " .content", {
            type: 'ajax',
            afterContent: function () {
               thiuff.bindContent(this.$content);
            }
        });
        e.preventDefault();
        return false;
    });
    // Lightbox closing buttons
    content.find(".js-close-lightbox").click(function (e) {
        $.featherlight.close();
        e.preventDefault();
        return false;
    });
    // Other binders
    for (var i = 0; i < thiuff.contentBinders.length; i++) {
        thiuff.contentBinders[i](content);
    }
}

// Additional content binder storage
thiuff.contentBinders = [];

// Make one global instance for streaming stuff
thiuff.mainStreamer = new thiuff.Streamer(document.body.dataset.streamUrl);

// Subscribe to per-user events if logged in.
if (document.body.dataset.userId) {
    thiuff.mainStreamer.addStream("user-" + document.body.dataset.userId);
}

$(function () {
    thiuff.bindContent(document.body);
    // Make flashes fade away after a while
    window.setTimeout(function () { $(".flashes").fadeOut(); }, 7000);
});

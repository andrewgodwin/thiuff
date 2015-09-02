window.thiuff = window.thiuff || {};
window.console = window.console || {log: function () {}};

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
    sentStreams: false,
    connectFailures: 0,
    connect: function () {
        var self = this;
        this.sentStreams = false;
        this.socket = new WebSocket(this.url);
        this.socket.onopen = function () {
            this.send("streams " + self.streams.join(" "));
            this.sentStreams = true;
            self.connectFailures = 0;
            console.log("Streamer open for " + self.streams.join(" "));
        }
        this.socket.onclose = function () {
            self.connectFailures += 1;
            var retryTime = Math.min(120, 5 * self.connectFailures);
            window.setTimeout(self.connect.bind(self), retryTime * 1000);
            console.log("Streamer closed; retrying in " + retryTime + " seconds");
        }
        this.socket.onmessage = function (msg) {
            console.log("Streamer message:" + msg);
        }
    },
    addStream: function (stream) {
        this.streams.push(stream);
        if (this.sentStreams) {
            this.socket.send("streams " + stream);
            console.log("Added additional stream " + stream);
        }
    }
}

// Make one global instance for streaming stuff
thiuff.mainStreamer = new thiuff.Streamer(document.body.dataset.streamUrl);

$(function () {
    // Hook up any optional-lightbox links
    $(".opt-lightbox").click(function (e) {
        // If it wasn't left mouse click, don't do anything (middle mouse
        // should still open in new tab)
        if (e.button != 0) return true;
        // Fire up featherlight lightbox
        $.featherlight(this.href + " .content", {
            type: 'ajax',
        });
        e.preventDefault();
        return false;
    });
});

window.thiuff = window.thiuff || {};

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

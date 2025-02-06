require(["gitbook", "jQuery"], function(gitbook, $) {
    function addSlidesButton() {
        var baseurl = gitbook.state.root; // Get base URL
        var currentPage = window.location.pathname.split("/").pop().replace(".html", "");
        var slideURL = baseurl + "slides/" + currentPage + ".html";

        // Check if slides exist before adding the button
        $.ajax({
            url: slideURL,
            type: 'HEAD',
            success: function() {
                console.log("Slides found, adding button...");

                // Create the button
                var button = $('<a>', {
                    "class": "slides-button",
                    "title": "View Slides",
                    "href": slideURL
                }).append('<i class="fa fa-file-powerpoint-o"></i>');

                // Insert the button into the left toolbar (before ToC button)
                $(".book-summary").prepend(button);
            },
            error: function() {
                console.log("Slides not found: " + slideURL);
            }
        });
    }

    gitbook.events.bind("start", function(e, config) {
        addSlidesButton();
    });
});
﻿

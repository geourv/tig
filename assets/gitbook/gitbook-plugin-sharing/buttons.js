require(['gitbook', 'jquery'], function(gitbook, $) {
    var SITES = {
        'facebook': {
            'label': 'Facebook',
            'icon': 'fa fa-facebook',
            'onClick': function(e) {
                e.preventDefault();
                window.open('http://www.facebook.com/sharer/sharer.php?s=100&p[url]='+encodeURIComponent(location.href));
            }
        },
        'twitter': {
            'label': 'Twitter',
            'icon': 'fa fa-twitter',
            'onClick': function(e) {
                e.preventDefault();
                window.open('http://twitter.com/home?status='+encodeURIComponent(document.title+' '+location.href));
            }
        },
        'github': {
            'label': 'Github',
            'icon': 'fa fa-github',
            'onClick': function(e) {
                e.preventDefault();
                window.open('https://github.com');
            }
        }
    };

    gitbook.events.bind('start', function(e, config) {
        var opts = config.sharing;

        // Create dropdown menu
        var menu = $.map(opts.all, function(id) {
            var site = SITES[id];
            return {
                text: site.label,
                onClick: site.onClick
            };
        });

        // Create main button with dropdown
        if (menu.length > 0) {
            gitbook.toolbar.createButton({
                icon: 'fa fa-share-alt',
                label: 'Share',
                position: 'right',
                dropdown: [menu]
            });
        }

        // 🔹 Add the "View Slides" Button in the GitBook Toolbar
        $(document).ready(function() {
            var baseurl = (typeof gitbook.state.basePath !== "undefined") ? gitbook.state.basePath : "";
            var currentPage = window.location.pathname.split("/").pop().replace(".html", "");
            var slideURL = baseurl + "slides/" + currentPage + ".html";  // Adjust for your setup

            $.ajax({
                url: slideURL,
                type: 'HEAD',
                success: function() {
                    console.log("Slides found: Adding button...");

                    // Add button to GitBook toolbar
                    gitbook.toolbar.createButton({
                        icon: 'fa fa-file-powerpoint-o', // PowerPoint style icon
                        label: 'View Slides',
                        position: 'right', // Places it in the navbar
                        onClick: function(e) {
                            e.preventDefault();
                            window.location.href = slideURL;
                        }
                    });
                },
                error: function() {
                    console.log("Slides not found: " + slideURL);
                }
            });
        });

        // Direct actions to share
        $.each(SITES, function(sideId, site) {
            if (!opts[sideId]) return;

            var onClick = site.onClick;
            
            // Override target link with provided link
            var side_link = opts[`${sideId}_link`];
            if (side_link !== undefined && side_link !== "") {
                onClick = function(e) {
                    e.preventDefault();
                    window.open(side_link);
                };
            }

            gitbook.toolbar.createButton({
                icon: site.icon,
                label: site.text,
                position: 'right',
                onClick: onClick
            });
        });
    });
});


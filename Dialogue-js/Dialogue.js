/* Author: Emmy Noether of IntransigentMS (intransigentms.com) */
var Dialogue = (function() {
    var load = function(c, o) {
        return (function() {
            var convo = c;
            var opts = o;

            var node = c;
            var nodeIndex = [];
            var lastPrompt = "";

            var talk = function(selection) {
                function exit() {
                    if (opts.callback) {
                        opts.callback();
                    }
                    if (!opts.nodispose) {
                        cm.dispose();
                    }
                    return lastPrompt;
                }

                var i;
                if (selection !== undefined) {
                    if (selection == -1) {
                        if (opts.endchat == "continue") {
                            selection = 0;
                        } else if (opts.endchat == "back") {
                            selection = -3;
                        } else if (opts.endchat == "stay") {
                            selection = -1;
                        } else {
                            return exit();
                        }
                    }

                    if (nodeIndex.length === 0 && selection < -1) return exit();

                    if (selection >= 0) {
                        if (!node.choices[selection]) return exit();
                        node = node.choices[selection][1];
                        nodeIndex.push(selection);
                    } else if (selection != -1) {
                        for (i = -2; i > selection; --i) {
                            if (nodeIndex.pop() === undefined) return exit();
                        }
                        node = convo;
                        for (i = 0; i < nodeIndex.length; ++i) {
                            node = node.choices[nodeIndex[i]][1];
                        }
                    }
                }

                if (!node || !node.prompt) return exit();
                lastPrompt = node.prompt;
                if (!node.choices) {
                    cm.sendOk(lastPrompt);
                    return exit();
                }

                var message = lastPrompt + "\r\n\r\n";
                var choices = node.choices;
                for (i = 0; i < choices.length; ++i) {
                    var choice = choices[i];
                    if (choice[1].move !== undefined) {
                        message += "#L" + (choice[1].move > 0 ? i : (choice[1].move == 0 ? -1 : choice[1].move - 2)) + "#" + choice[0] + "#l\r\n";
                    } else {
                        message += "#L" + i + "#" + (Array.isArray(choice) ? choice[0] : choice) + "#l\r\n";
                    }
                }
                cm.sendSimple(message);
            };

            var setCallback = function(cb) {
                opts.callback = cb;
            };

            var setEndChat = function(ec) {
                opts.endchat = ec;
            };

            var setNoDispose = function(nd) {
                opts.nodispose = nd;
            }

            var unload = function() {
                convo = opts = node = nodeIndex = lastPrompt = void 0;
                delete this.setCallback;
                delete this.setEndChat;
                delete this.setNoDispose;
                delete this.talk;
                delete this.unload;
            };

            return {
                talk: talk,
                setCallback: setCallback,
                setEndChat: setEndChat,
                setNoDispose: setNoDispose,
                unload: unload
            };
        })();
    };

    return {
        load: load
    };
})();

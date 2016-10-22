Dialogue.js / Dialogue.min.js
=============================

####Author: Emmy Noether of IntransigentMS ([intransigentms.com](http://intransigentms.com/splash.html))
____________________________

Table Of Contents
-----------------
* [How To Use](#how-to-use)
* [Transcript Format](#transcript-format)
* [Options](#options)
* [Changing Options After Loading](#changing-options-after-loading)
* [Example](#example)

____________________________

<a name="how-to-use">How To Use</a>
----------
Copy + paste the contents of **Dialogue.min.js** somewhere into the top of your NPC script, or load in the **Dialogue.min.js** file if you're fancy like that.

Create a new dialogue variable like so:
```javascript
var myDialogue = Dialogue.load(transcript[, options]);
```
Where `transcript` is a Javascript object (hard-coded or from a *.json) containing the dialogue's transcript formatted as specified in [Transcript Format](#transcript-format) below, and `options` is an optional argument consisting of an object with any of the properties as defined below in [Options](#options).

You only want to call this function once, so a good paradigm is to put any instances of the `load()` function in your NPC's `start()` function, or at least qualify them with some conditional.

Now that you have your dialogue variable (in this case, `myDialogue`), the dialogue can be used as follows:
```javascript
myDialogue.talk(selection);
```
Where `selection` is the variable (should be from a function parameter) that stores the player's last selection choice.

`selection` should be absent or undefined the first time that `talk()` is called, to start the conversation. (Can also be used to raise the conversation at any time where it last was, i.e. **not** progressing as if the user made a selection.)

For example:
```javascript
if (status === 0) {
    myDialogue.talk();
} else {
    myDialogue.talk(selection);
}

// or, equivalently:

myDialogue.talk(status === 0 ? void 0 : selection);
```
This is all that really needs to be done. See "Example" below for a simple example of a common usage.

The `talk()` function returns `undefined` when the conversation progresses normally, and returns a string with the contents of the last prompt displayed to the player upon `exit`ing.

You can also unload a dialogue if it is no longer in use:
```javascript
myDialogue.unload();
```
...but it is not typically necessary to do so.

<a name="transcript-format">Transcript Format</a>
-----------------
Perhaps the best way to figure out the format is to simply check the example under the [Example](#example) header below.

Transcripts are objects (denoted with `{ }`), with objects/arrays nested inside to create a tree structure.
Each object has a `prompt` property, which holds a string containing whatever the NPC says at that point.
In addition, it has a `choices` property (actually optional, sends an "OK" dialogue with the prompt if absent), which is a list of choices for the user to make. Each choice can be one of two things:

1. A simple string, simply containing the text for that selection.
  * When a user chooses one of these selections, the dialogue is ended.

2. A 2-element array (denoted with `[ ]`), with the first element being a string containing the text for that selection, and the second element being an object contining another `prompt` and `choices`.
  * The second element, of course, corresponds to the prompt and choices that the player gets if they select this particular choice.

Objects that would normally have `prompt`s and `choices`s can also *instead* be either **movement nodes** or **goto nodes**. These objects, instead of having `prompt` and `choices`, have a single property called either `move` or `goto`, which is an integer:

* `goto === x` : Moves directly to the first node `n` in the dialogue tree such that `n.id === x`. Any node can have an `id` property.
* `move < 0` : Backtracks `move` nodes in the dialogue tree, e.g. `move: -1` would act similarly to a *Previous* button.
* `move > 0` : Guaranteed to exit chat if this is selected.
* `move === 0` : Counts as if the player selected "End Chat" (viz.: `selection = -1`).

<a name="options">Options</a>
-------
* `endchat` : Controls the behavior for when `selection === -1`, i.e. the player presed "End Chat", or hit a node with `move === 0`.
    - Possible values:
        + `"exit"` : This is the default value, and exits normally, calling the `callback` if there is one, and returning the last prompt displayed to the player.
        + `"continue"` : Behaves as if the user selected the first option (`selection = 0`).
        + `"back"` : Behaves like a *Previous* button, going to the previous node.
        + `"stay"` : Do nothing.
* `nodispose` : Default value is `false`; set this to `true` if you do not want the dialogue to `dispose()` the NPC conversation when it `exit`s. Useful for chaining dialogues together, using the return value of `talk()` to decide what to do next.
* `callback` : This option must be equal to a `function`, which is then called as soon as the dialogue `exit`s, i.e. before `dispose()`ing (assuming `nodispose == false`). By default no function is called.

<a name="changing-options-after-loading">Changing Options After Loading</a>
------------------------------
It is also possible to change the options of a dialogue after having already created the dialogue variable:
```javascript
myDialogue.setCallback(function() {
    print("The dialogue is over.");
});
```

Functions:

* `setCallback(callback)`
* `setEndChat(endchat)`
* `setNoDispose(nodispose)`

<a name="example">Example</a>
-------
```javascript
var myTranscript = {
    prompt: "No one likes hard-coding nested switch statements " +
                                  "inside of switch statements " +
                                  "inside of switch statements " +
                                  "inside of... right?",
    choices: [
        ["Yeah, I like JSON anyways.", {
            prompt: "Right? I mean, if you can convert it to JSON it's all good as far as I'm concerned.",
            choices: [
                "Click here to exit.",
                "Or here, if you like."
            ]
        }],
        ["No weird temp variables and knick-knacks for keeping track of shit? Easier on the eyes? Sign me up.", {
            prompt: "What are you waiting for? Paste this shit in your scripts!",
            choices: [
                ["Show me a man in an ushanka.", {
                    prompt: "Sure thing:\r\n  [*|:^)"
                }],
                ["Actually, can I just go back?", {
                    move: -1
                }],
                "(clear throat and paste minified Javascript quietly)"
            ]
        }],
        ["Err... I actually think it's great. I enjoy it #eevery time#n I rewrite the same thing.", {
            prompt: "Bullshit. Just for that, I've trapped you in this dialogue box.",
            choices: [
                ["D:", {
                    move: 0
                }]
            ]
        }]
    ]
};

var status, currentDialogue;

function start() {
    currentDialogue = Dialogue.load(myTranscript, { endchat: "stay", callback: function() { print("callback!"); } });
    status = -1;
    action(1, 0, 0);
}

function action(mode, type, selection) {
    mode >= 0 ? ++status : --status;
    currentDialogue.talk(status === 0 ? void 0 : selection);
}
```

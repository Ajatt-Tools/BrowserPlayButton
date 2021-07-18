<p align="center"><img src="icons/play.png" alt="icon" width="128px"></p>

# Browser Play Button

[![Rate on AnkiWeb](https://glutanimate.com/logos/ankiweb-rate.svg)](https://ankiweb.net/shared/info/xxx)
[![Chat](https://img.shields.io/badge/chat-join-green)](https://tatsumoto-ren.github.io/blog/join-our-community.html)
[![Channel](https://shields.io/badge/channel-subscribe-blue?logo=telegram&color=3faee8)](https://t.me/ajatt_tools)
[![Patreon](https://img.shields.io/badge/patreon-support-orange)](https://www.patreon.com/bePatron?u=43555128)
![GitHub](https://img.shields.io/github/license/Ajatt-Tools/BrowserPlayButton)

This tiny add-on adds a play button to the Anki Browser's toolbar.
When clicked, it looks for `[sound:...]`-tags on the selected note
and plays them in the order of their appearance on the note's fields.
If there is selected text, the action is limited to the sound tags
that appear only in the selected text.
If you select "Play field" in the context menu,
the action is limited to the currently selected field.

Audio can be directly played with a shortcut: `alt + m`.

This add-on is similar to
[Play audio in browser](https://ankiweb.net/shared/info/388541036)
but doesn't create any dialog windows when playing audio.

## Installation

Install from [AnkiWeb](https://ankiweb.net/shared/info/xxx), or manually with `git`:

```
$ git clone 'https://github.com/Ajatt-Tools/BrowserPlayButton.git' ~/.local/share/Anki2/addons21/BrowserPlayButton
```

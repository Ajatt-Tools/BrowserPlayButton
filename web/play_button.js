const BrowserPlayButton = {
    class_name: 'ajt-play-icon',
    make_play_button: (ord) => {
        const play_button = document.createElement('span')
        play_button.classList.add(BrowserPlayButton.class_name)
        play_button.setAttribute('title', 'play sound')
        play_button.addEventListener('click', () => pycmd(`play_field:${ord}`))
        return play_button
    },
    load_icons: () => {
        // forEditorField is supported by Anki 2.1.41+
        pycmd(`get_fields_with_audio`, (fields) => {
            forEditorField(fields, (field, contains_audio) => {
                if (field.play_button === undefined) {
                    const play_button = BrowserPlayButton.make_play_button(field.getAttribute("ord"))
                    field.labelContainer.insertBefore(play_button, field.label)
                    field.play_button = play_button
                }
                field.play_button.classList.toggle('hidden', !contains_audio)
            })
        })
    },
    hide_icons: () => {
        const fields = document.getElementById("fields")
        if (fields) {
            for (const icon of fields.getElementsByClassName(BrowserPlayButton.class_name)) {
                icon.classList.toggle('hidden', true)
            }
        }
    },
};

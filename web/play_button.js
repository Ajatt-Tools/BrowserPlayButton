const BrowserPlayButton = {
    make_play_button: (ord, display) => {
        const play_button = document.createElement('span')
        play_button.classList.add('play-icon')
        play_button.addEventListener('click', () => pycmd(`play_field:${ord}`))
        if (!display) {
            play_button.classList.add('hidden')
        }
        return play_button
    },
    load_icons: () => {
        pycmd(`get_fields_with_audio`, (fields) => {
            forEditorField(fields, (field, contains_audio) => {
                if (field.play_button === undefined) {
                    const play_button = BrowserPlayButton.make_play_button(field.getAttribute("ord"), contains_audio)
                    field.labelContainer.insertBefore(play_button, field.label)
                    field.play_button = play_button
                } else {
                    field.play_button.classList.toggle('hidden', !contains_audio)
                }
            })
        })
    },
};

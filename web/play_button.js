const BrowserPlayButton = {
    class_name: 'ajt-play-icon',
    trailing_num_regex: /[0-9]+$/,
    make_play_button: (ord) => {
        const play_button = document.createElement('span')
        play_button.classList.add(BrowserPlayButton.class_name)
        play_button.setAttribute('title', 'play sound')
        play_button.addEventListener('click', () => pycmd(`play_field:${ord}`))
        return play_button
    },
    load_icons: () => {
        pycmd(`get_fields_with_audio`, (audio_flags) => {
            const fnames = document.querySelectorAll('.fname')
            if (audio_flags.length == fnames.length) {
                audio_flags.forEach((contains_audio, i) => {
                    const field_id = BrowserPlayButton.trailing_num_regex.exec(fnames[i].id)
                    let play_button = fnames[i].getElementsByClassName(BrowserPlayButton.class_name)[0]
                    if (!play_button) {
                        play_button = BrowserPlayButton.make_play_button(field_id)
                        fnames[i].prepend(play_button)
                    }
                    play_button.toggleAttribute('hidden', !contains_audio)
                })
            }
        })
    },
    hide_icons: () => {
        const fields = document.getElementById("fields")
        if (fields) {
            for (const icon of fields.getElementsByClassName(BrowserPlayButton.class_name)) {
                icon.toggleAttribute('hidden', true)
            }
        }
    },
};

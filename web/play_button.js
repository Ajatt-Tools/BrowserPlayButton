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
        pycmd(`get_fields_with_audio`, (audio_flags) => {
            const label_containers = document.querySelectorAll('.label-container > span:last-child')
            if (label_containers.length > 0 && audio_flags !== null) {
                audio_flags.forEach((contains_audio, i) => {
                    let play_button = label_containers[i].getElementsByClassName(BrowserPlayButton.class_name)[0]
                    if (!play_button) {
                        play_button = BrowserPlayButton.make_play_button(i)
                        label_containers[i].prepend(play_button)
                    }
                    play_button.toggleAttribute('hidden', !contains_audio)
                })
            }
        })
    },
    hide_icons: () => {
        const fields = document.querySelector(".fields")
        if (fields) {
            for (const icon of fields.getElementsByClassName(BrowserPlayButton.class_name)) {
                icon.toggleAttribute('hidden', true)
            }
        }
    },
};

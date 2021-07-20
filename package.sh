#!/bin/sh

cd -- "$(git rev-parse --show-toplevel)" &&
	git archive HEAD --format=zip -o "browser_play_button_$(git branch --show-current).ankiaddon"

# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import re

ADDON_NAME = 'Browser Play Button'
PLAY_ICON_FILEPATH = 'icons/play.png'
MEDIA_TAG_REGEX = re.compile(r'\[sound:([^\[\]]+?\.[^\[\]]+?)]', flags=re.MULTILINE | re.IGNORECASE)
TOOLTIP_ITEM_OFFSET = 14
TOOLTIP_INITIAL_OFFSET = 80

import re

ADDON_NAME = 'Browser Play Button'
PLAY_ICON_FILEPATH = 'icons/play.png'
MEDIA_TAG_REGEX = re.compile(r'\[sound:([^\[\]]+?\.[^\[\]]+?)]', flags=re.MULTILINE | re.IGNORECASE)
TOOLTIP_ITEM_OFFSET = 14
TOOLTIP_INITIAL_OFFSET = 80

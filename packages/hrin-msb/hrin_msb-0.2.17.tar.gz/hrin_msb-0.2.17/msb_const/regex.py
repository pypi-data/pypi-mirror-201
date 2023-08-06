"""
REGEX PATTERNS FOR ENV FILE
"""
REGEX_TO_SELECT_ENV_VARIABLE = r"(\s)*?([\w_]*)=(['\"])?([\w\d()\-:/*?=@.+!%$_#^&,]*)(['\"])?([\s\r\n]*)"
REGEX_TO_REPLACE_ENV_VARIABLE = r'\1\2=\3\2_VALUE\5\6'
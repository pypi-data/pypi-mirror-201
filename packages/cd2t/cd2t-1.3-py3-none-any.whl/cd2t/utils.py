import re

    
def _re_fullmatch(regex_string, test_string):
    return re.fullmatch(regex_string, test_string)
def _re_fullmatch_multi(regex_string, test_string):
    return re.fullmatch(regex_string, test_string, re.MULTILINE)
def _re_search(regex_string, test_string):
    return re.search(regex_string, test_string)
def _re_search_multi(regex_string, test_string):
    return re.search(regex_string, test_string, re.MULTILINE)

def get_match_function(multiline :bool, full_match :bool):
    if full_match:
        if multiline:
            return _re_fullmatch_multi
        else:
            return _re_fullmatch
    else:
        if multiline:
            return _re_search_multi
        else:
            return _re_search

def string_matches_regex_list(string :str, regex_list :list, multiline=False, full_match=False):
    match_fct = get_match_function(multiline, full_match)
    for regex in regex_list:
        match = match_fct(regex, string)
        if match:
            return regex
    return None

def any_string_matches_regex_list(strings :list, regex_list :list, multiline=False, full_match=False):
    for string in strings:
        match = string_matches_regex_list(string, regex_list, multiline, full_match)
        if match:
            return string, match
    return None

def regex_matches_in_string_list(regex :str, strings :list, multiline=False, full_match=False):
    match_fct = get_match_function(multiline, full_match)
    for string in strings:
        match = match_fct(regex, string)
        if match:
            return string
    return None

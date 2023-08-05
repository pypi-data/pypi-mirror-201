from typing import List, NoReturn, Tuple, Union


def reverse_lookup(lookup: str, match_list: Union['List', 'Tuple']) -> Union[str, NoReturn]:
    """Matches word in list to the phrase given.

    Args:
        lookup: Takes the phrase spoken as an argument in lowercase.
        match_list: List or tuple of words against which the phrase has to be checked.

    Returns:
        str:
        Returns the word that was reverse matched.
    """
    reverse = sum([w.split() for w in match_list], [])  # extract multi worded conditions in match list
    for word in lookup.split():  # loop through words in the phrase
        if word in reverse:  # check at least one word in phrase matches the multi worded condition
            return word


def word_match(phrase: str, match_list: Union['List', 'Tuple'], strict: bool = False) -> Union[str, NoReturn]:
    """Matches phrase to word list given.

    Args:
        phrase: Takes the phrase spoken as an argument.
        match_list: List or tuple of words against which the phrase has to be checked.
        strict: Look for the exact word match instead of regex.

    Returns:
        str:
        Returns the word that was matched.
    """
    if not all((phrase, match_list)):
        return
    if strict:  # simply check at least one string in the match list is present in phrase
        lookup = phrase.lower().split()
        for word in match_list:
            if word in lookup:
                return word
    else:
        lookup = phrase.lower()
        for word in match_list:  # loop through strings in the match list
            # check if the string is present in phrase and vice versa
            if word in lookup and reverse_lookup(lookup=lookup, match_list=match_list):
                return word

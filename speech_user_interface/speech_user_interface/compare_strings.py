from fuzzywuzzy import fuzz


def compare_strings(str1, str2):
    # Use fuzz.ratio to compare the two strings
    similarity_score = fuzz.ratio(str1, str2)
    return similarity_score / 100

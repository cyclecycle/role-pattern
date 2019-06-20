import collections
from spacy.matcher import DependencyTreeMatcher


class RolePatternMatch(collections.UserDict):

    def __init__(self, *args, **kwargs):
        self.match_tokens = []
        super().__init__(*args, **kwargs)


def build_matcher(vocab, pattern_dict):
    matcher = DependencyTreeMatcher(vocab)
    for name, pattern in pattern_dict.items():
        dep_pattern = pattern['spacy_dep_pattern']
        matcher.add(name, None, dep_pattern)
    return matcher


def find_matches(doc, pattern, pattern_name='pattern'):
    pattern_dict = {pattern_name: pattern}
    matcher = build_matcher(doc.vocab, pattern_dict)
    matches = matcher(doc)
    labels = pattern['token_labels']
    match_list = []
    for match_id, token_idxs in matches:
        pattern_name = matcher.vocab.strings[match_id]
        tokens = [doc[idx] for idx in token_idxs]
        labels = pattern['token_labels']
        match_dict = label_tokens(tokens, labels)
        match_dict = RolePatternMatch(match_dict)
        match_dict.match_tokens = tokens
        match_list.append(match_dict)
    return match_list


def label_tokens(tokens, labels):
    tokens = sorted(tokens, key=lambda t: t.i)
    match_dict = {label: [] for label in labels if label}
    for label, token in zip(labels, tokens):
        if label:
            match_dict[label].append(token)
    return match_dict
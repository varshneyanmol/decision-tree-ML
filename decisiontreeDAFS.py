import collections
from math import log
from functools import partial

inputs = [
    ({'level': 'Senior', 'lang': 'Java', 'tweets': 'no', 'phd': 'no'},
     False),
    ({'level': 'Senior', 'lang': 'Java', 'tweets': 'no', 'phd': 'yes'},
     False),
    ({'level': 'Mid', 'lang': 'Python', 'tweets': 'no', 'phd': 'no'},
     True),
    ({'level': 'Junior', 'lang': 'Python', 'tweets': 'no', 'phd': 'no'},
     True),
    ({'level': 'Junior', 'lang': 'R', 'tweets': 'yes', 'phd': 'no'},
     True),
    ({'level': 'Junior', 'lang': 'R', 'tweets': 'yes', 'phd': 'yes'},
     False),
    ({'level': 'Mid', 'lang': 'R', 'tweets': 'yes', 'phd': 'yes'},
     True),
    ({'level': 'Senior', 'lang': 'Python', 'tweets': 'no', 'phd': 'no'}, False),
    ({'level': 'Senior', 'lang': 'R', 'tweets': 'yes', 'phd': 'no'},
     True),
    ({'level': 'Junior', 'lang': 'Python', 'tweets': 'yes', 'phd': 'no'}, True),
    ({'level': 'Senior', 'lang': 'Python', 'tweets': 'yes', 'phd': 'yes'}, True),
    ({'level': 'Mid', 'lang': 'Python', 'tweets': 'no', 'phd': 'yes'},
     True),
    ({'level': 'Mid', 'lang': 'Java', 'tweets': 'yes', 'phd': 'no'},
     True),
    ({'level': 'Junior', 'lang': 'Python', 'tweets': 'no', 'phd': 'yes'}, False)
]


def entropy(class_probabilities):
    '''computes the entropy, given the list of class probabilities'''
    return sum(-p * log(p, 2) for p in class_probabilities if p)    # ignores zero probabilities


def data_entropy(labeled_data):
    labels = [label for _,label in labeled_data]
    total_count = len(labels)
    class_probabilities = [count/total_count for count in collections.Counter(labels).values()]
    return entropy(class_probabilities)


def partition_by_attribute(inputs, attribute):
    '''every input is a pair of (attribute_dict, lavel)
    this funciton returns a dict with atrribute_value as key and all the inputs corrosponding to that attribute_value as value'''
    groups = collections.defaultdict(list)
    for input in inputs:
        key = input[0][attribute]   # using value of the attribute as the key to the groups dict
        groups[key].append(input)   # adding that input to the correct list

    return groups


def partition_entropy(subsets):
    total_count = sum(len(subset) for subset in subsets)
    _partition_entropy = sum(data_entropy(subset)*(len(subset)/total_count)
                                for subset in subsets)
    return _partition_entropy


def partition_by_info_gain(inputs, attribute):
    parent_entropy = data_entropy(inputs)
    partitions = partition_by_attribute(inputs, attribute)
    return parent_entropy - partition_entropy(partitions.values())


def build_tree(inputs, split_candidates=None):
    if split_candidates is None:
        split_candidates = inputs[0][0].keys()

    num_inputs = len(inputs)
    num_trues = len([label for _, label in inputs if label])
    num_false = num_inputs - num_trues

    if num_trues == 0: return False
    if num_false == 0: return True

    if not split_candidates:
        return num_trues >= num_false

    best_candidate = max(split_candidates, key=partial(partition_by_info_gain, inputs))

    partitions = partition_by_attribute(inputs, best_candidate)
    new_candidates = [candidate for candidate in split_candidates if candidate != best_candidate]

    subtrees = {
        attribute_value: build_tree(subset, new_candidates)
        for attribute_value, subset in partitions.items()
    }

    subtrees[None] = num_trues >= num_false

    return (best_candidate, subtrees)


def classify(tree, input):
    if tree in [True, False]:
        return tree

    attribute, subtree_dict = tree
    subtree_key = input.get(attribute)
    if subtree_key not in subtree_dict:
        subtree_key = None

    subtree = subtree_dict[subtree_key]
    return classify(subtree, input)


if __name__ == '__main__':
    tree = build_tree(inputs)
    print(tree)

    answer = classify(tree, { "level" : "Junior",
    "lang" : "Java",
    "tweets" : "yes",
    "phd" : "no"} )
    print(answer)

    answer = classify(tree, { "level" : "Junior",
    "lang" : "Java",
    "tweets" : "yes",
    "phd" : "yes"} )
    print(answer)

    answer = classify(tree, { "level" : "Intern" } )
    print(answer)

    answer = classify(tree, { "level" : "Senior" } )
    print(answer)
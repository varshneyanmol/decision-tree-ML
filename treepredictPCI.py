import collections
from math import log

my_data = [
    ['slashdot', 'USA', 'yes', 18, 'None'],
    ['google', 'France', 'yes', 23, 'Premium'],
    ['digg', 'USA', 'yes', 24, 'Basic'],
    ['kiwitobes', 'France', 'yes', 23, 'Basic'],
    ['google', 'UK', 'no', 21, 'Premium'],
    ['(direct)', 'New Zealand', 'no', 12, 'None'],
    ['(direct)', 'UK', 'no', 21, 'Basic'],
    ['google', 'USA', 'no', 24, 'Premium'],
    ['slashdot', 'France', 'yes', 19, 'None'],
    ['digg', 'USA', 'no', 18, 'None'],
    ['google', 'UK', 'no', 18, 'None'],
    ['kiwitobes', 'UK', 'no', 19, 'None'],
    ['digg', 'New Zealand', 'yes', 12, 'Basic'],
    ['slashdot', 'UK', 'no', 21, 'None'],
    ['google', 'UK', 'yes', 18, 'Basic'],
    ['kiwitobes', 'France', 'yes', 19, 'Basic']
]


def getdata():
    return my_data


class decisionnode:
    def __init__(self, col = -1, value = None, tb = None, fb = None, results = None):
        self.col = col
        self.value = value
        self.tb = tb
        self.fb = fb
        self.results = results


def uniquecounts(rows):
    results = collections.defaultdict(int)
    for row in rows:
        r = row[len(row) - 1]
        results[r] += 1

    return results


def entropy(rows):
    results = uniquecounts(rows)
    total_rows = len(rows)
    ent = 0.0
    for result in results.keys():
        p = results[result] / total_rows
        ent -= p * log(p, 2)

    return ent


def divideset(rows, column, value):
    split_function = None
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row:row[column] >= value
    else:
        split_function = lambda row:row[column] == value

    set1 = []
    set2 = []
    for row in rows:
        if split_function(row):
            set1.append(row)
        else:
            set2.append(row)

    return (set1, set2)


def columnvalues(rows, col):
    column_values = []
    for row in rows:
        if row[col] not in column_values: column_values.append(row[col])
    return column_values


def buildtree(rows):
    if len(rows) == 0:
        return decisionnode()

    current_score = entropy(rows)
    column_count = len(rows[0]) - 1

    best_gain = 0.0
    best_criteria = None
    best_sets = None

    for col in range(0, column_count):
        column_values = columnvalues(rows, col)

        for value in column_values:
            (set1, set2) = divideset(rows, col, value)

            p = len(set1) / len(rows)
            info_gain = current_score - (p*entropy(set1) + (1-p)*entropy(set2))
            if info_gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = info_gain
                best_criteria = (col, value)
                best_sets = (set1, set2)

    if best_gain > 0:
        truebranch = buildtree(best_sets[0])
        falsebranch = buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0], value=best_criteria[1], tb=truebranch, fb=falsebranch)

    else:
        return decisionnode(results=uniquecounts(rows))


def classify(tree, observations):
    if tree.results != None:
        return tree.results
    else:
        value = observations[tree.col]
        if value == None:
            tr = classify(tree.tb, observations)
            fr = classify(tree.fb, observations)
            t_count = sum(tr.values())
            f_count = sum(fr.values())
            tw = t_count/(t_count + f_count)
            fw = f_count/(t_count + f_count)
            result = collections.defaultdict(float)
            for k, v in tr.items():
                result[k] = v*tw
            for k, v in fr.items():
                result[k] = v*fw
            return result
        else:
            if isinstance(value, int) or isinstance(value, float):
                if value >= tree.value:
                    branch = tree.tb
                else:
                    branch = tree.fb
            else:
                if value == tree.value:
                    branch = tree.tb
                else:
                    branch = tree.fb
            return classify(branch, observations)


if __name__ == '__main__':

    #print(uniquecounts(my_data))
    #print(entropy(my_data))
    #print(divideset(my_data, 0, 'slashdot'))
    #print(str(buildtree(my_data).tb.tb.results))
    tree = buildtree(my_data)
    print(classify(tree, ['(direct)', 'USA', 'yes', '5']))
    print(classify(tree, ['google', 'France', None, None]))
    print(classify(tree, ['google', None, 'yes', None]))
    print(classify(tree, [None, None, None, None]))
    print(classify(tree, ['slashdot', 'France', 'yes', 19, 'None']))
#!/usr/bin/env python
# encoding: utf-8

# The task is to maximize the `sum(len(friends[i]) for i in surfers)`, while
# keeping the difference between group sizes equal to minimum possible.

from collections import defaultdict
import random


def get_group_sizes(n_surfers, n_groups):
    """
    >>> get_group_sizes(10, 3)
    [4, 3, 3]
    """
    min_surfers_in_group = n_surfers // n_groups
    ret = [min_surfers_in_group for i in range(n_groups)]
    for i in range(n_surfers - min_surfers_in_group * n_groups):
        ret[i] += 1
    return ret


def shuffle_groups(surfers, n_groups):

    friends = defaultdict(set)

    result = []

    was_in_trip = [set() for i in range(n_groups)]

    for iteration in range(n_groups):
        groups = [set() for i in range(n_groups)]
        left_surfers = set(surfers)
        while left_surfers:
            trip_nums = list(range(n_groups))
            trip_nums = trip_nums[iteration:] + trip_nums[:iteration]
            for trip_num in trip_nums:
                candidates = list(left_surfers - was_in_trip[trip_num])
                if not candidates:
                    continue
                surfer = random.choice(candidates)
                left_surfers.remove(surfer)
                was_in_trip[trip_num].add(surfer)
                groups[trip_num].add(surfer)
        result.append(groups)

    for groups in result:
        for g in groups:
            for i in g:
                friends[i].update(g)

    score = sum(len(friends[i]) for i in surfers)

    return result, score


def check_result(surfers, n_groups, res):

    g = range(n_groups)

    for i in g:
        # all surfers should be in each round
        assert list(sorted(k for j in g for k in res[i][j])) == surfers
        # all surfers should be in each destination
        assert list(sorted(k for j in g for k in res[j][i])) == surfers

    # all trips should have at least `n_surfers // n_groups` members
    min_surfers_in_group = len(surfers) // n_groups

    return all(len(j) >= min_surfers_in_group for i in res for j in i)


def main(n_surfers, n_groups, iterations=100):
    best_score = 0
    surfers = list(range(1, n_surfers+1))
    for i in range(iterations):
        while True:
            result, score = shuffle_groups(surfers, n_groups)
            if check_result(surfers, n_groups, result):
                break
        if score > best_score:
            best_result, best_score = result, score
    for n, groups in enumerate(best_result, 1):
        print(f"Вылазка #{n}:")
        for n, i in enumerate(groups, 1):
            print(f"Группа {n}: {' '.join(map(lambda x: '%2s' % x, i))}")
        print()
    print(f"Score: {best_score}")


if __name__ == "__main__":
    import sys
    main(*map(int, sys.argv[1:]))

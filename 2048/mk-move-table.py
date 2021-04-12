#!/usr/bin/env python

from collections import defaultdict
from more_itertools import locate

all_numbers = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
one_row = []

def multi_dict(K, type):
    if K == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: multi_dict(K-1, type))

all_rows = multi_dict(4, int)

def move_row(row):
    ''' Moves one row according to the rules of the game 2048
        example [0, 2, 0, 2] => [4, 0, 0, 0]
        to test [2, 2, 2, 2] => [4, 4, 0, 0]
        to test [4, 2, 2, 0] => [4, 4, 0, 0]
    '''
    row_score = 0
    # Move all numbers to left. (or remove all 0's)
    all_numbers = list(locate(row))
    row_with_nmrs = [row[i] for i in all_numbers]
    if len(row_with_nmrs) > 1:
        for i in range(len(row_with_nmrs) - 1):
            if row_with_nmrs[i] == row_with_nmrs[i + 1]:
                row_with_nmrs[i] *= 2
                row_score += row_with_nmrs[i]
                row_with_nmrs[i + 1] = 0
    all_numbers = locate(row_with_nmrs)
    row = [row_with_nmrs[i] for i in all_numbers]
    # to add 0's at the end
    new_row = [0, 0, 0, 0]
    new_row[:len(row)] = row
    return new_row, row_score


for i1 in all_numbers:
    for i2 in all_numbers:
        for i3 in all_numbers:
            for i4 in all_numbers:
                this_row = [i4, i3, i2, i1]
                one_row, score = move_row(this_row)
                all_rows[i4][i3][i2][i1] = one_row

for i1 in all_numbers:
    for i2 in all_numbers:
        for i3 in all_numbers:
            for i4 in all_numbers:
                one_row = all_rows[i4][i3][i2][i1]
                print("Old: [{},{},{},{}]: New: {}".format(i4,i3,i2,i1,one_row))


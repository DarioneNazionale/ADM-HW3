#!/usr/bin/env python
# coding: utf-8

def algorithm(s):
    n = len(s)

    # Create a table to store results of subproblems
    L = [[0 for x in range(n)] for x in range(n)]

    # Strings of length 1 are palindrome of length 1
    for i in range(n):
        L[i][i] = 1

    # sub_l is length of substring
    for sub_l in range(2, n+1):
        for i in range(n-sub_l+1):
            j = i+sub_l-1
            if s[i] == s[j] and sub_l == 2:
                L[i][j] = 2
            elif s[i] == s[j]:
                L[i][j] = L[i+1][j-1] + 2
            else:
                L[i][j] = max(L[i][j-1], L[i+1][j]);

    return L[0][n-1]



print(algorithm("DATAMININGSAPIENZA"))

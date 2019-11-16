"""
for solve this problem we use dynamic programming, we build a matrix of zeros
where rows and columns are equal to the number of letters in the input string,
then each element L[i][j] of the matrix represent the length of the maximum palindrome
substring contained in the section of the original string s that goes from the ith
character to the jth one.

so first we fill the diagonal (since all letters by it sel is a palindrome word of length 1)
then we continue with the upper diagonal until we reach the upper right element that contains
the length on maximum palindrome string contained in all the string.
since the right upper triangle is a mirrored copy of the left lower triangle we don't need to
compute all the matrix, but just the upper triangle.

furthermore we can observe that each element of the upper triangle (except for the diagonals)
can be built exploiting the elements at the left and and below, since this two elements represents
the two the length of the biggest palindrome substring, so if the two characters represented by
the row and the column aren't equal the biggest palindrome the biggest palindrome string will be the
the te greater individuated by the two sub strings (the left and the lower elements)
if instead this two characters are equal that means that the biggest sub string will be incremented by 2,
since this two characters can be added as end and start of the new palindrome sub string.
"""

def algorithm(string):
    n = len(string)

    # Create a table to store results of subproblems
    L = [[0 for x in range(n)] for x in range(n)]

    # Strings of length 1 are palindrome of length 1
    for i in range(n):
        L[i][i] = 1

    # sub_l is the length of the substring
    for sub_l in range(2, n+1):
        for i in range(n-sub_l+1):
            j = i+sub_l-1
            if string[i] == string[j] and sub_l == 2:
                L[i][j] = 2
            elif string[i] == string[j]:
                L[i][j] = L[i+1][j-1] + 2
            else:
                L[i][j] = max(L[i][j-1], L[i+1][j]);

    #returning the upper right element.
    return L[0][n-1]



print(algorithm("DATAMININGSAPIENZA"))

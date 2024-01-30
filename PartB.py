from PartA import PartAClass
import sys

# Runtime complexity: O(N + M), N being the number of unique tokens in file1, and M being the number of tokens in
# file 2, as file2 could have more tokens than file1 vice versa, where tokenizing the tokens of both and turning the lists into dictionaries
# both take linear time. Also, the for loop on line 25 loops through file 1's dictionary and checks if each key
# exists in file 2's dictionary, each check taking constant O(1) time (in Python3+)
def intersection(file_1, file_2):
    # Tokenizing the files and storing the results
    newPartAObject = PartAClass()
    file1Tokens = newPartAObject.tokenize(file_1) # takes O(N) time
    file2Tokens = newPartAObject.tokenize(file_2) # takes O(M) time

    commonCount = 0

    # I turn the token lists into dictionaries so that I could easily check if a dictionary has a certain key in O(1) time
    file1Dict = newPartAObject.computeWordFrequencies(file1Tokens) # takes O(N) time
    file2Dict = newPartAObject.computeWordFrequencies(file2Tokens) # takes O(M) time

    # If the token exists in the other dictionary, then I increment the commonCount by 1
    # This for loop loops through N keys, checking if each key exists in O(1) time in Python3, 
    # which results in O(N) total time for the loop
    for token in file1Dict.keys():
        if token in file2Dict:
            commonCount += 1

    print(commonCount)
        

if __name__ == "__main__":
    try:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
    except IndexError:
        print("Not enough arguments.")
        sys.exit(0)
    intersection(file1, file2)

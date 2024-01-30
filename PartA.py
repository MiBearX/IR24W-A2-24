from pathlib import Path
import sys


class PartAClass:
    # Runtime complexity: O(N), N being the number of characters in the file, where a for loop goes through each character
    # And does two constant checks on it, resulting in O(N) for the for loop. Everything else in the function takes
    # constant time.
    def tokenize(self, TextFilePath):
        tokensList = []
        currentToken = ""

        # Trying to open the file. If it opens, I continue tokenizing. If not, I print out an error message 
        # and the function stops.
        try:
            with open(Path(TextFilePath), mode="r", encoding="utf-8") as openedFile:
                # Getting the file size and then resetting the counter to the beginning of the file (constant time)
                fileSize = openedFile.seek(0, 2)
                openedFile.seek(0)

                # Looping through all of the characters in the file (O(N) time, N being the number of characters in the file)
                for i in range(0, fileSize - 1):
                    data = openedFile.read(1) # Reads a single character, taking constant time (O(1))

                    # Checking to see if the current character is an alphanumeric character or not
                    if (data.isalnum() and ord(data) <= 122): # Both the isalnum and ord built in functions take constant time (O(1))    
                        currentToken += data.lower() # .lower() happens on a single character, taking O(1) time
                    else:
                        if currentToken != "":
                            tokensList.append(currentToken) # appending takes O(1) time
                        currentToken = ""
                
                # Appending whatever is left
                if currentToken != "":
                    tokensList.append(currentToken) # appending takes O(1) time

                return sorted(tokensList)
        except FileNotFoundError:
            print("File was not found!")
            sys.exit(0)


    # Runtime complexity: O(N) as the for loop loops through the n items in the tokens list
    def computeWordFrequencies(self, tokensListInput):
        tokensMap = dict()

        # Loops through all the items in the list and checks to see if their lowercase version was accounted for
        # in the dictionary. If it exists, increment the frequency, else add it to the dictionary. Searching in a dictionary
        # in Python version 3+ takes O(1) time when using the "in" keyword, so this loop takes a total of O(N) time
        for token in tokensListInput:
            if token in tokensMap:
                tokensMap[token] += 1
            else:
                tokensMap[token] = 1

        return tokensMap

    # Runtime complexity: O(N * log N) as the dictionary is first sorted before being printed out. Python uses the Tim Sort
    # for its sorting algorithm, which takes O(N * log N) time.
    def print(self, tokensDict):
        # Sorting the dictionary based on the frequencies in a decreasing order, where tied tokens are alphabetized
        for token, frequency in sorted(tokensDict.items(), key=lambda item: (-item[1], item[0])):
            print(f"{token} - {frequency}")
    
if __name__ == "__main__":
    newPartAObject = PartAClass()
    try:
        sortList = newPartAObject.tokenize(sys.argv[1])
    except IndexError:
        print("Not enough arguments.")
        sys.exit(0)

    sortDict = newPartAObject.computeWordFrequencies(sortList)
    newPartAObject.print(sortDict)
    

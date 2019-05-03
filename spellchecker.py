import os
import pickle
import re
import sys

# change the way of checking - permutate check_word to a mineditdistance of 2
# cleaning by removing the words 

def spell_checker(check_word, filepath):
    """
    Check if spelling is done right, 
        if wrong spelling - suggested & corrected word is returned
        else signify word is spelt correctly
    @inputs: filepath takes in either the text.txt file 
             or the already saved pickle file
    """    
    if os.path.isfile(filepath):
        if filepath.endswith('.txt'):
            word_dict = build_dict(filepath) ## dump into local file and reload for ease of use
        elif filepath.endswith(".pkl"):
            word_dict = read_dict(filepath)
    print(check_word in word_dict)
    plausible_words = {}
    for word in word_dict:
        if check_word in word_dict:
            print("Word is spelled correctly!")
            return
        
        min_dist = minimumEditDistance(check_word.lower(), word)
        if len(word) > 8: 
            if min_dist <= 2:
                plausible_words[word] = min_dist
        else: # any word shorter than length of 8
            if min_dist <= 2:
                plausible_words[word] = min_dist
    
    best_word = sorted(plausible_words.items(), key=lambda item: item[1])[-1]
    print(f"This is the suggested correction to wrongly spelled word \"{check_word}\": {best_word[0]}")
    return
    
def read_dict(filepath):
    """
    Reads the pickle file that was pre-computed to save on computational time
    """
    with open(filepath, "rb") as f:
        word_dict = pickle.load(f)
        f.close()
    return word_dict
    
def build_dict(filepath, filename="word_dic.pkl"):
    """
    Build dictionary of words and their counts for spellchecking,
    sorted by their counts and then name
    """
    f = open(filepath)
    dic = {}
    abbr = {'Co.', 'Dr.', 'Jan.', 'Feb.', 'Mr.',
            'Ms.', 'Mrs.', 'Inc.', 'Mar.', 'Apr.',
            'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'}
    for sent in f:
        sent = remove_punctuations(sent)
        sent = standardize_sentence(sent)
        for word in sent:
            # is the fullstop part of a common abbreviation
            if word not in abbr:
                word = word.replace('.', '') 
            
            if word not in dic:
                dic[word] = 1
            else: 
                dic[word] += 1
    sorted_word_lst = sorted(dic.items(), key=lambda item: (item[1], item[0]), reverse=True)
    word_dict=  {word: counts for word, counts in sorted_word_lst if counts >= 10}
    
    f = open(f"./{filename}","wb")
    pickle.dump(dic, f)
    print("Written dictionary of word counts into pickle file")
    f.close()
    return word_dict

def standardize_sentence(sent):
    """
    Lowercase the words for spellcheck,
    and tokenize the sentence into a list of words
    """
    sent = [word.strip().lower() for word in sent.split()]
    return sent

def remove_punctuations(sent):
    """
    Remove punctuations that are certain to not appear in a word
    Excluded &, $, %, -, ', "."
    """
    punctuations = ["#", "\"", "(", ")", "{", "}", ",", "=", 
                    "+", "|", "<", ">", "[", "]", "_", "!", "@",
                    "^", "*", "?", "~", "`", "/", "\\"]
    for punc in punctuations:
        sent = sent.replace(punc, '') 
    return sent

def minimumEditDistance(target, source):
    """
    Adapted from github
    minimumEditDistance() two strings and find the minimum cost of transforming
    one into the other through substituting two characters and inserting or
    deleting a character. This algorithm is implemented dynamically (table).
    @params: Two strings (target, source).
    @return: Distance from target to source (integer).
    """
    n = len(target) # vertical
    m = len(source) # horizontal

    # Set up table and fill in appropriate initial numbers.
    distance = [[0 for i in range(m + 1)] for j in range(n + 1)]
    distance[0][0] = 0

    # insertion
    for i in range(1, n + 1):
        distance[i][0] = distance[i - 1][0] + 1

    # deletion
    for j in range(1, m + 1):
        distance[0][j] = distance[0][j - 1] + 1

    # Complete the table by finding hte lowest value of insertion/deletion/
    # substitution. Final minimum edit distance will be in the top-right
    # corner (distance[n][m]).
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            distance[i][j] = min(distance[i - 1][j] + 1,
                                 distance[i][j - 1] + 1,
                                 distance[i - 1][j - 1] + 
                                   substitution(source[j - 1], target[i - 1]))

    return distance[n][m]

def substitution(j, i):
    """
    substitution() takes two characters and finds the cost of substituting one
    for the other. If the characters are the same the cost is 0, while if they
    are within reasonable distance of each other the cost is 1, otherwise the
    cost is 2.
    @params: Two single characters.
    @return: The cost of a substition (integer: 0,1,2).
    """
    # If the letters are the same there is no cost of substituting them.
    if j == i:
        return 0
    elif j.lower() == i.lower():
        return 0


    # List used to find out whether a character was a 'likely' typo or not.
    # a-z, 0-9, comma, full stop, semi-colon, square bracket ([) and dash
    # are included in the list and maps to a string with all keys that
    # surround it. Surrounding keys are taken to be 'likely' typos and given
    # a lesser weight of 1. 
    surrounding = {'1': 'q', '2': 'qw', '3': 'we', '4': 'er', 
                   '5': 'rt', '6': 'ty', '7': 'yu', '8': 'ui', 
                   '9': 'io', '0': 'op', '-': 'p', 'q': 'wsa', 
                   'w': 'qeasd', 'e': 'wrsdf', 'r': 'etdfg', 
                   't': 'ryfgh', 'y': 'tughj', 'u': 'yihjk', 
                   'i': 'uojkl', 'o': 'ipkl', 'p': 'ol', '[': 'p', 
                   'a': 'qwszx', 's': 'qweadzx', 'd': 'wersfxc', 
                   'f': 'ertdgcv', 'g': 'rtyfhvb', 'h': 'tyugjbn', 
                   'j': 'yuihknm', 'k': 'uiojlm', 'l': 'iopk', 
                   ';': 'olp', 'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 
                   'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk', 
                   '.': 'klm', ',': 'l'}

    if j.lower() in surrounding:
        if i.lower() in surrounding[j.lower()]:
            return 1
    return 2

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("please input: (word, filepath of pickle file/corpus)")
    spell_checker(sys.argv[1], sys.argv[2])

# E.gs to use --> volumes:=, weceives, white;
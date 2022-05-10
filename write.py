import numpy as np;
import re;

def GetCharacters():
    characters_file = open("characters.txt", "r");
    characters = characters_file.readlines();
    characters_file.close();

    character_list = [];

    for i in range(0, len(characters)):
        character = characters[i].upper()[:-1];
        if(not character in character_list):
            character_list.append(character);
    
    character_list.sort();

    character_list.append("NONE");

    return character_list;


def FinishQuote(new_text, goal_length, character_to_check):

    """
    Create the word dictionary.

    """

    lines_file = open("lines.txt", "r");
    lines = lines_file.readlines();
    lines_file.close();

    characters_file = open("characters.txt", "r");
    characters = characters_file.readlines();
    characters_file.close();

    character_for_line = {};
    for i in range(0, len(characters)):
        character_for_line[i] = characters[i].upper()[:-1];

    tempest_by_word = [];
    characters_by_word = [];

    """ 
    Finish the line
    
    """

    words_indices = {};
    for i in range(0, len(lines)):    
        split_line = lines[i].split();
        for word_unf in split_line:
            word = re.sub(r'[^\w\s]', '', word_unf).upper();
            if(not word in words_indices):
                words_indices[word] = len(words_indices);
            tempest_by_word.append(word);
            characters_by_word.append(character_for_line.get(i));
    indices_lookup = {v: k for k, v in words_indices.items()}

    max_length_to_look_back = len(new_text);
    while(len(new_text) < goal_length):
        max_length_to_look_back = min(max_length_to_look_back, 2); # BOUND WITHIN 2
        frequencies = [0 for i in range(0, len(words_indices))];
        while(True):
            length_to_look_back = max_length_to_look_back;
            if(length_to_look_back == 0):
                return ["WORD NOT FROUND FROM THE CHARACTER(S)"];
            for i in range(length_to_look_back, len(tempest_by_word)):
                flag = True;
                for j in range(0, length_to_look_back):
                    if(not tempest_by_word[i - length_to_look_back + j] == new_text[len(new_text) - length_to_look_back + j] or (not character_to_check == "NONE" and not characters_by_word[i - length_to_look_back + j] == character_to_check)):
                        flag = False;
                        break;
                if(flag):
                    frequencies[words_indices.get(tempest_by_word[i])] += 1;
            if(np.amax(frequencies) == 0):
                max_length_to_look_back -= 1;
                continue;
            break;
        new_text.append(indices_lookup.get(np.argmax(frequencies)));
        max_length_to_look_back += 1;
    return new_text

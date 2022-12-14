import re
import json
import numpy as np

def abbreviator(path):
    ''' 
    ###Reading the Test Name file
    path= input('Please enter test data file path')
    '''
   
    with open(str(path)) as file:
        names = file.readlines()
    #/Users/ebuka/Downloads/trees.txt


    '''Reading, wrangling, and sorting the letter scores
    letters= []
    values= []
    with open('/Users/ebuka/Downloads/values.txt') as file:
        for line in file:
            letters.append(line.rstrip().split()[0])                            # takes each line, creates a letter-value pair ['A': '25'], slice out the letter (index of 0) and append to a list: letters
            values.append(int(line.rstrip().split()[1]))                        # slices out the number (index of 1) from the letter-value pair ['A': '25'], converts to integer and append to a list: values
    postn_values = dict(zip(letters, values))                                   # create a dictionary from the two lists
    sorted_postn_values= dict(sorted(postn_values.items(), key=lambda x: x[1])) #sorts the dictionary, this will be necessary later in Abbreviation score.
    '''

    sorted_postn_values= {'Q': 1, 'Z': 1, 'J': 3, 'X': 3, 'K': 6, 'F': 7, 'H': 7, 'V': 7, 'W': 7, 'Y': 7, 'B': 8, 'C': 8, 'M': 8, 'P': 8, 'D': 9, 'G': 9, 'L': 15, 'N': 15, 'R': 15, 'S': 15, 'T': 15, 'O': 20, 'U': 20, 'A': 25, 'I': 25, 'E': 35}


    '''Clean Data: Separate compounded names (having special characters), remove special characters and new lines'''
    staged_names= []
    for  name in names:
        staged_names.append(name.upper().replace("'","").replace("\n",""))       
        cleaned_names= []
        for name in staged_names: 
            name = re.sub('[^a-zA-Z \n]', ' ', name)                            #replace any special character with space ie remove special characters
            name = re.sub('\s+',' ', name)                                      #replace multiple spaces with one
            name = name.lstrip().rstrip()                                       #remove leading and trailing spaces
            cleaned_names.append(name)
    #print(cleaned_names)


    def word_least_letter_checker(theword):
        '''
        Input: word -> string;
        Outputs = least_letter (letter having the least score), least_letter_score (score of the least letter), index_count(index of the least letter in the word)
        '''
        least_letter= None                                                    #defaults least letter to the second letter in the word
        least_letter_score= 1000                                              #corresponding score of the word
        index_count= 0                                                        #to track index of the letter (in the word) being checked

        for letter in theword[1:]:                                      
            index_count+=1
            
            if sorted_postn_values[letter] < least_letter_score or least_letter== None:              #if the current letter's score is lower than the established least score letter or there is no established least score
                least_letter= letter
                if index_count<=2 :                                                                   # if the index of th letter in the word is below 3, then add index to score
                    least_letter_score= sorted_postn_values[letter] + index_count           
                elif index_count> 2:                                                                  #if above 3, add 3 to the score
                    least_letter_score= sorted_postn_values[letter] + 3 

                if least_letter== theword[-1]:                                                        #if the least is the last letter(value defaults to 5), check if there is any letter with lower value than 5 and make it least
                    for letter in theword[1:-1]:
                        if sorted_postn_values[letter] < 5:
                            least_letter= letter                   
                            if index_count<=2:                                                         # if the index of th letter in the word is below 3, then add index to value
                                least_letter_score= sorted_postn_values[letter] + index_count           
                            elif index_count>=3:
                                least_letter_score= sorted_postn_values[letter] + 3            

                elif sorted_postn_values[least_letter] > 5 and theword[-1]!= 'E':                      #if the least letter is greater than 5 and the last letter is NOT E (if E it defaults to 20), make the last letter the least(defaults to 5) 
                    least_letter= theword[-1]
                    least_letter_score= 5
                elif sorted_postn_values[least_letter] > 20 and theword[-1]== 'E':                     #if the least letter is greater than 20 and the last letter is E, make it the least (it defaults to 20) 
                    least_letter = theword[-1]
                    least_letter_score= 20
                else: 
                    if index_count<=2 :                                                                   # if the index of th letter in the word is below 3, then add index to value
                        least_letter_score= sorted_postn_values[letter] + index_count           
                    elif index_count> 2:
                        least_letter_score= sorted_postn_values[letter] + 3                              #if the index of th letter in the word is above 3, then add 3 to value
    
        return(least_letter, least_letter_score, index_count)


    def least_score_checker_updated(name):
        '''
        Input-> string: name(words);
        output -> dicts: least_letter_tracker, least_score_tracker
            least_letter_tracker: dictionary containing the each word and the least letter, e.g for WONDER MAN {'WONDER': 'R', 'MAN': 'N'}, 
            least_score_tracker: dictionary containing the each word and the least letter score, e.g for WONDER MAN {'WONDER': 5, 'MAN': 5}
            '''
        index_count= 0
        least_letter_tracker= {}
        least_score_tracker= {}
        names_split = name.split()
        for theword in names_split:
            #print(theword)
            least_letter, least_letter_score, index_count= word_least_letter_checker(theword)
            least_score_tracker[theword]  = least_letter_score
            least_letter_tracker[theword]  = least_letter
        return (least_letter_tracker, least_score_tracker)


    def nameAbbreviator(name: str)->str:
        '''
        Input-> string: name 
        Output-> tuple: abb, score
            abb: abbreviation of the name(words)
            score: score of the abbreviation based on score of the letters and their positions
            '''
        abb= '' 
        score= -1
        abbreviations_dic= {}
        words=  name.split()                                                #slipt each name into words
        if len(words)==1:                                                   #if the name has only one word
            for word in words:                                              #for that word
                if len(word)<3:                                             #if the word has less than 3 letters
                    abb= ''                                                 # it can not have a three word abbreviation, return empty 
                    score= np.nan
                elif len(word) == 3:                                        #if a three letter word  
                    abb= word                                               #abb = the word
                    score_of_mid_letter= sorted_postn_values[word[1]]       #get the score of the middle letter
                    if abb[-1]== 'E':
                        score= score_of_mid_letter + 20                     #score of 1st letter =0, score of E as last = 20
                    else:
                        score= score_of_mid_letter + 5                      #score of 1st letter =0, score of last = 5
                elif len(word)> 3:
                    abb= word[0] 
                    least_letter, least_letter_score, least_index_count= word_least_letter_checker(word)        #get the least letter
                    if least_letter == word[-1]:                                                                                        #if the least is the last letter
                        second_least_letter, second_least_letter_score, second_least_index_count= word_least_letter_checker(word[:-1])  #drop the last letter, and find the second least
                        abb+= second_least_letter
                        abb+= least_letter
                        score= least_letter_score + second_least_letter_score
                    else:
                        second_least_letter, second_least_letter_score,second_least_index_count = word_least_letter_checker(word.replace(least_letter,''))  #drop the leatt letter, and find the second least
                        #if the letters are not in order within the abbreviation, exchange them
                        if second_least_index_count< least_index_count:                                             
                            abb+= second_least_letter
                            abb+= least_letter
                        else:
                            abb+= least_letter
                            abb+= second_least_letter
                        score+= least_letter_score + second_least_letter_score
                    
        elif len(words)>= 3:                                                #Best case Scenario, handling names with 3 or more words
            for word in words:                                              #for each of the words
                abb +=word[0]                                               #slice out the first letter of each word and create an abbreviation
                abb= abb[0:3]                                               #if abbreviation is longer than 3 letters, take the first three letters
                score= 0                                                    #since the abbreviation letters are the first letters in each word in the name, score = 0 (condition in the question)

        elif len(words)== 2 and len(name.replace(' ',''))== 3:              #Handling 2 words names with three letters like 'I AM' or 'AM I'
            abb= name.replace(' ','')                                       #remove the space
            for word in words:                                   
                if len(word[0])== 1:                                        #like 'I AM'
                    if abb[-1]== 'E':                                       #score of 1st letter in each word =0, score of E as last = 20, score of last(if not E) = 5
                        score=  20                                           
                    else:
                        score=  5                                            
                else:                                                       #like "AM I"
                    if abb[1]== 'E':
                        score=  20                                          #score of 1st letter in each word =0, score of E as last = 20, score of last(if not E) = 5
                    else:
                        score=  5
                        
        elif len(words)== 2:
            abb +=words[0][0]                                                                               #get the 1st letter of the 1st word(value =0)
            least_letter_tracker, least_score_tracker= least_score_checker_updated(name)                    #returns dicts containing each word and the least letter/ corrsp. score
            least_letter_word= list(least_score_tracker.keys())[list(least_score_tracker.values()).index(min(least_score_tracker.values()))]        #keeps track of the word containing the least letter in the name/ dict
            if least_letter_word == words[1]:                                                               #if the second word contains the letter with least score(then value of 1st letter in 2nd word =0)
                abb+= words[1][0]
                abb+= least_letter_tracker[least_letter_word]
                score = least_score_tracker[least_letter_word]                                              #value = 0(1st letter from 1st word) + 0(1st letter from 2nd word) + least_score_tracker[least_letter_word]

            elif least_letter_word == words[0]:                                                             #if the second word contains the letter with least score(then value of 1st letter in 2nd word =0)
                abb+= least_letter_tracker[least_letter_word]
                abb+= words[1][0]
                score = least_score_tracker[least_letter_word]                                              #value = 0(1st letter from 1st word) + least_score_tracker[least_letter_word] + 0(1st letter from 2nd word)
                

        return(abb, score)



    '''Putting it all together: Abbreviating each word in the cleaned data using the name abrbreviator function'''
    abbreviations_dic= {}
    abbreviatons_only= []
    for name in cleaned_names:
        abb, score= nameAbbreviator(name)
        abbreviations_dic[name]={abb: score}
        abbreviatons_only.append(abb)

    name_and_abb_dic = dict(zip(names, abbreviatons_only))               #gets each name from the original file and map it to the computed abbreviation

    names_and_abbs = []
    for name_only, abbreviation_only in name_and_abb_dic.items():        # convert the dictionary of name and abb to list for easy writing to txt file
        names_and_abbs.append(name_only.split('\n')[0])                  # get the original name, remove newline (\n) and add it to the list 
        names_and_abbs.append(abbreviation_only)                         # add the computed abbreviation to the list


    #Create output file name
    input_filename= path_name.split('/')[-1].split('.')[0].lower()
    surname= 'akwiwu-uzoma'
    output_name= surname +'_'+ input_filename + '_abbrevs.txt'

    #Write each item of the list as a new line to the output file
    with open(output_name, 'w') as file:
        file.write('\n'.join(names_and_abbs))                           

if __name__ == '__main__':
    path_name= input('Please enter data filename and path: ')
    names= abbreviator(path_name)


'''
path= input('Please enter data file path')
with open(str(path)) as file:
    names = file.readlines()
#/Users/ebuka/Downloads/trees.txt
'''
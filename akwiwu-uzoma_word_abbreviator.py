import re
import json
import numpy as np
from utils.helpers import nameAbbreviator

def abbreviator(path):
    '''The abbreviator() takes in a 
    input-> string: location of the txt file containing names to be abbreviated
    output-> txt file: file containing the each name and the abbreviation in succeeding line'''
    
    #Reading each line of the file /Users/ebuka/Downloads/trees.txt
    with open(str(path)) as file:
        names = file.readlines()


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


    '''Putting it all together: Abbreviating each word in the cleaned data using the name abbreviator function to calculate score and return the least scored'''
    abbreviations_dic= {}                                               
    abbreviatons_only= []
    for name in cleaned_names:
        abb, score= nameAbbreviator(name)
        abbreviations_dic[name]={abb: score}                            # Dictionary of form {name: {abbreviation: score}}
        abbreviatons_only.append(abb)

    name_and_abb_dic = dict(zip(names, abbreviatons_only))               #gets each name from the original file and map it to the computed abbreviation

    names_and_abbs = []
    for name_only, abbreviation_only in name_and_abb_dic.items():        # convert the dictionary of name and abb to list for easy writing to a .txt file
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

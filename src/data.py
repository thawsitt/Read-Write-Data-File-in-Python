# -*- coding: utf-8 -*- 
#!/usr/bin/env python3

'''
File: data.py (v1.0)
--------------------
Read/Write the data file of an anime for merge.py

Author: thawsitt@gmail.com
Date: Dec 23 2016
'''

import os
import datetime
import subprocess
from sys import platform

# Constants (used as keys in data dictionary)
LAST_UPDATED = '00. Last Updated'
NAME = '01. anime_name'
EPI_NUM = '02. episode_num'
QUAL = '03. quality'
FANSUB = '04. fansubs' 
SHORT = '05. short_file_name' 
CRF = '06. crf_value'
OUTPUT_FILE = '07. output_file_name' 
SRC_FILE = '08. source_file_name'
VIDEO_FILE = '09. video_file_name' 
VIDEO_TITLE = '10. video_title'
AUDIO_FILE = '11. audio_file_name'
AUDIO_TITLE = '12. audio_title'
CHAPTER = '13. chapter_file_name'
SUB1 = '14. sub_track_name'
SUB1_D = '15. sub_description'
SUB2 = '16. sub_track_name_2'
SUB2_D = '17. sub_description_2'


def main():
    printIntro()
    file_list = searchDataFile()
    if len(file_list) == 0:
        # No data file.
        if askYesOrNo('> No data file found. Do you want to create a new one?'):
            createDataFile()       
    else:
        # Data File Found.
        if len(file_list) > 1:
            data_file = chooseFile(file_list)
        data = readData(data_file)
        displayData(data)
        if askYesOrNo('> Do you want to edit the data?'):
            editData(data)
            saveDataFile(data)
    print('\n-------- Thanks for using data.py! --------\n')


def printIntro():
    print('===================================================================')
    print('                 Welcome to data.py! (v 1.0)')
    print('A Python program that manages data file for anime encoding process.')
    print('===================================================================')


def searchDataFile():
    """ Return a list containing the names of files that ends with "_datafile.txt" 
    in the current directory. Return an empty string if no data file is found.
    """
    file_list = []
    for filename in os.listdir(os.curdir):
        if filename.endswith('_datafile.txt'):
            file_list.append(filename)
    return file_list


def readData(data_file: str):
    """ Read values from a data file into a dictionary. """
    print('\n> Data file found: ' + data_file)
    print('\n===================================================================')
    print('              Reading Data from: ' + data_file)
    print('===================================================================\n')
    data = dict()
    with open(data_file, 'r') as file:
        # Nice idiom to read lines into a string list without '\n'
        # data_list = file.readlines()
        for line in file.read().splitlines(): 
            values = processLine(line)
            data[values[0]] = values[1]
    return data
    

def processLine(line):
    """ Given a string like this: '01. anime_name---------: Naruto'
    This function returns a list: ['01. anime name', 'Naruto'] 
    which is later used as key-value pairs in our data dictionary.
    """
    sep_index = line.find('-:')
    if sep_index == -1:
            err_msg = 'Index Error. Can\'t find the index of "-:"'
            err_msg += 'in the following input line.\n"' + line + '"\n'
            raise ValueError(err_msg)

    key_end_index = -1 
    for i in range(sep_index - 1, -1, -1):  # if sep_index is 4, loop through 3, 2, 1, 0
        if line[i] != '-':
            key_end_index = i
            break

    key = line[0:key_end_index + 1]
    value = line[sep_index + 3:]    # 'key-: value' sep_index = 3, index of value, 3 + 3
    return [key, value]


def createDataFile():
    printInstructions()
    data = {LAST_UPDATED : 'file_not_written_yet'}
    askInput(data)
    displayData(data)
    if askYesOrNo('> Do you want to edit the data?'):
        editData(data)
    saveDataFile(data)

    
def printInstructions():
    """ Print instructions on screen for createDataFile() """
    print('\nPlease provide the information of the anime to create a data file.')
    print('You will have a chance to edit your input again before the file is saved.')
    input('\nPress Enter to proceed: ')
    print('\n===================================================================')
    print('              Data File Creation in progress . . .')
    print('===================================================================\n')


def askInput(data: dict):
    print('\nAnime Info')
    print('-------------------------------------------------------------------')
    data[NAME] = input('> Name of the anime (e.g. "One_Piece"): ')
    data[EPI_NUM] = str(getIntegerInput('> Episode number (e.g. 12): '))
    data[QUAL] = input('> Quality of the source file (e.g. 1080p): ')
    data[FANSUB] = input('> Fansub group: ')
    print('\nEncoding Settings')
    print('-------------------------------------------------------------------')
    data[SHORT] = input('> Short file name of the anime (e.g. "bw" for Brave Witches): ')
    data[CRF] = input('> Enter CRF value used for encoding video (e.g. 23): ')
    anime_name = data[NAME]
    episode_num = data[EPI_NUM]
    quality = data[QUAL]
    fansubs = data[FANSUB]
    filename = data[SHORT]
    crf_value = data[CRF]
    data[OUTPUT_FILE] = '"(Hi10)_' + anime_name + '_-_' + getEpisodeNumInStr(episode_num) + '_(' + quality + ')_(' + fansubs + ').mkv"'
    data[SRC_FILE] = '"' + filename + episode_num + '.mkv"'
    data[VIDEO_FILE] = '"' + filename + episode_num + '_Encoded.mkv"'
    data[VIDEO_TITLE] = '"0:Hi10 Encode @' + ' CRF ' + str(crf_value) + '"'
    data[AUDIO_FILE] = '"' + filename + episode_num + '-Audio.aac"'
    data[AUDIO_TITLE] = '"0:2.0 AAC-LC @ 0.4"'
    data[CHAPTER] = '"' + filename + episode_num + '_Chapter.xml"'
    data[SUB1] = '"' + filename + episode_num + '_Subtitle_Trimmed_2.ass"'
    data[SUB1_D] = '"0:' + fansubs + ' (.ass)"'
    data[SUB2] = '"' + filename + episode_num + '_Subtitle_Trimmed_1.ass"'
    data[SUB2_D] = '"0:' + fansubs + ' (no honorifics) (.ass)"'


def displayData(data):
    print('===================================================================')
    print('                     Current Data Values                           ')
    print('===================================================================')
    for k,v in sorted(data.items()):
        print(k + '-'*(30-len(k)) + ': ' + v)


def editData(data):
    print('\n===================================================================')
    print('                           Edit Data                                 ')
    print('===================================================================\n')
    print('You can edit the following fields.')
    print('1. Anime Name\n2. Episode Number\n3. Quality\n4. Fansubs\n5. Short File Name\n6. CRF value')

    while True:
        index = askForIndex(data)
        if index == -1:
            break
        changeData(data, index)


def changeData(data: dict, index: int):
    if index == 1:
        old_name = data[NAME]
        new_name = input('> Name of the anime (e.g. "One_Piece"): ')
        data[NAME] = new_name
        data[OUTPUT_FILE] = data[OUTPUT_FILE].replace(old_name, new_name)
    
    elif index == 2:
        # Changing the episode number changes a lot of values. =)
        old_str_short = data[EPI_NUM]           # e.g. '2'
        old_str_long = getEpisodeNumInStr(old_str_short)   # e.g. '02'
        data[EPI_NUM] = str(getIntegerInput('> Episode number (e.g. 12): '))
        new_str_short = data[EPI_NUM]           # e.g. '2'
        new_str_long = getEpisodeNumInStr(new_str_short)   # e.g. '02'

        old_combo = data[SHORT] + old_str_short
        new_combo = data[SHORT] + new_str_short
        data[OUTPUT_FILE] = data[OUTPUT_FILE].replace(old_str_long, new_str_long)
        data[SRC_FILE] = data[SRC_FILE].replace(old_combo, new_combo)
        data[VIDEO_FILE] = data[VIDEO_FILE].replace(old_combo, new_combo)
        data[AUDIO_FILE] = data[AUDIO_FILE].replace(old_combo, new_combo)
        data[CHAPTER] = data[CHAPTER].replace(old_combo, new_combo)
        data[SUB1] = data[SUB1].replace(old_combo, new_combo)
        data[SUB2] = data[SUB2].replace(old_combo, new_combo)

    elif index == 3:
        old_quality = data[QUAL]
        new_quality = input('> Quality of the source file (e.g. 1080p): ')
        data[QUAL] = new_quality
        data[OUTPUT_FILE] = data[OUTPUT_FILE].replace(old_quality, new_quality)
    
    elif index == 4:
        old_fansubs = data[FANSUB]
        new_fansubs = input('> Fansub group: ')
        data[FANSUB] = new_fansubs
        data[OUTPUT_FILE] = data[OUTPUT_FILE].replace(old_fansubs, new_fansubs)
        data[SUB1_D] = data[SUB1_D].replace(old_fansubs, new_fansubs)
        data[SUB2_D] = data[SUB2_D].replace(old_fansubs, new_fansubs)
        
    elif index == 5:
        old_filename = data[SHORT]
        new_filename = input('> Short file name of the anime (e.g. "bw" for Brave Witches): ')
        data[SHORT] = new_filename
        old_combo = old_filename + data[EPI_NUM]
        new_combo = new_filename + data[EPI_NUM]
        data[SRC_FILE] = data[SRC_FILE].replace(old_combo, new_combo)
        data[VIDEO_FILE] = data[VIDEO_FILE].replace(old_combo, new_combo)
        data[AUDIO_FILE] = data[AUDIO_FILE].replace(old_combo, new_combo)
        data[CHAPTER] = data[CHAPTER].replace(old_combo, new_combo)
        data[SUB1] = data[SUB1].replace(old_combo, new_combo)
        data[SUB2] = data[SUB2].replace(old_combo, new_combo)

    elif index == 6:
        old_crf = data[CRF]
        new_crf = str(getIntegerInput('> Enter CRF value used for encoding video (e.g. 23): '))
        data[CRF] = new_crf
        data[VIDEO_TITLE] = data[VIDEO_TITLE].replace(old_crf, new_crf)

    else:
        print('Invalid index.')


def saveDataFile(data):
    """ Saves content of the 'data' dictionary into a text file. """
    data_file = data[NAME] + '_datafile.txt'
    data[LAST_UPDATED] = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
    with open(data_file, 'w') as file:
        for k,v in sorted(data.items()):
            file.write(k + '-' * (30-len(k)) + ': ' + v + '\n')
    print('\nSuccess! Data file saved as: "' + data_file + '"\n')
    input('Press Enter to exit.')


#------------------------------------------------------------
# Helper Functions below.
#------------------------------------------------------------

def askYesOrNo(msg):
    """ Asks a Yes/No question. Returns True/False. """
    while True:
        edit = input('\n' + msg + ' (y/n): ')
        if edit == 'y':
            return True
        elif edit == 'n':
            return False
        else:
            print('Please enter Yes ("y") or No ("n").')


def askForIndex(data) -> int:
    """ Helper Function for editData(). Returns an int (index to edit) """
    while True:
        index = input('\nWhich number do you want to edit? ("Enter" to quit): ')
        if index == '':
            return -1
        if isValidInt(index):
            if int(index) in range(1, 7): # From 1 to 6, inclusive.
                return int(index)
            if int(index) in range(7, 18): # From 7 to 17, inclusive
                print('\n> It is not recommended to edit this value, as it is managed automatically.')
                print('However, there is no stopping you from editing the text file directly.')
                openTextFile(data)
            else:
                print('You can only edit the following fields.')
                print('1. Anime Name\n2. Episode Number\n3. Quality\n4. Fansubs\n5. Short File Name\n6. CRF value')
        else:
            print('Not a valid number.')


def chooseFile(file_list):
    print('\n> More than one data file found! \n')
    for i in range(len(file_list)):
        print(str(i) + '. ' + file_list[i])
    while True:
        index = getIntegerInput('\nWhich file do you want to open?: ')
        if index in range(len(file_list)):
            return file_list[index]
        else:
            print('Invalid input.')


def getEpisodeNumInStr(episode_num: str) -> str:
    """ Change the string representation of one-digit int to two-digit (e.g. "3" -> "03") """
    if int(episode_num) >= 10:
        return episode_num
    else:
        return '0' + episode_num


def getIntegerInput(msg='Please enter an integer: ') -> int:
    """ Ask user for integer input. Only accepts integers. """
    while True:
        user_input = input(msg)
        if isValidInt(user_input):
            return int(user_input)
        else:
            print('You can only enter an integer.')


def isValidInt(string):
    """ '34': True,  'n7': False """
    try:
        int(string)
        return True
    except ValueError:
        return False


# This funciton is confirmed working on MacOS. 
# It might not work on Windows.
def openTextFile(data):
    if askYesOrNo('Do you want to open the data file?'):
        data_file = data[NAME] + '_datafile.txt'
        if platform == 'darwin':
            subprocess.run(['open', '-t', data_file])
        if platform == 'win32':
            command = 'notepad.exe ' + data_file
            subprocess.run(command)

if __name__ == '__main__':
    main()

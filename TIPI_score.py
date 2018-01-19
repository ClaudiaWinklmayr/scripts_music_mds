import numpy as np
import pandas as pd

####################################VARIABLES################################################
#############################################################################################
XLS_FILE = 'GERMAN_MDS_MUSIC.xlsx'  # name of xls- file to read
SHEET_NAME  = 'COMMON SPACE'        # name of relevant tab
ID_HEADER = 'ID'                    # name of column containing participant ID
NEW_FILE = 'TIPI_score.csv'             # name of file that will contain matrix representation

BIG_FIVE = {'Extraversion': [1, 6],
            'Agreeableness': [2, 7], 
            'Conscientiousness': [3, 8],
            'Emotional Stability': [4, 9],
            'Openness to Experiences': [5, 10]}

REVERSE_ITEMS = [2,4,6,8,10]

RESULT_LABELS = ['ID', 'Extraversion', 'Agreeableness', 'Conscientiousness', 'Emotional Stability', 'Openness to Experiences']

#############################################################################################

def reverse(result, scale_length = 7): 
    # assuming a scale from 1 to scale_length
    if result > scale_length or result < 1: 
        print('Invalid score')
        pass
    else: 
        return (scale_length +1) - result 
        
def score_TIPI(TIPI_data, reverse_items = REVERSE_ITEMS, big_five = BIG_FIVE):
    results = {}
    for key in big_five: 
        score = 0
        
        for idx in big_five[key]: 
            if idx in reverse_items:
                score += reverse(TIPI_data[idx-1])
            else: 
                score += TIPI_data[idx-1]
        
        results[key] = score *.5
        
    return results



xls = pd.ExcelFile(XLS_FILE)            # build pandas dataframe from xls sheet
df = xls.parse(SHEET_NAME)

IDs= df[ID_HEADER].values               # read out partcicipant IDs
IDs = [i for i in IDs if isinstance(i, int)]
print(IDs)

newfile = open(NEW_FILE, 'w')           # open the new file 

for rl in RESULT_LABELS:                # write headers 
    newfile.write(rl + ',')
newfile.write('\n')

for i, idx in enumerate(IDs):           # iterate participants
    newfile.write(str(idx) + ',')       # writepartcipant ID 
    tipi = np.zeros(10)                 
    
    for j in range(10):                 # read out tipi answerd
        tipi[j] = df['TIPI_'+str(j+1)].values[i]
    score = score_TIPI(tipi)            # calculate TIPI score
    
    for rl in RESULT_LABELS[1:]:
        newfile.write(str(score[rl]) + ',') # write results
        
    newfile.write('\n')
    
    
newfile.close()                         # close file
    
    
    
        
        

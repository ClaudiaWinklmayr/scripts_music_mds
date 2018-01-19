import pandas as pd
import numpy as np

####################################VARIABLES################################################
#############################################################################################
XLS_FILE = 'GERMAN_MDS_MUSIC.xlsx'  # name of xls- file to read
SHEET_NAME  = 'COMMON SPACE'        # name of relevant tab
ID_HEADER = 'ID'                    # name of column containing participant ID
NEW_FILE = 'matrix.csv'             # name of file that will contain matrix representation
GENRE_NAMES = ['HH_RAP', 'Rock', 'Punk', 'Pop', 'Gospel', 'Country', 'Folk', 'Classical ', 'TECHNO', 'Jazz'] #name of genres

CONSTRAINT_COLUMN = 'RELS'          # name of the constraint column
CONSTRAINT_OPERATOR = '=='          # comparison operator. possible values are: ">", ">=", "==", "<=", "<"
CONSTRAINT_VALUE = [9, 10]          # comparison value. allowed are numbers or lists of numbers 
                                    # (like [2,3,7], in that case operator must be '=='),
#############################################################################################


def check_constraint(df, column, operator, values):
    ''' this function identifies the participants based on the constrains specified above''' 
    col = df[column].values    
    if type(values) ==  int: 
        if operator in ['>', '>=', '==', '<=', '<']: 
            idx = list(np.where(eval('col ' +operator + ' ' + str(values)))[0])
        else:
            print('Operator not allowed. Valid Operators are ">", ">=", "==", "<=", "<" ')
    elif len(values) > 1: 
        if operator == '==': 
            idx = [i for i in range(len(col)) if col[i] in values]
        else: 
            print('Operator not allowed for comparison to list. Use "==" instead.')
    else: 
        pass
        print('Invalid values for comparison')        
    return idx



xls = pd.ExcelFile(XLS_FILE)            # build pandas dataframe from xls sheet
df = xls.parse(SHEET_NAME)

IDs_all = df[ID_HEADER].values          # read out partcicipant IDs
use_idx = check_constraint(df, CONSTRAINT_COLUMN, CONSTRAINT_OPERATOR, CONSTRAINT_VALUE)
IDs = [IDs_all[i] for i in range(len(IDs_all)) if isinstance(IDs_all[i], int) and i in use_idx] 

newfile = open(NEW_FILE, 'w')           # open the new file 

for gn in GENRE_NAMES:                  # write headers with genre names to new file
    newfile.write(gn + '\t')

print(IDs)    
newfile.write('\n')
for i, idx in enumerate(IDs):           # iterate through participants 
    for j in range(len(GENRE_NAMES)):   # iterate through all combinations of music genres
        for k in range(len(GENRE_NAMES)):  
            name = GENRE_NAMES[j] + '/' + GENRE_NAMES[k] + '_CMB' # build name of comparison (genre1/genre2_CMB)
            if k < j+1:                 # if in lower half of tringle, write 0
                newfile.write('0' + ',')
            else:                       # if in upper half of tringle, write value
                newfile.write(str(df[name].values[i]) + ',')
        newfile.write('\n')

newfile.close() # close file.

import pandas as pd
import numpy as np

####################################VARIABLES################################################
#############################################################################################
XLS_FILE = 'GERMAN_MDS_MUSIC.xlsx'  # name of xls- file to read
SHEET_NAME  = 'COMMON SPACE'        # name of relevant tab
ID_HEADER = 'ID'                    # name of column containing participant ID
NEW_FILE = 'matrix_new.csv'             # name of file that will contain matrix representation
GENRE_NAMES = ['HH_RAP', 'Rock', 'Punk', 'Pop', 'Gospel', 'Country', 'Folk', 'Classical ', 'TECHNO', 'Jazz'] #name of genres

#############################################################################################


xls = pd.ExcelFile(XLS_FILE)            # build pandas dataframe from xls sheet
df = xls.parse(SHEET_NAME)

IDs= df[ID_HEADER].values          # read out partcicipant IDs
IDs = [i for i in IDs if isinstance(i, int)]
print(IDs)

newfile = open(NEW_FILE, 'w')           # open the new file 

for gn in GENRE_NAMES:                  # write headers with genre names to new file
    newfile.write(gn + '\t')
    
for i, idx in enumerate(IDs):           # iterate through participants 
    newfile.write('\n' + str(idx) + '\n') # write participant ID to new file 
    
    for j in range(len(GENRE_NAMES)):   # iterate through all combinations of music genres
        for k in range(len(GENRE_NAMES)):  
            name = GENRE_NAMES[j] + '/' + GENRE_NAMES[k] + '_CMB' # build name of comparison (genre1/genre2_CMB)
            if k < j+1:                 # if in lower half of tringle, write 0
                newfile.write('0' + ',')
            else:                       # if in upper half of tringle, write value
                newfile.write(str(df[name].values[i]) + ',')
        newfile.write('\n')

newfile.close() # close file.

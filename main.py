import os
from prep import initialize_folder, correct_texts
from labeling import corenlp_coparsing_files, edct_labeling_files
from discourse import get_sac_indices

### paths
input_path = './data/samples/'              # input files (.txt | .csv)
output_path = './data/sac_indices.csv'      # output file
corrected_path = './data/corrected_files/'  # corrected texts (.txt)
coparse_path = './data/coparsed_files/'     # constitutent parsing results (.json)
edct_path = './data/labeled_trees/'         # labeled tree files (.txt)
model_path = './stanford-corenlp/'          # stanford corenlp model path
filelist_path = './data/filelist.txt'
current_path = os.getcwd()

# initialize the folders
for folder in [corrected_path, coparse_path, edct_path]:
    initialize_folder(folder)

### Step 1. Corrects spelling, grammar, and punctuation errors in each text with LanguageTool. 
correct_texts(input_path, corrected_path, mode='txt')
print('*** Step 1. LT correction done')

### Step 2. Performs constituent parsing using Stanford CoreNLP. 
corenlp_coparsing_files(corrected_path, filelist_path, coparse_path, model_path)
print('*** Step 2. CORENLP constituent parsing done')

### Step 3. Tags connectives in each parsed text with the Explicit Discourse Connectives Tagger.
os.chdir(current_path)
edct_labeling_files(coparse_path, edct_path)
print('*** Step 3. EDCT connectives labeling done')

## Step 4. Calculates the sense-aware connective-based cohesion indices.
get_sac_indices(edct_path, output_path)
print('*** Step 4. Analysis of sense-aware connective-based cohesion indices done')




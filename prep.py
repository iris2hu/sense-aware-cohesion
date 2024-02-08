import pandas as pd
import os, glob, shutil
import language_tool_python
import subprocess

tool = language_tool_python.LanguageTool('en-US')

def initialize_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def get_correct_text(text, tool=tool):
    text = text.replace('\n\n', '\n')
    text = text.replace('  ', ' ')
    correct_text = tool.correct(text)
    return correct_text

# test = 'This is a tests.'
# print(get_correct_text(test))

def correct_texts(inpath, outpath, mode='txt'):

    if mode == 'txt':
        files = glob.glob(inpath + '*.txt')
        for i, file in enumerate(files):
            # if i % 100 == 0:
            #     print(i, 'files processed')
            filename = os.path.split(file)[-1]
            text = open(file, 'r').read()
            corrected_text = get_correct_text(text)
            newfile = os.path.join(outpath, filename)
            with open(newfile, 'w', encoding='utf-8') as f:
                f.write(corrected_text)

    elif mode == 'csv':
        df = pd.read_csv(inpath)
        # sample five files for test
        # inputs = df.head(5).filter(items=['text_id', 'full_text'])
        inputs = df.filter(items=['text_id', 'full_text'])

        for index, row in inputs.iterrows():
            text_id, text = row['text_id'], row['full_text']
            corrected_text = get_correct_text(text)
            newfile = outpath + text_id + '.txt'
            with open(newfile, 'w') as f:
                f.write(corrected_text)



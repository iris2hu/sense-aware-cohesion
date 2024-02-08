import glob, os
import json
import subprocess

# model parameters
nthreads = "10" 
memory = "4"

def corenlp_coparsing_files(inpath, filelist, outpath, modelpath):

    '''
    input: corrected texts
    output: trees in json
    '''

    # generate a filelist for processing
    corrected_files = glob.glob(inpath + '*.txt')
    if len(corrected_files) == 0:
        print('unable to find corrected texts...')
        exit()

    with open(filelist, 'w') as f:
        for cf in corrected_files:
            f.write('.' + cf + '\n')
    print('generated filelist for parsing...')

    # start parsing
    os.chdir(modelpath)    # change working path
    print('current working path:', os.getcwd())
    call_parser = 'java -Xmx' + memory + 'g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLP -threads ' + nthreads + ' -annotators tokenize,ssplit,parse -filelist .' + filelist + ' -outputDirectory .' + outpath  + ' -outputFormat json'
    subprocess.call(call_parser, shell=True)


def edct_labeling_files(inpath, outpath):

    jsonfiles = glob.glob(inpath + '*.json')
    if len(jsonfiles) == 0:
        print('unable to find corenlp parsing files...')
        exit()

    for file in jsonfiles:
        text_id = os.path.split(file)[-1].replace('.txt.json', '')
        tree1file = 'tmp_tree.txt'
        with open(tree1file, 'w', encoding='utf-8') as f:
            parse_result = open(file, 'r').read().strip()
            d = json.loads(parse_result, strict=False)
            sents = d['sentences']
            for s in sents:
                f.write(s['parse'] + '\n')
        tree2file = outpath + text_id + '.txt'
        command = 'perl addDiscourse.pl --parses ' + tree1file + ' --output ' + tree2file
        subprocess.call(command, shell=True)
    os.unlink(tree1file)

    
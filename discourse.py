import glob, re, os
import pandas as pd

def extract_edct_features(infile):
    content = open(infile, 'r').read()
    tokens = re.findall('\([A-Z$]+ [\w\d#]+\)', content)
    types = set(tokens)
    co_units = re.findall(' (\w+#\d+#\w+)\)', content)
    cod, indices, tmp = {}, {}, []

    for i, co in enumerate(co_units):
        cl = co.split('#')
        if len(cl) != 3:
            print(cl, 'error')
            continue
        word, cid, func = cl[0].lower(), cl[1], cl[2]
        if i == 0:
            tmp = [word, cid, func]
        elif tmp:
            if cid == tmp[1] and func == tmp[2]:
                tmp[0] += ' ' + word
            else:
                if tmp[2] not in cod:
                    cod[tmp[2]] = []
                cod[tmp[2]].append(tmp[0])
                tmp = [word, cid, func]

    if tmp:
        if tmp[2] not in cod:
            cod[tmp[2]] = []
        cod[tmp[2]].append(tmp[0])

    connectives, discourse_connectives = [], []  # 5 & 4 classes
    for k,v in cod.items():
        for word in v:
            token_func = word + '_' + k
            if k != '0':
                discourse_connectives.append(token_func)
            connectives.append(token_func)

    # indices['DC_token_num'] = len(discourse_connectives)
    indices['DC_type_num'] = len(set(discourse_connectives))
    indices['DC_token_density'] = len(discourse_connectives) / len(tokens)
    indices['DC_type_density'] = len(set(discourse_connectives)) / len(types)
    if discourse_connectives:
        indices['DC_ttr'] = len(set(discourse_connectives)) / len(discourse_connectives)
    else:
        indices['DC_ttr'] = 0
        
    for k,v in cod.items():
        # 5 classes (could be adjusted to 4)
        if k == '0':
            k = 'NoneDC'
        # indices[k + '_token_num'] = len(v)
        indices[k + '_type_num'] = len(set(v))
        indices[k + '_ttr'] = len(set(v)) / len(v)
        indices[k + '_token_ratio'] = len(v) / len(connectives)
        indices[k + '_token_density'] = len(v) / len(tokens)
        indices[k + '_type_ratio'] = len(set(v)) / len(set(connectives))
        indices[k + '_type_density'] = len(set(v)) / len(types)
    return indices

def get_sac_indices(inpath, outpath):
    '''
    inpath: edct tree files
    outpath: csv file for sense-aware connective-based indices
    '''
    sac_indices = {}
    treefiles = glob.glob(inpath + '*.txt')
    for file in treefiles:
        text_id = os.path.split(file)[-1].replace('.txt', '')
        sac_indices[text_id] = extract_edct_features(file)
    
    df_dct = pd.DataFrame.from_dict(sac_indices, orient='index')
    df_dct = df_dct.fillna(0)
    df_dct.to_csv(outpath, index_label='text_id')

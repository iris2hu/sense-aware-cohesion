# Sense-aware connective-based indices of cohesion

This project releases the automatic analysis tool and the data in the article:

<em>Xiaofei Lu and Renfen Hu (2024). Sense-aware connective-based indices of cohesion and their relationship to cohesion ratings of English language learners’ written production. Studies in Second Language Acquisition. in press. </em>

## Prerequisites

**1. Install Python, Java, Perl and required packages**

*   **`Python 3.7+`**
*   **`Java 8+`**
*   **`Perl 5.10.1+`**
*   **`Pandas 0.22.0+`** (Python)
*   **`language-tool-python 2.5.3+`** (Python)

**2. Stanford CoreNLP setup**

In this study, we used **`stanford-corenlp-3.6.0`** for constituent parsing. You may find newer versions [`here`](https://stanfordnlp.github.io/CoreNLP/download.html).

Download the zip file (approx. 400-500 MB) which includes (1) CoreNLP code jar, (2) CoreNLP models jar, (3) required libraries, and (4) documentation/source code.

Please unzip and place the files in the directory **`stanford-corenlp`** before running the codes.

## Automatic analysis 

Run the analysis using the following command:

```python
python main.py
```

The default input format is text files, but a .csv file is also supported. Example files can be found at **`./data/samples/*.txt`** or **`./data/samples.csv`**. 

The analysis results will be output to **`./data/sac_indices.csv`**.

The command executes a four-step process:

- Step 1. Corrects spelling, grammar, and punctuation errors in each text with LanguageTool.  
- Step 2. Performs constituent parsing using Stanford CoreNLP.  
- Step 3. Tags connectives in each parsed text with the Explicit Discourse Connectives Tagger.  
- Step 4. Calculates the sense-aware connective-based cohesion indices.  

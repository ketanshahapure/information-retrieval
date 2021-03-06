"""
Divyesh Chitroda, d151@umbc.edu
CampusId: GW92650

CMSC 676 – Information Retrieval
Homework 2
"""

import html2text as h2t
import os, codecs, sys, time, math

# check for command line arguments, must have input and output directory path
if len(sys.argv) != 3:
    print("2 arguments required: input and output directory path.")
    exit()

# get input directory
inpath = sys.argv[1]
# get output directory
outpath = sys.argv[2]

if not os.path.exists(outpath):
    os.mkdir(outpath)

# list of escape characters, unwanted characters
escapeChars = ["\n","\t","\r",",",".","-","_","'",'"',"`","[","]","(",")","?","|","*",";","!","{","}",">","$","=","%","#","+","<","&","\\","0","1","2","3","4","5","6","7","8","9"]
doc_freq = {}
freq_dist = {}
tf = {}

# get programs start time
prev = time.time()

# file counter
idx=0

# read stopwords.txt file to get list of stopwords
stfile = open("stopwords.txt", "r")
stopwordslist = stfile.read()
stopwordslist = stopwordslist.replace("'", "")
stopwordslist = stopwordslist.split("\n")

# get all files in the input folder
files  = os.listdir(inpath)
print("Preprocessing:")
# iterate through all the files in input directory
for file in files:
    # check for html files only
    if file.endswith(".html"):
        # open the file with ascii encoding and ignore encoding errors
        fr = open(os.path.join(inpath, file), "r",  encoding="ascii", errors="ignore")
        # read html content of the file
        html = fr.read()
        # extract text from html using html parser
        text_maker = h2t.HTML2Text()
        text_maker.ignore_links = True
        text_maker.ignore_images = True
        text_maker.images_to_alt = True
        text_maker.protect_links = True
        text_maker.ignore_anchors = True
        text_maker.inline_links = False
        text = text_maker.handle(html)
        # replace all unwanted characters from escape sequence with whitespace character
        for esc in escapeChars:
            text = text.replace(esc, " ")
        
        # split text string into tokens using whitespace
        tokens = text.split(' ')

        # contains token frequency for each file
        freq_dist[file] = {}
        # contains term frequency weight of tokens for each file
        tf[file] = {}

        # iterate all tokens and create hashmap with frequency and document count
        for i in tokens:
            # lower case all characters
            i = i.lower()
            # ignore empty tokens and stopwords
            if len(i) > 1 and i not in stopwordslist:
                # create frequency distrbution hashmap
                if i in freq_dist[file]:
                    freq_dist[file][i] += 1
                else:
                    freq_dist[file][i] = 1

                # create document frequency hashmap
                if i in doc_freq:
                    if file not in doc_freq[i]:
                        doc_freq[i].append(file)
                else:
                    doc_freq[i] = [file]

        for i in freq_dist[file]:
            # calculate term frequency weights, tf = f(d,w)/|D|
            wordtf = freq_dist[file][i]/len(tokens)
            tf[file][i] = wordtf

        # find elapsed CPU time of files proccessed
        if idx in [10, 20, 40, 80, 100, 200, 300, 400, 500]:
            print(time.time() - prev)
        
        # increment file counter
        idx += 1

# total number of documents
collection = idx

idx = 0
# get programs start time
prev = time.time()

print("Calculate weights:")
# calculate and store tf-idf weights of tokens
for file in freq_dist:
    # conatins tf-idf for each token
    tfidf = {}
    tokens = freq_dist[file]
    for tok in tokens:
        # calculate idf = |c|/df(w)
        idf = math.log(collection/len(doc_freq[tok]))
        # calculate tfidf = tf(d,w) * idf(w)
        tfidf[tok] = tf[file][tok] * idf

    if idx in [10, 20, 40, 80, 100, 200, 300, 400, 500]:
        print(time.time() - prev)
    
    idx += 1

    # write tfidf weights to filename.wts as tsv
    fw = codecs.open(os.path.join(outpath, file) +".wts", 'w', encoding='ascii',errors="ignore")
    # sort tokens in descending order of tfidf weights
    sortedvals = sorted(tfidf.items(), key=lambda kv: kv[1], reverse=True)
    for tok, tfidf in sortedvals:
        # write weights to wts file
        fw.write(tok + "\t" + str(tfidf) + "\n")
    # close file
    fw.close()
import sys, glob, re, os, shutil, math
from os.path import join, getsize
sys.path.append("C:\\My Documents\\Python\\Workspace\\scripts")
import mgr, csv, textwrap

# Folders and Files
toponymicListRaw = "./WorkingLists/MuCjambuldan_WorkingList.txt"
sourceFolder     = "./SourcesToAnalyze/"
tempFolder       = "./tempFolder/"

# Variables
topHolder        = "ــاسمــالمكانــ"
topPrefix        = "و?ب?" # topRE = r"\b"

# prepare toponymic list: function processes file with toponyms and returns
# several a list of toponyms, converted into RE for further manipulations
# REparameters
# ".*"       --- for all toponyms
# "MANUAL"   --- manually tagged
# "NOTFOUND" --- not recognized by Buckwalter as common words
# "COMPOUND" --- compound toponyms
def prepToponyms(fileName, REparameter):
    topList = open(fileName, "r", encoding="utf-8").read()
    # make spaces optional with RE
    topList = re.sub(" ", " ?", topList)
    # denormalize the entire list
    
    toponymRElist = re.findall(r"(.*?)\t%s" % REparameter,topList)
    toponymRElist = mgr.reFromList(toponymRElist)
    
    return(toponymRElist)

# generating topHolders
def generateTopHolders(sourceFile):
    print("\ngenerating topHolders...")
    sourceFileBase = re.sub("\.[a-z]+$", "", sourceFile)
    
    source = open(sourceFolder+sourceFile, 'r', encoding="utf-8").read()
    
    source = re.sub("\n  ", " ", source)
    source = re.sub("( )+", " ", source)

    topReList = prepToponyms(toponymicListRaw, "MANVER2")
    print("Processing MANVER2 (%d)..." % len(topReList))
    for i in topReList:
        source = re.sub(r"\b(%s)(%s)\b" % (topPrefix,i), r"\1%s [\2]" % topHolder, source)

    topReList = prepToponyms(toponymicListRaw, "NOTFOUND")
    print("Processing NOTFOUND (%d)..." % len(topReList))
    for i in topReList:
        source = re.sub(r"\b(%s)(%s)\b" % (topPrefix,i), r"\1%s [\2]" % topHolder, source)

    topReList = prepToponyms(toponymicListRaw, "COMPOUND")
    print("Processing COMPOUND (%d)..." % len(topReList))
    for i in topReList:
        source = re.sub(r"\b(%s)(%s)\b" % (topPrefix,i), r"\1%s [\2]" % topHolder, source)

    source = source.split("\n")
    countPar = 0
    
    outFile  = tempFolder+sourceFileBase+"_TopHolders.txt"
    with open(outFile, 'w', encoding='utf-8') as w:
        for par in source:
            par = mgr.wrapPar(par)
            countPar = mgr.counter(countPar, 10000)
            w.write(par+"\n")

#generateTopHolders("Tarikhislam.source")

##def genFreqList(sourceFile):
##    sourceFileBase = re.sub("\.[a-z]+$", "", sourceFile)
##    fileForAnalysis = tempFolder+sourceFileBase+"_TopHolders.txt"
##    fileForAnalysis = open(fileForAnalysis, 'r', encoding="utf-8").read()
##    results = re.findall(r"\w+%s|%s" % (topHolder, topHolder), fileForAnalysis)
##    results = "\n".join(results)
##    #results = re.sub(topHolder, "", results)
##    results = mgr.freqList(results, 1)
##    freqFile = tempFolder+sourceFileBase+"_TopHolders_Freq.txt"
##    with open(freqFile, 'w', encoding='utf-8') as w:
##        w.write(results)       
    
#genFreqList("Tarikhislam.source")

def genTopNgrams(sourceFile):
    print("%s:\ngenerating a freqList of toponymic nGrams..." % sourceFile)
    sourceFileBase = re.sub("\.[a-z]+$", "", sourceFile)
    fileForAnalysis = tempFolder+sourceFileBase+"_TopHolders.txt"
    fileForAnalysis = open(fileForAnalysis, 'r', encoding="utf-8").read()
    fileForAnalysis = re.sub("\[.*?\]", "", fileForAnalysis)

    fileForAnalysis = mgr.eNassClean(fileForAnalysis)
    fileForAnalysisFile = tempFolder+sourceFileBase+"_Raw_DoNotOpen.txt"
    with open(fileForAnalysisFile, 'w', encoding='utf-8') as w:
        w.write(fileForAnalysis)

    # one of the transformations:
    # - proper names should be replaced with placeHolders

    # collecting toponymic ngrams
    bigrams = re.findall(r"\w+ \w+%s|\w+ %s" % (topHolder, topHolder), fileForAnalysis)
    bigrams = "\n".join(bigrams)
    trigrams = re.findall(r"\w+ \w+ \w+%s|\w+ \w+ %s" % (topHolder, topHolder), fileForAnalysis)
    trigrams = "\n".join(trigrams)
    results = bigrams+"\n"+trigrams    
    results = mgr.freqList(results, 2)
    
    freqFile = tempFolder+sourceFileBase+"_TopNgrams_Frequencies.txt"
    with open(freqFile, 'w', encoding='utf-8') as w:
        w.write(results)

def genTopNgramsWeight(sourceFile):
    print("%s:\nanalyzing ngram frequencies and generating their relative weights..." % sourceFile)
    sourceFileBase = re.sub("\.[a-z]+$", "", sourceFile)
    fileForAnalysisFile = tempFolder+sourceFileBase+"_Raw_DoNotOpen.txt"
    fileForAnalysis = open(fileForAnalysisFile, 'r', encoding="utf-8").read()

    ngramFile = tempFolder+sourceFileBase+"_TopNgrams_Frequencies.txt"
    ngramFile = open(ngramFile, 'r', encoding="utf-8").read()

    newResults = []
    #ngramFile = re.sub(topHolder, "", ngramFile) 
    ngramFile = ngramFile.split("\n")
    countLines = 0
    for line in ngramFile:
        line = line.split("\t")
        topNgramStat = int(line[0])
        if topNgramStat > 10:
            topNgram     = line[1]
            topNgramSrch = re.sub(topHolder, "", topNgram)
            NgramTotal   = len(re.findall(r"\b%s" % mgr.deNormalize(topNgramSrch), fileForAnalysis))
            if NgramTotal == 0:
                print("Warning: NgramTotal is 0 for\n%s" % line)
                NgramTotal = topNgramStat
            NgramProb    = "{0:.5f}".format(topNgramStat/NgramTotal)
            newLine = "%s\t%08d\t%08d\t%s" % (str(NgramProb), int(NgramTotal), int(topNgramStat), topNgram)
            newResults.append(newLine)
            countLines = mgr.counter(countLines, 100)
        
    newResults = sorted(newResults, reverse=True)
    newResults = "\n".join(newResults)
    
    freqFile = tempFolder+sourceFileBase+"_TopNgrams_Weights.txt"
    with open(freqFile, 'w', encoding='utf-8') as w:
        w.write(newResults)
        
#genTopNgramsWeight("Tarikhislam.source")

def applyToAllSources(sourceFolder):
    for file in os.listdir(sourceFolder):
        print("=============================\n\n"+file)
        #generateTopHolders(file)
        #genTopNgrams(file)
        genTopNgramsWeight(file)

applyToAllSources(sourceFolder)

# TEST
#genTopNgramsWeight("KitabAnsab.source")

print("Done!")












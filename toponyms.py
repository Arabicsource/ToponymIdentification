import sys, glob, re, os, shutil, math, operator, collections
from os.path import join, getsize
sys.path.append("C:\\My Documents\\Python\\Workspace\\scripts")
import mgr, csv, textwrap

# Folders and Files
toponymicListRaw = "./WorkingLists/MuCjambuldan_WorkingList.txt"
sourceFolder     = "./SourcesToAnalyze/"
tempFolder       = "./tempFolder/"

# Variables
topHolder        = "ــاسمــالمكانــ"
nameHolder       = "ـــالإسمــالمرقبـــ"
topPrefix        = "و?ب?" # topRE = r"\b"

def modifyResult(matchobj):
    return((matchobj.group()).replace(" ", ".."))

def arabicNameRE():
    nisbaProper = "\w+ي"
    faCCala = "\w\wا\w"
    faaCil = "\wا\w\w"
    mimParticiple = "م\w+"
    faCiil = "\w\wي\w"
    afCal  = "أ\w\w\w"
    #---------------------------------------------
    nisba = "(ال(%s|%s|%s|%s|%s|%s)ة? )" % (nisbaProper,faCCala,faaCil,mimParticiple,faCiil,afCal)
    #---------------------------------------------
    abdName = "%s ?\w{2,}" % "عبي?د"
    allahName = "\w{2,} ?%s" % "الله" 
    dinName = "\w{2,} ?%s" % "الدين"
    dhuName = "%s \w{2,}" % "ذو|ذي|ذات?"
    #---------------------------------------------
    ismMuraqqab = "((%s|%s|%s|%s) )" % (abdName,dinName,allahName,dhuName)
    ismMufrad  = "\w+ "
    bn   = "بنت?"
    ibn  = "ابنة?"
    ben  = "ا?بن[تة]?"
    #---------------------------------------------
    # compound elements
    #---------------------------------------------
    kunya = "(%s ?(%s|%s|\w+) )" % ("(أبو|أبي|أبا|أم)",ismMuraqqab,nisba)
    nasab = "(%s (%s|%s|%s|\w+) )" % (ben,ismMuraqqab,nisba,kunya)
    
    #---------------------------------------------
    # Name patterns
    #---------------------------------------------
    nameList = []
    # 1. ismMuraqqab+ nasab+ (nisba+)?
    name1 = mgr.deNormalize("(%s|%s)+(%s)?(%s)+((%s)+)?" % (ismMuraqqab,kunya,ismMufrad,nasab,nisba))
    # 2. ismMufrad nasab+ (nisba+)?
    name2 = mgr.deNormalize("(%s)(%s)+((%s)+)?" % (ismMufrad,nasab,nisba))
    # 3. ibn ismMuraqqab+ (nisba+)?
    name3 = mgr.deNormalize("(%s )(%s)+((%s)+)?" % (ibn,ismMuraqqab,nisba))
    # 4. muraqqabat mukhtalifa
    nameA = mgr.deNormalize("(%s(%s)?%s)" % (ismMuraqqab,kunya,nisba))
    nameB = mgr.deNormalize("(%s(%s)?%s)" % (kunya,ismMuraqqab,nisba))    
    nameC = mgr.deNormalize("(%s%s)" % (dhuName,nisba))
    name4 = nameA+"|"+nameB+"|"+nameC

    name5 = mgr.deNormalize("(%s \w+ )" % (ibn))
    #input(name5)


    ##############################################################
    prophet = "رسول الله|النبي"
    slCm    = "صلى الله عليه وسلم"
    Cm      = ""
    rHm     = ""
    rDh     = ""
    ##############################################################
    prophet = mgr.deNormalize("(%s )%s" % (prophet,slCm))

    nameList.append(prophet)
    nameList.append(name1)
    nameList.append(name2)
    nameList.append(name3)
    nameList.append(name4)
    nameList.append(name5)

    #input(nameList)
    return(nameList)

#arabicNameRE()

# prepare toponymic list: function processes file with toponyms and returns
# several a list of toponyms, converted into RE for further manipulations
def prepToponyms(fileName, REparameter):
    topList = open(fileName, "r", encoding="utf-8").read()
    # make spaces optional with RE
    topList = re.sub(" ", " ?", topList)
    # denormalize the entire list
    
    toponymRElist = re.findall(r"(.*?)\t%s" % REparameter,topList)
    toponymRElist = mgr.reFromList(toponymRElist)
    
    return(toponymRElist)

def generateRawFiles(sourceFile):
    print("\n%s:\ngenerating RAW files..." % sourceFile)
    sourceFileBase = re.sub("\.[a-z]+$", "", sourceFile)
    
    source = open(sourceFolder+sourceFile, 'r', encoding="utf-8").read()
    source = mgr.eNassClean(source)

    rawFileName = tempFolder+sourceFileBase+"_Raw.txt"
    with open(rawFileName, 'w', encoding='utf-8') as w:
        w.write(source)

# generating semantic placeHolders (compound names and toponymic suspects)
def generatePlaceHolders(sourceFile):
    print("\n%s:\ngenerating semantic placeholders..." % sourceFile)
    sourceFileBase = re.sub("\.[a-z]+$", "", sourceFile)
    
    source = open(sourceFolder+sourceFile, 'r', encoding="utf-8").read()
    source = mgr.eNassClean(source)

    rawFileName = tempFolder+sourceFileBase+"_Raw.txt"
    with open(rawFileName, 'w', encoding='utf-8') as w:
        w.write(source)

    nameResultRE = re.compile(r"\{\{.*?\}\}")
    topoResultRE = re.compile(r"\[.*?\]")
    
##    print("Generating nameHolders...")
##    nameReList = arabicNameRE()
##    for i in nameReList:
##          source = re.sub(r"\b(%s)" % (i), r"%s {{\1}} " % nameHolder, source)
##          source = re.sub(nameResultRE, modifyResult, source)
##          source = re.sub("( )+", " ", source)

##    rawFileName = tempFolder+sourceFileBase+"_NameHoldersRaw.txt"
##    with open(rawFileName, 'w', encoding='utf-8') as w:
##        w.write(source)

    print("Generating placeHolders...")

    topReList = prepToponyms(toponymicListRaw, "MANVER3BW")
    print("Processing MANVER3BW (%d)..." % len(topReList))
    for i in topReList:
        source = re.sub(r"\b(%s)(%s)\b(?!(\]|\.))" % (topPrefix,i), r"\1%s [\2]" % topHolder, source)

    topReList = prepToponyms(toponymicListRaw, "COMPOUND")
    print("Processing COMPOUND (%d)..." % len(topReList))
    for i in topReList:
        source = re.sub(r"\b(%s)(%s)\b(?!(\]|\.))" % (topPrefix,i), r"\1%s [\2]" % topHolder, source)

    topReList = prepToponyms(toponymicListRaw, "NEWMORPH")
    print("Processing NEWMORPH (%d)..." % len(topReList))
    for i in topReList:
        source = re.sub(r"\b(%s)(%s)\b(?!(\]|\.))" % (topPrefix,i), r"\1%s [\2]" % topHolder, source)

    source = mgr.wrapPar(source)
   
    outFile  = tempFolder+sourceFileBase+"_PlaceHolders.txt"
    with open(outFile, 'w', encoding='utf-8') as w:
        w.write(source)

##def genFreqList(sourceFile):
##    sourceFileBase = re.sub("\.[a-z]+$", "", sourceFile)
##    fileForAnalysis = tempFolder+sourceFileBase+"_PlaceHolders.txt"
##    fileForAnalysis = open(fileForAnalysis, 'r', encoding="utf-8").read()
##    results = re.findall(r"\w+%s|%s" % (topHolder, topHolder), fileForAnalysis)
##    results = "\n".join(results)
##    #results = re.sub(topHolder, "", results)
##    results = mgr.freqList(results, 1)
##    freqFile = tempFolder+sourceFileBase+"_TopHolders_Freq.txt"
##    with open(freqFile, 'w', encoding='utf-8') as w:
##        w.write(results)       

def genTopNgrams(sourceFile):
    sourceFileBase = re.sub("\.[a-z]+$", "", sourceFile)
    print("\n%s:\ngenerating a freqList of toponymic nGrams..." % sourceFile)

    topHolders = tempFolder+sourceFileBase+"_PlaceHolders.txt"
    topHolders = open(topHolders, 'r', encoding="utf-8").read()
    topHolders = re.sub("\n", "", topHolders)
    topHolders = re.sub("( )+", " ", topHolders)
    topHolders = re.sub("\[.*?\]|\{\{.*?\}\}", "", topHolders)
    topHolders = re.sub("( )+", " ", topHolders)

    topHoldersRaw = topHolders

    # collecting toponymic ngrams
    #bigrams = re.findall(r"\w+ %s%s" % (topPrefix,topHolder), topHoldersRaw)
    bigrams = re.findall(r"\w+ \w+%s|\w+ %s" % (topHolder,topHolder), topHoldersRaw)
    bigrams = "\n".join(bigrams)
    trigrams = re.findall(r"\w+ \w+ %s%s" % (topPrefix,topHolder), topHoldersRaw)
    trigrams = "\n".join(trigrams)
    results = bigrams+"\n"+trigrams
    
    results = mgr.freqList(results, 2)
    
    freqFile = tempFolder+sourceFileBase+"_TopNgrams_Frequencies.txt"
    with open(freqFile, 'w', encoding='utf-8') as w:
        w.write(results)

def genTopNgramsWeight(sourceFile):
    print("%s:\nanalyzing ngram frequencies and generating their relative weights..." % sourceFile)
    sourceFileBase = re.sub("\.[a-z]+$", "", sourceFile)

    topHolders = tempFolder+sourceFileBase+"_PlaceHolders.txt"
    topHolders = open(topHolders, 'r', encoding="utf-8").read()
    topHolders = re.sub("\n", "", topHolders)
    topHolders = re.sub("( )+", " ", topHolders)
    topHolders = re.sub("\[.*?\]|\{\{.*?\}\}", "", topHolders)
    topHolders = re.sub("( )+", " ", topHolders)

    topHoldersRaw = topHolders
    sourceLen  = len(topHolders.split(" "))
    
    ngramFile = sourceFileBase+"_TopNgrams_Frequencies.txt"
    print("\n%s:\ngenerating a freqList of toponymic nGrams..." % ngramFile)
    ngramFile = open(tempFolder+ngramFile, 'r', encoding="utf-8").read()

    newResults = []
    ngramFile = ngramFile.split("\n")
    countLines = 0
    for line in ngramFile:
        line = line.split("\t")
        topNgramStat = int(line[0])
        if topNgramStat > 0:
            topNgram     = line[1]
            topNgramSrch = re.sub("%s$" % topHolder, "", topNgram)
            topNgramSrch = mgr.deNormalize(topNgramSrch)
            NgramTotal   = re.findall(r"%s" % topNgramSrch, topHoldersRaw)
            #ngramResults = dict((i,NgramTotal.count(i)) for i in NgramTotal)
            #ngramResultsLen = len(set(NgramTotal))
            #print(topNgram+": variety %d" % ngramResultsLen)
            NgramTotalLen = len(NgramTotal)
            if NgramTotalLen == 0:
                print("Warning: NgramTotal is 0 for\n%s" % line)
                #input(topNgramSrch)
                NgramProb = "{0:.5f}".format(9.0)
            else:
                NgramProb    = "{0:.5f}".format(topNgramStat/NgramTotalLen)
            NgramProbFloat = float(NgramProb)
            testIndex = int(NgramProbFloat*NgramProbFloat*NgramTotalLen*100000)
            newLine = "%10d\t%s\tNgramTotal:%s\ttopNgram:%s\t%s" % (testIndex, str(NgramProb), '{:>8}'.format(str(NgramTotalLen)),'{:>8}'.format(str(topNgramStat)),topNgram)
            #input(newLine)
            newResults.append(newLine)
            countLines = mgr.counter(countLines, 100)
            #input(ngramResults)
        
    newResults = sorted(newResults, reverse=True)
    newResults = "\n".join(newResults)
    
    freqFile = tempFolder+sourceFileBase+"_TopNgrams_Weights.txt"
    with open(freqFile, 'w', encoding='utf-8') as w:
        w.write(newResults)
        

def applyToAllSources(sourceFolder):
    fileList = os.listdir(sourceFolder)
    fileList = "\n".join(fileList)
    fileList = re.sub(r"(^|\n)", r"\1%s" % sourceFolder, fileList)
    fileList = fileList.split("\n")
    sortedList = sorted(fileList, key=os.path.getsize) # arranges files by size ascending (desc > reverse=True)
    for file in sortedList:
        file = re.sub(sourceFolder, "", file)
        print("\n=============================\n"+file+"\n=============================")
        generateRawFiles(file)
        #generatePlaceHolders(file)
        #genTopNgrams(file)
        #genTopNgramsWeight(file)


applyToAllSources(sourceFolder)
    
print("Done!")












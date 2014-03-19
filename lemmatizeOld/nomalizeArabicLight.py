import glob, re, os, shutil, sys, collections
sys.path.append("C:\\My Documents\\Python\\Workspace\\scripts")
from os.path import join, getsize
import mgr

folder     = "C:\\My Documents\\Python\\Workspace\\Perl scripts\\"
sourceFile = "MB_Resid.txt"
targetFile = "MB_Resid_Normalized.txt"
toponymList = 'C:\\My Documents\\Python\\Workspace\\research_files\\MB_AllToponyms.txt'

sourceText = open(folder+sourceFile, 'r', encoding='utf-8').read()
sourceText = mgr.normalizeArabicLight(sourceText)

targetText = open(folder+targetFile, 'w', encoding = 'utf-8')
targetText.write(sourceText)
targetText.close()

print('Done!')

#!/usr/bin/env python
#-*- coding:utf-8 -*-
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import re,io
from urllib import request
import time
import sys,os
#problem to be solved 
#identify word separated by "-\n"
#the output of words should have the same order as in paper
#add pronunciation to the word

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    #print(type(content))
    return content.lower()
def saveTxt(txt):
    with open("/Users/apple/Desktop/fulltxt.txt", "w") as f:
        f.write(txt)

# txt is string
def words_filter(txt, thredshold = 3):
    txt = [i if ord(i)==32 or 96<ord(i)<123 else " " for i in txt]
    #txt = [i for i in txt if ord(i)==32 or 64<ord(i)<91 or 96<ord(i)<123 ]
    txt = "".join(txt)
    order = txt.split()
    txt = list(set(order))
    txt.sort(key = order.index)
    txt = [i if len(i)>thredshold else "" for i in txt]
    txt = list(set(txt))
    return txt

#copy from https://blog.csdn.net/gaopu12345/article/details/46315479
def word_translate(word):
    #print(word)
    searchUrl = "http://dict.youdao.com/search?q=" + word + "&keyfrom=dict.index"
    response = str(request.urlopen(searchUrl).read(),"utf-8")
    searchResult = re.search(r"(?s)<span class=\"keyword\">.*?<div class=\"trans-container\">.*?<ul>.*?</div>",str(response))
    #searchResult = re.search(r"(?s)<div class=\"trans-container\">.*?<ul>.*?</div>",str(response))
    if searchResult:
        means = re.findall(r"(?m)<li>(.*?)</li>",searchResult.group())
        pronouce = re.findall(r"(?m)<span class=\"phonetic\">(.*?)</span>",searchResult.group())
        pronouce = [" ".join(pronouce)]
        #for i in range(len(means)):
            #means[i] = means[i].decode(encoding="utf-8")
        if len(means) == 1 and re.match(r".*(人名|姓氏).*",means[0]):
            print(len(means),means[0],re.match(r"人名",means[0]))
            print(word+"  is a name")
            means = False
            pronouce = False
    else:
        means = False
        pronouce = False
    #print(type(means))
    return pronouce+means

if __name__ == "__main__":
    #print(sys.argv[0])
    #print (os.path.abspath('.'))
    #print (os.path.abspath('..'))
    #txt = readPDF(open('/Users/apple/Desktop/A neural algorithm for a fundamental computing problem.pdf', 'rb'))
    path = input("pdf file:")
    path = re.sub(r"\\","",path)
    print(path)
    txt = readPDF(open(path,"rb"))
    txt = words_filter(txt)
    #saveTxt(txt)
    print("txt:",len(txt))
    #f_words = open("/Users/apple/Desktop/word.txt", "w")
    f_words_translate = open(path+"word_translate.txt", "a")
    #why need full path 
    database_mywords = open("/Users/apple/Desktop/Python/word_filter/myword_database.txt", "r+")
    mywords = database_mywords.readlines()
    print("database: "+str(len(mywords)))
    #print(mywords)

    #for i in txt:
        #f_words.writelines(i+"\n")
    count = 0
    for i in txt:
        #time.sleep(0.2)
        if i+"\n" not in mywords:
            translate = word_translate(i)
            if translate:
                print("translate and add to database: "+i)
                f_words_translate.writelines(i+"\n"+"\n".join(translate)+"\n\n")
                count+=1
                database_mywords.writelines(i+"\n")
            else:
                pass
        else:
            pass
    #f_words.close()
    print("new: "+str(count))
    f_words_translate.close()
    database_mywords.close()




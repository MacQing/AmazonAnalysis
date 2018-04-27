#!/usr/bin/python
# -*- coding: latin-1 -*-

import requests, re, sys
from bs4 import BeautifulSoup

# Amazon????????????
pattern = r"of.*(\d+?)results for"

# ???????url
def generateAmzaonUrl(keyword='huawei'):
    urlAmazon = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' + keyword
    return urlAmazon

# ????url?html????
def getHtmlContent(url='http://wwww.baidu.com'):
    html=requests.get(url)
    return html.text

# ?????HTML?????
def getResultNum(htmlContent):
    # of over 1,000 results for
    results = re.findall(pattern, htmlContent)
    return results[0] if len(results) > 0 else None

# ???????????
def loadKeywordsFromTxt(filePath):
    with open(filePath) as f:
        keywords = [word.strip() for word in f.readlines()]
        return keywords
    return []

def getResultNumByKewords(keywords, outFilePath):
    keywordNumList = []
    for kw in keywords:
        url = generateAmzaonUrl(kw)
        htmlContent = getHtmlContent(url)
        num = getResultNum(htmlContent)

        keywordNumList.append((kw, num))

    # ????????
    with open(outFilePath, 'wb+') as f:
        f.truncate()
        content = '\n'.join([kn[0] + '\t' + kn[1] for kn in keywordNumList])
        f.write(content)

def getResultNumByFile(inFilePath, outFilePath):
    keywords = loadKeywordsFromTxt(inFilePath)
    print('load keywords successfully: file=%s, len(keywords)=%s' % (inFilePath, len(keywords)))
    getResultNumByKewords(keywords, outFilePath)
    print('write results to file successfully: file=%s' % (outFilePath))

if __name__ == "__main__":
    # inFilePath, outFilePath = sys.argv[0], sys.argv[1]
    inFilePath = "data/keywords.txt"
    outFilePath = "data/keywordsNum.txt"
    getResultNumByFile(inFilePath, outFilePath)

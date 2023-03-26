#-*- encoding:utf-8 -*-
from __future__ import print_function
import datetime
 
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import json
import os
import sys
import django
import io
import requests
import pdfminer
import hashlib                                   #导入hashlib模块

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

sys.path.append("../")
os.chdir("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ESG_site.settings")
django.setup()

from ESG import models
from django.core.files import File

with open("datas/esg_data.json",'r', encoding='utf-8') as f:
    json_data = json.load(f)

def download_pdf(save_path,pdf_name,pdf_url) -> None:
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}
    response = requests.get(pdf_url, headers=send_headers)
    bytes_io = io.BytesIO(response.content)
    with open(save_path + "%s.pdf" % pdf_name, mode='wb') as f:
        f.write(bytes_io.getvalue())
        print('%s.pdf,下载成功！' % (pdf_name))

def pdf_to_text(save_path,pdf_path,text_name) -> None:
    # 打开PDF文件
    pdf_file = open(pdf_path, 'rb')

    # 创建一个PDF解析器对象
    pdf_parser = PDFParser(pdf_file)

    # 创建一个PDF文档对象
    pdf_document = PDFDocument(pdf_parser)

    # 创建一个PDF资源管理器对象
    pdf_resource_manager = PDFResourceManager()

    # 创建一个PDF设备对象
    output_stream = io.StringIO()
    text_converter = TextConverter(pdf_resource_manager, output_stream, laparams=LAParams())

    # 创建一个PDF解释器对象
    pdf_page_interpreter = PDFPageInterpreter(pdf_resource_manager, text_converter)

    # 遍历每一页，提取文本
    for page in PDFPage.create_pages(pdf_document):
        pdf_page_interpreter.process_page(page)

    text = output_stream.getvalue()
    with open(save_path + "%s.text" % text_name,'w',encoding='utf-8') as f:
    # 遍历每一页，提取文本
        f.write(text)
        print('%s.text,转换成功！' % (text_name))

    # 关闭文件
    pdf_file.close()

def analyze_text(text_path) -> list:
    result = []

    with open(text_path,'r',encoding='utf-8') as f:
        text = f.read()
    tr4w = TextRank4Keyword()
    
    tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    
    key_words = []
    for item in tr4w.get_keywords(20, word_min_len=1):
        key_words.append(item.word)
    result.append(key_words)

    key_phrases = []
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2):
        key_phrases.append(phrase)
    result.append(key_phrases)

    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'all_filters')
    
    abstract = []
    for item in tr4s.get_key_sentences(num=5):
        abstract.append(item.sentence)
    result.append(abstract)

    print('文本解析转换完成！')
    print("---------------------------------------------------------------------------------------")

    return result

def md5(file_path,Bytes=1024):
    md5_1 = hashlib.md5()                        #创建一个md5算法对象
    with open(file_path,'rb') as f:              #打开一个文件，必须是'rb'模式打开
        while 1:
            data =f.read(Bytes)                  #由于是一个文件，每次只读取固定字节
            if data:                      #当读取内容不为空时对读取内容进行update
                md5_1.update(data)
            else:                         #当整个文件读完之后停止update
                break
    ret = md5_1.hexdigest()              #获取这个文件的MD5值
    return ret

save_path = 'ESG_site/media/pdf/'
pdf_name = 'processing'
text_name = 'processing'
pdf_path = save_path + pdf_name + '.pdf'
text_path = save_path + text_name + '.text'
pdf_url=""

pdf_url = json_data[0]['url']
download_pdf(save_path, pdf_name, pdf_url)

for i in range(len(json_data)):
    try:    
        if i <= 629:
            continue
        data = json_data[i]
        report = models.esg_reports()
        report.title = data['title']
        report.edittime = datetime.datetime.strptime(data['publishdate'], '%Y-%m-%d')
        report.pdf_url = data['url']
        report.site = data['src']
        pdf_url = data['url']
        download_pdf(save_path, pdf_name, pdf_url)
        pdf_to_text(save_path, pdf_path, text_name)
        analysis = analyze_text(text_path)
        words = ''
        for word in analysis[0]:
            words += word
            words += ' '
        report.key_words = words
        phrases = ''
        for phrase in analysis[1]:
            phrases += phrase
            phrases += ' '
        report.key_phrases = phrases
        abstract = ''
        for abs in analysis[2]:
            abstract += abs
            abstract += '\n'
        report.abstract = abstract
        report.md5 = md5(pdf_path)
        report.save()
        print(f'第{i}条已完成')
        print('---------------------------------------------------------')
    except:
        print('Unexpected limit')

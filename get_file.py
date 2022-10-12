from ast import Sub
import os
from tokenize import Token
import urllib
import importlib,sys
importlib.reload(sys)
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
# from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

import re
from io import BytesIO
from io import open
from urllib.request import urlopen
import pandas as pd

path = "/Volumes/尹你而起/Previous Content/myOneDrive/工作/实验室项目/stock/file09/"
path_list = os.listdir(path)
path_list.remove('.DS_Store')    # 同上
# path_list.sort()
# print(path_list)
def get_program(out_text):
    p1 = '(38.{0,2}\..{0,3}收入.*?39)'
    # p2 = '(请保荐机构.*?)。'
    # p3 = '(问题.*?\. [0-9]{1,})'
    u1 = re.compile(p1, re.S)
    # u2 = re.compile(p2, re.S)
    lists = u1.findall(out_text)
    # lists2 = u2.findall(out_text)
    return lists
    # print(lists)

def convert_pdf_to_txt(path):
    print(path)
    fp = open(path, 'rb')
    txt = ''
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    parser.set_document(doc)
    # doc.set_parser(parser)
    # doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    out_text=''
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
        layout = device.get_result()
        # for lt_obj in layout:
        #     if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
        #         txt += lt_obj.get_text()
        for out in layout:
            if hasattr(out, 'get_text'):
                # if "38." in out.get_text() and "收入" in out.get_text():
                    # print(out.get_text())
                # print("*"*30)
                # print(out.get_text())
                out_text = out_text + out.get_text()
    return(out_text) 
# m={}
IN=[]
To=[]
Su=[]
Tax=[]
CC=[]
for file in path_list:
    txt=convert_pdf_to_txt(path+file)
    txt=txt.split('\n')
    IN.append(str(txt[1].split(':')[1]))
    To.append(txt[10])
    Su.append(txt[26])
    Tax.append(txt[27])
    CC.append(txt[29])
df=pd.DataFrame()
df['Invoice Number']=IN
df['To']=To
df['Subtotal']=Su
df['Tax']=Tax
df['Courier Company']=CC
# df.to_csv("lingjie-09.csv", mode='a', encoding='utf-8-sig')
# df['Invoice Number']=df['Invoice Number'].astype(str)
df.to_csv("lingjie09.csv", mode='a', encoding='utf-8-sig')
print(df)
    # t=get_program(txt)
    # m["name"]=file
    # m["txt"]=t
    # df = pd.DataFrame(m)

    # print(t)
    # print(path+file)

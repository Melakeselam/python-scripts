import tkinter as tk
from tkinter import filedialog
import PyPDF2
import re
import os


root = tk.Tk()
root.withdraw()

sections_file = filedialog.askopenfilename(initialdir="~/")
dirs = sections_file.split("/")
base_dir = "/".join(dirs[:len(dirs)-1]) + "/"

section_pgs = [int(pg.replace("\n","")) for pg in open(sections_file,"r").readlines()]

file_path = filedialog.askopenfilename(initialdir=base_dir)

#create reader variable that will read the pdffileobj
pdfreader=PyPDF2.PdfReader(file_path)
 
#This will store the number of pages of this pdf file
last_pg=len(pdfreader.pages)-3
print("last_pg= "+ str(last_pg))
 
#create a variable that will select the selected number of pages
pageobj=pdfreader.pages

def cleanup(txt:str):
    return ' '.join(txt.split())

def split_q_and_a(txt:str):
    split = txt.split('?')
    if len(split) == 1:
        return '\n' + split[0].strip()

    q = ''
    a = ''
    l = len(split)
    if l > 2:
        questions = split[0:l-1]
        q = '? '.join(questions)+ '?'
        
    else:
        q = split[0] + '?'
    q = ' '.join((q.replace(r"\n", " ")).split())
    a = split[l-1].strip()
    a = re.sub(r"(.*\d)[\s]+(\.)[\s]+([^\s]+)", r"\1\2 \3",a)
    return q + "`" + a + "|"


 
#(x+1) because python indentation starts with 0.
#create text variable which will store all text datafrom pdf file
p=0
q=p+1
if not os.path.exists(f"{base_dir}/flash_cards"):
    os.makedirs(f"{base_dir}/flash_cards")
while(p < len(section_pgs) - 1):
    topic_name = " ".join(pageobj[section_pgs[p]].extract_text().replace("\n"," ").split())
    # print("pageobj: ", pageobj, " extracted title: ", topic_name)
    # input()
    q_and_a_s= []
    for page in pageobj[section_pgs[p] + 1 : section_pgs[q]]:
        prepped = split_q_and_a(page.extract_text())
        
        if prepped.find('?') == -1:
            q_and_a_s[len(q_and_a_s)-1] = q_and_a_s[len(q_and_a_s)-1].replace("|",prepped + "|")
            continue
        q_and_a_s.append(prepped)
    text = "".join(q_and_a_s)
    file=open(f"{base_dir}/flash_cards/{topic_name}.txt","w")
    file.writelines(text)
    file.close()
    p+= 1
    q+= 1
# print(text[0])
#save the extracted data from pdf to a txt file
#we will use file handling here
#dont forget to put r before you put the file path
#go to the file location copy the path by right clicking on the file
#click properties and copy the location path and paste it here.
#put "\\your_txtfilename"

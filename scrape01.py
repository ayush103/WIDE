import csv
import datetime
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import Counter
from tkinter import *
from nltk.corpus import stopwords



global flag
flag=0
global temp
global domain
global exclusion_list
global javascript_jargon
global numbers
global word_counts

large_font = ('Verdana',30)

exclusion_list=["","|","!" ,"?",".",":",",",";",")","(","-","--",'—',"&","=",'~',"–",':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*','|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';','?', '#', '$', ')', '/',"›","·"]
javascript_jargon=['abstract','else','instanceof','super','boolean','enum','int','switch','break','export','interfacesynchronized','httpschemaorg','byte','@twitter','extends','let','this','case','false','long','throw','catch','final','nativethrows','char','finally','new',"www",'http','"wwwcommon"','"wwwwatch"','transient','class','float','null','true','const','for','package','try','continue','function','@context','@type','=â','private','typeof','debugger','goto','protected','var','default','ifpublic','void','delete','implements','return','volatile','do','import','short','while','double','instatic','with']
numbers=list(map(str, range(101)))
#main_screen = Tk() 

#t1 = Text(main_screen) 
#t1.pack() 

global main_screen
   

def create_csv_path(csv_path):
            if not os.path.exists(csv_path):
                with open(csv_path, 'w') as csvfile: # open that path w = write/create
                    header_columns = ['WORD', 'COUNT', 'TIMESTAMP']
                    writer = csv.DictWriter(csvfile, fieldnames=header_columns)
                    writer.writeheader()
            else:
                os.remove(csv_path)
                
def generate_csv():
            filename = domain.replace(".", "-") + '.csv'    
            path  = 'csv/' + filename 
            timestamp = datetime.datetime.now()
            time=timestamp.strftime("%Y-%m-%d %H:%M:%S")
            create_csv_path(path)
            with open(path, 'a') as csvfile:
                header_columns = ['word', 'count', 'timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=header_columns)
                for word, count in word_counts.most_common(30):
                        if((word not in exclusion_list)and (word not in javascript_jargon)and (word not in numbers)and(len(word)<=15)):
                            word=word.encode("utf-8")
                            writer.writerow({
                                    "word": word,
                                    "count": count,
                                    "timestamp": time})

    
    


def main_p():
        global domain
        global javascript_jargon
        global numbers
        global temp
    
        lblInfo = Label(main_screen, font = ('helvetica',10, 'bold'), 
              text = "Grabbing the URL : "+username_verify.get(), 
                         fg = "Black", bd = 10, anchor='w') 
                           
        lblInfo.pack()
        
        #print("Grabbing The URL"+ my_url)
        domain = urlparse(username_verify.get()).netloc # domain name

        lblInfo = Label(main_screen, font = ('helvetica',10, 'bold'), 
              text = "VIA Domain : "+domain, 
                         fg = "Black", bd = 10, anchor='w') 
                           
        lblInfo.pack()
        #print("VIA Domain", domain)
        #print("-----------------------------------------------------------------------------")
        global response
        response = requests.get(username_verify.get())
        a = response.status_code
        lblInfo = Label(main_screen, font = ('helvetica',10, 'bold'), 
              text = "Status is 200", 
                         fg = "Black", bd = 10, anchor='w') 
                           
        lblInfo.pack()
        Button(text="SAVE TO EXCEL", height="2", width="30", command =generate_csv).pack()
        
        #print("Status is", response.status_code)
        #print("-----------------------------------------------------------------------------")

        

        def clean_word(word):
            word = word.replace("!", "")
            word = word.replace("?", "")
            word = word.replace(".", "")
            word = word.replace(":", "")
            word = word.replace(",", "")
            word = word.replace(";", "")
            word = word.replace(")", "")
            word = word.replace("{", "")
            word = word.replace("}", "")
            word = word.replace("[", "")
            word = word.replace("]", "")
            word = word.replace("(", "")
            word = word.replace("-", "")
            word = word.replace("--", "")
            word = word.replace('—', "")
            word = word.replace("\\n", "")
            word = word.replace("\\t", "")
            word = word.replace("\\r", "")
            word = word.replace("'", "")
            word = word.replace('"', "")
            word = word.replace("/", "")
            word = word.replace("\\","")
            word = word.replace("|", "")
            word = word.replace("&", "")
            word = word.replace("1", "")
            word = word.replace("2","")
            word = word.replace("3", "")
            word = word.replace("4", "")
            word = word.replace("5", "")
            word = word.replace("6","")
            word = word.replace("7", "")
            word = word.replace("8", "")
            word = word.replace("9", "")
            word = word.replace("0","")
            return word

        def clean_up_words(words):
            new_words = []
            pkg_stop_words = stopwords.words('english')
            for word in words:
                word = word.lower()
                cleaned_word = clean_word(word)
                if cleaned_word in pkg_stop_words:
                    pass
                else:
                    new_words.append(cleaned_word)
            return new_words

        

        if response.status_code != 200: # not equal, == equal
            
            print("YOU CAN'T SCRAPE THIS WEBSITE")
            print("-----------------------------------------------------------------------------")
        else:
            print("Scraping")
            print("-----------------------------------------------------------------------------")
            # print(response.text)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            body_ = soup.find("body")
            #print(body_.text)
            words = body_.text.split() # removing stop words
            clean_words = clean_up_words(words)
            word_counts = Counter(clean_words)
            temp=[]
       
            for word1,count1 in word_counts.most_common(30):
                    if(word1 not in exclusion_list) and (word1 not in javascript_jargon)and (word1 not in numbers)and(len(word1)<=15) :
                        temp_str="("+word1+","+str(count1)+")"
                        temp.append(temp_str)
                        print(temp_str)


            scraping = Tk()
            scraping.title('SCRAPED OBJECTS')
            

            j=0
            k=0
            for temp_item in temp:
                if j<6:
                    lblInfo = Label(scraping, font = ('helvetica',10, 'bold'),text =temp_item,fg = "Green", bd = 10, anchor='w') 
                    lblInfo.grid(row=k,column=j)
                    j+=1
                else:
                    k+=1
                    j=0
        
            print("-----------------------------------------------------------------------------")
            
            
global word_counts
def temp1():
    pass
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("800x600")
    global Tops
    Tops = Frame(main_screen, width = 1600, relief = SUNKEN) 
    Tops.pack(side = TOP) 
    main_screen.title("WIDE")
    Label(text="WEBSITE INDEPENDENT DATA EXTRACTION TOOL ", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    cmd=temp1    

    main_screen.title("LOGIN")
    main_screen.geometry("800x600")
    Label(main_screen, text="ENTER THE URL OF THE WEBSITE YOU").pack()
    Label(main_screen, text="").pack()
 
    global username_verify
    global password_verify

    global flag
    flag=0

 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(main_screen, text="-------------URL-------------").pack()
    username_login_entry = Entry(main_screen, textvariable=username_verify,font=large_font)
    username_login_entry.pack()
    Label(main_screen, text="").pack()
    
        
        
        
    Button(main_screen, text="SCRAPE", width=10, height=1, command = main_p).pack()
    global my_url
    my_url = username_verify

    main_screen.mainloop()
 

main_account_screen()
        
        
    

#mainloop() 


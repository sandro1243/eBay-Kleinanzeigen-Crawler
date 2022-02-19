import requests
from bs4 import BeautifulSoup as bs
import random

import re
import csv
import argparse
import os

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


forbidden = [
    "DEFEKT",
    "FÜR BASTLER",
    "TAUSCHE",
    "BESCHÄDIGT",
    "NUR OVP",
    "DISPLAYSCHADEN", 
    "Panelschaden",
    "Wasserkühler",
    "Waterblock",
    "Gaming PC"
    ]



def lAnime():
   

    #loadingstring = "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁" # 15
    loadingstring = "⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿" #62
    print(color.GREEN,end="")
    for i in range(0,120):
        print(loadingstring[random.randrange(1,62)],end="")
    print("\r",end=color.END)
       

header = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

def buildUrl(item, p=1, ad="", location="/k0r0"):
    url = "https://www.ebay-kleinanzeigen.de/"
    
    
    seite = "seite:"
    return url + "s-anzeige:angebote/" + ad + seite + str(p) + "/" + buildSearch(item) + location + "+pcs.versand_s:ja"

def buildSearch(term):
    t = term.split()
    t = "-".join(t)
    
    return t

def getSuche(file):
    regex = "^[\w ]+"
    out = []
    try:
        with open(file,encoding='utf-8') as f:
            x = f.readlines()
        f.close()

        for i in x:
            if not i.startswith("#") and len(i) > 2:
                out.append(i.split("#")[0].rstrip())
    except:
        print("Error! Maybe your input File doesn't exist")
    
    return out

def getAllPrices(item):
    prices = []
    

    #get First Page
    response = requests.get(buildUrl(item), headers=header)
    
    #Get Number of Pages
    pages = getPages(response)
    
    #Check first Page for Prices
    #text = getPrices(response)

    #Check Prices on all pages
    for i in range(2,pages+1):
        lAnime()
        response = requests.get(buildUrl(item,i), headers=header)
        for i in getPrices(response):
            prices.append(i['price'])

        
    
    nextPages = pages + 1
    pages = getPages(response)
    
    for i in range(nextPages,pages+1):
        lAnime()
        response = requests.get(buildUrl(item,i), headers=header)
        for i in getPrices(response):
            prices.append(i['price'])

    nextPages = pages + 1
    pages = getPages(response)
    
    for i in range(nextPages,pages+1):
        lAnime()
        response = requests.get(buildUrl(item,i), headers=header)
        for i in getPrices(response):
            prices.append(i['price'])


    return prices, pages


def getPrices(response,forbidden=forbidden):
    
    prices = []
    regex = r"\d+"
    
    if response.status_code == 200:
        soup = bs(response.content, "lxml")
        for i in soup.find_all("li"):
            soup = bs(str(i),"lxml")
            titel = soup.find("a", {"class": "ellipsis"})
            description = soup.find("p",{"class": "aditem-main--middle--description"})
            price = soup.find("p", {"class": "aditem-main--middle--price"})
            location = soup.find("div", {"class": "aditem-main--top--left"})
            
            
            if titel != None:
                location = " ".join(location.text.replace("\n"," ").split())
                
                forbiddenWord = False
                for word in forbidden:
                    if word.upper() in titel.contents[0].upper() or word.upper() in description.contents[0].upper():
                        forbiddenWord = True
                        break
                if forbiddenWord:
                    continue
                price = price.contents[0]
                price = price.replace(".","").replace("€","")
                price = re.findall(regex,price)
                if len(price) == 0:
                    continue
                else:
                    price = int(price[0])
                #prices.append( (price,titel['href'], titel.contents[0] , description.contents[0], " ".join(location.text.replace("\n"," ").split()) ))
                prices.append( 
                    {
                        "price"     :price,
                        "link"      :titel['href'],
                        "title"     :titel.contents[0],
                        "desc"      :description.contents[0],
                        "location"  :location,
                        
                    }
                )
                
    return prices
            




def getPages(response):
    x = []
    if response.status_code == 200:
        soup = bs(response.content, 'lxml')
        for i in soup.find_all("a", {"class": "pagination-page"}):
            x.append(i.contents[0])
    
    if len(x) <= 1:
        return 1

    return int(x[-1])

def getMedian(p):
    prices = p[0]
    prices.sort()
    prices = list(filter((1).__ne__, prices))
    avg = 0
    median = 0 
    low10 = 0

    

    mid = int(len(prices)/2)
    perc = int(len(prices)/100*10)
    five_percent = int(len(prices)/100*2)

    counter = 0
    if len(prices) < 10 :
        perc = 1
    
    for i in prices:
        avg += i
        counter += 1
    if counter == 0:
        avg = 0
    else:
        avg = avg / counter

    if len(prices) > 2:
        counter = 0
        for i in range(mid-perc,mid+perc):
            median += prices[i-1]
            counter += 1 
        median = median / counter
    else:
        median = 0

    counter = 0
    if len(prices) > 2:
        for i in range(1,perc+1):
            low10 += prices[i-1]
            counter +=1 
        low10 = low10 / counter
    elif len(prices) == 1:
        low10 = prices[0]
    else:
        low10 = 0

    
    if len(prices) < 1:
        lowest = 0
        highest = 0
    else:
        lowest = prices[0]
        highest = prices[-1]

    return {"avg":avg,"median":median,"low10":low10,"pages":p[1],"lowest":lowest,"highest":highest}
    #return avg,median,low10,p[1]

def start(terms,minPages,file = "prices.csv", mode="w"):
    oldFile = os.path.exists(file)
    print("_"*120)
    print("{:^33} | {:^17} | {:^10} | {:^10} | {:^10} | {:^10} | {:^11} ".format("Item","Pages Crawled","Low 10%","AVG","Lowest","Median","Highest"))
    print("-"*120)
    with open(file, mode, newline="",) as csvfile:
            fieldnames = ["Artikel","Highest","Lowest","Durchschnitt","Median", "Low 10%","Target"]
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)

            if not oldFile or mode == "w":
                writer.writeheader()

            for item in terms:
                prices = getMedian(getAllPrices(item))
                low10 = lambda x: str(int(x))+"€" if prices["pages"] > minPages else color.YELLOW + "Ignored" + color.END
                if prices["pages"] > minPages:
                    writer.writerow({
                        'Artikel':item, 
                        'Highest':int(prices["highest"]),
                        'Lowest':int(prices["lowest"]),
                        'Durchschnitt':int(prices["avg"]), 
                        "Median":int(prices["median"]), 
                        "Low 10%":int(prices["low10"])
                        })
                if prices['pages'] < minPages:
                    print("{:<33} | {:>17} | {}{:^63}{} ".format( 
                        item, str(prices["pages"]) + " Pages",color.YELLOW,"- "*10 + "  Ignored  " + " -"*10,color.END ))
                else:
                    print("{:<33} | {:>17} | {:>10} | {:>10} | {:>10} | {:>10} | {:>11} ".format( 
                        item, str(prices["pages"]) + " Pages", low10(prices["low10"]), low10(prices["avg"]), low10(prices["lowest"]) , low10(prices["median"]) , low10(prices["highest"])) )


def singleSearch(minpages,term,output="prices.csv",mode="a"):
    start(file=output,mode=mode,terms=[term],minPages=minpages)
    
def printLogo():
    os.system("cls")
    print(color.GREEN + 
    """                   ______               _   ___      _                           _                   
                   | ___ \             | | / / |    (_)                         (_)                  
                ___| |_/ / __ _ _   _  | |/ /| | ___ _ _ __   __ _ _ __  _______ _  __ _  ___ _ __   
               / _ \ ___ \/ _` | | | | |    \| |/ _ \ | '_ \ / _` | '_ \|_  / _ \ |/ _` |/ _ \ '_ \  
              |  __/ |_/ / (_| | |_| | | |\  \ |  __/ | | | | (_| | | | |/ /  __/ | (_| |  __/ | | | 
               \___\____/ \__,_|\__, | \_| \_/_|\___|_|_| |_|\__,_|_| |_/___\___|_|\__, |\___|_| |_| 
                                 __/ |                                              __/ |            
                                |___/                                              |___/             
                                        _____                    _                                       
                                       /  __ \                  | |                                      
                                       | /  \/_ __ __ ___      _| | ___ _ __                             
                                       | |   | '__/ _` \ \ /\ / / |/ _ \ '__|                            
                                       | \__/\ | | (_| |\ V  V /| |  __/ |                               
                                        \____/_|  \__,_| \_/\_/ |_|\___|_|                    V1.1.1  
    """ + color.END
    ) 


if __name__ == "__main__":


    


    parser = argparse.ArgumentParser(description='eBay Kleinanzeigen Crawler')

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('-start' ,  action='store_true', 
                    help='Starts the Script in Default Mode (Reading from suche.txt and writing to prices.csv)')
    mode.add_argument('-search' , metavar="SEARCHTERM" , 
                    help='Starts a single search. By Deafault appends it to prices.csv')    
    parser.add_argument('-o', "--output" , metavar="FILE", default="prices.csv",
                    help='Defines the Output CSV')
    parser.add_argument('-i', "--input" , metavar="FILE", default="search.txt",
                    help='Defines the Input TXT File. One Search Term per Line. Supports Comments with #')
    parser.add_argument('-p', "--minpages" , default=3, type=int,
                    help='Minimum Pages found to be Included.')
    parser.add_argument('-a', "--append" , default="w", action='store_const' , const="a",
                    help='Append Mode. Default Overwrite Outputfile (Single Search appends by Default)')
    parser.add_argument("-ignored" , metavar="FILE", default="ignored.txt",
                    help='Defines an input File for Ignored words. One Word per Line. Example: Defect')
       


    args = parser.parse_args()
    
    
    oFile = args.output
    iFile = args.input
    
    sSearch = args.search


    printLogo()
    
    forbidden = []
    try:
        with open(args.ignored,encoding='utf-8') as file:
            x = file.readlines()
            for line in x:
                forbidden.append( line.strip())
        file.close()
        
    except:
        print("Ignored Words File not found!")
            
    
    print("_"*120 + color.CYAN +"\nIgnored Words:\n"+ ", ".join(forbidden).upper() + "\n" + color.END + "-"*120 + "\n")

    if args.start == True:
        start(file=oFile,terms=getSuche(iFile),mode=args.append,minPages=args.minpages)
        input("\nPress any Key to Exit")
        exit()
    
    if not args.search == False:
        singleSearch(term=args.search,output=oFile,mode="a",minpages=args.minpages)
        input("\nPress any Key to Exit")
        exit()
    


    input()
    

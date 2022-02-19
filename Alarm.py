import csv
import webbrowser
import eBayMedian
import requests
import os
import argparse
import re
#import tkinter
from tkinter import *

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


header = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
os.system("cls")

def show(link,price,artikel,counter,titel,desc,location,target,targetPrice,message):
    
    
    if counter == 0:
        print(color.CYAN + "-"*120 + color.END + "\n\n")
        print(color.CYAN + color.BOLD + "Found low Prices for " + color.GREEN + "{:<60}".format(artikel) + color.END + "{:>7} {:>9} ({:>5}€)".format("Target:",target,targetPrice) )
        print(color.CYAN + "-"*120 + color.END)
    
    print(color.YELLOW + "{:<5} -  ".format(str(price) + "€") + "{:<50}".format(titel) + color.END )
    print(color.END + location + color.END)
    print(color.END + desc.replace("\n"," ") + color.END)
    print(color.PURPLE + "https://www.ebay-kleinanzeigen.de"+link + color.END, end="\n\n")

    if message:
        desc = desc.replace("\n"," ")
        if len(desc) > 54:
            desc = desc[:54] + "\n" + "{:<54}".format(desc[54:len(desc)])
        titel = titel
        if len(titel) > 54:
            titel = titel[:54] + "\n" + "{:<54}".format(titel[54:len(titel)])
        root = Tk()
        root.title("Low Price Found!")
        root.geometry("600x450")
        text1 = Label(root, text=
                            "{:<20} {:<33}\n".format("Found low Prices for",artikel) +
                            "{:<54}\n\n".format(location) + 
                            "{:<20} {:>24} ({:>5}€)\n".format("Target:",target,targetPrice) + 
                            
                            "{:<54}\n{:<54}\n\n".format("Titel:",titel) +
                            "{:<54}\n{:<54}\n\n".format("Description:",desc) + 
                            "{:>54}".format("Price: "+str(price)+"€"))

        text2 = Label(root,text="\n\n")

        text1.pack()

        text2.pack()

        text1.configure(font=("Courier", 12, ))
       


        Label(root,text=" ").pack(side=RIGHT)
        Button(root, text="\n       OK       \n" ,command=lambda: root.destroy()).pack(side=RIGHT)
        Label(root,text=" ").pack(side=RIGHT)
        Button(root, text="\n       Visit       \n", command=lambda: openBrowser(root,"https://www.ebay-kleinanzeigen.de"+link)).pack(side=RIGHT)
        Label(root,text=" ").pack(side=RIGHT)
        Button(root, text="\n       Abort All       \n", command=lambda: exit()).pack(side=RIGHT)
        
        
        root.mainloop()
        # messagebox.showinfo(
        #     "Low Price Found", 
        #     "{:<20} {:<33}\n\n".format("Found low Prices for",artikel) +
        #     "{:<20} {:>24} ({:>5}€)\n".format("Target:",target,targetPrice) + 
        #     "{}\n".format(titel) +
        #     "{}\n".format(desc.replace("\n"," ")) +
        #     "{}\n".format("https://www.ebay-kleinanzeigen.de"+link))


def openBrowser(tk, link):
    webbrowser.open_new(link)
    tk.destroy()

def start(file,target,lowPerc,highPerc,loc,maxpages,forbidden,message,maxkm):
    with open(file, newline='') as csvfile:
        
        
        reader = csv.DictReader(csvfile)
        useTarget = target
        for row in reader:
            counter = 0
            url = eBayMedian.buildUrl(row['Artikel'],location="/" + loc)
            result = requests.get(url, headers=header)
            pages = eBayMedian.getPages(result)
            prices = eBayMedian.getPrices(result,forbidden=forbidden)
            
            if target == "csv":
                if row['Target'] != "":
                    useTarget = returnTarget(row["Target"])
                else:
                    useTarget = "Low 10%"
            #prices = prices.replace(".","")
            # prices = list(map(int,re.findall(regex,prices)))
        
            eBayMedian.lAnime()
            
            for price in prices:
                regex = r"\([a-z]*\.?[ ]?(\d+\.?\d?) km\)"
                result = re.findall(regex,price['location'])
                km = result[0]
                #if len(price[0]) > 0 : 
                if price['price'] < (int(row[useTarget])*(highPerc/100)) and price['price'] > (int(row[useTarget])*(lowPerc/100)):
                    if int(km) <= maxkm:
                        show(link=price['link'],price=price['price'],artikel=row["Artikel"],counter=counter,titel=price['title'],
                        desc=price['desc'],location=price['location'],target=useTarget,targetPrice=row[useTarget],message=message)
                    
                        counter += 1
                    
            # if count > 0:
            #     print("{:>2} Low Prices Found for {:<30} {}".format(count, row['Artikel']+"!", eBayMedian.buildUrl(row['Artikel'],1,"preis:{}:{}/".format(int((int(row['Low 10%'])*0.3)),(int(int(row['Low 10%'])*0.8))))))

            if pages > 1:
                if pages > maxpages:
                    pages = maxpages
                for page in range(2,pages):
                    
                    url = eBayMedian.buildUrl(row['Artikel'],page,location="/" + loc)
                    result = requests.get(url, headers=header)
                    prices = eBayMedian.getPrices(result)
                    # prices = prices.replace(".","")
                    # prices = list(map(int,re.findall(regex,prices)))
                    eBayMedian.lAnime()
                    for price in prices:
                        regex = r"\([a-z]*\.?[ ]?(\d+\.?\d?) km\)"
                        result = re.findall(regex,price['location'])
                        km = result[0]
                        #if len(price[0]) > 0 : 
                        if price['price'] < (int(row[useTarget])*(highPerc/100)) and price['price'] > (int(row[useTarget])*(lowPerc/100)):
                            if int(km) >= maxkm:
                                show(link=price['link'],price=price['price'],artikel=row["Artikel"],counter=counter,titel=price['title'],
                                desc=price['desc'],location=price['location'],target=useTarget,targetPrice=row[useTarget],message=message)

                                counter += 1
                    
        
                        

                
            
    csvfile.close()



def returnTarget(target):
    if target == "low10":
        return "Low 10%"
    if target == "avg":
        return "Durchschnitt"
    if target == "med":
        return "Median"
    if target == "csv":
        return "csv"

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Alarm Component of eBay Kleinanzeigen Crawler')

#file,mode,lowPerc,highPerc
    parser.add_argument('-i', "--input" , metavar="FILE", default="prices.csv",
                    help='Defines the Input File. Should be the Output CSV File of the Crawler Module. Default: prices.csv')
    parser.add_argument('-t', "--target" , choices=['avg', 'med', 'low10','csv'], default="low10",
                    help="Search for Average, Median or Low 10 Prices. You can Specify a Target for each Item in the CSV and use csv")  
    parser.add_argument('-p', "--maxpages" ,  default=5, type=int, 
                    help="Maxpages to be crawled")
    parser.add_argument('-k', "--maxkm" , metavar="30", default=30, type=int,
                    help='Filter for Radius from Location. Default: 30')  
    parser.add_argument('-l', "--location" , metavar="k0l1130r30", default="k0l1130r30", 
                    help='Filter for Location. Get the link from eBay. Search for Somethin with location and look at the last / . Should look like: k0l2131')
    parser.add_argument('-L', "--lowest" , metavar="20", default=20, type=int,
                    help='Filter for Lowest Percentage of Target Price. Used to filter out Rubbish. Default: 20')
    parser.add_argument("-H" ,"--highest", metavar="80" , default=80,type=int,
                    help='Filter for Highest Percentage of Target Price. Default: 80')
    parser.add_argument("-ignored" , metavar="FILE", default="ignored.txt",
                    help='Defines an input File for Ignored words. One Word per Line. Example: Defect')
    parser.add_argument("-messagebox" ,"-m" , action="store_true",
                    help='Defines an input File for Ignored words. One Word per Line. Example: Defect')
    parser.add_argument("-unattended" ,"-u" , action="store_true",
                    help='Defines an input File for Ignored words. One Word per Line. Example: Defect')

    
    args = parser.parse_args()
    
    

    target = returnTarget(args.target)

    forbidden = []
    try:
        with open(args.ignored,encoding='utf-8') as file:
            x = file.readlines()
            for line in x:
                forbidden.append( line.strip())
        file.close()
        
    except:
        print("Ignored Words File not found!")

    start(target=target,file=args.input,lowPerc=args.lowest,highPerc=args.highest,loc=args.location,maxpages=args.maxpages,forbidden=forbidden,message=args.messagebox,maxkm=args.maxkm)

if not args.unattended: 
    input("{:<120}".format("Press a Key to Exit!"))
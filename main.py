from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
import csv

# If needed:
# pip install beautifulsoup4

print("\nIf executed file is in the same folder, input only file name.\n")
fname = input('Enter file name (eg. your/path/links.txt): ')
        


# static dicts to gather data
mskills_dict = {}
eskills_dict = {}

print('Processing...')

for url in open(fname):
    # opening link and creating necessary BS files types
    try:
        html = urlopen(url)
        soup = BS(html, "html.parser")
        msource = soup.find('nfj-posting-requirements', id='posting-requirements')
        esource = soup.find('nfj-posting-requirements', id='posting-nice-to-have')
    except: pass
    # creating list of skills from BS types
    mskills = msource.find_all('common-posting-item-tag')
    mskills_lst = [(tag.text).strip().lower() for tag in mskills]
    try:
        eskills = esource.find_all('common-posting-item-tag')
        eskills_lst = [(tag.text).strip().lower() for tag in eskills]
    except:
        print(f'None extra requirements in {url}')
        pass
    # adding to dicts and counting
    for skill in mskills_lst:
        mskills_dict[skill] = mskills_dict.get(skill, 0)+1
    try:
        for skill in eskills_lst:
            if len(eskills) > 1:
                eskills_dict[skill] = eskills_dict.get(skill, 0)+1
            else: pass
    except: pass        
    print(f'Operation finished for {url}')    

# sorting    
mskills_dict = dict(sorted(mskills_dict.items(), key=lambda item: item[1], reverse=True))
eskills_dict = dict(sorted(eskills_dict.items(), key=lambda item: item[1], reverse=True))

# creating csv type file and adding to it from dicts
csvname = fname.split('.')[0]
with open(f'{csvname}.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    writer.writerow('M')
    for key, value in mskills_dict.items():
       writer.writerow([key, value])
    writer.writerow('E')
    for key, value in eskills_dict.items():
        writer.writerow([key, value])

print(f'Done, created file: {csvname}.csv')

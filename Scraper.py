# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
#
import requests
import csv
from lxml import html

#The structure of the website, which I have chosen to analyze, contains a blog page where only the first part of each blog post is shown. 
# So, before being able to scrape all the texts from each blog post it is necessary to scrape all the links to each post page.
    

## 1st Step : Getting the LINKS

#%% Creating the different URLs
list_range = list(range(1,14)) #the website contains 13 pages in tis blog section
baseurl= "https://basicincome.org/news/category/opinion/blogs/"
mid_url= "/page/" ## here I am creating the structure each page of the website

final = []
for i in list_range:
    final_url = baseurl + mid_url + str(i)
    final.append(final_url)
    
#%% #Scraping the links for each blog post 
posts = []
for l in final:
 post = requests.get(l).text
 posts.append(post)
 #print(posts)

#%% #Getting all the trees
alltree = []
for f in posts:
    tree = html.fromstring(f)
    alltree.append(tree)
#%% # Getting the x-path
listoflinks = []
for tree in alltree:
    j = tree.xpath('//article[*]/h2/a') #the x-path of the link that is contained in the page
    listoflinks.append(j)

#%% Getting all the links
links= []   
for g in listoflinks:
    for k in g:
      boh= k.attrib["href"]
      links.append(boh)
print(links)


## 2nd Step: Scraping the TEXT from each link

#%% Get the text for all the blog posts

htmlsources =[]

for link in links:
    h = requests.get(link).text
    htmlsources.append(h)

#%%
sometrees=[] #getting the trees
for htmlsource in htmlsources:
    tree = html.fromstring(htmlsource)
    sometrees.append(tree)
#%%
articles=[]

for tree in sometrees: 
    article = tree.xpath('//*[@class="entry clearfix"]//text()') #x-path for the body of the article
    articles.append(article)
#%%   
finals=[]
for a in articles:
    finali = str(a) #transforming it into a string 
    finals.append(finali)
#%% ##Cleaning the Output from the Scraper 
cleaned= []
for finali in finals:
  y= finali.replace("\n","").replace("\r","").replace("\\n","").replace("\\r","").replace("\\t\\t\\t\\t\\t\\t\\t\\t", "").replace("\\r\\n\\r\\n\\r\\n", "").replace("\t", "").replace("\\t", "").replace("\\r\\n\\t\\t\\t\\t\)", "").replace("\xa0", "")
  cleaned.append(y) #
 
    
#%%  ## Exporting it and Saving into a file

output = zip(links, cleaned)

with open("C:/Users/Camilla/Desktop/BigData/HEllo.csv",mode="w", encoding= "utf-8") as fo:
  writer=csv.writer(fo)
  writer.writerows(output)  



    



#
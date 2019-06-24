# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 13:35:00 2019

@author: shanthi
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd



baseurl		= "http://www.moneycontrol.com"

datenewsdict={}


def get_response(aurl):

	return requests.get(aurl).content

# Procedure to return a parseable BeautifulSoup object of a given url
def get_soup(aurl):
	response 		= get_response(aurl)
	soup 			= BeautifulSoup(response,'html.parser')
	return soup

def store_news(soup):
	news = soup.find_all('a',{'class':'g_14bl'})

	newslist=[]
	for link in news:
			# print(link.get_text()+" : "+baseurl+link['href'])
			newslist.append(link.get_text())
	datelist=[]
	date = soup.find_all('p',{'class':'PT3 a_10dgry'})
	
	for link in date:
			# print(link.get_text()+" : "+baseurl+link['href'])
			datelist.append(link.get_text().split("|")[1].strip().replace(" ","-"))



	for i,j in zip(newslist,datelist):
		val=datenewsdict.get(j.strip(),-1)
		if val==-1:
			datenewsdict[j.strip()]=i.strip()
		else:
			if i.strip() not in datenewsdict[j.strip()]:
				datenewsdict[j.strip()]=datenewsdict[j.strip()]+". "+i.strip()


def get_all_years_data(aurl):
	soup = get_soup(aurl)
	
	list = soup.find('div',{'class':'FR yrs'})

	links= list.find_all('a')

	for link in links:
		# print(link.get_text()+" : "+baseurl+link['href'])
		print("Year : "+link.get_text()+" "+baseurl+link['href'])
		soup1=get_soup(baseurl+link['href'])
		store_news(soup1)
		pagesoup = soup1.find('div',{'class':'pages MR10 MT15'})
		try:
			pages= pagesoup.find_all('a')
			for page in pages:
				print("page : "+page.get_text()+" "+baseurl+page['href'])                
				soup2=get_soup(baseurl+page['href'])
				store_news(soup2)
		except(AttributeError) :
			# Token not found. Replace 'pass' with additional logic.
			print(" page bar not found.")
				
	df = pd.DataFrame(data=datenewsdict, index=["news"])
	df = (df.T)
	df.to_excel('newsf.xlsx')		

if __name__ == '__main__':

	url 			= "https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=TCS&durationType=Y&Year=2019"

	print("Initializing")

	get_all_years_data(url)    

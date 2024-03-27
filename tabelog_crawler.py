from urllib.request import urlopen
import urllib.request
import urllib.parse
import urllib
import lxml.html
import os.path
import pandas as pd



shop_review_url = 'https://tabelog.com/tokyo/A1302/A130202/13193074/dtlrvwlst/COND-0/smp1/?smp=1&lc=0&rvw_part=all&PG='
max_reviewList_pages=100
for pageNo in range(max_reviewList_pages):
	print('page=',pageNo+1)
	
	bodyRes = urllib.request.urlopen(shop_review_url + str(pageNo+1))
		
	bodyHtml = bodyRes.read()						
	htmlTreeBody = lxml.html.fromstring(bodyHtml.decode('utf-8'))
	title_path = htmlTreeBody.xpath("//a[@class='rvw-item__title-target']/strong")
	
	
	review_path = htmlTreeBody.xpath("//div[@class='rvw-item__rvw-comment rvw-item__rvw-comment--custom']/p")
	
	#レビューリストページ1ページにあるフルレビューリンクリストを1つづつ読みだす
	for title,review in zip(title_path,review_path):
		
		print('title',title.text_content())	
		review = review.text_content().replace('<br />','').replace(' ','')
		print('tweets',review)
		

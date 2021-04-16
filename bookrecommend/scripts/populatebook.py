import pandas as pd 
import numpy as np 

from main.models import userinfo,book

def run():
	frame = pd.read_csv('main/main_dataset.csv')
	h,r = frame.shape
	print(len(frame['category'].unique()))
	# 0 - 9th row 

	categ = frame['category'].unique()
	print(categ)
	col_list = ['name','author','rating','category','image']
	frame = frame.loc[:,col_list]
	frame = frame.drop_duplicates(subset=['name'])

	# for i in range(3128+100,3128+1100):
	# 	(Name,Author,Rating,Category,Image) = frame.loc[i,col_list]
	# 	q = book(name = Name,author = Author,rating = Rating,category = Category,image = Image)
	# 	q.save()

	for i in categ:
		print('doing: ', i)
		frame_temp = frame['category'] == i
		frame_temp = frame[frame_temp]
		#print(frame_temp)
		temp = frame_temp.iloc[:30]
		#print(temp)
		for j in range(30):
			(Name,Author,Rating,Category,Image) = temp.iloc[j]
			q = book(name = Name,author = Author,rating = Rating,category = Category,image = Image)
			q.save()
			print("-",end = " ")
		print(" ")







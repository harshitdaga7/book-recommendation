import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import userinfo,book
import random as rnd

# Create your views here.
@csrf_exempt
def home(request):
	return render(request,'main/home.html')

#########################################
@csrf_exempt
def login(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		usrnm = data['username']
		password = data['password']
		print(data) #comment it afterwards

		#status code : 'OK' --> right user and password
		#status code : 'DNE' --> USER DOES NOT EXIST
		#status code : 'WP' --> wrong password
		try:
			#if user exists
			#if password match
			if password == userinfo.objects.get(username = usrnm).password:
				return JsonResponse({'status':'OK'})
			else:
				return JsonResponse({'status':'WP'})

		except userinfo.DoesNotExist:
			return JsonResponse({'status':'DNE'})

	else:
		return render(request,'main/login.html')


##################################################
@csrf_exempt
def signup(request):
	if request.method == "POST":
		data = json.loads(request.body)
		usrnm = data['username']
		password = data['password']
		email = data['email']
		print(data) #comment it
		#status code :'EX' --> username already exits
		#status code : 'OK' --> success  registered
		try:
			#if user already exist
			temp = userinfo.objects.get(username = usrnm).username
			return JsonResponse({'status':'EX'})
		except userinfo.DoesNotExist:
			#user does not exist
			u = userinfo(username = usrnm,password = password,email = email,category = initialize_cat())
			u.save()
			return JsonResponse({'status':'OK'})

	else:
		return render(request,'main/sign_up.html')



##################################################
@csrf_exempt
def name_search(request):
	print('name called')
	if request.method == 'POST':
		data = json.loads(request.body)
		username = data['username']
		query = data['query']
		print(data)
		q = book.objects.filter(name__icontains = query)[:10]
		update_recommend(q,username)
		res = makeJson(q)
		return JsonResponse(res)


#################################################
@csrf_exempt
def author_search(request):
	print('author called')
	if request.method == 'POST':
		data = json.loads(request.body)
		username = data['username']
		query = data['query']
		print(data) 
		q = book.objects.filter(author__icontains = query)[:10]
		update_recommend(q,username)
		res = makeJson(q)
		return JsonResponse(res)

@csrf_exempt
def category_search(request):
	print('cat called')
	if request.method == 'POST':
		data = json.loads(request.body)
		username = data['username']
		query = data['query']
		print(data)
		q = book.objects.filter(category__icontains = query)[:10]
		update_recommend(q,username)
		res = makeJson(q)
		return JsonResponse(res)


@csrf_exempt
def recommend(request):
	print('recommend calles')
	if request.method == 'POST':
		data = json.loads(request.body)
		username = data['username']
		print(data)
		key_main = ['Medical','Science-Geography','Art-Photography','Biography','Business-Finance-Law','Childrens-Books','Computing','Crafts-Hobbies','Crime-Thriller','Dictionaries-Languages','Entertainment','Food-Drink','Graphic-Novels-Anime-Manga','Health','History-Archaeology','Home-Garden','Humour','Mind-Body-Spirit','Natural-History','Personal-Development','Poetry-Drama','Reference','Religion','Romance','Science-Fiction-Fantasy-Horror','Society-Social-Sciences','Sport','Stationery','Teaching-Resources-Education','Technology-Engineering','Teen-Young-Adult','Transport','Travel-Holiday-Guides']
		user = userinfo.objects.get(username = username)
		rank = user.getRankings()
		rank_convert = [[freq,ind] for ind,freq in enumerate(rank)]
		rank_convert.sort(reverse = True)

		rank_convert = rank_convert[:5]
		cat_list = []

		for freq,ind in rank_convert:
			cat_list.append(key_main[ind])

		print(cat_list)

		res = {}

		for i in range(5):
			r = rnd.randint(0,25)
			q = book.objects.filter(category = cat_list[i])[r]
			res[i] = makeJson2(q)


		r1 = rnd.randint(0,32)
		r11 = rnd.randint(0,25)
		r2 = rnd.randint(0,32)
		r21 = rnd.randint(0,25)

		q1 = book.objects.filter(category = key_main[r1])[r11]
		q2 = book.objects.filter(category = key_main[r2])[r21]

		res[5] = makeJson2(q1)
		res[6] = makeJson2(q2)

		return JsonResponse(res)

def makeJson2(q):
	temp = {'name': q.name,
			'author':q.author,
			'rating':q.rating,
			'category':q.category,
			'image':q.image
			}

	return temp

def makeJson(q):
	res = {}
	if(len(q) > 0):
		res['status'] = 'OK'
	else:
		res['status'] = 'NOK'

	for i,val in enumerate(q):
		temp = {'name': val.name,
				'author':val.author,
				'rating':val.rating,
				'category':val.category,
				'image':val.image
				}
		res[i] = temp


	return res;

def initialize_cat():
	l = ['0' for i in range(33)]
	s = ','.join(l)
	return s



def update_recommend(q,username):
	user = userinfo.objects.get(username = username)
	cat_list = [i.category for i in q]
	key_main = ['Medical','Science-Geography','Art-Photography','Biography','Business-Finance-Law','Childrens-Books','Computing','Crafts-Hobbies','Crime-Thriller','Dictionaries-Languages','Entertainment','Food-Drink','Graphic-Novels-Anime-Manga','Health','History-Archaeology','Home-Garden','Humour','Mind-Body-Spirit','Natural-History','Personal-Development','Poetry-Drama','Reference','Religion','Romance','Science-Fiction-Fantasy-Horror','Society-Social-Sciences','Sport','Stationery','Teaching-Resources-Education','Technology-Engineering','Teen-Young-Adult','Transport','Travel-Holiday-Guides']
	converted_s = user.getRankings()

	for i in range(33):
		if(key_main[i] in cat_list):
			converted_s[i]+=1

	s = [str(i) for i in converted_s]
	res = ','.join(s)
	print(res)
	user.category = res
	user.save()

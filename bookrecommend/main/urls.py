from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login',views.login,name = 'login'),
    path('signup',views.signup,name = 'signup'),
    path('name',views.name_search,name = 'name'),
    path('author',views.author_search,name = 'author'),
    path('category',views.category_search,name = 'category'),
    path('recommend',views.recommend,name = 'recommend'),
]
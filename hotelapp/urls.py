from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('rooms/', views.rooms, name='rooms'),
    path('gym/', views.gym, name='gym'),
    path('explore/', views.explore, name='explore'),
    path('contact/', views.contact, name='contact'),
    path('category/<str:id>/', views.category, name='category'),
    path('room/<str:id>/', views.room, name='room'),
    path('password/', views.password, name='password'),
    path('logout/', views.logoutfunc, name='logout'),
    path('login/', views.loginpage, name='login'),    
    path('signup/', views.signupform, name='signupform'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('reservation/', views.reservation, name='reservation'),
    path('checkout', views.checkout, name='checkout'),
    path('deleteitem/',views.deleteitem, name='deleteitem'),
    path('increase/', views.increase, name='increase'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('completed/', views.completed, name='completed'),
    path('history/', views.history, name='history'),
]
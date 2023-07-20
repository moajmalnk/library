from django.urls import path

from . import views

app_name = 'mylibrary'

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:id>/', views.detail_view, name='detail'),
    path('add_book/', views.add_book, name='add_book'),
    path('update/<int:id>/', views.update_book, name='update'),
    path('delete/<int:id>/', views.delete_book, name='delete'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_patron/', views.add_patrons, name='add_patron'),
    path('all_patrons/', views.all_patrons, name='all_patrons'),
    path('update_patron/<int:id>/', views.update_patron, name='update_patron'),
    path('delete_patron/<int:id>/', views.delete_patron, name='delete_patron'),
    path('newspaper/', views.news_paper, name='newspaper'),
    path('program/<int:id>/', views.programmes, name='program'),
    path('category/', views.all_book_category, name='all_book_category'),
    path('category/<slug:c_slug>/', views.all_book_category, name='books_by_category'),

]

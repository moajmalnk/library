from django.urls import path

from mylibrary.views import *
from search_app import views

app_name = 'search_app'

urlpatterns = [
    path('', views.search_result, name='search'),
    path('patron/', views.patrons, name='patron'),
    path('superuser/', superuser, name='superuser'),
    path('add_notification/', add_notifications, name='add_notify'),
    path('download/<int:notification_id>/', download_card, name='download_page'),
    path('download/<int:notification_id>/', download_card, name='download'),
    path('update_notification/<int:id>/', update_notify, name='update_notify'),
    path('update_news/<int:id>/', update_news, name='update_news'),
    path('delete_notification/<int:id>/', delete_notify, name='delete_notify'),
    path('issue_patron/<int:id>/', issue_patron, name='issue_patron'),
    path('return_patron/<int:id>/', return_patron, name='return_patron'),
    path('renew_patron/<int:id>/', renew_patron, name='renew_patron'),
    path('return_all_books/<int:id>/', return_all_books, name='return_all_books'),
    path('renew_all_books/<int:id>/', renew_all_books, name='renew_all_books'),
    path('pay_all_fine/<int:id>/', pay_all_fine, name='pay_all_fine'),
    path('pay_fine/<int:id>/', pay_fine, name='pay_fine'),
    path('all_history/', all_history, name='all_history'),
    path('history/', history, name='history'),
    path('add_category/', add_category, name='add_category'),
    path('add_newspaper/', add_newspaper, name='add_newspaper'),
    path('delete_category/<int:id>/', delete_category, name="delete_category"),
    path('delete_newspaper/<int:id>/', delete_newspaper, name="delete_newspaper"),
    path('all_programmes/', all_programmes, name='all_programmes'),
    path('profile/<int:id>/', profile, name='profile'),

]

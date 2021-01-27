from django.urls import path
from .models import Jietu
from jietu import views

app_name = 'jietu'

urlpatterns = [
    path('add_domain', views.AddDomain.as_view(), name='add_domain'),
    path('jietu_detail/<str:domain>', views.jietu_detail, name='jietu_detail'),
    path('domaintype_list/', views.domaintype_list, name='domaintype_list'),
    path('domaintype/<domaintype>', views.show_domaintype_expiration_date,
         name='show_domaintype_expiration_date'),
    path('domaintype/<domaintype>/<str:expiration_date>',
         views.show_domaintype_expiration_date_pic, name='show_domaintype_expiration_date_pic'),
    path('domaintype/no/<domaintype>/<str:expiration_date>',
         views.show_domaintype_expiration_date_no_pic, name='show_domaintype_expiration_date_no_pic'),

]

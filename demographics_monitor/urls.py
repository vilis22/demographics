from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000 отвечает за главную страницу
    path('concept/', views.concept, name='concept'),
    path('platform/', views.platform, name='platform'),
    path('news/', views.news, name='news'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.login, name='login'),
    path('test_page/', views.test_page, name='test_page'),  # http://127.0.0.1:8000/test_page/
    path('target/', views.target, name='target'),
    path('population/', views.population, name='population'),
    path('fertility/', views.fertility, name='fertility'),
    path('mortality/', views.mortality, name='mortality'),
    path('migration/', views.migration, name='migration'),
    path('marriages/', views.marriages, name='marriages')
]

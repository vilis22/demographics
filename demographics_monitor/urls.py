from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000 отвечает за главную страницу
    path('concept/', views.concept, name='concept'),  # Концепция
    path('platform/', views.platform, name='platform'),  # О платформе
    path('news/', views.news, name='news'),  # Новости
    path('contacts/', views.contacts, name='contacts'),  # Контакты
    path('login/', views.login, name='login'),  # Авторизация
    path('target/', views.target, name='target'),  # Целевые показатели и прогноз
    path('population/', views.population, name='population'),  # Численность и структура населения
    path('fertility/', views.fertility, name='fertility'),  # Рождаемость
    path('mortality/', views.mortality, name='mortality'),  # Смертность
    path('migration/', views.migration, name='migration'),  # Миграция
    path('marriages/', views.marriages, name='marriages')  # Браки и разводы
]

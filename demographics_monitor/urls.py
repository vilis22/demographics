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

    path('mortality_main/', views.mortality_main, name='mortality_main'),  # Смертность

    path('migration_threads/', views.migration_threads, name='migration_threads'),  # Миграция по потокам
    path('migration_gender/', views.migration_gender, name='migration_gender'),  # Миграция по полу
    path('migration_age/', views.migration_age, name='migration_age'),  # Миграция по возрастным группам
    path('migration_gender_age/', views.migration_gender_age, name='migration_gender_age'),  # Миграция по полу и возрастным группам


    path('marriages/', views.marriages, name='marriages')  # Браки и разводы
]

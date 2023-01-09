from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('outlook/', views.outlook, name='outlook'),
    path('financial_forecast/', views.forecast, name='forecast'),
    path('financial_perspectives/', views.perspective, name='perspective'),
    path('financial_strategies/', views.strategies, name='strategies'),
    path('diversity/', views.diversity, name='diversity'),
    path('contact_us/', views.contact, name='contact'),
    path('AI_trading/', views.ai, name='ai'),
    path('FX_trading/', views.forex, name='forex'),
    path('ESG/', views.esg, name='esg'),
    path('investment/', views.investment, name='investment')
]
from django.urls import path
from . import views


urlpatterns = [
    path('watchlist', views.WatchListAPI.as_view()),
    path('watchlist/edit', views.WatchListEditAPI.as_view()),
    path("symbol", views.SymbolAPI.as_view()),
    path("stockvalues", views.StockValuesAPI.as_view()),
]


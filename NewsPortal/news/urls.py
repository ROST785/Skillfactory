from django.urls import path
from .views import NewsList, NewDetail


urlpatterns = [
    path('news/', NewsList.as_view()),
    path('news/<int:pk>', NewDetail.as_view())
]
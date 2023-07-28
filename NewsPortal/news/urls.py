from django.urls import path
from .views import NewsList, NewDetail, NewCreate, NewDelete, NewUpdate, NewsSearch


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewDetail.as_view()),
    path('create/', NewCreate.as_view(), name='new_create'),
    path('<int:pk>/edit/', NewUpdate.as_view(), name='new_update'),
    path('<int:pk>/delete/', NewDelete.as_view(), name='new_delete'),
    path('search/', NewsSearch.as_view())
]
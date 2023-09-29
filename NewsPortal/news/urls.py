from django.urls import path
from .views import NewsList, NewDetail, NewCreate, NewDelete, NewUpdate, NewsSearch, CategoryList, subscribe
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(300)(NewsList.as_view())),
    path('<int:pk>', NewDetail.as_view()),
    path('create/', cache_page(300)(NewCreate.as_view()), name='new_create'),
    path('<int:pk>/edit/', cache_page(300)(NewUpdate.as_view()), name='new_update'),
    path('<int:pk>/delete/', cache_page(300)(NewDelete.as_view()), name='new_delete'),
    path('search/', cache_page(300)(NewsSearch.as_view())),
    path('categories/<int:pk>', cache_page(300)(CategoryList.as_view()), name='category_list'),
    path('categories/<int:pk>/subscribe', cache_page(300)(subscribe), name='subscribe')
]
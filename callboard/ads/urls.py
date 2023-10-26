from django.urls import path
from .views import AdsList, AnnouncementDetail, AnnouncementCreate, AnnouncementUpdate, AnnouncementDelete, CategoryList, subscribe


urlpatterns = [
    path('', AdsList.as_view()),
    path('<int:pk>', AnnouncementDetail.as_view()),
    path('create/', AnnouncementCreate.as_view(), name='announcement_create'),
    path('<int:pk>/edit/', AnnouncementUpdate.as_view(), name='announcement_update'),
    path('<int:pk>/delete/', AnnouncementDelete.as_view(), name='announcement_delete'),
    path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe')
]
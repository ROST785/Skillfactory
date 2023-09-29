from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('admin/', cache_page(60)(admin.site.urls)),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('protect/', include('protect.urls'))
]

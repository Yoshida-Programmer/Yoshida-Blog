from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls')),
    path('markdownx/', include('markdownx.urls')),
    url(r'mdeditor/', include('mdeditor.urls')),
]

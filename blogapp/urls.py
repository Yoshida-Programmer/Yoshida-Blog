from django.urls import path
from . import views
from .views import BlogList, BlogDetail, TagView, CommentView

app_name = 'blogapp'

urlpatterns = [
    path('', BlogList.as_view(), name='list'),
    path('detail/<int:pk>', BlogDetail.as_view(), name='detail'),
    path('comment/create/<int:pk>/', views.CommentView.as_view(), name='comment_create'),
    path('tag/<str:tag>/', TagView.as_view(),name='tag'),
    path('search/', views.SearchView.as_view(), name='search'),
]

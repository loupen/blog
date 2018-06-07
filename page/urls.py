from django.urls import path

from . import views

app_name = 'page'
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('page/<int:pk>', views.PageView.as_view(), name='page'),
	path('author/<int:pk>', views.AuthorView.as_view(), name='author'),
	path('wx', views.WeChatView.as_view(), name='author'),
]


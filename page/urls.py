from django.urls import path,include,re_path

from . import views

app_name = 'page'
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('page/<int:pk>', views.PageView.as_view(), name='page'),
	path('author/<int:pk>', views.AuthorView.as_view(), name='author'),
	path('wx', views.WeChatView.as_view(), name='author'),
	re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
	path('tian_mao/', views.TianMaoView.as_view(), name='author'),
]


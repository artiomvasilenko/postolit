from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index')
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

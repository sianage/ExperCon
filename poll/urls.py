from django.urls import path
from . import views
from .views import poll_list, poll_detail

urlpatterns = [
    path('poll_list/', poll_list.as_view(), name='poll_list'),
    path('<int:poll_id>/poll_details/', views.poll_detail, name='poll_details'),
    path('<int:poll_id>/vote/', views.vote, name='vote'),
    path('<int:poll_id>/results/', views.results, name="results"),
    path('create_poll', views.CreatePollView, name='create_poll')
]
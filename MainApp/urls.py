from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import post_detail, home, debate_list, debate_detail, philosophy_blog, AddBlogView, UpdateBlogView, \
    DeleteBlogView, AddCommentView, AddDebateView

app_name = 'MainApp'

urlpatterns = [
    path('', views.home, name='home'),
    path('blog_post/<int:pk>/', post_detail.as_view(), name='post_detail'),
    path('debate_list/', debate_list.as_view(), name='debate_list'),
    path('debate/<int:pk>/', debate_detail.as_view(), name='debate-details'),
    path('philosophy/', views.home, name='philosophy_blog_list'),
    path('economics/', views.home, name='economics_blog_list'),
    path('add_post/', AddBlogView.as_view(), name="add_post"),
    path('blog_post/edit/<int:pk>', UpdateBlogView.as_view(), name='update_post'),
    path('blog_post/delete/<int:pk>', DeleteBlogView.as_view(), name='delete_post'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('delete_note/<int:pk>', views.delete_note, name='delete_note'),
    path('edit_note/<int:pk>', views.edit_note, name='edit_note'),
    path('debate/<int:pk>/comment/', views.AddCommentView, name="comment"),
    path('start_debate/', AddDebateView.as_view(), name="start_debate"),
    path('draft_list/', views.DraftListView.as_view(), name='draft_list'),
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('conversations/<int:receiver_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversations/<int:receiver_id>/send/', views.send_message, name='send_message'),
]
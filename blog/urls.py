from django.contrib import admin
from django.urls import path
from blog import views as blog_views

from django.contrib.auth import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', blog_views.post_list, name='post_list'),
    path('post/<int:pk>/', blog_views.post_detail, name='post_detail'),
    path('post/new/', blog_views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', blog_views.post_edit, name='post_edit'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('post/<int:pk>/delete/', blog_views.post_delete, name='post_delete'),
    path('post/<int:pk>/delete_confirmation/', blog_views.post_delete_confirmation, name='post_delete_confirmation'),
    path('draft/', blog_views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', blog_views.post_publish, name='post_publish'),
    path('post/<int:pk>/unpublish/', blog_views.post_unpublish, name='post_unpublish'),
    path('post/<int:pk>/comment/', blog_views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', blog_views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', blog_views.comment_remove, name='comment_remove'),
    path('comment/<int:pk>/vote/', blog_views.comment_vote, name='comment_vote')
]
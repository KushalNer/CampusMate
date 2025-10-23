from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'CampusMateApp'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile_view, name='edit_profile'),
    path('settings/', views.settings_view, name='settings'),
    path('explore-topics/', views.explore_topics_view, name='explore_topics'),
    path('explore-topics/<int:pk>/', views.explore_topic_detail_view, name='explore_topic_detail'),
    path('slips/', views.slip_solutions, name='slip_solutions'),
    path('slip/question/<int:pk>/', views.slip_question_detail, name='slip_question_detail'),
    path('community/', views.community_view, name='community'),
    path('community/create/', views.create_thread_view, name='create_thread'),
    path('community/thread/<int:pk>/', views.thread_detail_view, name='thread_detail'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service_view, name='terms_of_service'),
    path('support/', views.support_view, name='support'),
]

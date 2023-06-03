from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [path('',views.index, name='index'),
                path('<int:question_id>/form',views.detail, name='detail'),
path('<int:question_id>/results/',views.results, name='results'),
path('<int:question_id>/vote/',views.vote, name='vote'),
path('register/', views.register, name='register'),
path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
path('logout/', auth_views.LogoutView.as_view(template_name="logout.html"), name='logout'),
path('about/<int:pk>/', views.about, name='about'),
]
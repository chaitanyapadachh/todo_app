from . import views
from django.urls import path

urlpatterns = [
    path("register/",views.SignUpView.as_view(),name="signup"),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
]

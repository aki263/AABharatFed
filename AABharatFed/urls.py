"""AABharatFed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from AccAggApp.views import ProfileView, Conset1,profile2,Dashboard,Expense

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),
    path('accounts/profile/', ProfileView.as_view()),
    path('accounts/consent1/', Conset1.as_view()),
    path('accounts/profile2/', profile2.as_view()),
    path('accounts/dashboard/', Dashboard.as_view()),
    path('accounts/expense/', Expense.as_view())

]

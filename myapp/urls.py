"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_records', views.add_records, name='add_records'),
    path('display_all', views.display_all, name='display_all'),
    path('search_all', views.search_all, name='search_all'),
    # path('records_per_page_view', views.records_per_page_view, name='records_per_page_view'),
    path('records_per_page_view_2', views.records_per_page_view_2, name='records_per_page_view_2'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('update/<int:id>', views.update, name='update'),
    # path('display/<int:id>', views.display, name='display'),
    

]

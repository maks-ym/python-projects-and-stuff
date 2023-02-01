"""notes app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import path
from .views import AddView, DeleteView, DetailView, EditView, IndexView

app_name = 'notes'
urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('list', IndexView.as_view(), name='home'),
    path('<int:pk>', DetailView.as_view(), name='detail'),
    path('add', AddView.as_view(), name='add'),
    path('<int:pk>/edit', EditView.as_view(), name='edit'),
    path('<int:pk>/delete', DeleteView.as_view(), name='delete')
]

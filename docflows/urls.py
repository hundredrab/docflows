"""docflows URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static

from process import views as pviews
from documents import views as dviews
from account import views as aviews
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/processes', pviews.ListProcesses.as_view()),
    path('api/documents', dviews.ListDocuments.as_view()),
    path('api/documents/permissions', dviews.ViewableDocuments.as_view()),
    path('api/documents/details/<int:pk>', dviews.DocumentDetails.as_view()),
    path('api/committees', aviews.ListCreateCommittees.as_view()),
    path('api/search', dviews.SearchDocuments.as_view()),
    path('api/auth-token', obtain_auth_token),
    path('docs/', include('rest_framework_docs.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

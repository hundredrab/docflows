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
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('processes', pviews.ListProcesses.as_view()),
    path('documents', dviews.ListDocuments),
    path('documents/permissions', dviews.ViewableDocuments.as_view()),
    path('documents/create', dviews.DocumentCreate.as_view()),
    path('documents/details/<int:pk>', dviews.DocumentDetails.as_view()),
    path('committees', aviews.ListCreateCommittees.as_view()),
    path('committees/<int:pk>/add', aviews.add_member),
    path('committees/<int:pk>', aviews.RolesView.as_view()),
    path('committees/<int:pk>/details', aviews.CommitteeDetails.as_view()),
    path('users/all', aviews.UserListView.as_view()),
    path('roles/all', aviews.RoleListView.as_view()),
    path('search', dviews.SearchDocuments.as_view()),
    path('profile/<str:username>', aviews.ProfileDetailsView.as_view()),
#    path('auth-token', obtain_auth_token),
    path('token', aviews.AdditionalTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('docs/', include('rest_framework_docs.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

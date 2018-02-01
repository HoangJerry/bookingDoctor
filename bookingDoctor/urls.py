"""bookingDoctor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from api import urls as api_urls
import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^api/', include(api_urls)),
    url(r'^$', views.home, name='home'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^singup/$', views.signup, name='signup'),
    url(r'^profile/(?P<pk>[0-9]+)/$', login_required(views.ProfileUser.as_view()), name='profile'),
    url(r'^appointment/book/$', views.AppointmentBook.as_view(), name='appointment-book'),
    url(r'^appointment/(?P<pk>[0-9]+)/$', views.AppointmentDetail.as_view(), name='appointment-detail'),
    url(r'^patients/$', views.PatientListView.as_view(), name='patients'),
    url(r'^appointment/me/$', views.AppointmentMe.as_view(), name='appointment-me'),
    url(r'^appointment/change/$', views.AppointmentUpdate.as_view(), name='appointment-update'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL.replace(settings.SITE_URL, ''), document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL.replace(settings.SITE_URL, ''), document_root=settings.MEDIA_ROOT)

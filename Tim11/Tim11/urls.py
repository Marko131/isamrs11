"""Tim11 URL Configuration

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
from django.views.generic import TemplateView
from Users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('admin/', admin.site.urls),
    path('', include('FlightService.urls')),
    path('hotels/', include('HotelService.urls')),
    path('rentacar/', include('RentACarService.urls')),

    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='Users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='airlines_home.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('friends/', user_views.FriendList.as_view(), name='friends'),
    path('send_request/<int:user_id>', user_views.send_request, name='send_request'),
    path('ignore_request/<int:request_id>', user_views.ignore_request, name='ignore_request'),
    path('accept_request/<int:request_id>', user_views.accept_request, name='accept_request'),
    path('remove_friend/<int:user_id>', user_views.remove_friend, name='remove_friend'),

    path('my_reservations', user_views.my_reservations, name='my_reservations'),
    path('cancel_resevation/<int:reservation_id>', user_views.cancel_resevation, name='cancel_resevation'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
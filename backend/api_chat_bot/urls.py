"""
URL configuration for seikai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.conf import settings
from django.shortcuts import redirect
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.conf.urls.static import static
from django.contrib import admin

swagger_url = []

if settings.DISPLAY_SWAGGER:
    swagger_url = [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        # path("", lambda request: redirect("api/", permanent=True)),
        path(
            "api/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
        ),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]


urlpatterns = (
    swagger_url
    + [
        path("api/", include("accounts.urls")),
        path("api/", include("chat_service.urls")),
        path("api/restaurant-booking/", include("restaurant_booking.urls")),
        path("api/order-bot/", include("order_bot.urls")),
        path("admin/", admin.site.urls),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

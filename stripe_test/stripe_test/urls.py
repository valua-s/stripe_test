"""
URL configuration for stripe_test project.

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

from core.views import index, sucsess, cancel
from api.views import get_item, create_checkout_session, get_order, payment_window, create_intent

urlpatterns = [
    path('admin/', admin.site.urls),
    path('item/<int:item_id>', get_item),
    path('buy/<int:item_id>', create_checkout_session),
    path('order/<str:order_unicode>', get_order),
    path('payment/<str:order_unicode>', payment_window),
    path('create-payment-intent/<str:order_unicode>', create_intent),
    path('success', sucsess),
    path('cancel', cancel),
    path('', index)
]

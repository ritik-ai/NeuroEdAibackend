"""
URL configuration for Education project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from EducationAi.views import google_gemani_api, anthropicdata
from google_drive.views import google_drive_files
from payments.views import create_paypal_product, create_paypal_subscription, paypal_webhook
from EducationAi.views import save_data_user
from signup.views import send_verification_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Google-gemani-api', google_gemani_api, name='Gemini'),
    path('google-drive-files/', google_drive_files, name="google-drive-files"),
    path('create_paypal_product', create_paypal_product,
         name='create_paypal_product'),
    path('create_paypal_subscription', create_paypal_subscription,
         name='create_paypal_subscription'),
    path('anthropic_crude', anthropicdata, name='anthropic'),
    path('api/create-user/', save_data_user, name='create-user'),
    path('verification-email/',send_verification_email,name='send_verification_email')
    # path('paypal_webhook/',paypal_webhook, name='paypal_webhook'),
    #  path('subscription_details/<str:subscription_id>/',get_subscription_details, name='get_subscription_details'),

]

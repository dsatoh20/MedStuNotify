from .views import PrivacyPolicyView, AboutView, ContactView, redirect_to_about
from django.urls import path

urlpatterns = [
    path('privacy_policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('', redirect_to_about, name='home'),  # ルートURLを/about/にリダイレクト
]
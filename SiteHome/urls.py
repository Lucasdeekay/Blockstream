from django.urls import path, include
from rest_framework import routers

from SiteHome import views
from UserAccount.views import admin_manager, approve, decline, update_profit

app_name = 'SiteHome'

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("faq", views.faq, name="faq"),
    path("contact", views.contact, name="contact"),
    path("privacy", views.privacy, name="privacy"),
    path("terms-and-conditions", views.legal_doc, name="legal_doc"),
    path('admin-manager', admin_manager, name='admin_manager'),
    path('admin-manager/approve-<str:mode>-<int:id>', approve, name='approve'),
    path('admin-manager/decline-<str:mode>-<int:id>', decline, name='decline'),
    path('admin-manager/update-profit-<int:id>', update_profit, name='update_profit'),
]
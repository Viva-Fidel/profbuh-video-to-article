from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('save-video/', views.save_video, name='save_video'),
    ]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
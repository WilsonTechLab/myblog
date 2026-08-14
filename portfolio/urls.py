from django.urls import path
from django.views.generic.base import RedirectView
from .views import*


from portfolio import views

urlpatterns = [
      path('', views.home, name='home'),
      #path('post/<slug:slug>/', post_detail, name='post_detail'),
      path('about', views.about, name='about'),
      path('contact', views.contact_page, name='contact_page'),
    path('api/contact', views.contact_api, name='contact_api'),
      #path('portfolio', views.portfolio_page, name='portfolio_page'),
      path('services', views.services_page, name='services_page'),
      #path('resume', views.resume, name='resume'),
]
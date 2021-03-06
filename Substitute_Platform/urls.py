from django.conf.urls import url

from . import views

app_name = "Substitute_Platform"

urlpatterns = [
    url(r'^details/(?P<product_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^$', views.index, name='index'),
    url(r'^listing/$', views.listing_substitutes, name='substitutes_list'),
    url(r'^account/$', views.account, name='account'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^authentication/$', views.connect, name='authentication'),
    url(r'^disconnect/$', views.disconnect, name='disconnection'),
    url(r'^legal/$', views.legal_notice, name='legal'),
    url(r'^my_substitutes/$', views.my_substitutes, name="substitutes")
]

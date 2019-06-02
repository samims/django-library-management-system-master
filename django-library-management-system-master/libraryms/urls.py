from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('accounts.urls')),
    url(r'^', include('library.urls')),
    path('management/', include('management.urls'))
]

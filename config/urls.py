"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# Названия админки
admin.site.site_header = '1С Академия'
admin.site.site_title = '1С Академия'
admin.site.index_title = 'Управление системой'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('references.urls')),  
    path('documents/', include('documents.urls')),
    path('warehouse/', include('warehouse.urls')),
    path('accounting/', include('accounting.urls')),
    path('reports/', include('reports.urls')),
    path('users/', include('users.urls')),
]

# ПРИНУДИТЕЛЬНОЕ ЧТЕНИЕ ИЗ КОРНЕВОЙ ПАПКИ STATIC
urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'static'}),
]
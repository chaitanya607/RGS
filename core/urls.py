from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# app_name = 'core'
# urlpatterns = [
#     path('', include(router.urls)),
# ]


# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload_image/', views.upload_image, name='upload_image'),
]

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, preview_document

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('documents/<int:pk>/preview/', preview_document, name='preview_document'),
]

urlpatterns += router.urls

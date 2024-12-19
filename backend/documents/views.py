from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(uploaded_by=self.request.user, active=True)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user, active=True)

    def update(self, request, *args, **kwargs):
        document = self.get_object()
        if document.uploaded_by != request.user:
            return Response({"detail": "You cannot edit this document."}, status=403)

        # No intentes actualizar el campo file si no está presente en la solicitud
        if 'file' not in request.data:
            request.data._mutable = True  # Solo necesario si estás usando QueryDict
            request.data.pop('file', None)  # Elimina el campo file de la solicitud
            request.data._mutable = False

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        document = self.get_object()
        if document.uploaded_by != request.user:
            return Response({"detail": "You cannot delete this document."}, status=403)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='assigned-to-me')
    def assigned_to_me(self, request):
        """
        Endpoint personalizado para obtener los documentos asignados al usuario en sesión.
        """
        user_email = request.user.email
        documents = Document.objects.filter(approved_by=user_email, active=True)
        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate(self, request, pk=None):
        """
        Endpoint para desactivar un documento.
        """
        document = self.get_object()
        if document.uploaded_by != request.user:
            return Response({"detail": "You are not authorized to deactivate this document."}, status=status.HTTP_403_FORBIDDEN)

        document.deactivate()
        return Response({"message": "Document deactivate successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='approve', url_name='approve')
    def approve_document(self, request, pk=None):
        """
        Endpoint para aprobar un documento.
        """
        document = get_object_or_404(Document, pk=pk, approved_by=request.user.email)
        document.status = Document.Status.APPROVED
        document.save()
        return Response({"message": "Document approved successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='reject', url_name='reject')
    def reject_document(self, request, pk=None):
        """
        Endpoint para rechazar un documento.
        """
        document = get_object_or_404(Document, pk=pk, approved_by=request.user.email)
        document.status = Document.Status.REJECTED
        document.save()
        return Response({"message": "Document rejected successfully."}, status=status.HTTP_200_OK)


def preview_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return FileResponse(document.file.open(), content_type='application/pdf')


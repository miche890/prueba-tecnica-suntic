from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'created_at', 'updated_at']

        def _init_(self, *args, **kwargs):
            # Llama al constructor de la clase padre
            super()._init_(*args, **kwargs)
            # Si estamos realizando una actualización (PATCH o PUT), el campo file será opcional
            if self.instance and self.context['request'].method in ['PATCH', 'PUT']:
                self.fields['file'].required = False



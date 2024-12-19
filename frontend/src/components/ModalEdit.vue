<script>
import { ref, watchEffect } from 'vue'

export default {
  name: 'EditDocumentModal',
  props: {
    isOpen: {
      type: Boolean,
      required: true
    },
    document: {
      type: Object,
      required: true
    }
  },
  emits: ['close', 'save'],
  setup (props, { emit }) {
    // Variables reactivas para el formulario
    const title = ref('')
    const description = ref('')
    const approver = ref('')
    const file = ref(null)

    const isSaving = ref(false)

    // Usamos watchEffect para actualizar los campos si el documento cambia
    watchEffect(() => {
      if (props.document) {
        title.value = props.document.title || ''
        description.value = props.document.description || ''
        approver.value = props.document.approved_by || ''
        file.value = null // Reiniciar el archivo si es necesario
      }
    })

    const saveDocument = async () => {
      isSaving.value = true
      const formData = new FormData()
      formData.append('title', title.value)
      formData.append('description', description.value)
      formData.append('approved_by', approver.value)

      if (file.value) {
        formData.append('file', file.value)
      }

      try {
        const response = await fetch(`http://localhost:8000/api/documents/${props.document.id}/`, {
          method: 'PATCH',
          credentials: 'include',
          body: formData
        })

        if (!response.ok) {
          throw new Error('Error al guardar los cambios')
        }

        const updatedDocument = await response.json()
        emit('save', updatedDocument)
        emit('close')
      } catch (error) {
        alert('Error al guardar el documento')
      } finally {
        isSaving.value = false
      }
    }

    const closeModal = () => {
      emit('close')
    }

    return {
      title,
      description,
      approver,
      file,
      isSaving,
      saveDocument,
      closeModal
    }
  }
}
</script>

<template>
  <div v-if="isOpen" class="modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Editar Documento: {{ title }}</h5>
          <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveDocument" class="needs-validation" id="form-edit-document">
            <div class="form-group">
              <label for="document-title">Título</label>
              <input
                v-model="title"
                type="text"
                class="form-control"
                id="document-title"
                placeholder="Ingrese el título del documento"
                required
              />
            </div>
            <div class="form-group">
              <label for="document-description">Descripción</label>
              <textarea
                v-model="description"
                class="form-control"
                id="document-description"
                placeholder="Ingrese una descripción"
                required
              ></textarea>
            </div>
            <div class="form-group">
              <label for="document-approver">Aprobador</label>
              <input
                v-model="approver"
                type="email"
                class="form-control"
                id="document-approver"
                placeholder="Ingrese el nombre del aprobador"
                required
              />
            </div>
            <div class="form-group">
              <label for="document-file">Nuevo Archivo (opcional)</label>
              <input
                type="file"
                class="form-control-file"
                id="document-file"
                accept="application/pdf"
                @change="file = $event.target.files[0]"
              />
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">Cerrar</button>
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="isSaving"
            form="form-edit-document"
          >
            <span v-if="isSaving">Guardando...</span>
            <span v-else>Guardar</span>
          </button>
        </div>
      </div>
    </div>
    <div class="modal-backdrop z-n1 fade show"></div>
  </div>
</template>

<style scoped>
.modal {
  display: block;
}
</style>

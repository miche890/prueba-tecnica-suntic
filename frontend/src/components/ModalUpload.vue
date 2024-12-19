<script>
export default {
  name: 'UploadDocumentModal',
  data () {
    return {
      title: '',
      description: '',
      approver: '',
      file: null
    }
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true
    }
  },
  emits: ['close', 'save'],
  methods: {
    save () {
      this.$emit('save')
    },

    close () {
      this.$emit('close')
    },

    handleFileUpload (event) {
      this.file = event.target.files[0]
    },

    async uploadDocument () {
      const formData = new FormData()
      formData.append('title', this.title)
      formData.append('description', this.description)
      formData.append('approved_by', this.approver)
      formData.append('file', this.file)

      try {
        const response = await fetch('http://localhost:8000/api/documents/', {
          method: 'POST',
          credentials: 'include',
          body: formData
        })

        if (!response.ok) {
          throw new Error('Error al subir el documento')
        }

        alert('Documento subido exitosamente')
        this.$emit('reloadDocuments')
        this.close()
      } catch (error) {
        alert(error.message || 'Error al subir el documento')
      }
    }
  }
}
</script>

<template>
  <div v-if="isOpen" class="modal fade show d-block" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Subir nuevo documento</h5>
          <button type="button" class="btn-close" @click="close" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="uploadDocument" class="needs-validation" novalidate>
            <div class="mb-3">
              <label for="title" class="form-label">Título</label>
              <input type="text" id="title" v-model="title" class="form-control" placeholder="Ingrese el título"
                required />
            </div>
            <div class="mb-3">
              <label for="description" class="form-label">Descripción</label>
              <textarea id="description" v-model="description" class="form-control" placeholder="Ingrese la descripción"
                rows="3" required></textarea>
            </div>
            <div class="mb-3">
              <label for="approver" class="form-label">Correo del aprobador</label>
              <input type="email" id="approver" v-model="approver" class="form-control"
                placeholder="Ingrese el correo del aprobador" required />
            </div>
            <div class="mb-3">
              <label for="file" class="form-label">Archivo PDF</label>
              <input type="file" id="file" @change="handleFileUpload" class="form-control" accept="application/pdf"
                required />
            </div>
            <button type="submit" class="btn btn-success w-100">Subir</button>
          </form>
        </div>
      </div>
    </div>
    <div class="modal-backdrop z-n1 fade show"></div>
  </div>
</template>

<style scoped></style>

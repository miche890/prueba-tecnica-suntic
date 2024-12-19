<script>
import ModalEdit from '@/components/ModalEdit'

export default {
  name: 'ListMyDocuments',
  components: {
    ModalEdit
  },
  data () {
    return {
      documents: [],
      isLoading: false,
      error: null,
      selectedDocument: null,
      isModalOpen: false
    }
  },
  methods: {
    async fetchDocuments () {
      this.isLoading = true
      try {
        const response = await fetch('http://localhost:8000/api/documents/', {
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        })
        if (!response.ok) {
          throw new Error('Error al cargar los documentos')
        }
        this.documents = await response.json()
      } catch (err) {
        this.error = err.message
      } finally {
        this.isLoading = false
      }
    },
    deactivateDocument: async function (id) {
      try {
        const response = await fetch(`http://localhost:8000/api/documents/${id}/deactivate/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        })
        if (!response.ok) {
          throw new Error('Error al desactivar el documento')
        }
        this.documents = this.documents.filter(doc => doc.id !== id)
        alert('Documento desactivado con éxito.')
      } catch (err) {
        alert(err.message)
      }
    },
    openEditModal (document) {
      this.selectedDocument = document
      this.isModalOpen = true
    },
    closeModal () {
      this.isModalOpen = false
      this.selectedDocument = null
    },
    updateDocument (updatedDocument) {
      const index = this.documents.findIndex(doc => doc.id === updatedDocument.id)
      if (index !== -1) {
        this.documents[index] = updatedDocument
      }
    }
  },
  mounted () {
    this.fetchDocuments()
  }

}
</script>

<template>
  <div>
    <h2 class="mt-3">Mis Documentos</h2>

    <div v-if="isLoading" class="text-center">
      <p>Cargando documentos...</p>
    </div>

    <div v-if="error" class="text-danger">
      <p>{{ error }}</p>
    </div>

    <table v-if="documents.length > 0" class="table table-striped mt-3">
      <thead>
        <tr>
          <th>#</th>
          <th>Id</th>
          <th>Nombre</th>
          <th>Ultima modificación</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(document, index) in documents" :key="document.id">
          <td>{{ index + 1 }}</td>
          <td>{{ document.id }}</td>
          <td>{{ document.title }}</td>
          <td>{{ new Date(document.updated_at).toLocaleDateString() }}</td>
          <td class="d-flex">
            <a :href="`http://localhost:8000/api/documents/${document.id}/preview/`" target="_blank"
              class="btn btn-outline-primary btn-sm me-1">
              Ver
            </a>
            <div v-if="document.status === 'PENDING'">

              <button @click="openEditModal(document)" class="btn btn-outline-warning btn-sm me-1">
                Editar
              </button>

              <button @click="deactivateDocument(document.id)" class="btn btn-outline-danger btn-sm me-1">
                Borrar
              </button>

            </div>

            <div v-if="document.status !== 'PENDING'">
              <small class="text-success" v-if="document.status === 'APPROVED'">Documento Aprobado</small>
              <small class="text-danger" v-if="document.status === 'REJECTED'">Documento Rechazado</small>
            </div>

          </td>
        </tr>
      </tbody>
    </table>

    <div v-else class="text-center">
      <p>No has subido documentos.</p>
    </div>
  </div>

  <!-- Modal de edición -->
  <ModalEdit :isOpen="isModalOpen" :document="selectedDocument" @close="closeModal" @save="updateDocument" />
</template>

<style scoped>
.table {
  width: 100%;
}
</style>

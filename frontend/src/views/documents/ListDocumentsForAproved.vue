<script>
import { useStore } from 'vuex'

export default {
  name: 'ListMyDocuments',
  data () {
    return {
      documents: [],
      isLoading: false,
      error: null,
      selectedDocument: null,
      isModalOpen: false,
      store: useStore()
    }
  },
  methods: {
    async fetchDocuments () {
      this.isLoading = true
      try {
        const response = await fetch('http://localhost:8000/api/documents/assigned-to-me/', {
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        })
        if (!response.ok) {
          throw new Error('Error al cargar los documentos')
        }
        this.documents = await response.json()
        this.store.dispatch('setAuth', true)
      } catch (err) {
        this.error = err.message
        this.store.dispatch('setAuth', false)
      } finally {
        this.isLoading = false
      }
    },

    async approveDocument (documentId) {
      try {
        const response = await fetch(`http://localhost:8000/api/documents/${documentId}/approve/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        })
        if (!response.ok) {
          throw new Error('Error al aprobar el documento')
        }
        alert('Documento aprobado exitosamente')
        this.fetchDocuments() // Actualiza la lista después de la acción
      } catch (err) {
        alert(err.message)
      }
    },

    async rejectDocument (documentId) {
      try {
        const response = await fetch(`http://localhost:8000/api/documents/${documentId}/reject/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        })
        if (!response.ok) {
          throw new Error('Error al rechazar el documento')
        }
        alert('Documento rechazado exitosamente')
        this.fetchDocuments() // Actualiza la lista después de la acción
      } catch (err) {
        alert(err.message)
      }
    }
  },
  mounted () {
    this.fetchDocuments()
  }
}
</script>

<template>
  <div class="container mt-5">
    <h2 class="mt-3">Documentos asignados</h2>

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
              <button @click="approveDocument(document.id)" class="btn btn-outline-success btn-sm me-1">
                Aprobar
              </button>

              <button @click="rejectDocument(document.id)" class="btn btn-outline-danger btn-sm me-1">
                Rechazar
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
      <p>No te han asignado documentos.</p>
    </div>
  </div>

</template>

<style scoped>
.table {
  width: 100%;
}
</style>

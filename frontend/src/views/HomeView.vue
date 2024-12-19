<script>
import { onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import ModalUpload from '@/components/ModalUpload.vue'
import ListMyDocuments from '@/views/documents/ListMyDocuments.vue'

export default {
  name: 'HomeView',
  components: {
    ModalUpload,
    ListMyDocuments
  },
  setup () {
    const message = ref('No has iniciado sesion')
    const isAuth = ref(false)
    const isModalOpen = ref(false)
    const store = useStore()

    const openModal = () => {
      isModalOpen.value = true
    }

    onMounted(async () => {
      await fetch('http://localhost:8000/api/user', {
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
      }).then(async (response) => {
        const content = await response.json()
        if (content.email) {
          message.value = `Hola, ${content.email}`
          await store.dispatch('setAuth', true)
          isAuth.value = true
        } else {
          await store.dispatch('setAuth', false)
          message.value = 'No has iniciado sesion'
          isAuth.value = false
        }
      })
    })

    return {
      message,
      isAuth,
      isModalOpen,
      openModal
    }
  },
  methods: {
    closeModal () {
      this.isModalOpen = false
    },

    reloadDocuments () {
      // Obtener la referencia al componente ListMyDocuments
      const listMyDocuments = this.$refs.listMyDocuments

      // Llamar a la función de recarga de documentos
      if (listMyDocuments) {
        listMyDocuments.fetchDocuments()
      }
    }
  }
}

</script>

<template>
  <div class="container mt-5">
    <div>
      <button v-if="isAuth" class="btn btn-success" @click="openModal">Subir Documento</button>
      <ListMyDocuments ref="listMyDocuments" />
    </div>
    <!-- Modal para subir un archivo -->
    <ModalUpload :isOpen="isModalOpen" @close="closeModal" @save="uploadDocument" @reloadDocuments="reloadDocuments" />
  </div>
</template>

<style scoped></style>

<script lang="ts">
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
export default {
  name: 'NavBar',
  setup () {
    const store = useStore()
    const router = useRouter()
    const auth = computed(() => store.state.authenticated)

    const onLogout = async () => {
      await fetch('http://localhost:8000/api/logout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
      }).then(async (response) => {
        response.json()
        await store.dispatch('setAuth', false)
        await router.push('/login')
      })
    }

    return {
      auth,
      onLogout
    }
  }
}

</script>

<template>
  <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4" aria-label="Offcanvas navbar large">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">Home</router-link>
      <div>
        <ul class="navbar-nav me-auto mb-2 mb-md-0" v-if="!auth">
          <li class="nav-item">
            <router-link to="login/" class="nav-link">Iniciar sesion</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/register" class="nav-link">Registrarse</router-link>
          </li>
        </ul>

        <ul class="navbar-nav me-auto mb-2 mb-md-0" v-if="auth">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Mis documentos</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/assigned-to-me" class="nav-link">Documentos asignados</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/profile" class="nav-link">Perfil</router-link>
          </li>
          <li class="nav-item">
            <a href="#" class="nav-link" @click="onLogout">Cerrar sesion</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.border-dashed { --bs-border-style: dashed; }
</style>

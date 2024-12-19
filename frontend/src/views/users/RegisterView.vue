<script lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'RegisterView',
  setup () {
    const data = reactive({
      name: '',
      email: '',
      password: ''
    })

    const router = useRouter()

    const onSubmit = async () => {
      await fetch('http://localhost:8000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })

      await router.push('/login')
    }

    return {
      data,
      onSubmit
    }
  }
}
</script>

<template>
  <form @submit.prevent="onSubmit" class="form-signin w-100 m-auto">
    <h1 class="h3 mb-3 fw-normal">Por favor, registrese</h1>

    <div class="form-floating">
      <input type="text" v-model="data.name" class="form-control" id="floatingInputName" placeholder="Ingrese aqui su nombre">
      <label for="floatingInputName">Nombre</label>
    </div>
    <div class="form-floating">
      <input type="email" v-model="data.email" class="form-control" id="floatingInputEmail" placeholder="name@example.com">
      <label for="floatingInputEmail">Correo Electronico</label>
    </div>
    <div class="form-floating">
      <input type="password" v-model="data.password" class="form-control" id="floatingPassword" placeholder="Password">
      <label for="floatingPassword">Contraseña</label>
    </div>
    <button class="btn btn-primary w-100 py-2" type="submit">Enviar</button>
  </form>
</template>

<style scoped>
.form-signin {
  max-width: 330px;
  padding: 1rem;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>

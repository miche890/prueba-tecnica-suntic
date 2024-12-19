<script>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'LoginView',
  setup () {
    const data = reactive({
      email: '',
      password: '',
      token: ''
    })

    const require2FA = ref(false)
    const router = useRouter()
    const errorMessage = ref('')

    const onSubmit = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(data)
        })

        if (!response.ok) {
          const result = await response.json()
          if (result.detail === '2FA Token is required') {
            require2FA.value = true // Mostrar el campo de 2FA
            errorMessage.value = 'Por favor ingrese el token de 2FA.'
          } else {
            throw new Error(result.detail || 'Error en el inicio de sesión')
          }
        } else {
          await router.push('/')
        }
      } catch (e) {
        errorMessage.value = e.message
      }
    }

    return {
      data,
      require2FA,
      errorMessage,
      onSubmit
    }
  }
}

</script>

<template>
  <form @submit.prevent="onSubmit" class="form-signin w-100 m-auto">
    <h1 class="h3 mb-3 fw-normal">Por favor, inicie sesion</h1>

    <div class="form-floating">
      <input type="email" v-model="data.email" class="form-control" id="floatingInput" placeholder="name@example.com">
      <label for="floatingInput">Correo Electronico</label>
    </div>

    <div class="form-floating">
      <input type="password" v-model="data.password" class="form-control" id="floatingPassword" placeholder="Password">
      <label for="floatingPassword">Contraseña</label>
    </div>

    <!-- Campo adicional para el token de 2FA -->
    <div v-if="require2FA" class="form-floating">
      <input type="text" v-model="data.token" class="form-control" id="floatingToken" placeholder="2FA Token" required>
      <label for="floatingToken">Código 2FA</label>
    </div>

    <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
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

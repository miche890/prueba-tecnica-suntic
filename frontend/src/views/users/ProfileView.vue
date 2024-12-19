<script>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { useStore } from 'vuex'

export default {
  name: 'ProfileView',

  setup () {
    const qrUrl = ref(null)
    const code = ref('')
    const verificationResult = ref('')
    const mfaEnabled = ref(false)
    const router = useRouter()

    const message = ref('No has iniciado sesion')
    const store = useStore()

    onMounted(async () => {
      await fetch('http://localhost:8000/api/user', {
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
      }).then(async (response) => {
        const content = await response.json()
        if (content.email) {
          message.value = `Hola, ${content.email}`
          mfaEnabled.value = content.mfa_enabled
          await store.dispatch('setAuth', true)
        } else {
          await store.dispatch('setAuth', false)
          message.value = 'No has iniciado sesion'
        }
      })
    })

    const enable2fa = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/enable2fa', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        })
        if (!response.ok) {
          throw new Error('Error al habilitar 2FA')
        }

        const data = await response.json()
        qrUrl.value = data.qr_url
      } catch (e) {
        console.error(e.message)
      }
    }

    const disable2fa = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/disable2fa', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        })
        if (!response.ok) {
          throw new Error('Error al deshabilitar 2FA')
        }

        mfaEnabled.value = false
      } catch (e) {
        console.error(e.message)
      }
    }

    const verify2fa = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/verify2fa', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({ code: code.value })
        })

        const data = await response.json()
        if (response.ok) {
          verificationResult.value = 'Código verificado correctamente'
          await router.push('/')
        } else {
          verificationResult.value = data.detail || 'Error al verificar el código'
        }
      } catch (error) {
        console.error('Error:', error)
        verificationResult.value = 'Hubo un error en la solicitud'
      }
    }

    return {
      enable2fa,
      verify2fa,
      qrUrl,
      code,
      verificationResult,
      mfaEnabled,
      disable2fa
    }
  }
}

</script>

<template>
  <div class="container my-5">
    <div class="p-5 text-center bg-body-tertiary rounded-3" v-if="!mfaEnabled">
      <h1 class="text-body-emphasis">Activa la verificacion en 2 pasos</h1>
      <button @click="enable2fa" class="btn btn-primary px-5 mb-5" type="button">
        Generar QR
      </button>
      <div v-if="qrUrl" class="mt-3">
        <p>Escanea este código QR con la aplicación de Google Authentication:</p>

        <img :src="qrUrl" alt="QR Code" id="qr-code" />

        <div class="container my-5">
          <div class="p-5 text-center bg-body-tertiary rounded-3">
            <h1 class="text-body-emphasis">Verificar Código de 2FA</h1>
            <input v-model="code" class="form-control my-3" type="text" placeholder="Ingresa el código de la app" />
            <button @click="verify2fa" class="btn btn-success px-5 mb-5" type="button">
              Verificar
            </button>
            <p v-if="verificationResult">{{ verificationResult }}</p>
          </div>
        </div>

      </div>
    </div>
    <div class="p-5 text-center bg-body-tertiary rounded-3" v-if="mfaEnabled">
      <h1 class="text-body-emphasis">Tiene la verificacion en 2 pasos activada</h1>
      <button @click="disable2fa" class="btn btn-danger px-5 mb-5" type="button">
        Deshabilitar
      </button>
    </div>
  </div>
</template>

<style scoped>
#qr-code {
  height: 200px;
  width: auto;
}
</style>

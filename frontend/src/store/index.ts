import { Commit, createStore } from 'vuex'

export default createStore({
  state: {
    authenticated: false
  },
  getters: {
  },
  mutations: {
    // eslint-disable-next-line no-return-assign
    SET_AUTH: (state: { authenticated: boolean }, auth: boolean) => state.authenticated = auth
  },
  actions: {
    setAuth: ({ commit }: {commit: Commit}, auth: boolean) => commit('SET_AUTH', auth)
  },
  modules: {
  }
})

export const state = () => ({
  user: null,
  token: null
})

export const mutations = {
  addUser (state, user) {
    state.user = user
  },
  removeUser (state) {
    state.user = null
  },
  addToken (state, token) {
    state.token = token
  },
  removeToken (state) {
    state.token = null
  }
}


export default async function (context) {
  // If the user is not authenticated
  if (!context.store.state.token) {
    context.$http.setToken(null)
    context.redirect('/login')
  }

  context.$http.setToken(context.store.state.token, 'Bearer')

  let request = { ok: false }
  try {
    request = await context.$http.get('/users-api/users')
  } catch (e) {
    console.log(e)
  }

  if (!request.ok) {
    context.$http.setToken(context.store.state.token, null)
    context.store.commit('removeUser')
    context.store.commit('removeToken')
    context.redirect('/login')
  }
}

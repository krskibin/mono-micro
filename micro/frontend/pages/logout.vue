<template>
  <div>
    <h1>Logging out ....</h1>
  </div>
</template>

<script>
export default {
  computed: {
    isBrowser () {
      if (process) {
        return process.browser
      }
      return null
    }
  },
  watch: {
    isBrowser: {
      async handler (val) {
        if (val) {
          const response = await this.$http.post('/users-api/logout')
          if (!response.success) {
            this.$router.push('/tasks')
            this.$notify({
              title: 'Success',
              message: 'Logged out',
              type: 'success'
            })
            return
          }

          localStorage.removeItem('mt-todo-user')
          localStorage.removeItem('mt-todo-token')

          this.$store.commit('removeToken')
          this.$store.commit('removeUser')

          window.location.reload()
        }
      },
      immediate: true,
      deep: true
    }
  },
  middleware: 'authenticated'
}
</script>

<style scoped>

</style>

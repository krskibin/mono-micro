<template>
  <el-container>
    <el-header class="header">
      <div class="logo" style="display: flex; align-items: center;">
        <span style="font-size: 1.5rem; font-weight: bold">MtTodo</span> &nbsp;  <span style="font-size: 0.8rem">(micro)</span>
      </div>
      <div class="links">
        <nuxt-link v-if="!getUsername" to="/login">
          Login
        </nuxt-link>
        <div v-else>
          <nuxt-link to="/tasks">
            {{ getUsername }} tasks
          </nuxt-link>
          <nuxt-link to="/logout">
            logout
          </nuxt-link>
        </div>
      </div>
    </el-header>
    <el-main class="main">
      <div class="main-content">
        <nuxt />
      </div>
    </el-main>
    <el-footer class="footer">
      <p>MtTodo Microservices 2020</p>
      <p>Example Microservices app for Master Thesis purposes</p>
    </el-footer>
  </el-container>
</template>

<script>
export default {
  data () {
    return {
      user: null
    }
  },
  computed: {
    getUsername () {
      if (this.$store.state.user) {
        return this.$store.state.user.username
      }
      return null
    }
  }
}
</script>

<style>
@font-face {
    font-family: 'Pacifico';
    src: url('~assets/Pacifico-Regular.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}

html {
  font-family: 'Courier';
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
  height: 100vh;
}

*,
*:before,
*:after {
  box-sizing: border-box;
  margin: 0;
}

body {
  height: 100vh;
}
#__nuxt,
#__layout {
  height: 100vh;
}

.el-container {
  height: 100%;
}

.header {
  border-bottom: 1px solid #333;
}

.footer p {
  font-size: 0.7rem;
}

.el-header, .el-footer {
  color: #333;
  text-align: center;
  display: flex;
  align-items: center;
}

.el-header {
  display: flex;
  justify-content: space-between;
}

.el-footer {
  justify-content: center;
  flex-direction: column;
}

.el-main {
  color: #333;
  display: flex;
  justify-content: center;
  line-height: 1.5rem;
}

body > .el-container {
  margin-bottom: 40px;
}

a:hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>

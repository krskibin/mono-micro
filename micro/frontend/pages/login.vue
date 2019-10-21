<template>
  <div class="login">
    <h1 style="margin: 3rem;">
      Login user
    </h1>
    <el-form
      ref="ruleForm"
      :model="ruleForm"
      status-icon
      :rules="rules"
      label-width="120px"
      class="demo-ruleForm"
    >
      <el-form-item label="Username" prop="username">
        <el-input v-model.number="ruleForm.username" />
      </el-form-item>
      <el-form-item label="Password" prop="password">
        <el-input v-model="ruleForm.password" type="password" autocomplete="off" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">
          Submit
        </el-button>
        <el-button @click="resetForm('ruleForm')">
          Reset
        </el-button>
      </el-form-item>
    </el-form>
    <span>or <nuxt-link to="/register">register</nuxt-link> new user!</span>
  </div>
</template>

<script>
export default {
  data () {
    return {
      ruleForm: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: 'Please input username', trigger: 'blur' },
          { min: 3, max: 35, message: 'Length should be 3 to 5', trigger: 'blur' }
        ],
        password: [
          { required: true, message: 'Please input password', trigger: 'blur' },
          { min: 3, max: 35, message: 'Length should be 3 to 5', trigger: 'blur' }
        ]
      }
    }
  },
  mounted () {
    if (window) {
      const token = localStorage.getItem('mt-todo-token') || null
      const user = JSON.parse(localStorage.getItem('mt-todo-user')) || null
      if (token && user) {
        this.$store.commit('addToken', token)
        this.$store.commit('addUser', user)
        this.$router.push('tasks')
      }
    }
  },
  methods: {
    submitForm (formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          const req = await this.$http.$post('/users-api/login', this.ruleForm)
          if (window) {
            const user = JSON.stringify(req.user)
            localStorage.setItem('mt-todo-token', req.authToken)
            localStorage.setItem('mt-todo-user', user)

            this.$store.commit('addToken', req.authToken)
            this.$store.commit('addUser', req.user)

            this.$router.push('/tasks')
          }
        } else {
          this.$notify.error({
            title: 'Error',
            message: 'Login register user'
          })
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>

<style>
.login {
  width: 50vw;
}
</style>

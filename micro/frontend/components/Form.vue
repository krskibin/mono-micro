<template>
  <el-form ref="todoForm" :model="todoForm" :rules="rules" label-width="60px" class="demo-todoForm">
    <h3 style="margin-bottom: 1rem; margin-top: 2rem">
      Create new task
    </h3>
    <el-form-item label="Name" prop="name">
      <el-input v-model="todoForm.header" />
    </el-form-item>
    <el-form-item label="Body" prop="desc">
      <el-input v-model="todoForm.body" type="textarea" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('todoForm')">
        Create
      </el-button>
      <el-button @click="resetForm('todoForm')">
        Reset
      </el-button>
    </el-form-item>
  </el-form>
</template>
<script>
export default {
  data () {
    return {
      todoForm: {
        header: '',
        body: ''
      },
      rules: {
        header: [
          { required: true, message: 'Please input task header', trigger: 'blur' },
          { min: 3, max: 5, message: 'Length should be 3 to 5', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$http.post('/tasks-api/tasks', this.todoForm)
          this.resetForm('todoForm')
          this.$emit('created')
        } else {
          return false
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>

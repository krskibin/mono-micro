<template>
  <div v-if="$fetchState.pending">
    Fetching post #{{ $route.params.id }}...
  </div>
  <div v-else>
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
      <el-checkbox v-model="todoForm.isDone">
        is done?
      </el-checkbox>
      <el-form-item>
        <el-button type="primary" @click="submitForm('todoForm')">
          Update
        </el-button>
        <el-button @click="resetForm('todoForm')">
          Reset
        </el-button>
      </el-form-item>
    </el-form>

    <p>
      <n-link to="/tasks">
        Back to posts
      </n-link>
      or   <el-button type="danger" @click="deleteTask">
        Delete
      </el-button>
    </p>
  </div>
</template>

<script>
export default {
  async fetch () {
    const response = await this.$http.$get(`tasks-api/tasks/${this.$route.params.id}`)
    if (response.success) {
      this.task = response.task
      this.todoForm = {
        body: this.task.body,
        header: this.task.header,
        isDone: this.task.isDone
      }
    }
  },
  data () {
    return {
      task: {},
      todoForm: {
        body: '',
        header: '',
        isDone: false
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
          this.$http.put(`/tasks-api/tasks/${this.$route.params.id}`, this.todoForm)
          this.$notify({
            title: 'Success',
            message: 'Task updated',
            type: 'success'
          })
        } else {
          return false
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    deleteTask () {
      this.$http.delete(`/tasks-api/tasks/${this.$route.params.id}`)
      this.$notify({
        title: 'Success',
        message: 'Task updated',
        type: 'success'
      })
      this.$router.push('/tasks')
    }
  },
  middleware: 'authenticated'
}
</script>

<template>
  <div id="list" class="content">
    <div class="section">
      <div class="subsection">
        <h1>Todo</h1>
        <p>Awesome todo app</p>
      </div>
      <Form @created="refetchTasks" />
      <div>
        <p v-if="$fetchState.pending">
          Fetching posts...
        </p>
        <p v-else-if="$fetchState.error">
          Error while fetching posts: {{ $fetchState.error.message }}
        </p>
        <div v-else>
          <div class="filtering" style="margin-top: 1rem;">
            Filter tasks:
            <a :class="{'selected': selected==='all'}" @click.stop="query=null">show all</a>
            <a :class="{'selected': selected==='done'}" @click.stop="query='isDone=True'">only done</a>
            <a :class="{'selected': selected==='notdone'}" @click.stop="query='isDone=False'">only not done</a>
          </div>
          <div v-if="tasks.length===0">
            <h1>No tasks found</h1>
          </div>
          <div v-for="task of tasks" :key="task.id">
            <Task style="width: 100%;" :task="task" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Form from '@/components/Form'
import Task from '@/components/Task'

export default {
  components: { Task, Form },
  async fetch () {
    const request = await this.$http.$get('tasks-api/tasks')
    if (request.success) {
      this.tasks = request.tasks
    }
  },
  data () {
    return {
      tasks: [],
      query: null,
      selected: null
    }
  },
  watch: {
    async query (val) {
      let request
      if (!val) {
        this.selected = 'all'
        request = await this.$http.$get('tasks-api/tasks')
      } else {
        if (val === 'isDone=True') {
          this.selected = 'done'
        } else {
          this.selected = 'notdone'
        }
        request = await this.$http.$get(`tasks-api/tasks?${val}`)
      }

      if (request.success) {
        this.tasks = request.tasks
      }
    }
  },
  methods: {
    async refetchTasks () {
      const request = await this.$http.$get('tasks-api/tasks')
      if (request.success) {
        this.tasks = request.tasks
      }
    }
  },
  middleware: 'authenticated'
}
</script>

<style>
.subsection {
  margin-top: 2rem;
}
.el-card {
  margin: 1rem;
}
.selected {
  font-weight: bold;
  color: red;
}
</style>

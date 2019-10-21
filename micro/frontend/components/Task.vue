<template>
  <el-card class="box-card" shadow="never">
    <div slot="header" class="clearfix">
      <span>{{ task.header }}</span>
      <n-link :to="`/tasks/${task.id}`">
        Edit
      </n-link>
    </div>
    <div class="text item">
      {{ task.body }}
    </div>
    <div class="text item">
      is done {{ task.isDone }}
    </div>
  </el-card>
</template>

<script>
export default {
  props: {
    task: {
      type: Object,
      default: () => ({
        header: 'null',
        body: 'null',
        isDone: false
      })
    }
  }
}
</script>
<style>
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 480px;
  }
</style>

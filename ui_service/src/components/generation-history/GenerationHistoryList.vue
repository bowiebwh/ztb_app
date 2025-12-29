<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchGenerationHistory } from '@/lib/api'
import type { GenerationTask } from '@/lib/api'

const projectId = ref<string>('1')
const historyList = ref<GenerationTask[]>([])
const error = ref('')

const load = async () => {
  error.value = ''
  try {
    historyList.value = await fetchGenerationHistory(projectId.value)
  } catch (err) {
    console.error(err)
    error.value = '加载历史失败'
  }
}

onMounted(() => {
  projectId.value = new URLSearchParams(window.location.search).get('id') || '1'
  load()
})
</script>

<template>
  <div class="space-y-3">
    <h2 class="text-lg font-semibold">生成历史</h2>
    <div v-if="error" class="text-sm text-red-500">{{ error }}</div>
    <div v-else-if="historyList.length === 0" class="text-sm text-muted-foreground">暂无历史记录</div>
    <ul v-else class="space-y-2">
      <li v-for="item in historyList" :key="item.taskId" class="border rounded p-3">
        <div class="flex justify-between text-sm">
          <span>任务 ID: {{ item.taskId }}</span>
          <span>状态: {{ item.status }}</span>
        </div>
        <div class="text-xs text-muted-foreground mt-1">
          更新时间: {{ item.updateTime }}
        </div>
        <div class="text-xs text-muted-foreground">
          结果: <a v-if="item.resultUrl" :href="item.resultUrl" target="_blank" class="text-primary hover:underline">下载</a>
          <span v-else>暂无</span>
        </div>
      </li>
    </ul>
  </div>
</template>

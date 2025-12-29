<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchLatestGenerationTask } from '@/lib/api'
import type { GenerationTask } from '@/lib/api'

const projectId = ref<string>('1')
const task = ref<GenerationTask | null>(null)

onMounted(async () => {
  projectId.value = new URLSearchParams(window.location.search).get('id') || '1'
  try {
    task.value = await fetchLatestGenerationTask(projectId.value)
  } catch (err) {
    console.error(err)
  }
})
</script>

<template>
  <div class="bg-red-50 border border-red-200 rounded-lg p-6">
    <h2 class="text-lg font-semibold text-red-700">生成失败</h2>
    <p class="text-sm text-red-600 mt-2">
      任务状态：{{ task?.status || 'Unknown' }}
    </p>
    <p class="text-sm text-red-600 mt-1">
      错误信息：{{ task?.errorMessage || '无' }}
    </p>
  </div>
</template>

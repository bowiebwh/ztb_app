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
  <div class="bg-card border rounded-lg p-6 space-y-4">
    <h2 class="text-xl font-semibold">生成完成</h2>
    <p class="text-sm text-muted-foreground">
      项目 {{ projectId }} 的投标书已生成。
    </p>
    <div v-if="task?.resultUrl" class="flex items-center gap-3">
      <a :href="task.resultUrl" target="_blank" class="text-primary hover:underline">下载投标书</a>
    </div>
    <div v-else class="text-sm text-muted-foreground">暂无下载链接</div>
  </div>
</template>

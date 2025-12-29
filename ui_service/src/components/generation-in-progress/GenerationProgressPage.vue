<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchLatestGenerationTask } from '@/lib/api'
import type { GenerationTask } from '@/lib/api'
import GenerationStatus from '@/components/generate-download-step/GenerationStatus.vue'

const projectId = ref<string>('1')
const task = ref<GenerationTask | null>(null)
const isClient = ref(true)

const load = async () => {
  try {
    const res = await fetchLatestGenerationTask(projectId.value)
    task.value = res
  } catch (err) {
    console.error(err)
  }
}


onMounted(() => {
  projectId.value = new URLSearchParams(window.location.search).get('id') || '1'
  load()
  requestAnimationFrame(() => {
    isClient.value = true
  })
})

</script>

<template>
  <div class="p-6">
    <GenerationStatus
      v-if="task"
      :task="task"
      :visible="true"
    />
    <div v-else class="text-sm text-muted-foreground">暂无生成任务</div>
  </div>
</template>

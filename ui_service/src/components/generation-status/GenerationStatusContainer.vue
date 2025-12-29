<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchLatestGenerationTask } from '@/lib/api'
import type { GenerationTask } from '@/lib/api'
import GenerationStatus from '@/components/generate-download-step/GenerationStatus.vue'
import GenerationHistoryList from '@/components/generation-history/GenerationHistoryList.vue'

const projectId = ref<string>('1')
const currentTask = ref<GenerationTask | null>(null)
const isClient = ref(true)

const load = async () => {
  try {
    currentTask.value = await fetchLatestGenerationTask(projectId.value)
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
  <div class="space-y-6">
    <GenerationStatus
      v-if="currentTask"
      :task="currentTask"
      :visible="true"
    />
    <div v-else class="text-sm text-muted-foreground">暂无任务</div>

    <GenerationHistoryList />
  </div>
</template>

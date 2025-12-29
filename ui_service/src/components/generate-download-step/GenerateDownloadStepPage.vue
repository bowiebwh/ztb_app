<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { WORKFLOW_STEPS } from '@/data/config'
import type { GenerationTask } from '@/lib/api'
import { fetchLatestGenerationTask, startGeneration } from '@/lib/api'
import StepNavigation from '@/components/common/StepNavigation.vue'
import GenerateConfiguration from './GenerateConfiguration.vue'
import GenerationStatus from './GenerationStatus.vue'
import BidDocumentPreview from './BidDocumentPreview.vue'

type ViewMode = 'configuration' | 'status' | 'preview'

const isClient = ref(true)
const currentView = ref<ViewMode>('configuration')
const currentTask = ref<GenerationTask | null>(null)
const projectId = ref<string>('1')

const getProjectIdFromUrl = (): string => {
  if (typeof window !== 'undefined') {
    const params = new URLSearchParams(window.location.search)
    return params.get('id') || '1'
  }
  return '1'
}

const loadLatestTask = async () => {
  try {
    const task = await fetchLatestGenerationTask(projectId.value)
    currentTask.value = task
    if (task.status === 'Completed') {
      currentView.value = 'preview'
    } else {
      currentView.value = 'status'
    }
  } catch (error) {
    console.warn('暂无生成任务', error)
  }
}


const handleStartGeneration = async () => {
  try {
    const task = await startGeneration(projectId.value)
    currentTask.value = task
    currentView.value = 'status'
  } catch (error) {
    console.error('启动生成失败', error)
  }
}

const handleGenerationComplete = () => {
  currentView.value = 'preview'
}

const handleRegenerate = () => {
  currentView.value = 'configuration'
  currentTask.value = null
}

const handleBackToEdit = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './edit-bid-document-step.html'
  }
}

onMounted(() => {
  isClient.value = false
  projectId.value = getProjectIdFromUrl()
  loadLatestTask()
  requestAnimationFrame(() => {
    isClient.value = true
  })
})
</script>

<template>
  <div class="flex flex-col h-full">
    <aside class="sidebar">
      <div class="p-4">
        <h3 class="text-sm font-semibold mb-4 text-foreground">项目流程</h3>
        <StepNavigation
          :steps="WORKFLOW_STEPS"
          current-step="generate_download_step"
          orientation="vertical"
        />
      </div>
    </aside>

    <main class="flex-1 overflow-auto">
      <div class="container mx-auto px-6 py-8 max-w-4xl">
        <div class="mb-8">
          <h1 class="text-3xl font-bold mb-2">生成与下载投标书</h1>
          <p class="text-muted-foreground">配置输出选项并生成最终 Word 文档。</p>
        </div>

        <GenerateConfiguration
          v-if="currentView === 'configuration' || isClient"
          :visible="currentView === 'configuration' || isClient"
          @start-generation="handleStartGeneration"
          @back="handleBackToEdit"
        />

        <GenerationStatus
          v-if="currentView === 'status' && currentTask"
          :task="currentTask"
          :visible="currentView === 'status' || isClient"
          @complete="handleGenerationComplete"
        />

        <BidDocumentPreview
          v-if="currentView === 'preview' && currentTask"
          :task="currentTask"
          :visible="currentView === 'preview' || isClient"
          @regenerate="handleRegenerate"
          @back="handleBackToEdit"
        />
      </div>
    </main>
  </div>
</template>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: var(--header-height, 64px);
  width: 280px;
  height: calc(100vh - var(--header-height, 64px));
  overflow-y: auto;
  border-right: 1px solid hsl(var(--border));
  background: hsl(var(--sidebar-background));
}
</style>

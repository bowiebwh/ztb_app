<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { WORKFLOW_STEPS } from '@/data/config'
import type { Project } from '@/lib/api'
import { fetchProject } from '@/lib/api'
import WorkflowSidebar from './WorkflowSidebar.vue'
import StepContentArea from './StepContentArea.vue'
import MaterialLibraryPanel from './MaterialLibraryPanel.vue'
import EmptyState from '@/components/common/EmptyState.vue'

// State
const isClient = ref(true)
const projectId = ref<string>('')
const project = ref<Project | null>(null)
const showMaterialLibrary = ref(false)
const currentStepId = ref<string>('')

// Get project ID from URL query parameter
const getProjectIdFromUrl = (): string => {
  if (typeof window !== 'undefined') {
    const params = new URLSearchParams(window.location.search)
    return params.get('id') || '1'
  }
  return '1'
}

// Computed
const currentStep = computed(() => {
  return WORKFLOW_STEPS.find(step => step.id === currentStepId.value)
})

const isValidProject = computed(() => {
  return project.value !== null
})

const allowJumpAll = computed(() => {
  return (project.value?.status || '').toLowerCase() === 'completed'
})

// Methods
const handleStepChange = (stepId: string) => {
  currentStepId.value = stepId
  if (project.value) {
    project.value.currentStepId = stepId
  }
}

const toggleMaterialLibrary = () => {
  showMaterialLibrary.value = !showMaterialLibrary.value
}

const handleMaterialLibraryClose = () => {
  showMaterialLibrary.value = false
}

// Lifecycle
onMounted(async () => {
  isClient.value = false

  const actualProjectId = getProjectIdFromUrl()
  projectId.value = actualProjectId

  try {
    const loadedProject = await fetchProject(actualProjectId)
    project.value = loadedProject
    currentStepId.value = loadedProject.currentStepId || 'upload_tender_document_step'
  } catch (error) {
    console.error('加载项目失败', error)
  }

  requestAnimationFrame(() => {
    isClient.value = true
  })
})
</script>

<template>
  <div v-if="isValidProject || isClient" class="flex flex-col min-h-screen bg-muted/20">
    <!-- Project Header -->
    <div class="border-b bg-card px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold">{{ project?.projectName }}</h1>
          <p class="text-sm text-muted-foreground mt-1">
            当前步骤：{{ currentStep?.title }}
          </p>
        </div>
        <button
          @click="toggleMaterialLibrary"
          class="md:hidden px-4 py-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 transition-colors"
        >
          {{ showMaterialLibrary ? '关闭' : '打开' }}素材库
        </button>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="flex-1 overflow-hidden">
      <div class="w-full px-6 pb-6">
        <div class="w-full flex overflow-hidden gap-6">
          <!-- Left: Workflow Sidebar -->
          <aside class="hidden md:flex flex-col w-64 flex-shrink-0 bg-card rounded-lg border p-4 overflow-y-auto">
            <WorkflowSidebar
              :steps="WORKFLOW_STEPS"
              :currentStepId="currentStepId"
              :allowJumpAll="allowJumpAll"
              @step-change="handleStepChange"
            />
          </aside>

          <!-- Center: Step Content Area -->
          <main class="flex-1 flex flex-col min-w-0 bg-card rounded-lg border overflow-hidden">
            <StepContentArea
              :projectId="projectId"
              :currentStepId="currentStepId"
              :project="project"
              @step-change="handleStepChange"
              @open-material-library="showMaterialLibrary = true"
            />
          </main>

          <!-- Right: Material Library Panel (Desktop) -->
          <aside
            v-if="isClient || showMaterialLibrary"
            class="hidden md:flex flex-col w-80 flex-shrink-0 bg-card rounded-lg border overflow-hidden transition-all duration-300"
          >
            <MaterialLibraryPanel
              :projectId="projectId"
              @close="handleMaterialLibraryClose"
            />
          </aside>
        </div>
      </div>

      <!-- Right: Material Library Panel (Mobile Modal) -->
      <div
        v-if="showMaterialLibrary && (isClient || !isClient)"
        class="md:hidden fixed inset-0 z-40 bg-black/50"
        @click="handleMaterialLibraryClose"
      >
        <aside
          class="absolute right-0 top-0 bottom-0 w-full max-w-sm bg-card rounded-l-lg border-l overflow-hidden flex flex-col"
          @click.stop
        >
          <MaterialLibraryPanel
            :projectId="projectId"
            @close="handleMaterialLibraryClose"
          />
        </aside>
      </div>
    </div>
  </div>

  <!-- Empty State -->
  <div v-else class="flex items-center justify-center h-full">
    <EmptyState
      icon="AlertCircle"
      title="项目不存在"
      description="无法找到指定的项目，请返回项目列表重新选择。"
      actionLabel="返回项目列表"
      actionHref="./project-list.html"
    />
  </div>
</template>

<style scoped>
/* Smooth transitions for sidebar and panels */
aside {
  transition: all 0.3s ease-in-out;
}

/* Ensure proper scrolling behavior */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: hsl(var(--muted));
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--muted-foreground));
}
</style>

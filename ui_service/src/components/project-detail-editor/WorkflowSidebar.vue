
<script setup lang="ts">
import { computed } from 'vue'
import type { WorkflowStepModel } from '@/data/config'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { cn } from '@/lib/utils'

interface Props {
  steps: WorkflowStepModel[]
  currentStepId: string
  allowJumpAll?: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'step-change': [stepId: string]
}>()

const currentStepIndex = computed(() => {
  return props.steps.findIndex(step => step.id === props.currentStepId)
})

const getStepStatus = (index: number): 'completed' | 'current' | 'upcoming' => {
  if (index < currentStepIndex.value) return 'completed'
  if (index === currentStepIndex.value) return 'current'
  return 'upcoming'
}

const isDisabled = (index: number) => {
  if (props.allowJumpAll) return false
  return getStepStatus(index) === 'upcoming'
}

const handleStepClick = (stepId: string) => {
  const targetIndex = props.steps.findIndex(step => step.id === stepId)
  if (isDisabled(targetIndex)) return
  emit('step-change', stepId)
}
</script>

<template>
  <div class="space-y-2">
    <h3 class="text-sm font-semibold text-muted-foreground px-2 mb-4">工作流程</h3>
    
    <div class="space-y-3">
      <template v-for="(step, index) in steps" :key="step.id">
        <!-- Step Item -->
        <button
          @click="handleStepClick(step.id)"
          :class="cn(
            'w-full flex items-start gap-3 p-3 rounded-lg transition-all duration-200',
            'text-left hover:bg-muted/50',
            getStepStatus(index) === 'current' && 'bg-primary/10 border border-primary/20',
            getStepStatus(index) === 'completed' && 'hover:bg-muted',
            getStepStatus(index) === 'upcoming' && !allowJumpAll && 'opacity-60 cursor-not-allowed'
          )"
          :disabled="isDisabled(index)"
          :aria-current="getStepStatus(index) === 'current' ? 'step' : undefined"
        >
          <!-- Icon -->
          <div
            :class="cn(
              'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center transition-colors',
              getStepStatus(index) === 'completed' && 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
              getStepStatus(index) === 'current' && 'bg-primary text-primary-foreground',
              getStepStatus(index) === 'upcoming' && 'bg-muted text-muted-foreground'
            )"
          >
            <SafeIcon
              :name="getStepStatus(index) === 'completed' ? 'CheckCircle2' : step.iconName"
              :size="18"
              :stroke-width="2"
            />
          </div>

          <!-- Content -->
          <div class="flex-1 min-w-0">
            <div
              :class="cn(
                'text-sm font-medium transition-colors',
                getStepStatus(index) === 'current' && 'text-primary',
              getStepStatus(index) === 'completed' && 'text-foreground',
              getStepStatus(index) === 'upcoming' && !allowJumpAll && 'text-muted-foreground'
            )"
          >
            {{ step.title }}
            </div>
            <div
              v-if="getStepStatus(index) === 'completed'"
              class="text-xs text-green-700 dark:text-green-400 mt-0.5"
            >
              已完成
            </div>
          </div>
        </button>

        <!-- Connector Line -->
        <div
          v-if="index < steps.length - 1"
          :class="cn(
            'ml-4 h-6 w-0.5 transition-colors',
            getStepStatus(index) === 'completed' ? 'bg-green-200 dark:bg-green-900/50' : 'bg-border'
          )"
        />
      </template>
    </div>
  </div>
</template>

<style scoped>
button:disabled {
  cursor: not-allowed;
}

button:not(:disabled):hover {
  transform: translateX(2px);
}
</style>

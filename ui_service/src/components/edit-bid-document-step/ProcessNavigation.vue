
<script setup lang="ts">
import { computed } from 'vue'
import type { WorkflowStepModel } from '@/data/config'
import StepNavigation from '@/components/common/StepNavigation.vue'

interface Props {
  steps: WorkflowStepModel[]
  currentStep: string
}

const props = defineProps<Props>()

const navigationSteps = computed(() => {
  return props.steps.map(step => ({
    id: step.id,
    label: step.title,
    href: step.routePath,
  }))
})
</script>

<template>
  <div class="p-4 overflow-y-auto flex-1">
    <h3 class="text-sm font-semibold text-sidebar-foreground mb-4 px-2">项目流程</h3>
    <StepNavigation
      :steps="navigationSteps"
      :current-step="currentStep"
      orientation="vertical"
    />
  </div>
</template>

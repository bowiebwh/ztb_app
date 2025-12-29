
<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '@/lib/utils'
import SafeIcon from '@/components/common/SafeIcon.vue'

export interface Step {
  id: string
  label: string
  description?: string
  href?: string
}

interface Props {
  steps: Step[]
  currentStep: string
  orientation?: 'vertical' | 'horizontal'
}

const props = withDefaults(defineProps<Props>(), {
  orientation: 'vertical',
})

const currentStepIndex = computed(() => {
  return props.steps.findIndex(step => step.id === props.currentStep)
})

const getStepStatus = (index: number): 'completed' | 'current' | 'upcoming' => {
  if (index < currentStepIndex.value) return 'completed'
  if (index === currentStepIndex.value) return 'current'
  return 'upcoming'
}

const getStepIcon = (status: string) => {
  if (status === 'completed') return 'CheckCircle2'
  if (status === 'current') return 'Circle'
  return 'Circle'
}
</script>

<template>
  <nav
    :class="cn(
      'flex gap-4',
      orientation === 'vertical' ? 'flex-col' : 'flex-row items-center'
    )"
    aria-label="进度导航"
  >
    <template v-for="(step, index) in steps" :key="step.id">
      <!-- Step Item -->
      <a
        :href="step.href || '#'"
        :class="cn(
          'flex items-start gap-3 p-3 rounded-lg transition-colors group',
          getStepStatus(index) === 'current' && 'bg-primary/10',
          getStepStatus(index) === 'completed' && 'hover:bg-muted',
          getStepStatus(index) === 'upcoming' && 'opacity-60 cursor-not-allowed pointer-events-none'
        )"
        :aria-current="getStepStatus(index) === 'current' ? 'step' : undefined"
      >
        <!-- Icon -->
        <div
          :class="cn(
            'flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center transition-colors',
            getStepStatus(index) === 'completed' && 'bg-primary text-primary-foreground',
            getStepStatus(index) === 'current' && 'bg-primary text-primary-foreground',
            getStepStatus(index) === 'upcoming' && 'bg-muted text-muted-foreground'
          )"
        >
          <SafeIcon
            :name="getStepIcon(getStepStatus(index))"
            :size="16"
            :stroke-width="2.5"
          />
        </div>

        <!-- Content -->
        <div class="flex-1 min-w-0">
          <div
            :class="cn(
              'text-sm font-medium transition-colors',
              getStepStatus(index) === 'current' && 'text-primary',
              getStepStatus(index) === 'completed' && 'text-foreground group-hover:text-primary',
              getStepStatus(index) === 'upcoming' && 'text-muted-foreground'
            )"
          >
            {{ step.label }}
          </div>
          <div
            v-if="step.description"
            class="text-xs text-muted-foreground mt-0.5"
          >
            {{ step.description }}
          </div>
        </div>
      </a>

      <!-- Connector Line -->
      <div
        v-if="index < steps.length - 1"
        :class="cn(
          'transition-colors',
          orientation === 'vertical' ? 'ml-6 h-8 w-0.5' : 'h-0.5 flex-1',
          getStepStatus(index) === 'completed' ? 'bg-primary' : 'bg-border'
        )"
      />
    </template>
  </nav>
</template>


<script setup lang="ts">
import { computed } from 'vue'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { TaskStage } from '@/data/generation'

interface Props {
  currentStage: TaskStage
  stageConfig: Record<TaskStage, { label: string; description: string }>
}

const props = defineProps<Props>()

const stages: TaskStage[] = [
  'Initialization',
  'Analysis',
  'KnowledgeRetrieval',
  'Drafting',
  'Finalizing',
  'Rendering',
]

const currentStageIndex = computed(() => {
  return stages.indexOf(props.currentStage)
})

const getStageStatus = (index: number): 'completed' | 'current' | 'upcoming' => {
  if (index < currentStageIndex.value) return 'completed'
  if (index === currentStageIndex.value) return 'current'
  return 'upcoming'
}
</script>

<template>
  <div class="space-y-3">
    <template v-for="(stage, index) in stages" :key="stage">
      <div
        class="flex items-start gap-3 p-3 rounded-lg transition-colors"
        :class="{
          'bg-primary/10': getStageStatus(index) === 'current',
          'bg-muted/50': getStageStatus(index) === 'completed',
          'opacity-50': getStageStatus(index) === 'upcoming',
        }"
      >
        <!-- 图标 -->
        <div
          class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center mt-0.5"
          :class="{
            'bg-primary text-primary-foreground': getStageStatus(index) === 'current',
            'bg-green-500 text-white': getStageStatus(index) === 'completed',
            'bg-muted text-muted-foreground': getStageStatus(index) === 'upcoming',
          }"
        >
          <SafeIcon
            v-if="getStageStatus(index) === 'completed'"
            name="Check"
            :size="14"
            :stroke-width="3"
          />
          <SafeIcon
            v-else-if="getStageStatus(index) === 'current'"
            name="Loader2"
            :size="14"
            class="animate-spin"
          />
          <SafeIcon
            v-else
            name="Circle"
            :size="14"
          />
        </div>

        <!-- 内容 -->
        <div class="flex-1 min-w-0">
          <div
            class="text-sm font-medium"
            :class="{
              'text-primary': getStageStatus(index) === 'current',
              'text-foreground': getStageStatus(index) === 'completed',
              'text-muted-foreground': getStageStatus(index) === 'upcoming',
            }"
          >
            {{ props.stageConfig[stage].label }}
          </div>
          <div class="text-xs text-muted-foreground mt-0.5">
            {{ props.stageConfig[stage].description }}
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

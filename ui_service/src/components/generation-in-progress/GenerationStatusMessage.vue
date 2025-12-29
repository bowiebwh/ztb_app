
<script setup lang="ts">
import { computed } from 'vue'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { TaskStatus } from '@/data/generation'

interface Props {
  status: TaskStatus
  message: string
  errorMessage?: string
}

const props = defineProps<Props>()

const statusConfig = computed(() => {
  const configs: Record<TaskStatus, { icon: string; color: string; bgColor: string }> = {
    'Pending': { icon: 'Clock', color: 'text-blue-600', bgColor: 'bg-blue-50 dark:bg-blue-900/20' },
    'InProgress': { icon: 'Loader2', color: 'text-amber-600', bgColor: 'bg-amber-50 dark:bg-amber-900/20' },
    'Completed': { icon: 'CheckCircle2', color: 'text-green-600', bgColor: 'bg-green-50 dark:bg-green-900/20' },
    'Failed': { icon: 'XCircle', color: 'text-red-600', bgColor: 'bg-red-50 dark:bg-red-900/20' },
  }
  return configs[props.status]
})
</script>

<template>
  <div
    class="p-4 rounded-lg border"
    :class="statusConfig.bgColor"
  >
    <div class="flex gap-3">
      <SafeIcon
        :name="statusConfig.icon"
        :size="20"
        :class="[statusConfig.color, props.status === 'InProgress' && 'animate-spin']"
      />
      <div class="flex-1">
        <p class="text-sm font-medium" :class="statusConfig.color">
          {{ props.message }}
        </p>
        <p v-if="props.errorMessage" class="text-sm text-red-600 dark:text-red-400 mt-1">
          {{ props.errorMessage }}
        </p>
      </div>
    </div>
  </div>
</template>

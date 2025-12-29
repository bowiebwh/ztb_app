
<script setup lang="ts">
import { computed } from 'vue'
import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'
import SafeIcon from '@/components/common/SafeIcon.vue'

type StatusVariant = 'draft' | 'in-progress' | 'completed' | 'failed' | 'waiting'

interface Props {
  status: StatusVariant
  showIcon?: boolean
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  showIcon: true,
  size: 'md',
})

const statusConfig = computed(() => {
  const configs: Record<StatusVariant, { label: string; icon: string; class: string }> = {
    draft: {
      label: '草稿',
      icon: 'FileEdit',
      class: 'bg-muted text-muted-foreground hover:bg-muted',
    },
    'in-progress': {
      label: '生成中',
      icon: 'Loader2',
      class: 'bg-amber-100 text-amber-800 hover:bg-amber-100 dark:bg-amber-900/30 dark:text-amber-400',
    },
    completed: {
      label: '已完成',
      icon: 'CheckCircle2',
      class: 'bg-green-100 text-green-800 hover:bg-green-100 dark:bg-green-900/30 dark:text-green-400',
    },
    failed: {
      label: '失败',
      icon: 'XCircle',
      class: 'bg-red-100 text-red-800 hover:bg-red-100 dark:bg-red-900/30 dark:text-red-400',
    },
    waiting: {
      label: '等待中',
      icon: 'Clock',
      class: 'bg-blue-100 text-blue-800 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-400',
    },
  }
  return configs[props.status]
})

const iconSize = computed(() => {
  const sizes = { sm: 12, md: 14, lg: 16 }
  return sizes[props.size]
})
</script>

<template>
  <Badge :class="cn(statusConfig.class, 'inline-flex items-center gap-1.5')">
    <SafeIcon
      v-if="showIcon"
      :name="statusConfig.icon"
      :size="iconSize"
      :class="cn(status === 'in-progress' && 'animate-spin')"
    />
    <span>{{ statusConfig.label }}</span>
  </Badge>
</template>

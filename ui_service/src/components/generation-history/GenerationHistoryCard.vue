
<script setup lang="ts">
import { computed } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import SafeIcon from '@/components/common/SafeIcon.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import type { GenerationTaskModel } from '@/data/generation'

interface Props {
  task: GenerationTaskModel
  isClient?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isClient: true,
})

const emit = defineEmits<{
  preview: [task: GenerationTaskModel]
  download: [task: GenerationTaskModel]
  regenerate: [task: GenerationTaskModel]
}>()

const getStatusVariant = (status: string): 'draft' | 'in-progress' | 'completed' | 'failed' | 'waiting' => {
  switch (status) {
    case 'Completed':
      return 'completed'
    case 'Failed':
      return 'failed'
    case 'InProgress':
      return 'in-progress'
    case 'Pending':
      return 'waiting'
    default:
      return 'draft'
  }
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const getStageLabel = (stage: string): string => {
  const stageMap: Record<string, string> = {
    'Initialization': '初始化',
    'Analysis': '分析',
    'KnowledgeRetrieval': '知识检索',
    'Drafting': '起草',
    'Finalizing': '最终化',
    'Rendering': '渲染',
  }
  return stageMap[stage] || stage
}

const canDownload = computed(() => {
  return props.task.status === 'Completed' && props.task.resultUrl
})

const canPreview = computed(() => {
  return props.task.status === 'Completed' && props.task.generatedToc
})

const canRegenerate = computed(() => {
  return props.isClient
})
</script>

<template>
  <Card class="hover:shadow-card transition-shadow">
    <CardHeader class="pb-3">
      <div class="flex items-start justify-between gap-4">
        <div class="flex-1">
          <div class="flex items-center gap-3 mb-2">
            <CardTitle class="text-lg">
              任务 #{{ task.taskId.substring(5) }}
            </CardTitle>
            <StatusBadge :status="getStatusVariant(task.status)" :show-icon="true" size="sm" />
          </div>
          <CardDescription>
            {{ formatDate(task.startTime) }}
          </CardDescription>
        </div>
      </div>
    </CardHeader>

    <CardContent class="space-y-4">
      <!-- Status Message -->
      <div class="space-y-2">
        <p class="text-sm font-medium text-foreground">状态信息</p>
        <p class="text-sm text-muted-foreground">
          {{ task.statusMessage }}
        </p>
      </div>

      <!-- Progress & Stage (for in-progress or completed tasks) -->
      <div v-if="task.status === 'InProgress' || task.status === 'Completed'" class="space-y-2">
        <div class="flex items-center justify-between">
          <p class="text-sm font-medium">进度</p>
          <span class="text-sm text-muted-foreground">{{ task.progress }}%</span>
        </div>
        <div class="w-full bg-muted rounded-full h-2">
          <div
            class="bg-primary h-2 rounded-full transition-all"
            :style="{ width: `${task.progress}%` }"
          />
        </div>
        <p class="text-xs text-muted-foreground">
          当前阶段：{{ getStageLabel(task.currentStage) }}
        </p>
      </div>

      <!-- Error Message (for failed tasks) -->
      <div v-if="task.status === 'Failed' && task.errorMessage" class="space-y-2">
        <p class="text-sm font-medium text-destructive">错误信息</p>
        <p class="text-sm text-destructive/80 bg-destructive/10 p-2 rounded">
          {{ task.errorMessage }}
        </p>
      </div>

      <!-- Actions -->
      <div class="flex flex-wrap gap-2 pt-2">
        <Button
          v-if="canPreview"
          variant="default"
          size="sm"
          @click="emit('preview', task)"
          :disabled="!isClient"
        >
          <SafeIcon name="Eye" :size="16" class="mr-1" />
          预览
        </Button>

        <Button
          v-if="canDownload"
          variant="outline"
          size="sm"
          @click="emit('download', task)"
          :disabled="!isClient"
        >
          <SafeIcon name="Download" :size="16" class="mr-1" />
          下载
        </Button>

        <Button
          v-if="canRegenerate"
          variant="outline"
          size="sm"
          @click="emit('regenerate', task)"
          :disabled="!isClient"
        >
          <SafeIcon name="RotateCcw" :size="16" class="mr-1" />
          重新生成
        </Button>

        <!-- View Details Link -->
        <Button
          variant="ghost"
          size="sm"
          as-child
        >
          <a href="./generation-status.html" class="flex items-center gap-1">
            <SafeIcon name="ChevronRight" :size="16" />
            查看详情
          </a>
        </Button>
      </div>
    </CardContent>
  </Card>
</template>

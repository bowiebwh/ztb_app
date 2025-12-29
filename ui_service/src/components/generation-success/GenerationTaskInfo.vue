
<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { GenerationTaskModel } from '@/data/generation'

interface Props {
  task: GenerationTaskModel
}

const props = defineProps<Props>()

const formattedStartTime = computed(() => {
  try {
    const date = new Date(props.task.startTime)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })
  } catch {
    return props.task.startTime
  }
})

const estimatedDuration = computed(() => {
  try {
    const startTime = new Date(props.task.startTime)
    const now = new Date()
    const durationMs = now.getTime() - startTime.getTime()
    const minutes = Math.floor(durationMs / 60000)
    const seconds = Math.floor((durationMs % 60000) / 1000)
    
    if (minutes > 0) {
      return `${minutes}分${seconds}秒`
    }
    return `${seconds}秒`
  } catch {
    return '未知'
  }
})

const stageLabel = computed(() => {
  const labels: Record<string, string> = {
    'Initialization': '初始化',
    'Analysis': '分析',
    'KnowledgeRetrieval': '知识检索',
    'Drafting': '草稿生成',
    'Finalizing': '最终化',
    'Rendering': '渲染',
  }
  return labels[props.task.currentStage] || props.task.currentStage
})
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle class="flex items-center gap-2">
        <SafeIcon name="FileCheck" :size="20" />
        生成任务信息
      </CardTitle>
      <CardDescription>
        投标书生成任务已完成
      </CardDescription>
    </CardHeader>
    <CardContent>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Task ID -->
        <div>
          <p class="text-sm text-muted-foreground mb-1">任务 ID</p>
          <p class="font-mono text-sm break-all">{{ task.taskId }}</p>
        </div>

        <!-- Project ID -->
        <div>
          <p class="text-sm text-muted-foreground mb-1">项目 ID</p>
          <p class="font-mono text-sm break-all">{{ task.projectId }}</p>
        </div>

        <!-- Start Time -->
        <div>
          <p class="text-sm text-muted-foreground mb-1">开始时间</p>
          <p class="text-sm">{{ formattedStartTime }}</p>
        </div>

        <!-- Duration -->
        <div>
          <p class="text-sm text-muted-foreground mb-1">耗时</p>
          <p class="text-sm">{{ estimatedDuration }}</p>
        </div>

        <!-- Status -->
        <div>
          <p class="text-sm text-muted-foreground mb-1">状态</p>
          <Badge class="bg-green-100 text-green-800 hover:bg-green-100 dark:bg-green-900/30 dark:text-green-400">
            <SafeIcon name="CheckCircle2" :size="14" class="mr-1" />
            已完成
          </Badge>
        </div>

        <!-- Final Stage -->
        <div>
          <p class="text-sm text-muted-foreground mb-1">最终阶段</p>
          <p class="text-sm">{{ stageLabel }}</p>
        </div>

        <!-- Status Message -->
        <div class="md:col-span-2">
          <p class="text-sm text-muted-foreground mb-1">状态信息</p>
          <p class="text-sm">{{ task.statusMessage }}</p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { fetchLatestGenerationTask } from '@/lib/api'
import type { GenerationTask } from '@/lib/api'

const task = ref<GenerationTask | null>(null)
const projectId = ref<string>('1')

const load = async () => {
  try {
    task.value = await fetchLatestGenerationTask(projectId.value)
  } catch (err) {
    console.error(err)
  }
}


onMounted(() => {
  projectId.value = new URLSearchParams(window.location.search).get('id') || '1'
  load()
})
</script>

<template>
  <Card class="mb-6 border-2">
    <CardHeader>
      <div class="flex items-center justify-between">
        <div>
          <CardTitle class="flex items-center gap-2">
            <SafeIcon :name="task?.status === 'Completed' ? 'CheckCircle2' : 'Loader2'" :size="24" :class="task?.status === 'Completed' ? 'text-green-500' : 'animate-spin text-primary'" />
            生成进度
          </CardTitle>
          <CardDescription class="mt-2">
            {{ task?.statusMessage || '等待任务' }}
          </CardDescription>
        </div>
        <div class="text-right">
          <div class="text-3xl font-bold text-primary">{{ Math.round(task?.progress || 0) }}%</div>
          <div class="text-xs text-muted-foreground mt-1">进度</div>
        </div>
      </div>
    </CardHeader>

    <CardContent class="space-y-6">
      <div class="space-y-2">
        <div class="flex justify-between text-sm">
          <span class="font-medium">总体进度</span>
          <span class="text-muted-foreground">{{ Math.round(task?.progress || 0) }}%</span>
        </div>
        <Progress :value="task?.progress || 0" class="h-3" />
      </div>

      <div class="bg-muted/50 rounded-lg p-4 border border-border">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
            <SafeIcon name="Zap" :size="20" class="text-primary" />
          </div>
          <div class="flex-1 min-w-0">
            <div class="font-medium text-sm">当前阶段</div>
            <div class="text-sm text-muted-foreground mt-1">{{ task?.currentStage || '未知' }}</div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div class="bg-background border border-border rounded-lg p-3">
          <div class="text-xs text-muted-foreground mb-1">开始时间</div>
          <div class="text-sm font-medium">
            {{ task?.startTime ? new Date(task.startTime).toLocaleTimeString('zh-CN') : '--' }}
          </div>
        </div>
        <div class="bg-background border border-border rounded-lg p-3">
          <div class="text-xs text-muted-foreground mb-1">预计剩余</div>
          <div class="text-sm font-medium">约 {{ task?.progress ? Math.max(1, Math.ceil((100 - task.progress) / 25)) : '--' }} 分钟</div>
        </div>
      </div>

      <div class="bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-lg p-3">
        <div class="flex gap-2">
          <SafeIcon name="Info" :size="16" class="text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
          <div class="text-xs text-blue-700 dark:text-blue-300">
            生成过程中请勿关闭此页面。系统会自动保存进度，您可以稍后返回查看。
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

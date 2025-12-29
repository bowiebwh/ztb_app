
<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { GenerationTaskModel } from '@/data/generation'

interface Props {
  history: GenerationTaskModel[]
  currentTaskId: string
}

const props = defineProps<Props>()

const getStatusBadgeVariant = (status: string) => {
  switch (status) {
    case 'Completed':
      return 'default'
    case 'Failed':
      return 'destructive'
    case 'InProgress':
      return 'secondary'
    default:
      return 'outline'
  }
}

const getStatusLabel = (status: string) => {
  switch (status) {
    case 'Completed':
      return '已完成'
    case 'Failed':
      return '失败'
    case 'InProgress':
      return '生成中'
    case 'Pending':
      return '等待中'
    default:
      return status
  }
}

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'Completed':
      return 'CheckCircle2'
    case 'Failed':
      return 'XCircle'
    case 'InProgress':
      return 'Loader2'
    default:
      return 'Clock'
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const handleViewTask = (taskId: string) => {
  // 可以实现查看历史任务的详情
  console.log('查看任务:', taskId)
}

const handleDownloadTask = (taskId: string) => {
  // 下载历史任务的文件
  console.log('下载任务:', taskId)
}
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>生成历史</CardTitle>
      <CardDescription>显示最近的生成任务记录</CardDescription>
    </CardHeader>

    <CardContent>
      <div class="space-y-3">
        <div
          v-for="task in history"
          :key="task.taskId"
          class="p-4 border rounded-lg hover:bg-muted/50 transition-colors"
          :class="{ 'border-primary/50 bg-primary/5': task.taskId === currentTaskId }"
        >
          <div class="flex items-start justify-between gap-4">
            <!-- 左侧：任务信息 -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-2">
                <SafeIcon
                  :name="getStatusIcon(task.status)"
                  :size="16"
                  :class="[
                    task.status === 'Completed' && 'text-green-600',
                    task.status === 'Failed' && 'text-red-600',
                    task.status === 'InProgress' && 'text-amber-600 animate-spin',
                  ]"
                />
                <Badge :variant="getStatusBadgeVariant(task.status)">
                  {{ getStatusLabel(task.status) }}
                </Badge>
                <span v-if="task.taskId === currentTaskId" class="text-xs font-medium text-primary">
                  当前任务
                </span>
              </div>

              <div class="text-sm text-muted-foreground space-y-1">
                <div>
                  <span class="font-medium text-foreground">任务ID:</span>
                  {{ task.taskId }}
                </div>
                <div>
                  <span class="font-medium text-foreground">开始时间:</span>
                  {{ formatDate(task.startTime) }}
                </div>
                <div v-if="task.statusMessage" class="text-xs">
                  {{ task.statusMessage }}
                </div>
              </div>
            </div>

            <!-- 右侧：进度和操作 -->
            <div class="flex flex-col items-end gap-2">
              <div class="text-right">
                <div class="text-sm font-medium">{{ task.progress }}%</div>
                <div class="text-xs text-muted-foreground">进度</div>
              </div>

              <div class="flex gap-1">
                <Button
                  v-if="task.status === 'Completed'"
                  size="sm"
                  variant="outline"
                  @click="handleDownloadTask(task.taskId)"
                >
                  <SafeIcon name="Download" :size="14" class="mr-1" />
                  下载
                </Button>
                <Button
                  v-if="task.status === 'Completed'"
                  size="sm"
                  variant="outline"
                  @click="handleViewTask(task.taskId)"
                >
                  <SafeIcon name="Eye" :size="14" class="mr-1" />
                  预览
                </Button>
              </div>
            </div>
          </div>

          <!-- 错误信息 -->
          <div v-if="task.status === 'Failed' && task.errorMessage" class="mt-3 p-2 bg-red-50 dark:bg-red-900/20 rounded text-xs text-red-700 dark:text-red-300">
            <SafeIcon name="AlertCircle" :size="12" class="inline mr-1" />
            {{ task.errorMessage }}
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="history.length === 0" class="text-center py-8 text-muted-foreground">
          <SafeIcon name="History" :size="32" class="mx-auto mb-2 opacity-50" />
          <p class="text-sm">暂无生成历史</p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>


<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import StatusBadge from '@/components/common/StatusBadge.vue'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { TaskStatus } from '@/data/generation'

interface Props {
  taskId: string
  projectId: string
  startTime: string
  status: TaskStatus
}

const props = defineProps<Props>()

const formattedTime = computed(() => {
  try {
    const date = new Date(props.startTime)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return props.startTime
  }
})

const statusMap: Record<TaskStatus, 'completed' | 'in-progress' | 'failed' | 'waiting'> = {
  'Completed': 'completed',
  'InProgress': 'in-progress',
  'Failed': 'failed',
  'Pending': 'waiting',
}
</script>

<template>
  <Card>
    <CardHeader>
      <div class="flex items-start justify-between">
        <div>
          <CardTitle class="flex items-center gap-2">
            <SafeIcon name="FileText" :size="24" />
            投标书预览
          </CardTitle>
          <CardDescription class="mt-2">
            查看已生成的投标书内容，支持下载Word文件
          </CardDescription>
        </div>
        <StatusBadge :status="statusMap[status]" />
      </div>
    </CardHeader>
    <CardContent>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div>
          <p class="text-sm text-muted-foreground">任务ID</p>
          <p class="font-mono text-sm mt-1">{{ taskId }}</p>
        </div>
        <div>
          <p class="text-sm text-muted-foreground">项目ID</p>
          <p class="font-mono text-sm mt-1">{{ projectId }}</p>
        </div>
        <div>
          <p class="text-sm text-muted-foreground">生成时间</p>
          <p class="text-sm mt-1">{{ formattedTime }}</p>
        </div>
        <div>
          <p class="text-sm text-muted-foreground">状态</p>
          <p class="text-sm mt-1 font-medium">已完成</p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

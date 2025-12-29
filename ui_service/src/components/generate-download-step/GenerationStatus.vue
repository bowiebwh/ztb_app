
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import type { GenerationTaskModel, TaskStage } from '@/data/generation'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  task: GenerationTaskModel
  visible?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  visible: true,
})

const emit = defineEmits<{
  complete: []
}>()

const isClient = ref(true)

const stageLabels: Record<TaskStage, string> = {
  'Initialization': '初始化',
  'Analysis': '分析招标文件',
  'KnowledgeRetrieval': '检索知识库',
  'Drafting': '生成文档内容',
  'Finalizing': '最终处理',
  'Rendering': '渲染Word文档',
}

const stageIcons: Record<TaskStage, string> = {
  'Initialization': 'Zap',
  'Analysis': 'Cpu',
  'KnowledgeRetrieval': 'Database',
  'Drafting': 'PenTool',
  'Finalizing': 'CheckCircle2',
  'Rendering': 'FileText',
}

const statusLabel = computed(() => {
  const labels: Record<string, string> = {
    'Pending': '等待中',
    'InProgress': '生成中',
    'Completed': '已完成',
    'Failed': '失败',
  }
  return labels[props.task.status] || props.task.status
})

const statusColor = computed(() => {
  const colors: Record<string, string> = {
    'Pending': 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
    'InProgress': 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400',
    'Completed': 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    'Failed': 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
  }
  return colors[props.task.status] || ''
})

onMounted(() => {
  isClient.value = false
  requestAnimationFrame(() => {
    isClient.value = true
  })

  // 监听任务完成
  const checkCompletion = setInterval(() => {
    if (props.task.status === 'Completed') {
      clearInterval(checkCompletion)
      setTimeout(() => {
        emit('complete')
      }, 1000)
    }
  }, 500)

  return () => clearInterval(checkCompletion)
})
</script>

<template>
  <div v-if="visible" class="space-y-6">
    <!-- 状态卡片 -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>生成进度</CardTitle>
            <CardDescription>实时监控投标书生成任务</CardDescription>
          </div>
          <Badge :class="statusColor" class="inline-flex items-center gap-1.5">
            <SafeIcon
              :name="task.status === 'InProgress' ? 'Loader2' : 'CheckCircle2'"
              :size="14"
              :class="task.status === 'InProgress' ? 'animate-spin' : ''"
            />
            {{ statusLabel }}
          </Badge>
        </div>
      </CardHeader>
      <CardContent class="space-y-6">
        <!-- 进度条 -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium">总体进度</span>
            <span class="text-sm text-muted-foreground">{{ task.progress }}%</span>
          </div>
          <Progress :value="task.progress" class="h-2" />
        </div>

        <!-- 当前阶段 -->
        <div class="space-y-3">
          <h4 class="text-sm font-medium">当前阶段</h4>
          <div class="flex items-center gap-3 p-3 rounded-lg bg-muted">
            <SafeIcon
              :name="stageIcons[task.currentStage]"
              :size="20"
              class="text-primary flex-shrink-0"
            />
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium">{{ stageLabels[task.currentStage] }}</p>
              <p class="text-xs text-muted-foreground mt-1">{{ task.statusMessage }}</p>
            </div>
          </div>
        </div>

        <!-- 任务信息 -->
        <div class="grid grid-cols-2 gap-4 pt-4 border-t">
          <div>
            <p class="text-xs text-muted-foreground mb-1">任务ID</p>
            <p class="text-sm font-mono text-foreground">{{ task.taskId }}</p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground mb-1">开始时间</p>
            <p class="text-sm text-foreground">
              {{ new Date(task.startTime).toLocaleString('zh-CN') }}
            </p>
          </div>
        </div>

        <!-- 错误信息 -->
        <div
          v-if="task.status === 'Failed' && task.errorMessage"
          class="p-3 rounded-lg bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-900/30"
        >
          <p class="text-sm font-medium text-red-800 dark:text-red-400 mb-1">错误信息</p>
          <p class="text-xs text-red-700 dark:text-red-300">{{ task.errorMessage }}</p>
        </div>
      </CardContent>
    </Card>

    <!-- 提示信息 -->
    <Card v-if="task.status === 'InProgress'" class="border-blue-200 bg-blue-50 dark:border-blue-900/30 dark:bg-blue-900/10">
      <CardContent class="pt-6">
        <div class="flex gap-3">
          <SafeIcon name="Info" :size="20" class="text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
          <div class="text-sm text-blue-800 dark:text-blue-300">
            <p class="font-medium mb-1">生成中</p>
            <p class="text-xs">
              系统正在基于您的配置和编辑内容生成投标书。此过程可能需要几分钟，请耐心等待。
            </p>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- 操作按钮 -->
    <div v-if="task.status === 'Failed'" class="flex gap-3 justify-end">
      <Button variant="outline">
        返回编辑
      </Button>
      <Button>
        重新生成
      </Button>
    </div>
  </div>
</template>

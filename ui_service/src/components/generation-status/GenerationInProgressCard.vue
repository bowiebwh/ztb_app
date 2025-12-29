
<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { GenerationTaskModel } from '@/data/generation'

interface Props {
  task: GenerationTaskModel
}

const props = defineProps<Props>()

const emit = defineEmits<{
  retry: []
}>()

const stageLabels: Record<string, string> = {
  Initialization: '初始化',
  Analysis: '分析招标文件',
  KnowledgeRetrieval: '检索知识库',
  Drafting: '生成文档内容',
  Finalizing: '最终处理',
  Rendering: '渲染Word文档',
}

const getStageLabel = (stage: string) => {
  return stageLabels[stage] || stage
}

const progressPercentage = computed(() => {
  return Math.min(Math.max(props.task.progress, 0), 100)
})

const estimatedTimeRemaining = computed(() => {
  if (props.task.progress >= 100) return '即将完成'
  const remainingPercent = 100 - props.task.progress
  const estimatedSeconds = Math.ceil((remainingPercent / props.task.progress) * 30) // 假设已用30秒
  if (estimatedSeconds < 60) return `约${estimatedSeconds}秒`
  return `约${Math.ceil(estimatedSeconds / 60)}分钟`
})
</script>

<template>
  <Card class="border-amber-200 dark:border-amber-900/50">
    <CardHeader>
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <SafeIcon name="Loader2" :size="20" class="text-amber-600 animate-spin" />
          <div>
            <CardTitle>生成中</CardTitle>
            <CardDescription>{{ task.statusMessage }}</CardDescription>
          </div>
        </div>
        <div class="text-right">
          <div class="text-2xl font-bold text-amber-600">{{ Math.round(progressPercentage) }}%</div>
          <div class="text-xs text-muted-foreground">{{ estimatedTimeRemaining }}</div>
        </div>
      </div>
    </CardHeader>

    <CardContent class="space-y-6">
      <!-- 进度条 -->
      <div class="space-y-2">
        <div class="flex justify-between text-sm">
          <span class="text-muted-foreground">总体进度</span>
          <span class="font-medium">{{ Math.round(progressPercentage) }}%</span>
        </div>
        <Progress :value="progressPercentage" class="h-2" />
      </div>

      <!-- 当前阶段 -->
      <div class="space-y-3">
        <h4 class="text-sm font-semibold">当前阶段</h4>
        <div class="flex items-center gap-3 p-3 bg-muted rounded-lg">
          <SafeIcon name="Zap" :size="18" class="text-amber-600 flex-shrink-0" />
          <div class="flex-1">
            <div class="font-medium text-sm">{{ getStageLabel(task.currentStage) }}</div>
            <div class="text-xs text-muted-foreground mt-0.5">
              正在处理中，请稍候...
            </div>
          </div>
        </div>
      </div>

      <!-- 阶段列表 -->
      <div class="space-y-3">
        <h4 class="text-sm font-semibold">处理阶段</h4>
        <div class="space-y-2">
          <div
            v-for="(stage, index) in ['Initialization', 'Analysis', 'KnowledgeRetrieval', 'Drafting', 'Finalizing', 'Rendering']"
            :key="stage"
            class="flex items-center gap-2 text-sm"
          >
            <div
              :class="[
                'w-5 h-5 rounded-full flex items-center justify-center text-xs font-semibold',
                stage === task.currentStage
                  ? 'bg-amber-600 text-white'
                  : ['Initialization', 'Analysis', 'KnowledgeRetrieval', 'Drafting', 'Finalizing', 'Rendering'].indexOf(stage) < ['Initialization', 'Analysis', 'KnowledgeRetrieval', 'Drafting', 'Finalizing', 'Rendering'].indexOf(task.currentStage)
                    ? 'bg-green-600 text-white'
                    : 'bg-muted text-muted-foreground',
              ]"
            >
              <SafeIcon
                v-if="stage === task.currentStage"
                name="Loader2"
                :size="12"
                class="animate-spin"
              />
              <SafeIcon
                v-else-if="['Initialization', 'Analysis', 'KnowledgeRetrieval', 'Drafting', 'Finalizing', 'Rendering'].indexOf(stage) < ['Initialization', 'Analysis', 'KnowledgeRetrieval', 'Drafting', 'Finalizing', 'Rendering'].indexOf(task.currentStage)"
                name="Check"
                :size="12"
              />
              <span v-else>{{ index + 1 }}</span>
            </div>
            <span>{{ getStageLabel(stage) }}</span>
          </div>
        </div>
      </div>

      <!-- 提示信息 -->
      <div class="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-900/50">
        <div class="flex gap-2">
          <SafeIcon name="Info" :size="16" class="text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
          <div class="text-sm text-blue-800 dark:text-blue-300">
            <p>生成过程可能需要几分钟，请勿关闭此页面。</p>
            <p class="mt-1">您可以在此页面监控进度，或稍后返回查看结果。</p>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="flex gap-2 justify-end pt-4">
        <Button variant="outline" @click="$emit('retry')">
          返回配置
        </Button>
      </div>
    </CardContent>
  </Card>
</template>

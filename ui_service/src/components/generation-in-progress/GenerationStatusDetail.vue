<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { fetchLatestGenerationTask } from '@/lib/api'
import type { GenerationTask } from '@/lib/api'

const task = ref<GenerationTask | null>(null)
const projectId = ref<string>('1')

const stages = [
  { id: 'Initialization', label: '初始', description: '准备生成环境' },
  { id: 'Analysis', label: '分析', description: '分析招标文件内容' },
  { id: 'KnowledgeRetrieval', label: '检索', description: '从知识库检索相关内容' },
  { id: 'Drafting', label: '生成', description: '生成投标文档内容' },
  { id: 'Finalizing', label: '整理', description: '处理格式与样式' },
  { id: 'Rendering', label: '输出', description: '输出最终文档' },
]

const getStageStatus = (stageId: string) => {
  if (!task.value) return 'upcoming'
  const currentIndex = stages.findIndex((s) => s.id === task.value?.currentStage)
  const stageIndex = stages.findIndex((s) => s.id === stageId)
  if (stageIndex < currentIndex) return 'completed'
  if (stageIndex === currentIndex) return 'current'
  return 'upcoming'
}

onMounted(async () => {
  projectId.value = new URLSearchParams(window.location.search).get('id') || '1'
  try {
    task.value = await fetchLatestGenerationTask(projectId.value)
  } catch (err) {
    console.error(err)
  }
})
</script>

<template>
  <Card class="mb-6">
    <CardHeader>
      <CardTitle>生成阶段</CardTitle>
      <CardDescription>系统按照以下步骤生成您的投标文件</CardDescription>
    </CardHeader>

    <CardContent>
      <div class="space-y-3">
        <template v-for="(stage, index) in stages" :key="stage.id">
          <div
            class="flex items-start gap-3 p-3 rounded-lg transition-colors"
            :class="{
              'bg-primary/10': getStageStatus(stage.id) === 'current',
              'bg-green-50 dark:bg-green-950/20': getStageStatus(stage.id) === 'completed',
              'opacity-50': getStageStatus(stage.id) === 'upcoming',
            }"
          >
            <div
              class="w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5"
              :class="{
                'bg-primary text-primary-foreground': getStageStatus(stage.id) === 'current',
                'bg-green-600 text-white': getStageStatus(stage.id) === 'completed',
                'bg-muted text-muted-foreground': getStageStatus(stage.id) === 'upcoming',
              }"
            >
              <SafeIcon
                v-if="getStageStatus(stage.id) === 'completed'"
                name="Check"
                :size="14"
                :stroke-width="3"
              />
              <SafeIcon
                v-else-if="getStageStatus(stage.id) === 'current'"
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

            <div class="flex-1 min-w-0">
              <div class="font-medium text-sm">{{ stage.label }}</div>
              <div class="text-xs text-muted-foreground mt-0.5">{{ stage.description }}</div>
            </div>

            <div
              v-if="getStageStatus(stage.id) === 'current'"
              class="text-xs font-medium text-primary whitespace-nowrap ml-2"
            >
              进行中
            </div>
            <div
              v-else-if="getStageStatus(stage.id) === 'completed'"
              class="text-xs font-medium text-green-600 dark:text-green-400 whitespace-nowrap ml-2"
            >
              已完成
            </div>
          </div>

          <div
            v-if="index < stages.length - 1"
            class="ml-3 h-2 w-0.5 bg-border"
          />
        </template>
      </div>
    </CardContent>
  </Card>
</template>

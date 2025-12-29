
<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { GenerationTaskModel } from '@/data/generation'

interface Props {
  task: GenerationTaskModel
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'view-preview': []
  retry: []
  back: []
}>()

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}
</script>

<template>
  <Card class="border-green-200 dark:border-green-900/50">
    <CardHeader>
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <SafeIcon name="CheckCircle2" :size="20" class="text-green-600" />
          <div>
            <CardTitle>生成成功</CardTitle>
            <CardDescription>{{ task.statusMessage }}</CardDescription>
          </div>
        </div>
        <div class="text-right">
          <div class="text-2xl font-bold text-green-600">100%</div>
          <div class="text-xs text-muted-foreground">已完成</div>
        </div>
      </div>
    </CardHeader>

    <CardContent class="space-y-6">
      <!-- 成功信息 -->
      <div class="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-900/50">
        <div class="flex gap-3">
          <SafeIcon name="CheckCircle2" :size="20" class="text-green-600 flex-shrink-0 mt-0.5" />
          <div class="flex-1">
            <h4 class="font-semibold text-green-900 dark:text-green-300 mb-1">投标书已成功生成</h4>
            <p class="text-sm text-green-800 dark:text-green-400">
              您的投标书 Word 文档已准备就绪，可以进行预览或下载。
            </p>
          </div>
        </div>
      </div>

      <!-- 文档信息 -->
      <div class="space-y-3">
        <h4 class="text-sm font-semibold">生成的文档</h4>
        <div class="p-3 bg-muted rounded-lg flex items-center justify-between">
          <div class="flex items-center gap-3">
            <SafeIcon name="FileText" :size="24" class="text-primary" />
            <div>
              <div class="font-medium text-sm">投标书.docx</div>
              <div class="text-xs text-muted-foreground">Word 文档</div>
            </div>
          </div>
          <div class="text-right">
            <div class="text-sm font-medium">约 2.5 MB</div>
            <div class="text-xs text-muted-foreground">已准备下载</div>
          </div>
        </div>
      </div>

      <!-- 章节预览 -->
      <div class="space-y-3">
        <h4 class="text-sm font-semibold">文档结构预览</h4>
        <div class="space-y-2 max-h-48 overflow-y-auto">
          <div v-if="task.generatedToc" class="space-y-1 text-sm">
            <div
              v-for="chapter in task.generatedToc"
              :key="chapter.id"
              class="flex items-center gap-2 p-2 hover:bg-muted rounded transition-colors"
            >
              <SafeIcon name="ChevronRight" :size="16" class="text-muted-foreground flex-shrink-0" />
              <span class="text-muted-foreground font-medium">{{ chapter.index }}</span>
              <span>{{ chapter.title }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="flex gap-2 justify-end pt-4">
        <Button variant="outline" @click="$emit('back')">
          返回项目
        </Button>
        <Button variant="outline" @click="$emit('retry')">
          <SafeIcon name="RotateCcw" :size="16" class="mr-2" />
          重新生成
        </Button>
        <Button @click="$emit('view-preview')">
          <SafeIcon name="Eye" :size="16" class="mr-2" />
          查看预览
        </Button>
      </div>
    </CardContent>
  </Card>
</template>

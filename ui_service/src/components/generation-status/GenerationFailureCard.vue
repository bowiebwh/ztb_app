
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
  retry: []
  back: []
}>()
</script>

<template>
  <Card class="border-red-200 dark:border-red-900/50">
    <CardHeader>
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <SafeIcon name="XCircle" :size="20" class="text-red-600" />
          <div>
            <CardTitle>生成失败</CardTitle>
            <CardDescription>{{ task.statusMessage }}</CardDescription>
          </div>
        </div>
        <div class="text-right">
          <div class="text-2xl font-bold text-red-600">失败</div>
          <div class="text-xs text-muted-foreground">{{ Math.round(task.progress) }}% 时中断</div>
        </div>
      </div>
    </CardHeader>

    <CardContent class="space-y-6">
      <!-- 错误信息 -->
      <div class="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-900/50">
        <div class="flex gap-3">
          <SafeIcon name="AlertCircle" :size="20" class="text-red-600 flex-shrink-0 mt-0.5" />
          <div class="flex-1">
            <h4 class="font-semibold text-red-900 dark:text-red-300 mb-2">生成过程中出现错误</h4>
            <div class="space-y-2">
              <div>
                <div class="text-xs font-medium text-red-800 dark:text-red-400 mb-1">错误信息：</div>
                <div class="text-sm text-red-700 dark:text-red-300 font-mono bg-red-100 dark:bg-red-900/30 p-2 rounded">
                  {{ task.errorMessage || '未知错误' }}
                </div>
              </div>
              <div>
                <div class="text-xs font-medium text-red-800 dark:text-red-400 mb-1">失败阶段：</div>
                <div class="text-sm text-red-700 dark:text-red-300">
                  {{ task.currentStage }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 故障排除建议 -->
      <div class="space-y-3">
        <h4 class="text-sm font-semibold">故障排除建议</h4>
        <ul class="space-y-2 text-sm text-muted-foreground">
          <li class="flex gap-2">
            <SafeIcon name="CheckCircle2" :size="16" class="text-muted-foreground flex-shrink-0 mt-0.5" />
            <span>检查上传的招标文件是否完整和有效</span>
          </li>
          <li class="flex gap-2">
            <SafeIcon name="CheckCircle2" :size="16" class="text-muted-foreground flex-shrink-0 mt-0.5" />
            <span>确保所有必需的占位符已绑定素材</span>
          </li>
          <li class="flex gap-2">
            <SafeIcon name="CheckCircle2" :size="16" class="text-muted-foreground flex-shrink-0 mt-0.5" />
            <span>检查网络连接是否正常</span>
          </li>
          <li class="flex gap-2">
            <SafeIcon name="CheckCircle2" :size="16" class="text-muted-foreground flex-shrink-0 mt-0.5" />
            <span>如问题持续，请联系技术支持</span>
          </li>
        </ul>
      </div>

      <!-- 操作按钮 -->
      <div class="flex gap-2 justify-end pt-4">
        <Button variant="outline" @click="$emit('back')">
          返回项目
        </Button>
        <Button @click="$emit('retry')">
          <SafeIcon name="RotateCcw" :size="16" class="mr-2" />
          重新配置并生成
        </Button>
      </div>
    </CardContent>
  </Card>
</template>

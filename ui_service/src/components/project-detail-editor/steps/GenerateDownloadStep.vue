<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Button } from '@/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { Project, GenerationTask } from '@/lib/api'
import { startGeneration, fetchLatestGenerationTask, API_BASE } from '@/lib/api'

interface Props {
  projectId: string
  project: Project | null
  mode?: 'generate' | 'download'
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'step-change': [stepId: string]
}>()

const outputLanguage = ref('zh-CN')
const outputScope = ref('all')
const task = ref<GenerationTask | null>(null)
const isGenerating = ref(false)
const error = ref('')

const progress = computed(() => Math.round(task.value?.progress ?? 0))
const isCompleted = computed(() => task.value?.status === 'Completed')
const isFailed = computed(() => task.value?.status === 'Failed')
const resultUrl = computed(() => task.value?.resultUrl || '')
const downloadHref = computed(() => {
  if (!resultUrl.value) return ''
  if (resultUrl.value.startsWith('http')) return resultUrl.value
  const base = (API_BASE || '').replace(/\/$/, '')
  return `${base}${resultUrl.value}`
})
const resultName = computed(() => {
  if (!resultUrl.value) return ''
  try {
    const parts = resultUrl.value.split('/')
    return parts[parts.length - 1] || resultUrl.value
  } catch {
    return resultUrl.value
  }
})

const loadLatest = async () => {
  error.value = ''
  try {
    task.value = await fetchLatestGenerationTask(props.projectId)
  } catch (err) {
    // 若不存在任务则静默
    task.value = null
  } finally {
    isGenerating.value = false
  }
}

const handleGenerateClick = async () => {
  error.value = ''
  isGenerating.value = true
  task.value = null
  try {
    task.value = await startGeneration(props.projectId, outputScope.value)
    // 生成接口同步完成后直接展示结果
  } catch (err: any) {
    error.value = err?.message || '启动生成失败'
  } finally {
    isGenerating.value = false
  }
}

const handlePreviousStep = () => {
  emit('step-change', props.mode === 'generate' ? 'analyze_tender_content_step' : 'edit_bid_document_step')
}

const handleDownload = () => {
  if (!downloadHref.value) return
  // 创建隐藏链接并附加到 DOM，确保触发请求
  const link = document.createElement('a')
  link.href = downloadHref.value
  link.target = '_blank'
  link.rel = 'noopener'
  link.style.display = 'none'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onMounted(async () => {
  await loadLatest()
})
</script>

<template>
  <div class="space-y-6">
    <div v-if="error" class="text-sm text-red-500 bg-red-50 border border-red-200 rounded-md p-3">
      {{ error }}
    </div>

    <!-- 配置区 -->
    <div v-if="!isGenerating && !isCompleted" class="space-y-6">
      <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
        <div class="flex gap-3">
          <SafeIcon name="Download" :size="20" class="text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
          <div class="text-sm text-green-900 dark:text-green-300">
            <p class="font-medium mb-1">{{ props.mode === 'generate' ? '生成投标书正文' : '下载文件' }}</p>
            <p>
              {{
                props.mode === 'generate'
                  ? '配置输出选项，点击“开始生成”即可生成投标书正文。'
                  : '如需更新内容请先返回编辑或生成，再在此处下载最新文件。'
              }}
            </p>
          </div>
        </div>
      </div>

      <div class="bg-card border rounded-lg p-6 space-y-6">
        <div>
          <label class="text-sm font-medium mb-2 block">输出语言</label>
          <Select v-model="outputLanguage">
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="zh-CN">中文</SelectItem>
              <SelectItem value="en-US">英文</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div>
          <label class="text-sm font-medium mb-2 block">输出范围</label>
          <Select v-model="outputScope">
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">全部</SelectItem>
              <SelectItem value="technical">技术标</SelectItem>
              <SelectItem value="business">商务标</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div>
          <label class="text-sm font-medium mb-2 block">输出格式</label>
          <div class="p-3 rounded-lg bg-muted text-sm">Word (.docx)</div>
        </div>
      </div>

      <div class="flex gap-3 justify-end pt-4 border-t">
        <Button variant="outline" @click="handlePreviousStep">
          <SafeIcon name="ArrowLeft" :size="16" class="mr-2" />
          上一步
        </Button>
        <Button @click="handleGenerateClick" size="lg">
          <SafeIcon name="Zap" :size="16" class="mr-2" />
          开始生成
        </Button>
      </div>
    </div>

    <!-- 生成中 -->
    <div v-if="isGenerating" class="space-y-6">
      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <div class="flex gap-3">
          <SafeIcon name="Loader2" :size="20" class="text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5 animate-spin" />
          <div class="text-sm text-blue-900 dark:text-blue-300">
            <p class="font-medium mb-1">正在生成投标书...</p>
            <p>系统正在处理您的文件，请稍候。</p>
          </div>
        </div>
      </div>

      <div class="bg-card border rounded-lg p-6 space-y-4">
        <div class="space-y-2">
          <div class="flex items-center justify-between text-sm">
            <span>生成进度</span>
            <span class="font-medium">{{ progress }}%</span>
          </div>
          <div class="w-full bg-muted rounded-full h-3 overflow-hidden">
            <div class="bg-primary h-full transition-all duration-300" :style="{ width: `${progress}%` }" />
          </div>
        </div>
      </div>
    </div>

    <!-- 生成完成 -->
    <div v-if="isCompleted" class="space-y-6">
      <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
        <div class="flex gap-3">
          <SafeIcon name="CheckCircle2" :size="20" class="text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
          <div class="text-sm text-green-900 dark:text-green-300">
            <p class="font-medium mb-1">投标书生成成功！</p>
            <p>{{ props.mode === 'generate' ? '正文已生成，可前往编辑。' : '您的投标书已生成完成，现在可以下载。' }}</p>
          </div>
        </div>
      </div>

      <div class="bg-card border rounded-lg p-6 space-y-4">
        <div>
          <p class="text-sm font-medium mb-2">生成结果</p>
          <div class="flex items-center gap-3 p-3 rounded-lg bg-muted">
            <SafeIcon name="FileText" :size="24" class="text-primary" />
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium">{{ resultName || '生成文件' }}</p>
              <p class="text-xs text-muted-foreground">状态：{{ task?.statusMessage || '已完成' }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="flex gap-3 justify-end pt-4 border-t">
        <Button
          v-if="props.mode === 'generate'"
          variant="outline"
          @click="handleGenerateClick"
          :disabled="isGenerating"
        >
          <SafeIcon name="RefreshCw" :size="16" class="mr-2" />
          重新生成
        </Button>
        <Button v-if="props.mode !== 'generate'" :disabled="!downloadHref" @click="handleDownload">
          <SafeIcon name="Download" :size="16" class="mr-2" />
          下载文件
        </Button>
        <Button v-else @click="emit('step-change', 'edit_bid_document_step')">
          下一步：投标文件编辑
          <SafeIcon name="ArrowRight" :size="16" class="ml-2" />
        </Button>
      </div>
    </div>
  </div>
</template>

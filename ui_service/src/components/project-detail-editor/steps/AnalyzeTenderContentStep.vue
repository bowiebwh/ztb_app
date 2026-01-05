<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { Project } from '@/lib/api'
import { fetchAnalysis, fetchDocument } from '@/lib/api'

interface Props {
  projectId: string
  project: Project | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'step-change': [stepId: string]
}>()

const isClient = ref(true)
const isLoading = ref(false)
const error = ref('')
const analysis = ref<{
  summary: string
  keyDates: Array<{ label: string; date: string }>
  documentStructure: Array<{ id: string; title: string; sections: string[] }>
} | null>(null)
const hasAnalysis = computed(() => !!analysis.value)
const disableNext = computed(() => isLoading.value && !hasAnalysis.value)

// 兼容 LLM 返回的字符串化 JSON（单引号等）
const tryParseLoose = (val: any): any => {
  if (typeof val !== 'string') return null
  let text = val.trim()
  if (!text) return null
  // 去掉首尾括号/元组符号
  if ((text.startsWith('(') && text.endsWith(')')) || (text.startsWith('[') && text.endsWith(']'))) {
    text = text.slice(1, -1)
  }
  const candidates = [text, text.replace(/'/g, '"')]
  for (const c of candidates) {
    try {
      return JSON.parse(c)
    } catch {
      continue
    }
  }
  return null
}

const viewStructure = computed(() =>
  (analysis.value?.documentStructure || []).map((ch: any, idx: number) => {
    const title = ch?.title || ch?.heading || ch?.id || `章节${idx + 1}`
    const sectionsRaw = Array.isArray(ch?.sections) ? ch.sections : []
    const sections = sectionsRaw.map((s: any) => {
      if (typeof s === 'string') {
        const parsed = tryParseLoose(s)
        if (parsed && typeof parsed === 'object') {
          const vals = Object.values(parsed)
            .filter(Boolean)
            .map(v => (Array.isArray(v) ? v.join('；') : typeof v === 'object' ? JSON.stringify(v) : String(v)))
          return vals.join('；')
        }
        return s
      }
      if (Array.isArray(s)) return s.join('；')
      if (s && typeof s === 'object') {
        const val =
          s?.value ||
          s?.title ||
          s?.text ||
          (Array.isArray(s?.content) ? s.content.join('；') : s?.content) ||
          (Array.isArray(s?.details) ? s.details.join('；') : s?.details) ||
          s?.paragraph ||
          s?.body ||
          ''
        return Array.isArray(val) ? val.join('；') : String(val)
      }
      return String(s)
    })
    return { title, sections }
  })
)

const loadCachedAnalysis = async () => {
  isLoading.value = true
  error.value = ''
  try {
    const doc = await fetchDocument(props.projectId)
    const ana = doc?.analysis
    if (ana && (ana.summary || (ana.documentStructure || []).length)) {
      analysis.value = {
        summary: ana.summary || '',
        keyDates: ana.keyDates || [],
        documentStructure: ana.documentStructure || [],
      }
      return
    }
    analysis.value = null
  } catch (err) {
    console.error(err)
    error.value = (err as Error)?.message || '获取招标分析失败'
    analysis.value = null
  } finally {
    isLoading.value = false
  }
}

const runAnalysis = async (refresh = true) => {
  isLoading.value = true
  error.value = ''
  try {
    analysis.value = await fetchAnalysis(props.projectId, refresh)
  } catch (err) {
    console.error(err)
    error.value = (err as Error)?.message || '获取招标分析失败'
    analysis.value = null
  } finally {
    isLoading.value = false
  }
}

const handleNextStep = () => {
  // 仅跳转，生成操作放在生成文档页面的按钮上
  emit('step-change', 'generate_document_step')
}

const handlePreviousStep = () => {
  emit('step-change', 'upload_tender_document_step')
}

const handleReanalyze = async () => {
  const confirmed = window.confirm('检测到已有招标分析结果，是否重新分析并覆盖当前结果？')
  if (!confirmed) return
  await runAnalysis(true)
}

const summaryText = computed(() => {
  const raw = analysis.value?.summary
  if (!raw) return ''
  if (typeof raw === 'string') {
    const parsed = tryParseLoose(raw)
    if (parsed && typeof parsed === 'object') {
      const parts: string[] = []
      if (parsed.paragraph) parts.push(String(parsed.paragraph))
      if (parsed.title) parts.push(String(parsed.title))
      Object.entries(parsed).forEach(([k, v]) => {
        if (k === 'paragraph' || k === 'title') return
        if (v === undefined || v === null) return
        const val = Array.isArray(v) ? v.join('；') : typeof v === 'object' ? JSON.stringify(v) : String(v)
        parts.push(`${k}: ${val}`)
      })
      if (parts.length) return parts.join('\n')
    }
    return raw
  }
  if (typeof raw === 'object') {
    const parts: string[] = []
    if ('paragraph' in raw && raw.paragraph) parts.push(String(raw.paragraph))
    if ('title' in raw && raw.title) parts.push(String(raw.title))
    Object.entries(raw).forEach(([k, v]) => {
      if (k === 'paragraph' || k === 'title') return
      if (v === undefined || v === null) return
      const val = Array.isArray(v) ? v.join('；') : typeof v === 'object' ? JSON.stringify(v) : String(v)
      parts.push(`${k}: ${val}`)
    })
    if (parts.length) return parts.join('\n')
    try {
      return JSON.stringify(raw, null, 2)
    } catch {
      return String(raw)
    }
  }
  return String(raw)
})

onMounted(async () => {
  isClient.value = false
  let autoRun = false
  if (typeof window !== 'undefined') {
    autoRun = window.sessionStorage.getItem('autoRunAnalysis') === '1'
    if (autoRun) {
      window.sessionStorage.removeItem('autoRunAnalysis')
    }
  }
  await loadCachedAnalysis()
  // 仅在上传后自动触发一次刷新，其余场景不调用分析接口，直接展示缓存
  if (autoRun) {
    await runAnalysis(true)
  }
  requestAnimationFrame(() => {
    isClient.value = true
  })
})
</script>

<template>
  <div class="space-y-6">
    <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
      <div class="flex gap-3 items-start">
        <SafeIcon name="Cpu" :size="20" class="text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
        <div class="text-sm">
          <p class="font-medium mb-1">招标内容解析</p>
          <p class="text-blue-900 dark:text-blue-300">
            系统从上传的招标文件中提取关键要点，供后续生成使用。
          </p>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="text-sm text-muted-foreground">分析中...</div>
    <div v-else-if="error" class="text-sm text-red-500">{{ error }}</div>
    <div v-else-if="!analysis" class="text-sm text-muted-foreground bg-muted/40 border border-dashed rounded p-4">
      暂无分析结果，请点击“重新分析”或继续下一步。
    </div>

    <div class="flex justify-end" :class="{ 'mt-2': analysis || error }">
      <Button variant="outline" size="sm" @click="handleReanalyze" :disabled="isLoading">
        重新分析
      </Button>
    </div>

    <template v-if="analysis">
      <div class="bg-card border rounded-lg p-4 space-y-4">
        <h3 class="font-semibold">分析概要</h3>
        <p class="text-sm text-muted-foreground leading-relaxed whitespace-pre-line">{{ summaryText }}</p>
      </div>

      <div class="bg-card border rounded-lg p-4 space-y-3">
        <h3 class="font-semibold">关键日期</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
          <div v-for="item in analysis.keyDates" :key="item.label" class="flex items-center gap-2">
            <SafeIcon name="Calendar" :size="16" class="text-primary" />
            <div>
              <p class="font-medium">{{ item.label }}</p>
              <p class="text-muted-foreground">{{ item.date }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-card border rounded-lg p-4 space-y-3">
        <h3 class="font-semibold">初步章节结构</h3>
        <div class="space-y-3">
          <div
            v-for="(chapter, idx) in viewStructure"
            :key="chapter.title || idx"
            class="border rounded-lg p-3 space-y-2"
          >
            <p class="font-medium mb-1">{{ chapter.title }}</p>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="section in chapter.sections"
                :key="section"
                class="px-2 py-1 text-xs rounded bg-muted text-muted-foreground"
              >
                {{ section }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </template>

    <div class="flex gap-3 justify-end pt-4 border-t">
      <Button variant="outline" @click="handlePreviousStep">
        <SafeIcon name="ArrowLeft" :size="16" class="mr-2" />
        上一步
      </Button>
      <Button @click="handleNextStep" :disabled="disableNext">
        下一步：生成文档
        <SafeIcon name="ArrowRight" :size="16" class="ml-2" />
      </Button>
    </div>
  </div>
</template>

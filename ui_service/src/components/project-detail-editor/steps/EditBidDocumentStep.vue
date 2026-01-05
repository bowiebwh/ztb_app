<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { Project } from '@/lib/api'
import {
  fetchDocumentStructure,
  fetchMaterialBindings,
  bindMaterial,
  saveDocumentStructure,
  exportCurrentDocument,
  deleteMaterialBinding,
} from '@/lib/api'

interface Props {
  projectId: string
  project: Project | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'step-change': [stepId: string]
  'open-material-library': []
}>()

// State
const isClient = ref(true)
const structure = ref<any[]>([])
const bindings = ref<any[]>([])
const loading = ref(false)
const bindingError = ref('')
const bindingSuccess = ref('')
const manualPlaceholders = ref<string[]>([])
const newPlaceholder = ref('')
const saving = ref(false)
const placeholderPage = ref(1)
const placeholderPageSize = ref(24)

const loadData = async () => {
  loading.value = true
  bindingError.value = ''
  bindingSuccess.value = ''
  try {
    const structRes = await fetchDocumentStructure(props.projectId)
    const raw = Array.isArray(structRes?.content) ? structRes.content : []
    // 确保每个章节都有 body 字段；如无则将 sections 拼成正文，便于回填展示
    structure.value = raw.map((item: any) => {
      const bodyExisting = item?.body
      let bodyText = typeof bodyExisting === 'string' ? bodyExisting : ''
      if (!bodyText) {
        const sections = Array.isArray(item?.sections) ? item.sections : []
        bodyText = sections
          .map((s: any) => {
            if (typeof s === 'string') return s
            if (s && typeof s === 'object') {
              if (Array.isArray(s.content)) {
                return s.content.map((x: any) => (typeof x === 'string' ? x : x?.value || '')).join('\n')
              }
              return s.body || s.content || s.title || s.text || ''
            }
            return ''
          })
          .filter(Boolean)
          .join('\n')
      }
      return {
        ...item,
        title: item?.title || item?.heading,
        heading: item?.heading || item?.title,
        body: bodyText,
      }
    })
    bindings.value = await fetchMaterialBindings(props.projectId)
  } catch (err) {
    console.error('加载文件结构或占位符绑定失败', err)
    structure.value = []
    bindings.value = []
  } finally {
    loading.value = false
  }
}

const handleOpenMaterialLibrary = () => {
  emit('open-material-library')
}

const handlePreviousStep = () => {
  emit('step-change', 'analyze_tender_content_step')
}

const placeholderKeys = computed(() => {
  const keys = new Set<string>()
  bindings.value.forEach((b: any) => {
    if (b.placeholderKey) keys.add(String(b.placeholderKey))
  })
  const regex = /\{\{\s*([^}]+)\s*\}\}/g
  const scan = (val: any) => {
    if (typeof val === 'string') {
      let m
      while ((m = regex.exec(val))) {
        if (m[1]) keys.add(m[1])
      }
    } else if (Array.isArray(val)) {
      val.forEach(scan)
    } else if (val && typeof val === 'object') {
      Object.values(val).forEach(scan)
    }
  }
  scan(structure.value)
  manualPlaceholders.value.forEach(k => keys.add(k))
  const arr = Array.from(keys)
  // 閲嶇疆椤电爜閬垮厤瓒婄晫
  const maxPage = Math.max(1, Math.ceil(arr.length / placeholderPageSize.value))
  if (placeholderPage.value > maxPage) placeholderPage.value = maxPage
  return arr
})

const placeholderPaged = computed(() => {
  const start = (placeholderPage.value - 1) * placeholderPageSize.value
  return placeholderKeys.value.slice(start, start + placeholderPageSize.value)
})

const placeholderTotalPages = computed(() =>
  Math.max(1, Math.ceil(placeholderKeys.value.length / placeholderPageSize.value))
)

const findBinding = (key: string) =>
  bindings.value.find((b: any) => String(b.placeholderKey) === String(key))

const findBindingName = (key: string) => {
  const b = findBinding(key)
  if (!b) return ''
  return b.materialName || b.materialId || ''
}

const allowDrop = (event: DragEvent) => {
  event.preventDefault()
  event.dataTransfer && (event.dataTransfer.dropEffect = 'copy')
}

const handleDropOnPlaceholder = async (placeholderKey: string, event: DragEvent) => {
  event.preventDefault()
  bindingError.value = ''
  bindingSuccess.value = ''
  try {
    const data = event.dataTransfer?.getData('application/json')
    if (!data) {
      bindingError.value = '拖拽数据为空'
      return
    }
    const parsed = JSON.parse(data)
    if (parsed.type !== 'material' || !parsed.materialId) {
      bindingError.value = '仅支持从素材库拖拽文件'
      return
    }
    await bindMaterial({
      projectId: props.projectId,
      placeholderKey,
      materialId: parsed.materialId,
    })
    bindingSuccess.value = `已绑定占位符 ${placeholderKey} 到素材 ${parsed.materialName || parsed.materialId}`
    bindings.value = await fetchMaterialBindings(props.projectId)
  } catch (err: any) {
    console.error('绑定占位符失败', err)
    bindingError.value = err?.message || '绑定占位符失败'
  }
}

const addPlaceholder = () => {
  bindingError.value = ''
  bindingSuccess.value = ''
  const key = newPlaceholder.value.trim()
  if (!key) {
    bindingError.value = '请输入占位符名称'
    return
  }
  if (!manualPlaceholders.value.includes(key)) {
    manualPlaceholders.value.push(key)
  }
  newPlaceholder.value = ''
}

const goPlaceholderPage = (target: number) => {
  const next = Math.min(Math.max(1, target), placeholderTotalPages.value)
  placeholderPage.value = next
}

const handleDeleteBinding = async (bindingId: string | number) => {
  try {
    await deleteMaterialBinding(bindingId)
    bindings.value = await fetchMaterialBindings(props.projectId)
  } catch (err: any) {
    console.error('删除占位符绑定失败', err)
    bindingError.value = err?.message || '删除占位符绑定失败'
  }
}

const handleSaveAndExport = async (goNext: boolean = false) => {
  saving.value = true
  bindingError.value = ''
  bindingSuccess.value = ''
  try {
    await saveDocumentStructure(props.projectId, structure.value)
    await exportCurrentDocument(props.projectId)
    bindingSuccess.value = '正文已保存并生成最新下载文件'
    if (goNext) {
      emit('step-change', 'generate_download_step')
    }
  } catch (err: any) {
    console.error('保存或导出失败', err)
    bindingError.value = err?.message || '保存或导出失败'
  } finally {
    saving.value = false
  }
}

// Lifecycle
onMounted(() => {
  isClient.value = false
  loadData()
  requestAnimationFrame(() => {
    isClient.value = true
  })
})
</script>

<template>
  <div class="space-y-6">
    <!-- Instructions -->
    <div class="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4">
      <div class="flex gap-3">
        <SafeIcon name="BookOpen" :size="20" class="text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
        <div class="text-sm text-amber-900 dark:text-amber-300">
          <p class="font-medium mb-1">编辑招标文件内容与占位符绑定</p>
          <p>您可以在下方修改 AI 解析出的文件结构和正文，并在正文中使用占位符替换需要填写的内容。</p>
        </div>
      </div>
    </div>

    <!-- 占位符管理 -->
    <div class="bg-card border rounded-lg p-4 space-y-4">
      <div class="flex items-center justify-between gap-3">
        <h3 class="font-semibold">占位符管理</h3>
        <div class="flex items-center gap-2">
          <input
            v-model="newPlaceholder"
            type="text"
            placeholder="新增占位符，如 material:company_intro"
            class="h-9 rounded border px-3 text-sm"
          />
          <Button size="sm" variant="outline" @click="addPlaceholder">
            <SafeIcon name="Plus" :size="14" class="mr-1" />
            添加
          </Button>
        </div>
      </div>
      <div v-if="loading" class="text-sm text-muted-foreground">加载中...</div>
      <div v-else class="space-y-3">
        <div class="text-xs text-muted-foreground">
          提示：从右侧素材库拖拽文件到下方占位符卡片，即可绑定。也可手动新增占位符。
        </div>
        <div v-if="bindingError" class="text-sm text-red-500">{{ bindingError }}</div>
        <div v-if="bindingSuccess" class="text-sm text-green-600">{{ bindingSuccess }}</div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2">
          <div
            v-for="key in placeholderPaged"
            :key="key"
            class="p-1.5 rounded-lg border border-dashed hover:border-primary/60 transition-colors bg-muted/30 flex flex-col gap-1 h-[60px]"
            @dragover="allowDrop"
            @drop="handleDropOnPlaceholder(key, $event)"
          >
            <div class="flex items-center gap-2">
              <SafeIcon name="Package" :size="16" class="text-primary" />
              <p class="text-xs font-medium truncate" :title="key">{{ key }}</p>
              <span
                class="text-[10px] px-1.5 py-0.5 rounded-full"
                :class="findBinding(key) ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'"
              >
                {{ findBinding(key) ? '已绑定' : '未绑定' }}
              </span>
            </div>
            <div class="flex items-center justify-between">
              <p class="text-xs text-muted-foreground truncate" :title="findBindingName(key)">
                {{ findBinding(key) ? findBindingName(key) : '拖拽素材到此处进行绑定' }}
              </p>
              <Button
                v-if="findBinding(key)"
                size="sm"
                variant="ghost"
                class="text-red-500 h-7 px-2"
                @click="handleDeleteBinding(findBinding(key)?.bindingId)"
              >
                删除
              </Button>
            </div>
          </div>
        </div>
        <div v-if="!placeholderKeys.length" class="text-sm text-muted-foreground">
          暂无占位符，可添加新占位符或从正文中加入 {{placeholder}} 触发识别。
        </div>
        <div v-else class="flex items-center justify-end gap-2 text-xs text-muted-foreground">
          <Button variant="outline" size="sm" :disabled="placeholderPage <= 1" @click="goPlaceholderPage(placeholderPage - 1)">
            上一页
          </Button>
          <span>{{ placeholderPage }} / {{ placeholderTotalPages }}</span>
          <Button variant="outline" size="sm" :disabled="placeholderPage >= placeholderTotalPages" @click="goPlaceholderPage(placeholderPage + 1)">
            下一页
          </Button>
        </div>
      </div>
    </div>

    <div class="bg-card border rounded-lg p-4 space-y-4">
      <div class="flex items-center justify-between">
        <h3 class="font-semibold">文件结构</h3>
        <div class="flex items-center gap-2">
          <Button size="sm" variant="outline" @click="loadData" :disabled="loading">
            <SafeIcon name="RefreshCw" :size="14" class="mr-1" />
            重新加载
          </Button>
          <Button size="sm" @click="handleSaveAndExport()" :disabled="saving || loading">
            <SafeIcon name="Save" :size="14" class="mr-1" />
            {{ saving ? '保存中...' : '保存正文' }}
          </Button>
        </div>
      </div>
      <div v-if="loading" class="text-sm text-muted-foreground">加载中...</div>
      <div v-else-if="!structure.length" class="text-sm text-muted-foreground">
        未加载到文件结构，请尝试重新上传招标文件或手动添加。
      </div>
      <div v-else class="space-y-4">
        <div
          v-for="(item, idx) in structure"
          :key="item.id || idx"
          class="rounded-lg border p-3 space-y-2 bg-muted/30"
        >
          <div class="flex items-center gap-2">
            <SafeIcon name="ChevronRight" :size="16" class="text-muted-foreground" />
            <input
              :value="item.title || item.heading"
              @input="(e: any) => { item.title = e?.target?.value; item.heading = e?.target?.value }"
              class="flex-1 bg-transparent border-none outline-none text-sm font-medium"
              :placeholder="`章节 ${idx + 1}`"
            />
          </div>
          <textarea
            v-model="item.body"
            class="w-full h-32 text-sm rounded border px-3 py-2 bg-white"
            placeholder="在此处填写或修改正文内容，可使用 {{material:xxx}} 占位符"
          />
        </div>
      </div>
    </div>

        <!-- Tips -->
    <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
      <div class="flex gap-3">
        <SafeIcon name="Lightbulb" :size="20" class="text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
        <div class="text-sm text-blue-900 dark:text-blue-300">
          <p class="font-medium mb-2">小贴士</p>
          <ul class="space-y-1 list-disc list-inside">
            <li>点击右侧“素材库”按钮可打开素材库，查看和管理您的素材文件。</li>
            <li>正文中的占位符需与素材库中的内容进行绑定才能替换。</li>
            <li>目前支持的格式包括 PDF、Word、Excel 等。</li>
            <li>修改后请务必点击“保存并生成下载”按钮。</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-3 justify-end pt-4 border-t">
      <Button variant="outline" @click="handlePreviousStep">
        <SafeIcon name="ArrowLeft" :size="16" class="mr-2" />
        上一步
      </Button>
      <Button variant="outline" @click="handleOpenMaterialLibrary" class="md:hidden">
        <SafeIcon name="Package" :size="16" class="mr-2" />
        素材库
      </Button>
      <Button @click="handleSaveAndExport(true)" :disabled="saving || loading">
        {{ saving ? '保存中...' : '保存并生成下载' }}
        <SafeIcon name="ArrowRight" :size="16" class="ml-2" />
      </Button>
    </div>
  </div>
</template>




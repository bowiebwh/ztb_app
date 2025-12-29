<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import SafeIcon from '@/components/common/SafeIcon.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import type { Material } from '@/lib/api'
import { fetchMaterials, uploadMaterial } from '@/lib/api'

interface Props {
  projectId: string
}

defineProps<Props>()

const emit = defineEmits<{
  close: []
}>()

const isClient = ref(true)
const searchQuery = ref('')
const selectedType = ref<'all' | 'Image' | 'PDF' | 'Word' | 'Excel'>('all')
const isUploading = ref(false)
const materials = ref<Material[]>([])
const error = ref('')

const filteredMaterials = computed(() => {
  return materials.value.filter(material => {
    const matchesSearch = material.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesType = selectedType.value === 'all' || material.type === selectedType.value
    return matchesSearch && matchesType
  })
})

const materialsByType = computed(() => {
  return {
    Image: filteredMaterials.value.filter(m => m.type === 'Image'),
    PDF: filteredMaterials.value.filter(m => m.type === 'PDF'),
    Word: filteredMaterials.value.filter(m => m.type === 'Word'),
    Excel: filteredMaterials.value.filter(m => m.type === 'Excel'),
  }
})

const getTypeIcon = (type: string): string => {
  const icons: Record<string, string> = {
    Image: 'Image',
    PDF: 'FileText',
    Word: 'FileText',
    Excel: 'Table2',
  }
  return icons[type] || 'File'
}

const getTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    Image: '图片',
    PDF: 'PDF',
    Word: 'Word',
    Excel: 'Excel',
  }
  return labels[type] || type
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

const formatDate = (dateString: string): string => {
  if (typeof window === 'undefined') return dateString
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const handleUpload = async (event?: Event) => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.png,.jpg,.jpeg,.webp,.pdf,.doc,.docx,.txt,.md,.xls,.xlsx'
  input.onchange = async () => {
    const file = input.files?.[0]
    if (!file) return
    isUploading.value = true
    error.value = ''
    try {
      await uploadMaterial(file)
      await loadMaterials()
    } catch (err) {
      console.error(err)
      error.value = '上传失败'
    } finally {
      isUploading.value = false
    }
  }
  input.click()
}

const handleDragStart = (material: Material, event: DragEvent) => {
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'copy'
    event.dataTransfer.setData('application/json', JSON.stringify({
      type: 'material',
      materialId: material.materialId,
      materialType: material.type,
      materialName: material.name,
    }))
  }
}

const loadMaterials = async () => {
  error.value = ''
  try {
    materials.value = await fetchMaterials()
  } catch (err) {
    console.error(err)
    error.value = '加载素材失败'
  }
}

onMounted(async () => {
  isClient.value = false
  await loadMaterials()
  requestAnimationFrame(() => {
    isClient.value = true
  })
})
</script>

<template>
  <div class="flex flex-col h-full bg-card">
    <div class="border-b bg-muted/30 px-4 py-3 flex-shrink-0">
      <div class="flex items-center justify-between mb-3">
        <h3 class="font-semibold">素材库</h3>
        <button
          @click="emit('close')"
          class="md:hidden p-1 hover:bg-muted rounded transition-colors"
          aria-label="关闭素材库"
        >
          <SafeIcon name="X" :size="20" />
        </button>
      </div>
      <Input
        v-model="searchQuery"
        placeholder="搜索素材..."
        class="h-8 text-sm"
      />
    </div>

    <div class="border-b px-4 py-3 flex-shrink-0">
      <Button
        @click="handleUpload"
        :disabled="isUploading"
        class="w-full"
        size="sm"
      >
        <SafeIcon name="Upload" :size="16" class="mr-2" />
        {{ isUploading ? '上传中...' : '上传文件' }}
      </Button>
    </div>

    <div class="flex-1 overflow-hidden flex flex-col">
      <Tabs
        v-model="selectedType"
        class="flex-1 flex flex-col overflow-hidden"
        default-value="all"
      >
        <TabsList class="w-full rounded-none border-b bg-transparent p-0 h-auto">
          <TabsTrigger
            value="all"
            class="rounded-none border-b-2 border-transparent data-[state=active]:border-primary"
          >
            全部
          </TabsTrigger>
          <TabsTrigger value="Image" class="rounded-none border-b-2 border-transparent data-[state=active]:border-primary">
            图片
          </TabsTrigger>
          <TabsTrigger value="PDF" class="rounded-none border-b-2 border-transparent data-[state=active]:border-primary">
            PDF
          </TabsTrigger>
          <TabsTrigger value="Excel" class="rounded-none border-b-2 border-transparent data-[state=active]:border-primary">
            表格
          </TabsTrigger>
          <TabsTrigger value="Word" class="rounded-none border-b-2 border-transparent data-[state=active]:border-primary">
            Word
          </TabsTrigger>
        </TabsList>

        <TabsContent value="all" class="flex-1 overflow-y-auto p-3 space-y-2">
          <template v-if="filteredMaterials.length > 0">
            <div
              v-for="material in filteredMaterials"
              :key="material.materialId"
              draggable="true"
              @dragstart="handleDragStart(material, $event)"
              class="p-2 rounded-lg border border-border hover:bg-muted/50 cursor-move transition-colors group"
            >
              <div class="flex items-start gap-2">
                <div class="flex-shrink-0 w-8 h-8 rounded bg-muted flex items-center justify-center">
                  <SafeIcon :name="getTypeIcon(material.type)" :size="16" class="text-muted-foreground" />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-xs font-medium truncate">{{ material.name }}</p>
                  <p class="text-xs text-muted-foreground">{{ formatFileSize(material.size) }}</p>
                  <a :href="material.url" target="_blank" class="text-xs text-primary hover:underline">下载</a>
                </div>
              </div>
            </div>
          </template>
          <div v-else class="flex items-center justify-center h-full">
            <EmptyState
              v-if="!error"
              icon="Inbox"
              title="暂无素材"
              description="上传文件到素材库，随后可拖拽到文档占位符。"
            />
            <div v-else class="text-sm text-red-500">{{ error }}</div>
          </div>
        </TabsContent>

        <TabsContent value="Image" class="flex-1 overflow-y-auto p-3 space-y-2">
          <template v-if="materialsByType.Image.length > 0">
            <div
              v-for="material in materialsByType.Image"
              :key="material.materialId"
              draggable="true"
              @dragstart="handleDragStart(material, $event)"
              class="p-2 rounded-lg border border-border hover:bg-muted/50 cursor-move transition-colors"
            >
              <div class="flex items-start gap-2">
                <div class="flex-shrink-0 w-12 h-12 rounded bg-muted flex items-center justify-center overflow-hidden">
                  <img
                    v-if="material.url && material.url.startsWith('http')"
                    :src="material.url"
                    :alt="material.name"
                    class="w-full h-full object-cover"
                  />
                  <SafeIcon v-else name="Image" :size="20" class="text-muted-foreground" />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-xs font-medium truncate">{{ material.name }}</p>
                  <p class="text-xs text-muted-foreground">{{ formatFileSize(material.size) }}</p>
                  <a :href="material.url" target="_blank" class="text-xs text-primary hover:underline">下载</a>
                </div>
              </div>
            </div>
          </template>
          <div v-else class="flex items-center justify-center h-full">
            <EmptyState icon="Image" title="暂无图片" />
          </div>
        </TabsContent>

        <TabsContent value="PDF" class="flex-1 overflow-y-auto p-3 space-y-2">
          <template v-if="materialsByType.PDF.length > 0">
            <div
              v-for="material in materialsByType.PDF"
              :key="material.materialId"
              draggable="true"
              @dragstart="handleDragStart(material, $event)"
              class="p-2 rounded-lg border border-border hover:bg-muted/50 cursor-move transition-colors"
            >
              <div class="flex items-start gap-2">
                <div class="flex-shrink-0 w-8 h-8 rounded bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
                  <SafeIcon name="FileText" :size="16" class="text-red-600 dark:text-red-400" />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-xs font-medium truncate">{{ material.name }}</p>
                  <p class="text-xs text-muted-foreground">{{ formatFileSize(material.size) }}</p>
                </div>
              </div>
            </div>
          </template>
          <div v-else class="flex items-center justify-center h-full">
            <EmptyState icon="FileText" title="暂无PDF" />
          </div>
        </TabsContent>

        <TabsContent value="Excel" class="flex-1 overflow-y-auto p-3 space-y-2">
          <template v-if="materialsByType.Excel.length > 0">
            <div
              v-for="material in materialsByType.Excel"
              :key="material.materialId"
              draggable="true"
              @dragstart="handleDragStart(material, $event)"
              class="p-2 rounded-lg border border-border hover:bg-muted/50 cursor-move transition-colors"
            >
              <div class="flex items-start gap-2">
                <div class="flex-shrink-0 w-8 h-8 rounded bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                  <SafeIcon name="Table2" :size="16" class="text-green-600 dark:text-green-400" />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-xs font-medium truncate">{{ material.name }}</p>
                  <p class="text-xs text-muted-foreground">{{ formatFileSize(material.size) }}</p>
                </div>
              </div>
            </div>
          </template>
          <div v-else class="flex items-center justify-center h-full">
            <EmptyState icon="Table2" title="暂无表格" />
          </div>
        </TabsContent>

        <TabsContent value="Word" class="flex-1 overflow-y-auto p-3 space-y-2">
          <template v-if="materialsByType.Word.length > 0">
            <div
              v-for="material in materialsByType.Word"
              :key="material.materialId"
              draggable="true"
              @dragstart="handleDragStart(material, $event)"
              class="p-2 rounded-lg border border-border hover:bg-muted/50 cursor-move transition-colors"
            >
              <div class="flex items-start gap-2">
                <div class="flex-shrink-0 w-8 h-8 rounded bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                  <SafeIcon name="FileText" :size="16" class="text-blue-600 dark:text-blue-400" />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-xs font-medium truncate">{{ material.name }}</p>
                  <p class="text-xs text-muted-foreground">{{ formatFileSize(material.size) }}</p>
                </div>
              </div>
            </div>
          </template>
          <div v-else class="flex items-center justify-center h-full">
            <EmptyState icon="FileText" title="暂无Word" />
          </div>
        </TabsContent>
      </Tabs>
    </div>

    <div class="border-t bg-muted/30 px-4 py-2 flex-shrink-0 text-xs text-muted-foreground">
      <p>提示：拖拽素材到文档占位符进行替换</p>
    </div>
  </div>
</template>

<style scoped>
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: hsl(var(--muted));
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--muted-foreground));
}
</style>

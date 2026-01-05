<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ChapterNavigator from './ChapterNavigator.vue'
import EditorContent from './EditorContent.vue'
import MaterialLibraryPanel from './MaterialLibraryPanel.vue'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { fetchDocumentStructure, saveDocumentStructure, fetchMaterials, fetchMaterialBindings, bindMaterial } from '@/lib/api'
import type { DocumentNodeModel } from '@/data/document'

const documentContent = ref<DocumentNodeModel[]>([])
const materials = ref<any[]>([])
const bindings = ref<any[]>([])
const selectedChapterId = ref<string>('1')
const draggedMaterial = ref<any | null>(null)
const dragOverPlaceholder = ref<string | null>(null)
const isClient = ref(true)
const projectId = ref<string>('1')

const loadData = async () => {
  projectId.value = new URLSearchParams(window.location.search).get('id') || '1'
  documentContent.value = (await fetchDocumentStructure(projectId.value)).content || []
  const res = await fetchMaterials({ pageSize: 100 })
  materials.value = res.items || []
  bindings.value = await fetchMaterialBindings(projectId.value)
}

const bindMaterialToPlaceholder = async (placeholderKey: string, material: any) => {
  await bindMaterial({
    projectId: projectId.value,
    placeholderKey,
    materialId: material.materialId,
  })
  const bindInContent = (nodes: DocumentNodeModel[]): boolean => {
    for (let i = 0; i < nodes.length; i++) {
      const node: any = nodes[i]
      if (node.type === 'chapter' && node.children) {
        if (bindInContent(node.children)) return true
      } else if (node.type === 'paragraph' && node.children) {
        for (let j = 0; j < node.children.length; j++) {
          const child = node.children[j] as any
          if ((child.type === 'image_placeholder' || child.type === 'table_placeholder') && child.key === placeholderKey) {
            node.children[j] = {
              type: 'image',
              placeholderKey: placeholderKey,
              materialId: material.materialId,
              styleRef: 'FIGURE_STANDARD_W600',
              preview: { url: material.url, name: material.name },
            }
            return true
          }
        }
      }
    }
    return false
  }
  bindInContent(documentContent.value)
  await saveDocumentStructure(projectId.value, documentContent.value)
}

const handleDragStart = (material: any) => {
  draggedMaterial.value = material
}
const handleDragOver = (placeholderKey: string) => {
  dragOverPlaceholder.value = placeholderKey
}
const handleDragLeave = () => {
  dragOverPlaceholder.value = null
}
const handleDrop = (placeholderKey: string) => {
  if (draggedMaterial.value) {
    bindMaterialToPlaceholder(placeholderKey, draggedMaterial.value)
  }
  draggedMaterial.value = null
  dragOverPlaceholder.value = null
}

const goBack = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './edit-bid-document-step.html'
  }
}

onMounted(async () => {
  isClient.value = false
  try {
    await loadData()
  } catch (err) {
    console.error(err)
  }
  requestAnimationFrame(() => {
    isClient.value = true
  })
})
</script>

<template>
  <div class="flex h-[calc(100vh-64px)] bg-background">
    <div class="w-64 border-r bg-card overflow-y-auto">
      <ChapterNavigator
        :chapters="documentContent"
        :selected-chapter-id="selectedChapterId"
        @select-chapter="selectedChapterId = $event"
      />
    </div>

    <div class="flex-1 flex flex-col overflow-hidden">
      <div class="border-b bg-card px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <SafeIcon name="FileText" :size="20" class="text-primary" />
          <h1 class="text-lg font-semibold">结构化文档编辑器</h1>
        </div>
        <Button variant="outline" size="sm" @click="goBack">
          <SafeIcon name="ArrowLeft" :size="16" class="mr-2" />
          返回
        </Button>
      </div>

      <div class="flex-1 overflow-y-auto p-6">
        <EditorContent
          :document-content="documentContent"
          :selected-chapter="null"
          :dragged-material="draggedMaterial"
          :drag-over-placeholder="dragOverPlaceholder"
          :is-client="isClient"
          @drag-over="handleDragOver"
          @drag-leave="handleDragLeave"
          @drop="handleDrop"
        />
      </div>
    </div>

    <div class="w-80 border-l bg-card overflow-y-auto">
      <MaterialLibraryPanel
        :materials="materials"
        :dragged-material="draggedMaterial"
        :is-client="isClient"
        @drag-start="handleDragStart"
        @drag-end="draggedMaterial = null"
      />
    </div>
  </div>
</template>

<style scoped>
:deep(.placeholder-drag-over) {
  @apply bg-primary/10 border-primary;
}
</style>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { WORKFLOW_STEPS } from '@/data/config'
import ProcessNavigation from './ProcessNavigation.vue'
import DocumentEditor from './DocumentEditor.vue'
import MaterialLibraryPanel from './MaterialLibraryPanel.vue'
import { fetchDocumentStructure, saveDocumentStructure, fetchMaterials, fetchMaterialBindings, bindMaterial } from '@/lib/api'

const isClient = ref(true)
const currentProjectId = ref('1')
const documentContent = ref<any[]>([])
const documentStructure = ref<any[]>([])
const materials = ref<any[]>([])
const bindings = ref<any[]>([])
const draggedMaterial = ref<string | null>(null)

const normalizeContent = (content: any[]): any[] => {
  if (!Array.isArray(content)) return []
  return content.map((item, idx) => {
    if (item && item.type) return item
    const title = item?.heading || item?.title || `章节${idx + 1}`
    const body = item?.body || (Array.isArray(item?.sections) ? item.sections.join('\n') : '')
    return {
      type: 'chapter',
      title,
      index: String(idx + 1),
      children: body
        ? [
            {
              type: 'paragraph',
              children: [{ type: 'text', value: body }],
            },
          ]
        : [],
    }
  })
}

const handleMaterialDragStart = (materialId: string) => {
  draggedMaterial.value = materialId
}

const handleMaterialDragEnd = () => {
  draggedMaterial.value = null
}

const handlePlaceholderDrop = async (placeholderKey: string) => {
  if (!draggedMaterial.value) return
  const material = materials.value.find((m) => m.materialId === draggedMaterial.value)
  if (!material) return
  await bindMaterial({
    projectId: currentProjectId.value,
    placeholderKey,
    materialId: material.materialId,
  })
  const updateNode = (node: any): any => {
    if (Array.isArray(node)) return node.map(updateNode)
    if (node.type === 'image_placeholder' && node.key === placeholderKey) {
      return {
        type: 'image',
        placeholderKey: node.key,
        materialId: material.materialId,
        styleRef: 'FIGURE_STANDARD_W600',
        preview: {
          name: material.name,
          url: material.url,
        },
      }
    }
    if (node.children && Array.isArray(node.children)) {
      return { ...node, children: node.children.map(updateNode) }
    }
    return node
  }
  documentContent.value = documentContent.value.map(updateNode)
  await saveDocumentStructure(currentProjectId.value, documentContent.value, documentStructure.value)
  draggedMaterial.value = null
}

onMounted(async () => {
  isClient.value = false
  currentProjectId.value = new URLSearchParams(window.location.search).get('id') || '1'
  try {
    const docRes = await fetchDocumentStructure(currentProjectId.value)
    const rawContent = Array.isArray(docRes.content) ? docRes.content : []
    const rawStructure = Array.isArray(docRes.structure) ? docRes.structure : []
    documentStructure.value = rawStructure
    documentContent.value = normalizeContent(rawContent.length ? rawContent : rawStructure)
    materials.value = await fetchMaterials()
    bindings.value = await fetchMaterialBindings(currentProjectId.value)
  } catch (err) {
    console.error(err)
  }
  requestAnimationFrame(() => {
    isClient.value = true
  })
})
</script>

<template>
  <div class="flex h-full w-full bg-background">
    <div class="w-64 border-r bg-sidebar flex flex-col">
      <ProcessNavigation :steps="WORKFLOW_STEPS" current-step="edit_bid_document_step" />
    </div>

    <div class="flex-1 flex flex-col overflow-hidden">
      <DocumentEditor
        :document-content="documentContent"
        :is-client="isClient || draggedMaterial !== null"
        @placeholder-drop="handlePlaceholderDrop"
      />
    </div>

    <div class="w-80 border-l bg-sidebar flex flex-col">
      <MaterialLibraryPanel
        :materials="materials"
        :dragged-material="draggedMaterial"
        :is-client="isClient"
        @material-drag-start="handleMaterialDragStart"
        @material-drag-end="handleMaterialDragEnd"
      />
    </div>
  </div>
</template>

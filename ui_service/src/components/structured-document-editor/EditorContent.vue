
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { DocumentNodeModel, ChapterNode, ParagraphNode, RichTextNode, PlaceholderModel, BoundImageNode } from '@/data/document'
import type { MaterialModel } from '@/data/materials'
import { cn } from '@/lib/utils'
import PlaceholderRenderer from './PlaceholderRenderer.vue'
import TextEditableNode from './TextEditableNode.vue'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  documentContent: DocumentNodeModel[]
  selectedChapter: ChapterNode | null
  draggedMaterial: MaterialModel | null
  dragOverPlaceholder: string | null
  isClient: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'drag-over': [placeholderKey: string]
  'drag-leave': []
  'drop': [placeholderKey: string]
  'update-text': [nodeId: string, value: string]
}>()

const editingNodeId = ref<string | null>(null)

const chapterContent = computed(() => {
  if (!props.selectedChapter) return []
  return props.selectedChapter.children
})

const handleDragOver = (e: DragEvent, placeholderKey: string) => {
  e.preventDefault()
  e.dataTransfer!.dropEffect = 'copy'
  emit('drag-over', placeholderKey)
}

const handleDragLeave = () => {
  emit('drag-leave')
}

const handleDrop = (e: DragEvent, placeholderKey: string) => {
  e.preventDefault()
  emit('drop', placeholderKey)
}

const renderNode = (node: DocumentNodeModel, nodeId: string) => {
  if (node.type === 'paragraph') {
    const para = node as ParagraphNode
    return para.children
  }
  return []
}
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <!-- Chapter Header -->
    <div v-if="selectedChapter" class="mb-8">
      <div class="text-sm text-muted-foreground mb-2">
        {{ selectedChapter.index }}
      </div>
      <h1 class="text-3xl font-bold text-foreground">
        {{ selectedChapter.title }}
      </h1>
    </div>

    <!-- Content -->
    <div v-if="chapterContent.length > 0" class="space-y-6">
      <template v-for="(node, index) in chapterContent" :key="index">
        <!-- Sub-chapter -->
        <div v-if="node.type === 'chapter'" class="mt-8">
          <div class="text-sm text-muted-foreground mb-2">
            {{ (node as ChapterNode).index }}
          </div>
          <h2 class="text-2xl font-semibold text-foreground mb-4">
            {{ (node as ChapterNode).title }}
          </h2>
          
          <!-- Sub-chapter content -->
          <div class="space-y-4">
            <template v-for="(subNode, subIndex) in (node as ChapterNode).children" :key="subIndex">
              <div v-if="subNode.type === 'paragraph'" class="space-y-4">
                <template v-for="(child, childIndex) in (subNode as ParagraphNode).children" :key="childIndex">
                  <!-- Text node -->
                  <TextEditableNode
                    v-if="child.type === 'text'"
                    :node="child as RichTextNode"
                    :node-id="`${index}-${subIndex}-${childIndex}`"
                    :is-editing="editingNodeId === `${index}-${subIndex}-${childIndex}`"
                    :is-client="isClient"
                    @update:value="emit('update-text', `${index}-${subIndex}-${childIndex}`, $event)"
                    @edit="editingNodeId = $event ? `${index}-${subIndex}-${childIndex}` : null"
                  />
                  
                  <!-- Placeholder or Bound Image -->
                  <PlaceholderRenderer
                    v-else
                    :node="child"
                    :dragged-material="draggedMaterial"
                    :is-drag-over="dragOverPlaceholder === (child as PlaceholderModel).key"
                    :is-client="isClient"
                    @drag-over="handleDragOver($event, (child as PlaceholderModel).key)"
                    @drag-leave="handleDragLeave"
                    @drop="handleDrop($event, (child as PlaceholderModel).key)"
                  />
                </template>
              </div>
            </template>
          </div>
        </div>

        <!-- Paragraph -->
        <div v-else-if="node.type === 'paragraph'" class="space-y-4">
          <template v-for="(child, childIndex) in (node as ParagraphNode).children" :key="childIndex">
            <!-- Text node -->
            <TextEditableNode
              v-if="child.type === 'text'"
              :node="child as RichTextNode"
              :node-id="`${index}-${childIndex}`"
              :is-editing="editingNodeId === `${index}-${childIndex}`"
              :is-client="isClient"
              @update:value="emit('update-text', `${index}-${childIndex}`, $event)"
              @edit="editingNodeId = $event ? `${index}-${childIndex}` : null"
            />
            
            <!-- Placeholder or Bound Image -->
            <PlaceholderRenderer
              v-else
              :node="child"
              :dragged-material="draggedMaterial"
              :is-drag-over="dragOverPlaceholder === (child as PlaceholderModel).key"
              :is-client="isClient"
              @drag-over="handleDragOver($event, (child as PlaceholderModel).key)"
              @drag-leave="handleDragLeave"
              @drop="handleDrop($event, (child as PlaceholderModel).key)"
            />
          </template>
        </div>
      </template>
    </div>

    <!-- Empty State -->
    <div v-else class="py-12 text-center">
      <SafeIcon name="FileText" :size="48" class="mx-auto text-muted-foreground mb-4" />
      <p class="text-muted-foreground">选择左侧章节开始编辑</p>
    </div>
  </div>
</template>

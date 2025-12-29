
<script setup lang="ts">
import type { DocumentNodeModel } from '@/data/document'
import ChapterNode from './nodes/ChapterNode.vue'
import ParagraphNode from './nodes/ParagraphNode.vue'
import TextNode from './nodes/TextNode.vue'
import PlaceholderNode from './nodes/PlaceholderNode.vue'
import BoundImageNode from './nodes/BoundImageNode.vue'

interface Props {
  node: DocumentNodeModel
  isClient: boolean
  dragOverPlaceholder: string | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'drag-over': [e: DragEvent]
  'drop': [placeholderKey: string, e: DragEvent]
  'drag-enter': [placeholderKey: string]
  'drag-leave': []
}>()

const getComponentForNode = (node: DocumentNodeModel) => {
  switch (node.type) {
    case 'chapter':
      return ChapterNode
    case 'paragraph':
      return ParagraphNode
    case 'text':
      return TextNode
    case 'image_placeholder':
    case 'table_placeholder':
      return PlaceholderNode
    case 'image':
      return BoundImageNode
    default:
      return null
  }
}
</script>

<template>
  <component
    :is="getComponentForNode(node)"
    v-if="getComponentForNode(node)"
    :node="node"
    :is-client="isClient"
    :drag-over-placeholder="dragOverPlaceholder"
    @drag-over="emit('drag-over', $event)"
    @drop="emit('drop', $event, $event)"
    @drag-enter="emit('drag-enter', $event)"
    @drag-leave="emit('drag-leave')"
  />
</template>

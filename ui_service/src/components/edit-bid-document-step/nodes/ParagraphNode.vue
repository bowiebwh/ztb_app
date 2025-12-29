
<script setup lang="ts">
import type { ParagraphNode as ParagraphNodeType } from '@/data/document'
import DocumentNode from '../DocumentNode.vue'

interface Props {
  node: ParagraphNodeType
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
</script>

<template>
  <div class="space-y-2">
    <div class="flex flex-wrap gap-1">
      <template v-for="(child, index) in node.children" :key="index">
        <DocumentNode
          :node="child"
          :is-client="isClient"
          :drag-over-placeholder="dragOverPlaceholder"
          @drag-over="emit('drag-over', $event)"
          @drop="emit('drop', $event, $event)"
          @drag-enter="emit('drag-enter', $event)"
          @drag-leave="emit('drag-leave')"
        />
      </template>
    </div>
  </div>
</template>

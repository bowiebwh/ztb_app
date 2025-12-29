
<script setup lang="ts">
import type { ChapterNode as ChapterNodeType } from '@/data/document'
import DocumentNode from '../DocumentNode.vue'

interface Props {
  node: ChapterNodeType
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
  <div class="space-y-4">
    <!-- 章节标题 -->
    <div class="border-b-2 border-primary pb-2">
      <h2 class="text-2xl font-bold text-foreground">
        <span class="text-primary">{{ node.index }}</span>
        {{ node.title }}
      </h2>
    </div>

    <!-- 章节内容 -->
    <div class="space-y-4 ml-4">
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

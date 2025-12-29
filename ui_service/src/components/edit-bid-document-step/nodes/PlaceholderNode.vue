
<script setup lang="ts">
import type { PlaceholderModel } from '@/data/document'
import { cn } from '@/lib/utils'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  node: PlaceholderModel
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

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  e.dataTransfer!.dropEffect = 'copy'
  emit('drag-over', e)
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  emit('drop', props.node.key, e)
}

const handleDragEnter = () => {
  emit('drag-enter', props.node.key)
}

const handleDragLeave = () => {
  emit('drag-leave')
}

const getPlaceholderIcon = () => {
  return props.node.type === 'image_placeholder' ? 'Image' : 'Table'
}
</script>

<template>
  <div
    :class="cn(
      'block w-full p-6 border-2 border-dashed rounded-lg transition-all',
      props.isClient && 'cursor-copy',
      dragOverPlaceholder === node.key
        ? 'border-primary bg-primary/10'
        : 'border-muted-foreground/30 bg-muted/30 hover:border-primary/50'
    )"
    @dragover="handleDragOver"
    @drop="handleDrop"
    @dragenter="handleDragEnter"
    @dragleave="handleDragLeave"
  >
    <div class="flex flex-col items-center justify-center gap-2 text-center">
      <SafeIcon
        :name="getPlaceholderIcon()"
        :size="32"
        :class="cn(
          'text-muted-foreground transition-colors',
          dragOverPlaceholder === node.key && 'text-primary'
        )"
      />
      <div>
        <p class="font-medium text-foreground">{{ node.label }}</p>
        <p class="text-xs text-muted-foreground mt-1">
          拖拽文件到此处替换占位符
        </p>
      </div>
    </div>
  </div>
</template>

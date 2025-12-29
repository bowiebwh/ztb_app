
<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { RichTextNode } from '@/data/document'
import { cn } from '@/lib/utils'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  node: RichTextNode
  nodeId: string
  isEditing: boolean
  isClient: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:value': [value: string]
  'edit': [isEditing: boolean]
}>()

const editValue = ref(props.node.value)

watch(() => props.node.value, (newValue) => {
  editValue.value = newValue
})

const handleEdit = () => {
  emit('edit', true)
}

const handleSave = () => {
  emit('update:value', editValue.value)
  emit('edit', false)
}

const handleCancel = () => {
  editValue.value = props.node.value
  emit('edit', false)
}

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault()
    handleSave()
  }
  if (e.key === 'Escape') {
    handleCancel()
  }
}
</script>

<template>
  <div v-if="!isEditing" class="group">
    <p
      :class="cn(
        'text-base leading-relaxed text-foreground',
        node.format === 'bold' && 'font-semibold',
        node.format === 'italic' && 'italic',
        'cursor-text hover:bg-muted/50 px-2 py-1 rounded transition-colors',
        isClient && 'hover:bg-muted/50'
      )"
      @click="handleEdit"
    >
      {{ node.value }}
    </p>
    <div v-if="isClient" class="opacity-0 group-hover:opacity-100 transition-opacity mt-1">
      <Button
        variant="ghost"
        size="sm"
        @click="handleEdit"
        class="h-6 px-2 text-xs"
      >
        <SafeIcon name="Edit2" :size="14" class="mr-1" />
        编辑
      </Button>
    </div>
  </div>

  <div v-else class="space-y-2 bg-muted/30 p-4 rounded-lg border border-primary/20">
    <Textarea
      v-model="editValue"
      @keydown="handleKeyDown"
      class="min-h-24 resize-none"
      placeholder="输入文本内容..."
      autofocus
    />
    <div class="flex gap-2 justify-end">
      <Button
        variant="outline"
        size="sm"
        @click="handleCancel"
      >
        取消
      </Button>
      <Button
        size="sm"
        @click="handleSave"
      >
        <SafeIcon name="Check" :size="14" class="mr-1" />
        保存
      </Button>
    </div>
  </div>
</template>

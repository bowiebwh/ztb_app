
<script setup lang="ts">
import { ref } from 'vue'
import type { RichTextNode } from '@/data/document'
import { cn } from '@/lib/utils'

interface Props {
  node: RichTextNode
  isClient: boolean
}

const props = defineProps<Props>()

const isEditing = ref(false)
const editValue = ref(props.node.value)

const toggleEdit = () => {
  if (props.isClient) {
    isEditing.value = !isEditing.value
    if (!isEditing.value) {
      // 保存编辑内容（实际应用中应更新父组件状态）
    }
  }
}
</script>

<template>
  <span
    :class="cn(
      'inline cursor-text hover:bg-primary/5 px-1 rounded transition-colors',
      node.format === 'bold' && 'font-bold',
      node.format === 'italic' && 'italic',
      isEditing && 'bg-primary/10'
    )"
    @click="toggleEdit"
  >
    <span v-if="!isEditing" class="select-none">{{ node.value }}</span>
    <input
      v-else
      v-model="editValue"
      type="text"
      class="bg-transparent border-b border-primary outline-none w-full"
      @blur="toggleEdit"
      @keydown.enter="toggleEdit"
      @keydown.escape="isEditing = false"
      autofocus
    />
  </span>
</template>

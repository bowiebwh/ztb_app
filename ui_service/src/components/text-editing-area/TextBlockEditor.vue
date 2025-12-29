
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Textarea } from '@/components/ui/textarea'
import { Input } from '@/components/ui/input'
import { cn } from '@/lib/utils'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  blockId: string
  blockType: 'heading' | 'paragraph'
  level?: number
  content: string
  isSelected: boolean
}

const props = withDefaults(defineProps<Props>(), {
  level: 1,
})

const emit = defineEmits<{
  select: []
  'update:content': [value: string]
}>()

const isEditing = ref(false)
const localContent = ref(props.content)

const headingClass = computed(() => {
  const classes: Record<number, string> = {
    1: 'text-2xl font-bold',
    2: 'text-xl font-bold',
    3: 'text-lg font-semibold',
  }
  return classes[props.level] || 'text-base font-semibold'
})

const handleContentChange = (newContent: string) => {
  localContent.value = newContent
  emit('update:content', newContent)
}

const handleBlur = () => {
  isEditing.value = false
}

onMounted(() => {
  localContent.value = props.content
})
</script>

<template>
  <div
    :class="cn(
      'p-4 rounded-lg border-2 transition-all',
      isSelected ? 'border-primary bg-primary/5' : 'border-transparent hover:border-border',
      isEditing && 'ring-2 ring-primary/50'
    )"
    @click="emit('select')"
  >
    <!-- Heading -->
    <component
      v-if="blockType === 'heading'"
      :is="`h${level}`"
      :class="cn(
        headingClass,
        'text-foreground cursor-text outline-none',
        isEditing && 'bg-background'
      )"
      :contenteditable="isEditing"
      @focus="isEditing = true"
      @blur="handleBlur"
      @input="handleContentChange(($event.target as HTMLElement).textContent || '')"
    >
      {{ localContent }}
    </component>

    <!-- Paragraph -->
    <p
      v-else
      :class="cn(
        'text-base text-foreground cursor-text outline-none leading-relaxed',
        isEditing && 'bg-background'
      )"
      :contenteditable="isEditing"
      @focus="isEditing = true"
      @blur="handleBlur"
      @input="handleContentChange(($event.target as HTMLElement).textContent || '')"
    >
      {{ localContent }}
    </p>

    <!-- Edit Indicator -->
    <div
      v-if="isSelected && !isEditing"
      class="mt-2 flex items-center gap-2 text-xs text-muted-foreground"
    >
      <SafeIcon name="Edit2" :size="14" />
      <span>点击编辑内容</span>
    </div>
  </div>
</template>

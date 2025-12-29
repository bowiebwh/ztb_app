
<script setup lang="ts">
import { computed } from 'vue'
import type { DocumentNodeModel, ChapterNode } from '@/data/document'
import { cn } from '@/lib/utils'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  chapters: DocumentNodeModel[]
  selectedChapterId: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'select-chapter': [id: string]
}>()

const flatChapters = computed(() => {
  const result: Array<{ id: string; title: string; index: string; level: number }> = []
  
  const traverse = (nodes: DocumentNodeModel[], level: number = 0) => {
    nodes.forEach((node) => {
      if (node.type === 'chapter') {
        const chapter = node as ChapterNode
        result.push({
          id: chapter.index,
          title: chapter.title,
          index: chapter.index,
          level,
        })
        traverse(chapter.children, level + 1)
      }
    })
  }
  
  traverse(props.chapters)
  return result
})

const handleSelectChapter = (id: string) => {
  emit('select-chapter', id)
}
</script>

<template>
  <div class="p-4">
    <h2 class="text-sm font-semibold text-foreground mb-4 px-2">章节导航</h2>
    
    <nav class="space-y-1">
      <template v-for="chapter in flatChapters" :key="chapter.id">
        <button
          @click="handleSelectChapter(chapter.id)"
          :class="cn(
            'w-full text-left px-3 py-2 rounded-md text-sm transition-colors',
            'hover:bg-muted',
            selectedChapterId === chapter.id && 'bg-primary/10 text-primary font-medium'
          )"
          :style="{ paddingLeft: `${12 + chapter.level * 16}px` }"
        >
          <div class="flex items-center gap-2">
            <SafeIcon
              :name="chapter.level === 0 ? 'BookOpen' : 'FileText'"
              :size="16"
              class="flex-shrink-0"
            />
            <span class="truncate">
              <span class="font-medium">{{ chapter.index }}</span>
              <span class="ml-2">{{ chapter.title }}</span>
            </span>
          </div>
        </button>
      </template>
    </nav>
  </div>
</template>

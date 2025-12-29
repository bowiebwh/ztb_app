
<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '@/lib/utils'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Chapter {
  id: string
  title: string
  level: number
  children?: Chapter[]
}

interface Props {
  chapters: Chapter[]
  selectedChapterId: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'select-chapter': [chapterId: string]
}>()

const handleSelectChapter = (chapterId: string) => {
  emit('select-chapter', chapterId)
}

const getIndentClass = (level: number) => {
  const indents: Record<number, string> = {
    1: 'pl-4',
    2: 'pl-8',
    3: 'pl-12',
    4: 'pl-16',
  }
  return indents[level] || 'pl-4'
}

const renderChapters = (chapters: Chapter[]) => {
  return chapters
}
</script>

<template>
  <div class="space-y-1 p-4">
    <template v-for="chapter in renderChapters(chapters)" :key="chapter.id">
      <!-- Chapter Item -->
      <button
        @click="handleSelectChapter(chapter.id)"
        :class="cn(
          'w-full text-left px-3 py-2 rounded-md text-sm transition-colors',
          'hover:bg-muted',
          selectedChapterId === chapter.id && 'bg-primary text-primary-foreground font-medium',
          getIndentClass(chapter.level)
        )"
      >
        <div class="flex items-center gap-2">
          <SafeIcon
            :name="chapter.level === 1 ? 'BookOpen' : 'FileText'"
            :size="16"
            class="flex-shrink-0"
          />
          <span class="truncate">{{ chapter.title }}</span>
        </div>
      </button>

      <!-- Sub-chapters -->
      <template v-if="chapter.children && chapter.children.length > 0">
        <button
          v-for="subChapter in chapter.children"
          :key="subChapter.id"
          @click="handleSelectChapter(subChapter.id)"
          :class="cn(
            'w-full text-left px-3 py-2 rounded-md text-sm transition-colors',
            'hover:bg-muted',
            selectedChapterId === subChapter.id && 'bg-primary text-primary-foreground font-medium',
            getIndentClass(subChapter.level)
          )"
        >
          <div class="flex items-center gap-2">
            <SafeIcon name="FileText" :size="14" class="flex-shrink-0" />
            <span class="truncate text-xs">{{ subChapter.title }}</span>
          </div>
        </button>
      </template>
    </template>
  </div>
</template>

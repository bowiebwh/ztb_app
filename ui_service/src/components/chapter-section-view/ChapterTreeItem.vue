
<script setup lang="ts">
import { computed } from 'vue'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { ChapterNode } from '@/data/document'

interface Props {
  chapter: ChapterNode
  expanded: boolean
  selected: boolean
  level: number
}

const props = defineProps<Props>()

const emit = defineEmits<{
  toggle: [chapterId: string]
  select: [chapterId: string]
  navigate: [chapterId: string]
}>()

const chapterId = computed(() => `${props.chapter.index}-${props.chapter.title}`)

const hasChildren = computed(() => {
  return props.chapter.children && props.chapter.children.length > 0
})

const childChapters = computed(() => {
  return props.chapter.children?.filter(child => child.type === 'chapter') || []
})

const handleToggle = (e: Event) => {
  e.stopPropagation()
  emit('toggle', chapterId.value)
}

const handleSelect = () => {
  emit('select', chapterId.value)
}

const handleNavigate = (e: Event) => {
  e.stopPropagation()
  emit('navigate', chapterId.value)
}

const paddingLeft = computed(() => {
  return `${props.level * 1.5}rem`
})
</script>

<template>
  <div>
    <!-- Chapter Item -->
    <div
      :style="{ paddingLeft }"
      class="flex items-center gap-2 py-2 px-3 rounded-lg hover:bg-muted transition-colors cursor-pointer group"
      :class="selected && 'bg-primary/10 border-l-2 border-primary'"
      @click="handleSelect"
    >
      <!-- Toggle Button -->
      <button
        v-if="hasChildren"
        @click="handleToggle"
        class="flex-shrink-0 p-0.5 hover:bg-muted-foreground/20 rounded transition-colors"
        :aria-label="`${expanded ? '折叠' : '展开'} ${chapter.title}`"
      >
        <SafeIcon
          :name="expanded ? 'ChevronDown' : 'ChevronRight'"
          :size="16"
          class="transition-transform"
        />
      </button>
      <div v-else class="flex-shrink-0 w-6" />

      <!-- Chapter Icon -->
      <SafeIcon
        :name="level === 0 ? 'BookOpen' : 'FileText'"
        :size="16"
        class="flex-shrink-0 text-muted-foreground"
      />

      <!-- Chapter Title -->
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2">
          <span class="text-sm font-medium text-muted-foreground flex-shrink-0">
            {{ chapter.index }}
          </span>
          <span class="text-sm font-medium truncate">
            {{ chapter.title }}
          </span>
        </div>
      </div>

      <!-- Action Button -->
      <Button
        variant="ghost"
        size="sm"
        @click="handleNavigate"
        class="opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0"
      >
        <SafeIcon name="Eye" :size="14" />
      </Button>
    </div>

    <!-- Child Chapters -->
    <template v-if="expanded && hasChildren">
      <ChapterTreeItem
        v-for="child in childChapters"
        :key="`${child.index}-${child.title}`"
        :chapter="child"
        :expanded="expanded"
        :selected="selected"
        :level="level + 1"
        @toggle="emit('toggle', $event)"
        @select="emit('select', $event)"
        @navigate="emit('navigate', $event)"
      />
    </template>
  </div>
</template>

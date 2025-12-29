
<script setup lang="ts">
import { computed } from 'vue'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { cn } from '@/lib/utils'

interface Chapter {
  id: string
  title: string
  level: number
  pageNumber?: number
  children?: Chapter[]
}

interface Props {
  chapter: Chapter
  expanded: boolean
  isClient: boolean
  depth?: number
}

const props = withDefaults(defineProps<Props>(), {
  depth: 0,
})

const emit = defineEmits<{
  'toggle-expand': [id: string]
  navigate: [id: string]
}>()

const hasChildren = computed(() => {
  return props.chapter.children && props.chapter.children.length > 0
})

const paddingLeft = computed(() => {
  return `${props.depth * 24}px`
})

const handleToggle = (e: Event) => {
  e.stopPropagation()
  emit('toggle-expand', props.chapter.id)
}

const handleNavigate = (e: Event) => {
  e.stopPropagation()
  emit('navigate', props.chapter.id)
}
</script>

<template>
  <div class="chapter-item">
    <!-- Chapter Item -->
    <div
      :style="{ paddingLeft }"
      class="flex items-center gap-2 py-2 px-3 rounded-lg hover:bg-muted transition-colors group cursor-pointer"
      @click="handleNavigate"
    >
      <!-- Expand/Collapse Button -->
      <button
        v-if="hasChildren"
        @click="handleToggle"
        class="flex-shrink-0 w-6 h-6 flex items-center justify-center hover:bg-muted-foreground/10 rounded transition-colors"
        :aria-expanded="expanded"
        :aria-label="`${expanded ? '折叠' : '展开'} ${chapter.title}`"
      >
        <SafeIcon
          name="ChevronRight"
          :size="18"
          class="transition-transform"
          :class="{ 'rotate-90': expanded }"
        />
      </button>

      <!-- Placeholder for non-expandable items -->
      <div v-else class="w-6 flex-shrink-0" />

      <!-- Chapter Icon -->
      <div class="flex-shrink-0 w-5 h-5 flex items-center justify-center text-muted-foreground group-hover:text-primary transition-colors">
        <SafeIcon
          :name="chapter.level === 1 ? 'BookOpen' : 'FileText'"
          :size="18"
        />
      </div>

      <!-- Chapter Title -->
      <div class="flex-1 min-w-0">
        <div
          :class="cn(
            'text-sm font-medium truncate group-hover:text-primary transition-colors',
            chapter.level === 1 && 'font-semibold text-base'
          )"
        >
          {{ chapter.title }}
        </div>
      </div>

      <!-- Page Number -->
      <div
        v-if="chapter.pageNumber"
        class="flex-shrink-0 text-xs text-muted-foreground group-hover:text-foreground transition-colors"
      >
        第 {{ chapter.pageNumber }} 页
      </div>

      <!-- Navigate Icon -->
      <SafeIcon
        name="ArrowRight"
        :size="16"
        class="flex-shrink-0 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity"
      />
    </div>

    <!-- Children -->
    <template v-if="hasChildren && expanded">
      <ChapterTreeItem
        v-for="child in chapter.children"
        :key="child.id"
        :chapter="child"
        :expanded="expanded"
        :is-client="isClient"
        :depth="depth + 1"
        @toggle-expand="$emit('toggle-expand', $event)"
        @navigate="$emit('navigate', $event)"
      />
    </template>
  </div>
</template>

<style scoped>
.chapter-item {
  animation: slideIn 0.2s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

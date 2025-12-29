
<script setup lang="ts">
import { computed, ref } from 'vue'
import { Separator } from '@/components/ui/separator'
import { Badge } from '@/components/ui/badge'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface ContentNode {
  id: string
  type: 'heading' | 'paragraph' | 'table' | 'image' | 'list' | 'code'
  level?: number
  content?: string
  children?: ContentNode[]
  data?: Record<string, any>
}

interface Chapter {
  id: string
  title: string
  level: number
  content: ContentNode[]
}

interface Props {
  content: Chapter[]
  currentChapterId?: string
  isClient?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  currentChapterId: '',
  isClient: true,
})

const emit = defineEmits<{
  'chapter-change': [chapterId: string]
}>()

const expandedSections = ref<Set<string>>(new Set())

const currentChapter = computed(() => {
  if (!props.currentChapterId) {
    return props.content[0] || null
  }
  return props.content.find(ch => ch.id === props.currentChapterId) || props.content[0] || null
})

const toggleSection = (id: string) => {
  if (expandedSections.value.has(id)) {
    expandedSections.value.delete(id)
  } else {
    expandedSections.value.add(id)
  }
}

const handleChapterSelect = (chapterId: string) => {
  emit('chapter-change', chapterId)
  expandedSections.value.clear()
}

const renderContent = (nodes: ContentNode[]): any => {
  return nodes.map((node, index) => {
    switch (node.type) {
      case 'heading':
        return {
          type: 'heading',
          level: node.level || 2,
          content: node.content,
          key: `${node.id}-${index}`,
        }
      case 'paragraph':
        return {
          type: 'paragraph',
          content: node.content,
          key: `${node.id}-${index}`,
        }
      case 'table':
        return {
          type: 'table',
          data: node.data,
          key: `${node.id}-${index}`,
        }
      case 'image':
        return {
          type: 'image',
          data: node.data,
          key: `${node.id}-${index}`,
        }
      case 'list':
        return {
          type: 'list',
          children: node.children,
          key: `${node.id}-${index}`,
        }
      case 'code':
        return {
          type: 'code',
          content: node.content,
          key: `${node.id}-${index}`,
        }
      default:
        return null
    }
  })
}
</script>

<template>
  <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
    <!-- Sidebar Navigation -->
    <aside class="lg:col-span-1 hidden lg:block">
      <div class="sticky top-32 space-y-2">
        <h3 class="text-sm font-semibold text-muted-foreground px-3 py-2">章节导航</h3>
        <nav class="space-y-1">
          <button
            v-for="chapter in content"
            :key="chapter.id"
            @click="handleChapterSelect(chapter.id)"
            :class="[
              'w-full text-left px-3 py-2 rounded-md text-sm transition-colors',
              currentChapter?.id === chapter.id
                ? 'bg-primary/10 text-primary font-medium'
                : 'text-muted-foreground hover:bg-muted hover:text-foreground'
            ]"
          >
            <div class="flex items-center gap-2">
              <span
                :class="[
                  'inline-block w-1.5 h-1.5 rounded-full transition-colors',
                  currentChapter?.id === chapter.id ? 'bg-primary' : 'bg-border'
                ]"
              />
              <span class="truncate">{{ chapter.title }}</span>
            </div>
          </button>
        </nav>
      </div>
    </aside>

    <!-- Main Content -->
    <article class="lg:col-span-3 space-y-8 content-section">
      <div v-if="currentChapter" class="space-y-6">
        <!-- Chapter Title -->
        <div class="border-b pb-6">
          <div class="flex items-start justify-between gap-4">
            <div>
              <h1 class="text-3xl font-bold mb-2">{{ currentChapter.title }}</h1>
              <p class="text-sm text-muted-foreground">
                章节 {{ currentChapter.level }} · 只读预览
              </p>
            </div>
            <Badge variant="outline">只读</Badge>
          </div>
        </div>

        <!-- Content Sections -->
        <div class="space-y-6">
          <template v-for="(node, index) in currentChapter.content" :key="`${node.id}-${index}`">
            <!-- Heading -->
            <div v-if="node.type === 'heading'" class="mt-8 first:mt-0">
              <component
                :is="`h${Math.min(node.level || 2, 6)}`"
                class="font-semibold text-foreground"
                :class="{
                  'text-2xl': node.level === 2,
                  'text-xl': node.level === 3,
                  'text-lg': node.level === 4,
                }"
              >
                {{ node.content }}
              </component>
            </div>

            <!-- Paragraph -->
            <div v-else-if="node.type === 'paragraph'" class="text-base leading-relaxed text-foreground">
              {{ node.content }}
            </div>

            <!-- Table -->
            <div v-else-if="node.type === 'table'" class="overflow-x-auto">
              <table class="w-full border-collapse border border-border">
                <thead>
                  <tr class="bg-muted">
                    <th
                      v-for="(header, hIndex) in node.data?.headers || []"
                      :key="hIndex"
                      class="border border-border px-4 py-2 text-left font-semibold text-sm"
                    >
                      {{ header }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, rIndex) in node.data?.rows || []" :key="rIndex" class="hover:bg-muted/50">
                    <td
                      v-for="(cell, cIndex) in row"
                      :key="cIndex"
                      class="border border-border px-4 py-2 text-sm"
                    >
                      {{ cell }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Image -->
            <div v-else-if="node.type === 'image'" class="my-6">
              <figure class="space-y-2">
                <img
                  :src="node.data?.src || 'https://spark-builder.s3.cn-north-1.amazonaws.com.cn/image/2025/12/19/27505c9a-cf37-4d1b-bf99-c858c133e7a9.png'"
                  :alt="node.data?.alt || '图片'"
                  class="w-full rounded-lg border border-border object-cover max-h-96"
                />
                <figcaption v-if="node.data?.caption" class="text-sm text-muted-foreground text-center">
                  {{ node.data.caption }}
                </figcaption>
              </figure>
            </div>

            <!-- List -->
            <div v-else-if="node.type === 'list'" class="space-y-2">
              <ul class="list-disc list-inside space-y-1 text-base text-foreground">
                <li v-for="(item, lIndex) in node.children || []" :key="lIndex">
                  {{ item.content }}
                </li>
              </ul>
            </div>

            <!-- Code Block -->
            <div v-else-if="node.type === 'code'" class="bg-muted rounded-lg p-4 overflow-x-auto">
              <pre class="text-sm font-mono text-foreground"><code>{{ node.content }}</code></pre>
            </div>
          </template>
        </div>

        <!-- Separator -->
        <Separator class="my-8" />

        <!-- Chapter Navigation -->
        <div class="flex items-center justify-between pt-4">
          <div class="text-sm text-muted-foreground">
            章节 {{ content.findIndex(ch => ch.id === currentChapter.id) + 1 }} / {{ content.length }}
          </div>
          <div class="flex gap-2">
            <button
              v-if="content.findIndex(ch => ch.id === currentChapter.id) > 0"
              @click="handleChapterSelect(content[content.findIndex(ch => ch.id === currentChapter.id) - 1].id)"
              class="text-sm text-primary hover:underline flex items-center gap-1"
            >
              <SafeIcon name="ChevronLeft" :size="16" />
              上一章节
            </button>
            <button
              v-if="content.findIndex(ch => ch.id === currentChapter.id) < content.length - 1"
              @click="handleChapterSelect(content[content.findIndex(ch => ch.id === currentChapter.id) + 1].id)"
              class="text-sm text-primary hover:underline flex items-center gap-1 ml-auto"
            >
              下一章节
              <SafeIcon name="ChevronRight" :size="16" />
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <SafeIcon name="FileText" :size="48" class="mx-auto text-muted-foreground mb-4" />
        <p class="text-muted-foreground">暂无内容</p>
      </div>
    </article>
  </div>
</template>

<style scoped>
:deep(h1) {
  @apply text-3xl font-bold;
}

:deep(h2) {
  @apply text-2xl font-semibold mt-6 mb-3;
}

:deep(h3) {
  @apply text-xl font-semibold mt-4 mb-2;
}

:deep(h4) {
  @apply text-lg font-semibold mt-3 mb-2;
}

:deep(p) {
  @apply mb-4 leading-relaxed;
}

:deep(ul) {
  @apply list-disc list-inside space-y-2 mb-4;
}

:deep(ol) {
  @apply list-decimal list-inside space-y-2 mb-4;
}

:deep(table) {
  @apply w-full border-collapse my-4;
}

:deep(th) {
  @apply bg-muted border border-border px-4 py-2 text-left font-semibold;
}

:deep(td) {
  @apply border border-border px-4 py-2;
}

:deep(code) {
  @apply bg-muted px-2 py-1 rounded text-sm font-mono;
}

:deep(pre) {
  @apply bg-muted p-4 rounded-lg overflow-x-auto my-4;
}
</style>

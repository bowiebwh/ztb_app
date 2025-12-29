
<script setup lang="ts">
import { computed } from 'vue'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface ContentBlock {
  type: 'heading' | 'paragraph' | 'image' | 'table' | 'list' | 'quote'
  level?: number
  content?: string
  items?: string[]
  src?: string
  alt?: string
  rows?: Array<string[]>
  headers?: string[]
}

interface Props {
  content: ContentBlock[]
  chapterTitle?: string
}

const props = defineProps<Props>()

const hasContent = computed(() => {
  return props.content && props.content.length > 0
})
</script>

<template>
  <div class="prose prose-sm max-w-none dark:prose-invert">
    <!-- Chapter Title -->
    <h1 v-if="chapterTitle" class="text-3xl font-bold mb-6 text-foreground">
      {{ chapterTitle }}
    </h1>

    <!-- Content Blocks -->
    <template v-if="hasContent">
      <template v-for="(block, index) in content" :key="index">
        <!-- Heading -->
        <component
          v-if="block.type === 'heading'"
          :is="`h${block.level || 2}`"
          class="font-semibold text-foreground mt-6 mb-3"
        >
          {{ block.content }}
        </component>

        <!-- Paragraph -->
        <p v-else-if="block.type === 'paragraph'" class="text-foreground leading-relaxed mb-4">
          {{ block.content }}
        </p>

        <!-- Image -->
        <figure v-else-if="block.type === 'image'" class="my-6">
          <img
            :src="block.src || 'https://spark-builder.s3.cn-north-1.amazonaws.com.cn/image/2025/12/19/8258b1c0-0314-4675-8d8f-7e88673105eb.png'"
            :alt="block.alt || '文档图片'"
            class="w-full rounded-lg border border-border shadow-sm"
          />
          <figcaption v-if="block.alt" class="text-sm text-muted-foreground text-center mt-2">
            {{ block.alt }}
          </figcaption>
        </figure>

        <!-- Table -->
        <div v-else-if="block.type === 'table'" class="overflow-x-auto my-6">
          <table class="w-full border-collapse border border-border">
            <thead v-if="block.headers" class="bg-muted">
              <tr>
                <th
                  v-for="(header, hIndex) in block.headers"
                  :key="hIndex"
                  class="border border-border px-4 py-2 text-left font-semibold text-foreground"
                >
                  {{ header }}
                </th>
              </tr>
            </thead>
            <tbody v-if="block.rows">
              <tr v-for="(row, rIndex) in block.rows" :key="rIndex" class="hover:bg-muted/50">
                <td
                  v-for="(cell, cIndex) in row"
                  :key="cIndex"
                  class="border border-border px-4 py-2 text-foreground"
                >
                  {{ cell }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- List -->
        <ul v-else-if="block.type === 'list'" class="list-disc list-inside space-y-2 mb-4 text-foreground">
          <li v-for="(item, lIndex) in block.items" :key="lIndex">
            {{ item }}
          </li>
        </ul>

        <!-- Quote -->
        <blockquote
          v-else-if="block.type === 'quote'"
          class="border-l-4 border-primary pl-4 py-2 my-4 italic text-muted-foreground"
        >
          {{ block.content }}
        </blockquote>
      </template>
    </template>

    <!-- Empty State -->
    <div v-else class="flex flex-col items-center justify-center py-12 text-center">
      <SafeIcon name="FileText" :size="48" class="text-muted-foreground mb-4" />
      <p class="text-muted-foreground">暂无内容</p>
    </div>
  </div>
</template>

<style scoped>
:deep(.prose) {
  --tw-prose-body: hsl(var(--foreground));
  --tw-prose-headings: hsl(var(--foreground));
  --tw-prose-lead: hsl(var(--muted-foreground));
  --tw-prose-links: hsl(var(--primary));
  --tw-prose-bold: hsl(var(--foreground));
  --tw-prose-counters: hsl(var(--muted-foreground));
  --tw-prose-bullets: hsl(var(--muted-foreground));
  --tw-prose-hr: hsl(var(--border));
  --tw-prose-quotes: hsl(var(--muted-foreground));
  --tw-prose-quote-borders: hsl(var(--primary));
  --tw-prose-captions: hsl(var(--muted-foreground));
  --tw-prose-code: hsl(var(--foreground));
  --tw-prose-pre-code: hsl(var(--foreground));
  --tw-prose-pre-bg: hsl(var(--muted));
  --tw-prose-th-borders: hsl(var(--border));
  --tw-prose-td-borders: hsl(var(--border));
}

:deep(.dark .prose) {
  --tw-prose-body: hsl(var(--foreground));
  --tw-prose-headings: hsl(var(--foreground));
}
</style>

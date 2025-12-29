
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import SafeIcon from '@/components/common/SafeIcon.vue'
import DocumentChapterNav from './DocumentChapterNav.vue'
import DocumentContentRenderer from './DocumentContentRenderer.vue'
import DocumentActionBar from './DocumentActionBar.vue'
import { mockBidDocument } from '@/data/mock-bid-document'

interface Chapter {
  id: string
  title: string
  level: number
  children?: Chapter[]
}

const isClient = ref(true)
const selectedChapterId = ref<string>('chapter-1')
const isLoading = ref(false)

// Mock document data
const documentData = ref(mockBidDocument)

// Flatten chapters for navigation
const flattenedChapters = computed(() => {
  const result: Chapter[] = []
  
  const flatten = (chapters: Chapter[]) => {
    chapters.forEach(chapter => {
      result.push(chapter)
      if (chapter.children) {
        flatten(chapter.children)
      }
    })
  }
  
  flatten(documentData.value.chapters)
  return result
})

// Get current chapter content
const currentChapter = computed(() => {
  return flattenedChapters.value.find(ch => ch.id === selectedChapterId.value)
})

const currentChapterContent = computed(() => {
  return documentData.value.content[selectedChapterId.value] || []
})

// Handle chapter selection
const selectChapter = (chapterId: string) => {
  selectedChapterId.value = chapterId
  // Scroll to top of content area
  const contentArea = document.querySelector('[data-content-area]')
  if (contentArea) {
    contentArea.scrollTop = 0
  }
}

// Handle download
const handleDownload = () => {
  isLoading.value = true
  // Simulate download
  setTimeout(() => {
    isLoading.value = false
    // In real implementation, this would trigger actual download
    console.log('Downloading Word file...')
  }, 1000)
}

// Handle regenerate
const handleRegenerate = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './regenerate-bid-document-confirmation.html'
  }
}

onMounted(() => {
  isClient.value = false
  requestAnimationFrame(() => {
    isClient.value = true
  })
})
</script>

<template>
  <div class="flex h-[calc(100vh-64px)] bg-background">
    <!-- Left Sidebar - Chapter Navigation -->
    <div class="w-64 border-r bg-muted/30 flex flex-col">
      <div class="p-4 border-b">
        <h3 class="font-semibold text-sm">章节目录</h3>
      </div>
      <ScrollArea class="flex-1">
        <DocumentChapterNav
          :chapters="documentData.chapters"
          :selected-chapter-id="selectedChapterId"
          @select-chapter="selectChapter"
        />
      </ScrollArea>
    </div>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col">
      <!-- Content Header -->
      <div class="border-b bg-card p-4 flex items-center justify-between">
        <div>
          <h2 class="text-xl font-semibold">{{ currentChapter?.title || '投标书内容' }}</h2>
          <p class="text-sm text-muted-foreground mt-1">
            只读预览 · 共 {{ flattenedChapters.length }} 个章节
          </p>
        </div>
        <Button
          variant="outline"
          size="sm"
          @click="() => {
            if (typeof window !== 'undefined') {
              window.history.back()
            }
          }"
          :disabled="!isClient"
        >
          <SafeIcon name="ChevronLeft" :size="16" />
          返回
        </Button>
      </div>

      <!-- Content Area -->
      <ScrollArea
        data-content-area
        class="flex-1 overflow-hidden"
      >
        <div class="p-8 max-w-4xl mx-auto">
          <!-- Loading State -->
          <div v-if="isLoading" class="flex items-center justify-center py-12">
            <SafeIcon name="Loader2" :size="32" class="animate-spin text-primary" />
            <span class="ml-3 text-muted-foreground">加载中...</span>
          </div>

          <!-- Content Renderer -->
          <DocumentContentRenderer
            v-else
            :content="currentChapterContent"
            :chapter-title="currentChapter?.title"
          />
        </div>
      </ScrollArea>

      <!-- Action Bar -->
      <DocumentActionBar
        :is-client="isClient"
        :is-loading="isLoading"
        @download="handleDownload"
        @regenerate="handleRegenerate"
      />
    </div>
  </div>
</template>

<style scoped>
:deep([data-content-area]) {
  scroll-behavior: smooth;
}
</style>

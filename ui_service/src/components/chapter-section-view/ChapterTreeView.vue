
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ScrollArea } from '@/components/ui/scroll-area'
import SafeIcon from '@/components/common/SafeIcon.vue'
import ChapterTreeItem from './ChapterTreeItem.vue'
import type { ChapterNode, DocumentNodeModel } from '@/data/document'
import { fetchDocumentStructure } from '@/lib/api'

const isClient = ref(true)
const expandedChapters = ref<Set<string>>(new Set())
const selectedChapter = ref<string | null>(null)

const chapters = ref<ChapterNode[]>([])

// 获取章节的完整路径（用于面包屑）
const getChapterPath = (chapterId: string): Array<{ id: string; title: string; index: string }> => {
  const path: Array<{ id: string; title: string; index: string }> = []
  
  const findPath = (nodes: DocumentNodeModel[], targetId: string, currentPath: Array<{ id: string; title: string; index: string }>): boolean => {
    for (const node of nodes) {
      if (node.type === 'chapter') {
        const chapterId = `${node.index}-${node.title}`
        const newPath = [...currentPath, { id: chapterId, title: node.title, index: node.index }]
        
        if (chapterId === targetId) {
          path.push(...newPath)
          return true
        }
        
        if (findPath(node.children, targetId, newPath)) {
          return true
        }
      }
    }
    return false
  }
  
  findPath(chapters.value as unknown as DocumentNodeModel[], chapterId, [])
  return path
}

const toggleChapter = (chapterId: string) => {
  if (expandedChapters.value.has(chapterId)) {
    expandedChapters.value.delete(chapterId)
  } else {
    expandedChapters.value.add(chapterId)
  }
}

const selectChapter = (chapterId: string) => {
  selectedChapter.value = chapterId
  // 自动展开选中的章节
  expandedChapters.value.add(chapterId)
}

const handleNavigateToContent = (chapterId: string) => {
  selectChapter(chapterId)
  // 可以在这里添加导航到具体内容的逻辑
}

const handleBackToEditor = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './edit-bid-document-step.html'
  }
}

const currentChapterPath = computed(() => {
  if (!selectedChapter.value) return []
  return getChapterPath(selectedChapter.value)
})

onMounted(async () => {
  isClient.value = false
  const projectId = new URLSearchParams(window.location.search).get('id') || '1'
  try {
    const res = await fetchDocumentStructure(projectId)
    chapters.value = (res.content || []).filter((n: any) => n.type === 'chapter') as ChapterNode[]
    chapters.value.forEach(ch => expandedChapters.value.add(`${ch.index}-${ch.title}`))
  } catch (err) {
    console.error(err)
    chapters.value = []
  }
  requestAnimationFrame(() => {
    isClient.value = true
  })
})
</script>

<template>
  <div class="container mx-auto px-4 py-6 max-w-6xl">
    <!-- Header -->
    <div class="mb-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h1 class="text-3xl font-bold">文档章节结构</h1>
          <p class="text-muted-foreground mt-1">浏览和导航投标文档的完整层级结构</p>
        </div>
        <Button variant="outline" @click="handleBackToEditor">
          <SafeIcon name="ArrowLeft" :size="16" class="mr-2" />
          返回编辑
        </Button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left: Chapter Tree -->
      <div class="lg:col-span-2">
        <Card>
          <CardHeader>
            <CardTitle>章节导航</CardTitle>
            <CardDescription>点击章节可查看详细内容</CardDescription>
          </CardHeader>
          <CardContent>
            <ScrollArea class="h-[600px] pr-4">
              <div class="space-y-2">
                <template v-for="chapter in chapters" :key="`${chapter.index}-${chapter.title}`">
                  <ChapterTreeItem
                    :chapter="chapter"
                    :expanded="expandedChapters.has(`${chapter.index}-${chapter.title}`)"
                    :selected="selectedChapter === `${chapter.index}-${chapter.title}`"
                    :level="0"
                    @toggle="toggleChapter"
                    @select="selectChapter"
                    @navigate="handleNavigateToContent"
                  />
                </template>
              </div>
            </ScrollArea>
          </CardContent>
        </Card>
      </div>

      <!-- Right: Chapter Details -->
      <div class="lg:col-span-1">
        <Card v-if="selectedChapter" class="sticky top-20">
          <CardHeader>
            <CardTitle class="text-lg">章节详情</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <!-- Breadcrumb Path -->
            <div v-if="currentChapterPath.length > 0" class="space-y-2">
              <p class="text-sm font-medium text-muted-foreground">位置</p>
              <div class="flex flex-col gap-1">
                <template v-for="(item, index) in currentChapterPath" :key="item.id">
                  <div class="flex items-center gap-2">
                    <span class="text-xs text-muted-foreground">{{ item.index }}</span>
                    <span class="text-sm font-medium">{{ item.title }}</span>
                  </div>
                  <div v-if="index < currentChapterPath.length - 1" class="ml-2 h-4 border-l border-border" />
                </template>
              </div>
            </div>

            <!-- Statistics -->
            <div class="pt-4 border-t space-y-3">
              <div class="flex justify-between items-center text-sm">
                <span class="text-muted-foreground">总章节数</span>
                <span class="font-semibold">{{ chapters.length }}</span>
              </div>
              <div class="flex justify-between items-center text-sm">
                <span class="text-muted-foreground">当前深度</span>
                <span class="font-semibold">{{ currentChapterPath.length }}</span>
              </div>
            </div>

            <!-- Action -->
            <Button
              v-if="selectedChapter"
              class="w-full mt-4"
              @click="handleNavigateToContent(selectedChapter)"
            >
              <SafeIcon name="Eye" :size="16" class="mr-2" />
              查看内容
            </Button>
          </CardContent>
        </Card>

        <!-- Empty State -->
        <Card v-else class="sticky top-20">
          <CardContent class="pt-6">
            <div class="text-center py-8">
              <SafeIcon name="FileText" :size="32" class="mx-auto text-muted-foreground mb-3" />
              <p class="text-sm text-muted-foreground">选择左侧章节查看详情</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Statistics Footer -->
    <div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
      <Card>
        <CardContent class="pt-6">
          <div class="text-center">
            <p class="text-3xl font-bold text-primary">{{ chapters.length }}</p>
            <p class="text-sm text-muted-foreground mt-1">主章节</p>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="pt-6">
          <div class="text-center">
            <p class="text-3xl font-bold text-primary">
              {{ chapters.reduce((sum, ch) => sum + (ch.children?.filter(c => c.type === 'chapter').length || 0), 0) }}
            </p>
            <p class="text-sm text-muted-foreground mt-1">子章节</p>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="pt-6">
          <div class="text-center">
            <p class="text-3xl font-bold text-primary">
              {{ chapters.reduce((sum, ch) => sum + (ch.children?.filter(c => c.type === 'paragraph').length || 0), 0) }}
            </p>
            <p class="text-sm text-muted-foreground mt-1">段落</p>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

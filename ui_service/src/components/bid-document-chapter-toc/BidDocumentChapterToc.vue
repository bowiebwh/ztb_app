
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ScrollArea } from '@/components/ui/scroll-area'
import SafeIcon from '@/components/common/SafeIcon.vue'
import ChapterTreeItem from './ChapterTreeItem.vue'

interface Chapter {
  id: string
  title: string
  level: number
  pageNumber?: number
  children?: Chapter[]
}

// Mock data - 投标书章节目录
const mockChapters: Chapter[] = [
  {
    id: 'ch1',
    title: '第一章 投标人基本情况',
    level: 1,
    pageNumber: 1,
    children: [
      {
        id: 'ch1-1',
        title: '1.1 企业基本信息',
        level: 2,
        pageNumber: 1,
      },
      {
        id: 'ch1-2',
        title: '1.2 企业资质与荣誉',
        level: 2,
        pageNumber: 2,
      },
      {
        id: 'ch1-3',
        title: '1.3 组织结构与管理体系',
        level: 2,
        pageNumber: 3,
      },
    ],
  },
  {
    id: 'ch2',
    title: '第二章 技术方案',
    level: 1,
    pageNumber: 5,
    children: [
      {
        id: 'ch2-1',
        title: '2.1 总体设计方案',
        level: 2,
        pageNumber: 5,
      },
      {
        id: 'ch2-2',
        title: '2.2 系统架构',
        level: 2,
        pageNumber: 6,
        children: [
          {
            id: 'ch2-2-1',
            title: '2.2.1 硬件架构',
            level: 3,
            pageNumber: 6,
          },
          {
            id: 'ch2-2-2',
            title: '2.2.2 软件架构',
            level: 3,
            pageNumber: 7,
          },
        ],
      },
      {
        id: 'ch2-3',
        title: '2.3 关键技术指标',
        level: 2,
        pageNumber: 8,
      },
    ],
  },
  {
    id: 'ch3',
    title: '第三章 商务方案',
    level: 1,
    pageNumber: 10,
    children: [
      {
        id: 'ch3-1',
        title: '3.1 报价清单',
        level: 2,
        pageNumber: 10,
      },
      {
        id: 'ch3-2',
        title: '3.2 付款条件',
        level: 2,
        pageNumber: 11,
      },
      {
        id: 'ch3-3',
        title: '3.3 服务承诺',
        level: 2,
        pageNumber: 12,
      },
    ],
  },
  {
    id: 'ch4',
    title: '第四章 项目管理与实施计划',
    level: 1,
    pageNumber: 14,
    children: [
      {
        id: 'ch4-1',
        title: '4.1 项目管理体系',
        level: 2,
        pageNumber: 14,
      },
      {
        id: 'ch4-2',
        title: '4.2 实施进度计划',
        level: 2,
        pageNumber: 15,
      },
    ],
  },
  {
    id: 'ch5',
    title: '第五章 售后服务',
    level: 1,
    pageNumber: 17,
    children: [
      {
        id: 'ch5-1',
        title: '5.1 技术支持',
        level: 2,
        pageNumber: 17,
      },
      {
        id: 'ch5-2',
        title: '5.2 维护保障',
        level: 2,
        pageNumber: 18,
      },
    ],
  },
]

const isClient = ref(true)
const chapters = ref<Chapter[]>(mockChapters)
const expandedItems = ref<Set<string>>(new Set())

onMounted(() => {
  isClient.value = false
  requestAnimationFrame(() => {
    isClient.value = true
  })
})

const toggleExpand = (id: string) => {
  if (expandedItems.value.has(id)) {
    expandedItems.value.delete(id)
  } else {
    expandedItems.value.add(id)
  }
}

const navigateToContent = (chapterId: string) => {
  if (typeof window !== 'undefined') {
    window.location.href = `./bid-document-content-view.html?chapterId=${chapterId}`
  }
}

const goBack = () => {
  if (typeof window !== 'undefined') {
    window.history.back()
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center gap-4 mb-4">
        <Button
          variant="ghost"
          size="icon"
          @click="goBack"
          class="h-10 w-10"
        >
          <SafeIcon name="ArrowLeft" :size="20" />
        </Button>
        <div>
          <h1 class="text-3xl font-bold">投标书章节目录</h1>
          <p class="text-muted-foreground mt-1">共 {{ chapters.length }} 个主章节</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <Card class="border shadow-card">
      <CardHeader class="border-b bg-muted/50">
        <CardTitle class="text-lg">文档结构</CardTitle>
        <CardDescription>点击章节可查看详细内容</CardDescription>
      </CardHeader>

      <CardContent class="p-0">
        <ScrollArea class="h-[calc(100vh-300px)]">
          <div class="p-6 space-y-2">
            <template v-for="chapter in chapters" :key="chapter.id">
              <ChapterTreeItem
                :chapter="chapter"
                :expanded="expandedItems.has(chapter.id)"
                :is-client="isClient || true"
                @toggle-expand="toggleExpand"
                @navigate="navigateToContent"
              />
            </template>
          </div>
        </ScrollArea>
      </CardContent>
    </Card>

    <!-- Action Buttons -->
    <div class="flex gap-3 mt-8 justify-center">
      <Button
        variant="outline"
        @click="goBack"
      >
        <SafeIcon name="ArrowLeft" :size="18" class="mr-2" />
        返回预览页
      </Button>
      <Button
        @click="navigateToContent(chapters[0]?.id || '')"
      >
        <SafeIcon name="FileText" :size="18" class="mr-2" />
        查看第一章内容
      </Button>
    </div>
  </div>
</template>

<style scoped>
/* Smooth transitions for expand/collapse */
:deep(.chapter-item) {
  transition: all 0.2s ease-in-out;
}
</style>

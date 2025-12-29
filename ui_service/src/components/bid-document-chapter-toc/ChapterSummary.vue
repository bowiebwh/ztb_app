
<script setup lang="ts">
import { computed } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Chapter {
  id: string
  title: string
  level: number
  pageStart: number
  pageEnd: number
  summary: string
  children?: Chapter[]
  contentType: 'text' | 'image' | 'table' | 'mixed'
}

interface Props {
  selectedChapterId: string | null
  chapters: Chapter[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  navigate: [chapterId: string]
}>()

const selectedChapter = computed(() => {
  if (!props.selectedChapterId) return null
  
  const findChapter = (chapters: Chapter[]): Chapter | null => {
    for (const chapter of chapters) {
      if (chapter.id === props.selectedChapterId) return chapter
      if (chapter.children) {
        const found = findChapter(chapter.children)
        if (found) return found
      }
    }
    return null
  }
  
  return findChapter(props.chapters)
})

const contentTypeLabel = computed(() => {
  if (!selectedChapter.value) return ''
  const labels: Record<string, string> = {
    text: '文本',
    image: '图片',
    table: '表格',
    mixed: '混合内容',
  }
  return labels[selectedChapter.value.contentType] || '未知'
})

const pageCount = computed(() => {
  if (!selectedChapter.value) return 0
  return selectedChapter.value.pageEnd - selectedChapter.value.pageStart + 1
})

const handleNavigate = () => {
  if (selectedChapter.value) {
    emit('navigate', selectedChapter.value.id)
  }
}
</script>

<template>
  <div>
    <Card v-if="selectedChapter" class="sticky top-24">
      <CardHeader>
        <CardTitle class="text-base">章节详情</CardTitle>
      </CardHeader>
      <CardContent class="space-y-4">
        <!-- Title -->
        <div>
          <h3 class="font-semibold text-sm mb-2">{{ selectedChapter.title }}</h3>
          <p class="text-xs text-muted-foreground">
            {{ selectedChapter.summary }}
          </p>
        </div>

        <Separator />

        <!-- Info Grid -->
        <div class="space-y-3">
          <!-- Pages -->
          <div class="flex items-center justify-between">
            <span class="text-xs text-muted-foreground">页码范围</span>
            <span class="text-sm font-medium">
              第 {{ selectedChapter.pageStart }}-{{ selectedChapter.pageEnd }} 页
            </span>
          </div>

          <!-- Page Count -->
          <div class="flex items-center justify-between">
            <span class="text-xs text-muted-foreground">页数</span>
            <span class="text-sm font-medium">{{ pageCount }} 页</span>
          </div>

          <!-- Content Type -->
          <div class="flex items-center justify-between">
            <span class="text-xs text-muted-foreground">内容类型</span>
            <Badge variant="secondary" class="text-xs">
              {{ contentTypeLabel }}
            </Badge>
          </div>

          <!-- Level -->
          <div class="flex items-center justify-between">
            <span class="text-xs text-muted-foreground">层级</span>
            <span class="text-sm font-medium">
              {{ selectedChapter.level === 1 ? '主章节' : '子章节' }}
            </span>
          </div>
        </div>

        <Separator />

        <!-- Action Button -->
        <Button
          @click="handleNavigate"
          class="w-full gap-2"
        >
          <SafeIcon name="Eye" :size="16" />
          查看内容
        </Button>
      </CardContent>
    </Card>

    <!-- Empty State -->
    <Card v-else class="sticky top-24">
      <CardContent class="pt-6">
        <div class="text-center py-8">
          <SafeIcon name="FileText" :size="32" class="mx-auto text-muted-foreground mb-3" />
          <p class="text-sm text-muted-foreground">
            选择左侧章节查看详情
          </p>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

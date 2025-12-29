
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { DocumentTOCModel } from '@/data/generation'

interface Props {
  toc: DocumentTOCModel[]
}

const props = defineProps<Props>()

const isClient = ref(true)
const selectedChapterId = ref<string | null>(null)
const activeTab = ref('overview')

onMounted(() => {
  isClient.value = false
  requestAnimationFrame(() => {
    isClient.value = true
  })
})

const selectedChapter = computed(() => {
  if (!selectedChapterId.value) return null
  return findChapterById(props.toc, selectedChapterId.value)
})

const findChapterById = (items: DocumentTOCModel[], id: string): DocumentTOCModel | null => {
  for (const item of items) {
    if (item.id === id) return item
    if (item.children) {
      const found = findChapterById(item.children, id)
      if (found) return found
    }
  }
  return null
}

const handleSelectChapter = (id: string) => {
  selectedChapterId.value = id
  activeTab.value = 'content'
}
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle class="flex items-center gap-2">
        <SafeIcon name="BookOpen" :size="20" />
        内容预览
      </CardTitle>
    </CardHeader>
    <CardContent>
      <Tabs v-model="activeTab" class="w-full">
        <TabsList class="grid w-full grid-cols-2">
          <TabsTrigger value="overview">概览</TabsTrigger>
          <TabsTrigger value="content">详细内容</TabsTrigger>
        </TabsList>

        <!-- Overview Tab -->
        <TabsContent value="overview" class="space-y-4 mt-4">
          <div class="space-y-3">
            <h3 class="font-semibold text-sm">投标书结构</h3>
            <div class="space-y-2 text-sm">
              <template v-for="item in toc" :key="item.id">
                <div class="flex items-center gap-2 p-2 rounded hover:bg-muted cursor-pointer transition-colors"
                     @click="handleSelectChapter(item.id)">
                  <SafeIcon name="FileText" :size="16" class="text-muted-foreground" />
                  <div class="flex-1">
                    <p class="font-medium">{{ item.index }} {{ item.title }}</p>
                    <p v-if="item.children.length > 0" class="text-xs text-muted-foreground">
                      包含 {{ item.children.length }} 个子章节
                    </p>
                  </div>
                  <SafeIcon name="ChevronRight" :size="16" class="text-muted-foreground" />
                </div>
              </template>
            </div>
          </div>

          <div class="pt-4 border-t space-y-3">
            <h3 class="font-semibold text-sm">文档统计</h3>
            <div class="grid grid-cols-3 gap-4">
              <div class="text-center p-3 rounded-lg bg-muted">
                <p class="text-2xl font-bold text-primary">{{ toc.length }}</p>
                <p class="text-xs text-muted-foreground mt-1">主章节</p>
              </div>
              <div class="text-center p-3 rounded-lg bg-muted">
                <p class="text-2xl font-bold text-primary">
                  {{ toc.reduce((sum, item) => sum + item.children.length, 0) }}
                </p>
                <p class="text-xs text-muted-foreground mt-1">子章节</p>
              </div>
              <div class="text-center p-3 rounded-lg bg-muted">
                <p class="text-2xl font-bold text-primary">100%</p>
                <p class="text-xs text-muted-foreground mt-1">完成度</p>
              </div>
            </div>
          </div>
        </TabsContent>

        <!-- Content Tab -->
        <TabsContent value="content" class="space-y-4 mt-4">
          <div v-if="selectedChapterId" class="space-y-4">
            <div v-if="selectedChapter" class="space-y-4">
              <div class="border-b pb-4">
                <h2 class="text-xl font-semibold">
                  {{ selectedChapter.index }} {{ selectedChapter.title }}
                </h2>
              </div>

              <!-- Mock Content -->
              <div class="prose prose-sm max-w-none dark:prose-invert">
                <p class="text-muted-foreground">
                  本章节内容已从招标文件中提取并由AI系统生成。以下为该章节的主要内容概览。
                </p>
                
                <div class="mt-4 p-4 bg-muted rounded-lg">
                  <p class="text-sm">
                    <strong>{{ selectedChapter.title }}</strong> 部分详细阐述了项目的核心需求和实施方案。
                    该章节包含了系统架构设计、技术方案、实施计划等关键信息，确保投标文件的完整性和专业性。
                  </p>
                </div>

                <div v-if="selectedChapter.children.length > 0" class="mt-4 space-y-3">
                  <h3 class="font-semibold">子章节列表</h3>
                  <ul class="space-y-2">
                    <li v-for="child in selectedChapter.children" :key="child.id" class="flex items-start gap-2">
                      <SafeIcon name="ChevronRight" :size="16" class="text-primary mt-0.5 flex-shrink-0" />
                      <span>{{ child.index }} {{ child.title }}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-8 text-muted-foreground">
            <SafeIcon name="BookOpen" :size="32" class="mx-auto mb-2 opacity-50" />
            <p>请从左侧章节目录中选择要查看的章节</p>
          </div>
        </TabsContent>
      </Tabs>
    </CardContent>
  </Card>
</template>

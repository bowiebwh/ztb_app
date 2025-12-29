
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import type { GenerationTaskModel, DocumentTOCModel } from '@/data/generation'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  task: GenerationTaskModel
  visible?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  visible: true,
})

const emit = defineEmits<{
  regenerate: []
  back: []
}>()

const isClient = ref(true)
const selectedChapter = ref<DocumentTOCModel | null>(null)
const isDownloading = ref(false)

const flattenToc = (items: DocumentTOCModel[] = []): DocumentTOCModel[] => {
  return items.reduce((acc, item) => {
    acc.push(item)
    if (item.children && item.children.length > 0) {
      acc.push(...flattenToc(item.children))
    }
    return acc
  }, [] as DocumentTOCModel[])
}

const allChapters = computed(() => {
  return flattenToc(props.task.generatedToc || [])
})

const handleDownload = async () => {
  isDownloading.value = true
  // 模拟下载延迟
  setTimeout(() => {
    if (props.task.resultUrl && typeof window !== 'undefined') {
      const link = document.createElement('a')
      link.href = props.task.resultUrl
      link.download = `投标书-${new Date().toISOString().split('T')[0]}.docx`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
    isDownloading.value = false
  }, 1000)
}

const handleRegenerate = () => {
  emit('regenerate')
}

const handleBack = () => {
  emit('back')
}

onMounted(() => {
  isClient.value = false
  requestAnimationFrame(() => {
    isClient.value = true
  })

  // 默认选择第一个章节
  if (allChapters.value.length > 0) {
    selectedChapter.value = allChapters.value[0]
  }
})
</script>

<template>
  <div v-if="visible" class="space-y-6">
    <!-- 成功提示 -->
    <Card class="border-green-200 bg-green-50 dark:border-green-900/30 dark:bg-green-900/10">
      <CardContent class="pt-6">
        <div class="flex gap-3">
          <SafeIcon name="CheckCircle2" :size="20" class="text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
          <div class="flex-1">
            <p class="text-sm font-medium text-green-800 dark:text-green-300 mb-1">生成成功</p>
            <p class="text-xs text-green-700 dark:text-green-400">
              投标书已成功生成，您可以预览内容或直接下载Word文件。
            </p>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- 预览卡片 -->
    <Card>
      <CardHeader>
        <CardTitle>投标书预览</CardTitle>
        <CardDescription>查看生成的投标书内容和结构</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="toc" class="w-full">
          <TabsList class="grid w-full grid-cols-2">
            <TabsTrigger value="toc">章节目录</TabsTrigger>
            <TabsTrigger value="content">内容预览</TabsTrigger>
          </TabsList>

          <!-- 章节目录标签页 -->
          <TabsContent value="toc" class="space-y-4">
            <div class="space-y-2 max-h-96 overflow-y-auto">
              <button
                v-for="chapter in allChapters"
                :key="chapter.id"
                @click="selectedChapter = chapter"
                :class="[
                  'w-full text-left px-3 py-2 rounded-lg transition-colors',
                  selectedChapter?.id === chapter.id
                    ? 'bg-primary text-primary-foreground'
                    : 'hover:bg-muted'
                ]"
              >
                <div class="flex items-center gap-2">
                  <span class="text-sm font-medium">{{ chapter.index }}</span>
                  <span class="text-sm">{{ chapter.title }}</span>
                </div>
              </button>
            </div>
          </TabsContent>

          <!-- 内容预览标签页 -->
          <TabsContent value="content" class="space-y-4">
            <div v-if="selectedChapter" class="space-y-4">
              <div class="border-b pb-4">
                <div class="flex items-center gap-2 mb-2">
                  <Badge variant="outline">{{ selectedChapter.index }}</Badge>
                  <h3 class="text-lg font-semibold">{{ selectedChapter.title }}</h3>
                </div>
              </div>
              <div class="prose prose-sm dark:prose-invert max-w-none">
                <p class="text-muted-foreground text-sm">
                  这是章节 "{{ selectedChapter.title }}" 的内容预览。
                  完整的内容将在下载的Word文件中显示。
                </p>
              </div>
            </div>
            <div v-else class="text-center py-8 text-muted-foreground">
              <p>请从左侧选择章节查看内容</p>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>

    <!-- 文件信息 -->
    <Card>
      <CardHeader>
        <CardTitle class="text-base">文件信息</CardTitle>
      </CardHeader>
      <CardContent class="space-y-3">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-xs text-muted-foreground mb-1">文件格式</p>
            <p class="text-sm font-medium">Word (.docx)</p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground mb-1">生成时间</p>
            <p class="text-sm font-medium">
              {{ new Date(props.task.startTime).toLocaleString('zh-CN') }}
            </p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground mb-1">章节数</p>
            <p class="text-sm font-medium">{{ allChapters.length }}</p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground mb-1">任务ID</p>
            <p class="text-sm font-mono">{{ props.task.taskId }}</p>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- 操作按钮 -->
    <div class="flex gap-3 justify-end">
      <Button
        variant="outline"
        @click="handleBack"
      >
        返回项目
      </Button>
      <Button
        variant="outline"
        @click="handleRegenerate"
      >
        重新生成
      </Button>
      <Button
        @click="handleDownload"
        :disabled="isDownloading"
      >
        <SafeIcon v-if="isDownloading" name="Loader2" :size="16" class="mr-2 animate-spin" />
        {{ isDownloading ? '下载中...' : '下载Word文件' }}
      </Button>
    </div>
  </div>
</template>

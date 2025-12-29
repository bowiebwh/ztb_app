
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import SafeIcon from '@/components/common/SafeIcon.vue'
import StepNavigation from '@/components/common/StepNavigation.vue'
import { WORKFLOW_STEPS } from '@/data/config'

// Mock data for analysis progress and results
interface AnalysisStage {
  id: string
  name: string
  status: 'pending' | 'in-progress' | 'completed' | 'failed'
  progress: number
}

interface KeyInfo {
  label: string
  value: string
}

interface AnalysisResult {
  projectId: string
  fileName: string
  uploadTime: string
  stages: AnalysisStage[]
  overallProgress: number
  keyInfo: KeyInfo[]
  documentStructure: {
    chapters: Array<{
      id: string
      title: string
      sections: string[]
    }>
  }
  status: 'analyzing' | 'completed' | 'failed'
  errorMessage?: string
}

const isClient = ref(true)

// Mock analysis result
const analysisResult = ref<AnalysisResult>({
  projectId: 'proj-001',
  fileName: '智捷云招投标系统采购项目招标说明书.pdf',
  uploadTime: '2025-12-19 14:30:00',
  stages: [
    { id: 'extract', name: '文件提取', status: 'completed', progress: 100 },
    { id: 'parse', name: '内容解析', status: 'completed', progress: 100 },
    { id: 'structure', name: '结构识别', status: 'completed', progress: 100 },
    { id: 'knowledge', name: '知识库匹配', status: 'completed', progress: 100 },
  ],
  overallProgress: 100,
  keyInfo: [
    { label: '招标单位', value: '智捷云科技有限公司' },
    { label: '项目名称', value: '智捷云招投标系统采购项目' },
    { label: '招标方式', value: '公开招标' },
    { label: '预算金额', value: '500万元' },
    { label: '投标截止时间', value: '2025-12-31 17:00:00' },
    { label: '开标时间', value: '2026-01-05 10:00:00' },
  ],
  documentStructure: {
    chapters: [
      {
        id: 'ch1',
        title: '第一章 投标邀请',
        sections: ['投标邀请', '招标人信息', '招标代理机构'],
      },
      {
        id: 'ch2',
        title: '第二章 投标人须知',
        sections: ['投标人资格要求', '投标文件编制', '投标文件递交'],
      },
      {
        id: 'ch3',
        title: '第三章 评标办法',
        sections: ['评标委员会', '评标原则', '评分标准'],
      },
      {
        id: 'ch4',
        title: '第四章 合同条款',
        sections: ['合同形式', '合同主要条款', '履行期限'],
      },
    ],
  },
  status: 'completed',
})

const currentStepId = 'analyze_tender_content_step'

const stepsWithHref = computed(() => {
  return WORKFLOW_STEPS.map(step => ({
    id: step.id,
    label: step.title,
    href: step.routePath,
  }))
})

const isAnalyzing = computed(() => analysisResult.value.status === 'analyzing')
const isCompleted = computed(() => analysisResult.value.status === 'completed')
const isFailed = computed(() => analysisResult.value.status === 'failed')

onMounted(() => {
  isClient.value = false
  
  // Simulate analysis progress if needed
  if (isAnalyzing.value) {
    const interval = setInterval(() => {
      const totalProgress = analysisResult.value.stages.reduce((sum, s) => sum + s.progress, 0) / analysisResult.value.stages.length
      if (totalProgress < 100) {
        analysisResult.value.stages.forEach(stage => {
          if (stage.status === 'in-progress' && stage.progress < 100) {
            stage.progress = Math.min(stage.progress + Math.random() * 20, 100)
          }
        })
        analysisResult.value.overallProgress = Math.min(analysisResult.value.overallProgress + 5, 95)
      } else {
        analysisResult.value.status = 'completed'
        analysisResult.value.overallProgress = 100
        clearInterval(interval)
      }
    }, 1000)
  }
  
  // Trigger animation
  setTimeout(() => {
    isClient.value = true
  }, 0)
})

const handlePreviousStep = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './upload-tender-document-step.html'
  }
}

const handleNextStep = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './edit-bid-document-step.html'
  }
}
</script>

<template>
  <div class="flex h-full">
    <!-- Left Sidebar: Step Navigation -->
    <aside class="w-64 border-r bg-sidebar p-6 overflow-y-auto">
      <div class="mb-6">
        <h3 class="text-sm font-semibold text-sidebar-foreground mb-4">工作流程</h3>
        <StepNavigation
          :steps="stepsWithHref"
          :current-step="currentStepId"
          orientation="vertical"
        />
      </div>
    </aside>

    <!-- Center: Main Content -->
    <main class="flex-1 overflow-y-auto">
      <div class="p-8 max-w-4xl mx-auto">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold mb-2">招标内容解析</h1>
          <p class="text-muted-foreground">AI服务正在解析您上传的招标文件，请耐心等待</p>
        </div>

        <!-- File Info Card -->
        <Card class="mb-6">
          <CardHeader>
            <CardTitle class="text-lg">文件信息</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-muted-foreground mb-1">文件名</p>
                <p class="font-medium">{{ analysisResult.fileName }}</p>
              </div>
              <div>
                <p class="text-sm text-muted-foreground mb-1">上传时间</p>
                <p class="font-medium">{{ analysisResult.uploadTime }}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Analysis Progress Section -->
        <Card class="mb-6">
          <CardHeader>
            <CardTitle class="text-lg">解析进度</CardTitle>
            <CardDescription>系统正在多阶段处理您的招标文件</CardDescription>
          </CardHeader>
          <CardContent class="space-y-6">
            <!-- Overall Progress -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <span class="text-sm font-medium">总体进度</span>
                <span class="text-sm text-muted-foreground">{{ analysisResult.overallProgress }}%</span>
              </div>
              <Progress :value="analysisResult.overallProgress" class="h-2" />
            </div>

            <!-- Stage Progress -->
            <div class="space-y-4">
              <div v-for="stage in analysisResult.stages" :key="stage.id" class="space-y-2">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <SafeIcon
                      v-if="stage.status === 'completed'"
                      name="CheckCircle2"
                      :size="18"
                      class="text-green-600"
                    />
                    <SafeIcon
                      v-else-if="stage.status === 'in-progress'"
                      name="Loader2"
                      :size="18"
                      class="text-blue-600 animate-spin"
                    />
                    <SafeIcon
                      v-else-if="stage.status === 'failed'"
                      name="XCircle"
                      :size="18"
                      class="text-red-600"
                    />
                    <SafeIcon
                      v-else
                      name="Circle"
                      :size="18"
                      class="text-muted-foreground"
                    />
                    <span class="text-sm font-medium">{{ stage.name }}</span>
                  </div>
                  <span class="text-sm text-muted-foreground">{{ stage.progress }}%</span>
                </div>
                <Progress :value="stage.progress" class="h-1.5" />
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Key Information Section -->
        <Card v-if="isCompleted || !isAnalyzing" class="mb-6">
          <CardHeader>
            <CardTitle class="text-lg">关键信息提取</CardTitle>
            <CardDescription>系统从招标文件中提取的重要信息</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="grid grid-cols-2 gap-6">
              <div v-for="info in analysisResult.keyInfo" :key="info.label">
                <p class="text-sm text-muted-foreground mb-1">{{ info.label }}</p>
                <p class="font-medium text-foreground">{{ info.value }}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Document Structure Section -->
        <Card v-if="isCompleted || !isAnalyzing" class="mb-6">
          <CardHeader>
            <CardTitle class="text-lg">初步文档结构</CardTitle>
            <CardDescription>系统识别的投标文档章节结构</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="space-y-4">
              <div
                v-for="chapter in analysisResult.documentStructure.chapters"
                :key="chapter.id"
                class="border rounded-lg p-4"
              >
                <h4 class="font-semibold text-foreground mb-2">{{ chapter.title }}</h4>
                <div class="flex flex-wrap gap-2">
                  <Badge
                    v-for="section in chapter.sections"
                    :key="section"
                    variant="secondary"
                  >
                    {{ section }}
                  </Badge>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Error State -->
        <Card v-if="isFailed" class="mb-6 border-red-200 bg-red-50 dark:bg-red-950/20">
          <CardHeader>
            <CardTitle class="text-lg text-red-600">解析失败</CardTitle>
          </CardHeader>
          <CardContent>
            <p class="text-red-600">{{ analysisResult.errorMessage || '解析过程中出现错误，请重新上传文件' }}</p>
          </CardContent>
        </Card>

        <!-- Navigation Buttons -->
        <div class="flex justify-between gap-4 mt-8">
          <Button
            variant="outline"
            @click="handlePreviousStep"
          >
            <SafeIcon name="ChevronLeft" :size="18" class="mr-2" />
            上一步
          </Button>
          <Button
            @click="handleNextStep"
            :disabled="!isCompleted"
          >
            下一步
            <SafeIcon name="ChevronRight" :size="18" class="ml-2" />
          </Button>
        </div>
      </div>
    </main>

    <!-- Right Sidebar: Material Library (Placeholder) -->
    <aside class="w-64 border-l bg-sidebar p-6 overflow-y-auto hidden lg:block">
      <h3 class="text-sm font-semibold text-sidebar-foreground mb-4">材料库</h3>
      <div class="text-sm text-muted-foreground text-center py-8">
        <SafeIcon name="FileStack" :size="32" class="mx-auto mb-2 opacity-50" />
        <p>在编辑步骤中打开材料库</p>
      </div>
    </aside>
  </div>
</template>

<style scoped>
/* Page-specific styles */
:deep(.progress) {
  @apply bg-muted;
}
</style>

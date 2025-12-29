
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import StepNavigation from '@/components/common/StepNavigation.vue'
import SafeIcon from '@/components/common/SafeIcon.vue'
import UploadArea from './UploadArea.vue'
import UploadedFileList from './UploadedFileList.vue'
import { WORKFLOW_STEPS } from '@/data/config'

interface UploadedFile {
  id: string
  name: string
  size: number
  type: string
  uploadedAt: string
  status: 'success' | 'uploading' | 'failed'
  progress?: number
}

const isClient = ref(true)
const uploadedFiles = ref<UploadedFile[]>([
  {
    id: '1',
    name: '招标说明书_2024.pdf',
    size: 2048000,
    type: 'pdf',
    uploadedAt: '2024-01-15 10:30',
    status: 'success',
  },
])

const isUploading = ref(false)
const uploadProgress = ref(0)

onMounted(() => {
  isClient.value = false
  
  // 模拟初始化
  setTimeout(() => {
    isClient.value = true
  }, 0)
})

const handleFileUpload = (files: File[]) => {
  isUploading.value = true
  uploadProgress.value = 0

  // 模拟上传进度
  const interval = setInterval(() => {
    uploadProgress.value += Math.random() * 30
    if (uploadProgress.value >= 100) {
      uploadProgress.value = 100
      clearInterval(interval)
      
      // 模拟上传完成
      setTimeout(() => {
        files.forEach((file) => {
          uploadedFiles.value.push({
            id: Math.random().toString(36).substr(2, 9),
            name: file.name,
            size: file.size,
            type: file.type.split('/')[1] || 'unknown',
            uploadedAt: new Date().toLocaleString('zh-CN'),
            status: 'success',
          })
        })
        isUploading.value = false
        uploadProgress.value = 0
      }, 500)
    }
  }, 300)
}

const handleRemoveFile = (fileId: string) => {
  uploadedFiles.value = uploadedFiles.value.filter(f => f.id !== fileId)
}

const handleNextStep = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './analyze-tender-content-step.html'
  }
}

const handlePreviousStep = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './project-detail-editor.html'
  }
}
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- Header -->
    <div class="border-b bg-background/50 backdrop-blur-sm sticky top-16 z-40">
      <div class="container mx-auto px-6 py-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h1 class="text-3xl font-bold">上传招标文件</h1>
            <p class="text-muted-foreground mt-1">上传招标说明书，系统将自动解析文件内容</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-sm text-muted-foreground">第 1 / 4 步</span>
          </div>
        </div>

        <!-- Step Navigation -->
        <StepNavigation
          :steps="WORKFLOW_STEPS"
          current-step="upload_tender_document_step"
          orientation="horizontal"
        />
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-auto">
      <div class="container mx-auto px-6 py-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Left: Upload Area -->
          <div class="lg:col-span-2 space-y-6">
            <!-- Upload Card -->
            <Card>
              <CardHeader>
                <CardTitle>上传招标文件</CardTitle>
                <CardDescription>
                  支持 PDF、Word、Excel 等格式，单个文件不超过 100MB
                </CardDescription>
              </CardHeader>
              <CardContent>
                <UploadArea
                  :is-uploading="isUploading"
                  :progress="uploadProgress"
                  @upload="handleFileUpload"
                />
              </CardContent>
            </Card>

            <!-- Uploaded Files -->
            <Card v-if="uploadedFiles.length > 0 || isClient">
              <CardHeader>
                <CardTitle class="text-lg">已上传文件</CardTitle>
                <CardDescription>
                  {{ uploadedFiles.length }} 个文件
                </CardDescription>
              </CardHeader>
              <CardContent>
                <UploadedFileList
                  :files="uploadedFiles"
                  @remove="handleRemoveFile"
                />
              </CardContent>
            </Card>
          </div>

          <!-- Right: Info Panel -->
          <div class="space-y-6">
            <!-- Tips Card -->
            <Card>
              <CardHeader>
                <CardTitle class="text-base flex items-center gap-2">
                  <SafeIcon name="Lightbulb" :size="18" class="text-amber-500" />
                  上传提示
                </CardTitle>
              </CardHeader>
              <CardContent class="space-y-3 text-sm">
                <div class="flex gap-3">
                  <SafeIcon name="CheckCircle2" :size="16" class="text-green-600 flex-shrink-0 mt-0.5" />
                  <span>确保文件清晰完整，包含所有招标要求</span>
                </div>
                <div class="flex gap-3">
                  <SafeIcon name="CheckCircle2" :size="16" class="text-green-600 flex-shrink-0 mt-0.5" />
                  <span>支持多个文件同时上传</span>
                </div>
                <div class="flex gap-3">
                  <SafeIcon name="CheckCircle2" :size="16" class="text-green-600 flex-shrink-0 mt-0.5" />
                  <span>上传后系统自动解析内容</span>
                </div>
              </CardContent>
            </Card>

            <!-- File Format Card -->
            <Card>
              <CardHeader>
                <CardTitle class="text-base">支持的文件格式</CardTitle>
              </CardHeader>
              <CardContent class="space-y-2 text-sm">
                <div class="flex items-center gap-2">
                  <SafeIcon name="FileText" :size="16" class="text-red-500" />
                  <span>PDF</span>
                </div>
                <div class="flex items-center gap-2">
                  <SafeIcon name="FileText" :size="16" class="text-blue-500" />
                  <span>Word (.docx, .doc)</span>
                </div>
                <div class="flex items-center gap-2">
                  <SafeIcon name="FileText" :size="16" class="text-green-500" />
                  <span>Excel (.xlsx, .xls)</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer Actions -->
    <div class="border-t bg-background/50 backdrop-blur-sm sticky bottom-0 z-40">
      <div class="container mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <Button
            variant="outline"
            @click="handlePreviousStep"
          >
            <SafeIcon name="ChevronLeft" :size="16" class="mr-2" />
            返回
          </Button>

          <div class="flex items-center gap-3">
            <span class="text-sm text-muted-foreground">
              {{ uploadedFiles.length > 0 ? '已上传文件，可继续' : '请先上传招标文件' }}
            </span>
            <Button
              @click="handleNextStep"
              :disabled="uploadedFiles.length === 0"
            >
              下一步
              <SafeIcon name="ChevronRight" :size="16" class="ml-2" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

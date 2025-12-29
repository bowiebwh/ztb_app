
<script setup lang="ts">
import { computed } from 'vue'
import type { Project } from '@/lib/api'
import UploadTenderDocumentStep from './steps/UploadTenderDocumentStep.vue'
import AnalyzeTenderContentStep from './steps/AnalyzeTenderContentStep.vue'
import EditBidDocumentStep from './steps/EditBidDocumentStep.vue'
import GenerateDownloadStep from './steps/GenerateDownloadStep.vue'

interface Props {
  projectId: string
  currentStepId: string
  project: Project | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'step-change': [stepId: string]
  'open-material-library': []
}>()

const stepComponents: Record<string, any> = {
  'upload_tender_document_step': UploadTenderDocumentStep,
  'analyze_tender_content_step': AnalyzeTenderContentStep,
  'generate_document_step': GenerateDownloadStep,
  'edit_bid_document_step': EditBidDocumentStep,
  'generate_download_step': GenerateDownloadStep,
}

const currentComponent = computed(() => {
  return stepComponents[props.currentStepId] || null
})
</script>

<template>
  <div class="flex flex-col h-full overflow-hidden">
    <!-- Step Header -->
    <div class="border-b bg-muted/30 px-6 py-4 flex-shrink-0">
      <h2 class="text-lg font-semibold">
        {{ getStepTitle(currentStepId) }}
      </h2>
    </div>

    <!-- Step Content -->
    <div class="flex-1 overflow-y-auto p-6">
      <component
        v-if="currentComponent"
        :is="currentComponent"
        :key="currentStepId"
        :projectId="projectId"
        :project="project"
        :mode="currentStepId === 'generate_document_step' ? 'generate' : 'download'"
        @step-change="emit('step-change', $event)"
        @open-material-library="emit('open-material-library')"
      />
    </div>
  </div>
</template>

<script lang="ts">
function getStepTitle(stepId: string): string {
  const titles: Record<string, string> = {
    'upload_tender_document_step': '上传招标文件',
    'analyze_tender_content_step': '招标内容解析',
    'generate_document_step': '生成文档',
    'edit_bid_document_step': '投标文档编辑',
    'generate_download_step': '下载文档',
  }
  return titles[stepId] || '生成文档'
}
</script>

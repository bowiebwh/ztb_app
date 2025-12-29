<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { Project } from '@/lib/api'
import { fetchProject } from '@/lib/api'

const isClient = ref(true)
const isOpen = ref(true)
const isLoading = ref(false)
const projectId = ref<string>('1')
const project = ref<Project | null>(null)

const getProjectIdFromUrl = (): string => {
  if (typeof window !== 'undefined') {
    const params = new URLSearchParams(window.location.search)
    return params.get('id') || '1'
  }
  return '1'
}

onMounted(async () => {
  isClient.value = false
  projectId.value = getProjectIdFromUrl()
  try {
    project.value = await fetchProject(projectId.value)
  } catch (error) {
    console.error('加载项目失败', error)
  } finally {
    requestAnimationFrame(() => {
      isClient.value = true
    })
  }
})

const handleDelete = async () => {
  isLoading.value = true
  try {
    await fetch(`/api/projects/${projectId.value}`, { method: 'DELETE' })
    isOpen.value = false
    setTimeout(() => {
      if (typeof window !== 'undefined') {
        window.location.href = './project-list.html'
      }
    }, 300)
  } catch (error) {
    console.error('删除项目失败:', error)
    isLoading.value = false
  }
}

const handleCancel = () => {
  isOpen.value = false
  setTimeout(() => {
    if (typeof window !== 'undefined') {
      window.location.href = './project-list.html'
    }
  }, 300)
}

const projectName = computed(() => project.value?.projectName || '未知项目')
</script>

<template>
  <Dialog :open="isOpen || isClient" @update:open="handleCancel">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle class="flex items-center gap-2">
          <SafeIcon name="AlertTriangle" :size="20" class="text-destructive" />
          确认删除项目
        </DialogTitle>
        <DialogDescription>此操作无法撤销，请谨慎操作</DialogDescription>
      </DialogHeader>

      <Alert variant="destructive">
        <AlertDescription>
          您即将删除项目：<span class="font-semibold">{{ projectName }}</span>
        </AlertDescription>
      </Alert>

      <div class="space-y-3 py-4">
        <p class="text-sm text-foreground">
          删除后，该项目的所有数据（包括上传的文件、编辑内容和生成记录）都会被永久删除。
        </p>
      </div>

      <DialogFooter class="flex gap-2 sm:justify-end">
        <Button
          variant="outline"
          @click="handleCancel"
          :disabled="isLoading"
        >
          取消
        </Button>
        <Button
          variant="destructive"
          @click="handleDelete"
          :disabled="isLoading"
        >
          <SafeIcon
            v-if="isLoading"
            name="Loader2"
            :size="16"
            class="mr-2 animate-spin"
          />
          {{ isLoading ? '删除中...' : '确认删除' }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

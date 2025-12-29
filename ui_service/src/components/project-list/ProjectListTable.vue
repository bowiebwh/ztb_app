
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import type { Project } from '@/lib/api'
import { fetchProjects } from '@/lib/api'
import { Button } from '@/components/ui/button'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import SafeIcon from '@/components/common/SafeIcon.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const isClient = ref(true)
const projects = ref<Project[]>([])
const isLoading = ref(false)
const error = ref('')
const deleteConfirmOpen = ref(false)
const projectToDelete = ref<ProjectModel | null>(null)
const isDeleting = ref(false)

const loadProjects = async () => {
  isLoading.value = true
  error.value = ''
  try {
    projects.value = await fetchProjects()
  } catch (err) {
    console.error(err)
    error.value = '加载项目失败'
  } finally {
    isLoading.value = false
    requestAnimationFrame(() => {
      isClient.value = true
    })
  }
}

onMounted(loadProjects)

// 监听创建事件以刷新列表
onMounted(() => {
  const handler = () => loadProjects()
  if (typeof window !== 'undefined') {
    window.addEventListener('project-created', handler)
  }
})

const formatDate = (dateString: string): string => {
  if (typeof window === 'undefined') {
    return dateString
  }
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return dateString
  }
}

const getStatusVariant = (status: string): 'draft' | 'in-progress' | 'completed' | 'failed' | 'waiting' => {
  const statusMap: Record<string, 'draft' | 'in-progress' | 'completed' | 'failed' | 'waiting'> = {
    'Draft': 'draft',
    'Generating': 'in-progress',
    'Completed': 'completed',
    'Failed': 'failed',
  }
  return statusMap[status] || 'draft'
}

const handleEdit = (project: ProjectModel) => {
  if (typeof window !== 'undefined') {
    window.location.href = `./project-detail-editor.html?id=${project.projectId}`
  }
}

const handleDeleteClick = (project: ProjectModel) => {
  projectToDelete.value = project
  deleteConfirmOpen.value = true
}

const handleConfirmDelete = async () => {
  if (!projectToDelete.value) return
  
  isDeleting.value = true
  try {
    await fetch(`${import.meta.env.VITE_API_BASE || 'http://localhost:8000'}/api/projects/${projectToDelete.value.projectId}`, {
      method: 'DELETE',
    })
    projects.value = projects.value.filter(p => p.projectId !== projectToDelete.value?.projectId)
  } catch (err) {
    console.error('删除失败', err)
  } finally {
    isDeleting.value = false
    deleteConfirmOpen.value = false
    projectToDelete.value = null
  }
}

const handleCancelDelete = () => {
  deleteConfirmOpen.value = false
  projectToDelete.value = null
}

const hasProjects = computed(() => projects.value.length > 0)
</script>

<template>
  <div v-if="hasProjects || isClient" class="rounded-lg border bg-card">
    <div v-if="hasProjects" class="overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead class="w-[30%]">项目名称</TableHead>
            <TableHead class="w-[15%]">状态</TableHead>
            <TableHead class="w-[20%]">创建时间</TableHead>
            <TableHead class="w-[20%]">更新时间</TableHead>
            <TableHead class="w-[15%] text-right">操作</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="project in projects" :key="project.projectId" class="hover:bg-muted/50">
            <TableCell class="font-medium">
              <button
                @click="handleEdit(project)"
                class="text-primary hover:underline transition-colors"
              >
                {{ project.projectName }}
              </button>
            </TableCell>
            <TableCell>
              <StatusBadge :status="getStatusVariant(project.status)" :show-icon="true" size="sm" />
            </TableCell>
            <TableCell class="text-sm text-muted-foreground">
              {{ formatDate(project.createTime) }}
            </TableCell>
            <TableCell class="text-sm text-muted-foreground">
              {{ formatDate(project.updateTime) }}
            </TableCell>
            <TableCell class="text-right">
              <div class="flex items-center justify-end gap-2">
              <Button
                  variant="ghost"
                  size="sm"
                  @click="handleEdit(project)"
                  class="gap-1"
                >
                  <SafeIcon name="Edit2" :size="16" />
                  <span class="hidden sm:inline">编辑</span>
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  @click="handleDeleteClick(project)"
                  class="gap-1 text-destructive hover:text-destructive hover:bg-destructive/10"
                >
                  <SafeIcon name="Trash2" :size="16" />
                  <span class="hidden sm:inline">删除</span>
                </Button>
              </div>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <div v-else class="py-10">
      <EmptyState
        v-if="!isLoading && !error"
        icon="FolderOpen"
        title="暂无项目"
        description='还没有创建任何项目。点击上方的"创建项目"按钮开始新项目。'
      />
      <div v-else-if="error" class="text-center text-sm text-red-500">{{ error }}</div>
      <div v-else class="text-center text-sm text-muted-foreground">加载中...</div>
    </div>
  </div>

<!-- Delete Confirmation Dialog -->
  <ConfirmDialog
    :open="deleteConfirmOpen"
    title="确认删除项目"
    :description="`确定要删除项目 ${projectToDelete?.projectName} 吗？此操作无法撤销。`"
    confirm-text="删除"
    cancel-text="取消"
    variant="destructive"
    :loading="isDeleting"
    @update:open="deleteConfirmOpen = $event"
    @confirm="handleConfirmDelete"
    @cancel="handleCancelDelete"
  />
</template>

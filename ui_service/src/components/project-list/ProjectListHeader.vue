
<script setup lang="ts">
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'
import CreateProjectModal from '@/components/project-list/CreateProjectModal.vue'

const showCreateModal = ref(false)

const handleCreateProject = () => {
  showCreateModal.value = true
}

const handleModalClose = () => {
  showCreateModal.value = false
}
</script>

<template>
  <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">项目管理</h1>
      <p class="text-muted-foreground mt-2">管理和编辑您的招投标项目</p>
    </div>
    
    <Button @click="handleCreateProject" size="lg" class="gap-2">
      <SafeIcon name="Plus" :size="20" />
      <span>创建项目</span>
    </Button>
  </div>

  <CreateProjectModal
    :open="showCreateModal"
    @update:open="showCreateModal = $event"
    @close="handleModalClose"
  />
</template>


<script setup lang="ts">
import { computed } from 'vue'
import { Empty, EmptyContent, EmptyDescription, EmptyHeader, EmptyTitle } from '@/components/ui/empty'
import MaterialCard from './MaterialCard.vue'
import type { MaterialModel } from '@/src/data/materials'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  materials: MaterialModel[]
  isClient?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isClient: true,
})

const isEmpty = computed(() => props.materials.length === 0)
</script>

<template>
  <div>
    <div v-if="!isEmpty" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <MaterialCard
        v-for="material in materials"
        :key="material.materialId"
        :material="material"
        :is-client="isClient"
      />
    </div>

    <Empty v-else>
      <EmptyHeader>
        <div class="w-16 h-16 rounded-full bg-muted flex items-center justify-center mx-auto mb-4">
          <SafeIcon name="Inbox" :size="32" class="text-muted-foreground" />
        </div>
      </EmptyHeader>
      <EmptyTitle>暂无文件</EmptyTitle>
      <EmptyDescription>
        上传文件开始管理您的投标资源
      </EmptyDescription>
      <EmptyContent>
        <p class="text-sm text-muted-foreground">
          支持上传图片、PDF、Word 和 Excel 文件
        </p>
      </EmptyContent>
    </Empty>
  </div>
</template>

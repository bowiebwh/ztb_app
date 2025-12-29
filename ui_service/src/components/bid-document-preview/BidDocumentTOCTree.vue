
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { cn } from '@/lib/utils'
import type { DocumentTOCModel } from '@/data/generation'

interface Props {
  toc: DocumentTOCModel[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  selectChapter: [id: string]
}>()

const isClient = ref(true)
const expandedIds = ref<Set<string>>(new Set())
const selectedId = ref<string | null>(null)

onMounted(() => {
  isClient.value = false
  requestAnimationFrame(() => {
    isClient.value = true
  })
})

const toggleExpand = (id: string) => {
  if (expandedIds.value.has(id)) {
    expandedIds.value.delete(id)
  } else {
    expandedIds.value.add(id)
  }
}

const selectChapter = (id: string) => {
  selectedId.value = id
  emit('selectChapter', id)
}

const hasChildren = (item: DocumentTOCModel): boolean => {
  return item.children && item.children.length > 0
}

const isExpanded = (id: string): boolean => {
  return expandedIds.value.has(id)
}
</script>

<template>
  <Card class="sticky top-20 h-fit">
    <CardHeader>
      <CardTitle class="text-lg flex items-center gap-2">
        <SafeIcon name="List" :size="20" />
        章节目录
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div class="space-y-1">
        <template v-for="item in toc" :key="item.id">
          <div class="space-y-1">
            <!-- Chapter Item -->
            <div class="flex items-center gap-1">
              <Button
                v-if="hasChildren(item)"
                variant="ghost"
                size="sm"
                class="h-6 w-6 p-0"
                @click="toggleExpand(item.id)"
                :aria-expanded="isExpanded(item.id)"
              >
                <SafeIcon
                  :name="isExpanded(item.id) ? 'ChevronDown' : 'ChevronRight'"
                  :size="16"
                />
              </Button>
              <div v-else class="w-6" />
              
              <Button
                variant="ghost"
                class="flex-1 justify-start h-8 px-2 text-sm"
                :class="cn(
                  selectedId === item.id && 'bg-primary/10 text-primary'
                )"
                @click="selectChapter(item.id)"
              >
                <span class="text-xs text-muted-foreground mr-2 min-w-fit">{{ item.index }}</span>
                <span class="truncate">{{ item.title }}</span>
              </Button>
            </div>

            <!-- Children (Nested) -->
            <div
              v-if="hasChildren(item) && (isExpanded(item.id) || isClient)"
              :class="cn(
                'ml-4 space-y-1 transition-all duration-200',
                !isExpanded(item.id) && !isClient && 'hidden'
              )"
            >
              <template v-for="child in item.children" :key="child.id">
                <div class="flex items-center gap-1">
                  <Button
                    v-if="hasChildren(child)"
                    variant="ghost"
                    size="sm"
                    class="h-6 w-6 p-0"
                    @click="toggleExpand(child.id)"
                    :aria-expanded="isExpanded(child.id)"
                  >
                    <SafeIcon
                      :name="isExpanded(child.id) ? 'ChevronDown' : 'ChevronRight'"
                      :size="16"
                    />
                  </Button>
                  <div v-else class="w-6" />
                  
                  <Button
                    variant="ghost"
                    class="flex-1 justify-start h-8 px-2 text-sm"
                    :class="cn(
                      selectedId === child.id && 'bg-primary/10 text-primary'
                    )"
                    @click="selectChapter(child.id)"
                  >
                    <span class="text-xs text-muted-foreground mr-2 min-w-fit">{{ child.index }}</span>
                    <span class="truncate">{{ child.title }}</span>
                  </Button>
                </div>
              </template>
            </div>
          </div>
        </template>
      </div>
    </CardContent>
  </Card>
</template>

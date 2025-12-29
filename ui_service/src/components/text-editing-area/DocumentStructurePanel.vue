
<script setup lang="ts">
import { ref } from 'vue'
import { cn } from '@/lib/utils'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Section {
  id: string
  type: string
  level?: number
  content: string
  children?: Section[]
}

interface Props {
  sections: Section[]
  selectedBlockId: string | null
}

const emit = defineEmits<{
  select: [blockId: string]
}>()

const expandedSections = ref<Set<string>>(new Set())

const toggleExpand = (sectionId: string) => {
  if (expandedSections.value.has(sectionId)) {
    expandedSections.value.delete(sectionId)
  } else {
    expandedSections.value.add(sectionId)
  }
}

const getIndentClass = (level: number = 1) => {
  const indents: Record<number, string> = {
    1: 'pl-0',
    2: 'pl-4',
    3: 'pl-8',
  }
  return indents[level] || 'pl-0'
}

const getHeadingIcon = (level: number = 1) => {
  const icons: Record<number, string> = {
    1: 'Heading1',
    2: 'Heading2',
    3: 'Heading3',
  }
  return icons[level] || 'Heading1'
}
</script>

<template>
  <div class="p-4 space-y-2">
    <h3 class="text-sm font-semibold text-foreground mb-4">文档结构</h3>

    <div class="space-y-1">
      <template v-for="section in sections" :key="section.id">
        <!-- Section Item -->
        <div class="space-y-1">
          <!-- Heading -->
          <div
            :class="cn(
              'flex items-center gap-2 px-3 py-2 rounded-md cursor-pointer transition-colors',
              'hover:bg-muted',
              selectedBlockId === section.id && 'bg-primary/10 text-primary'
            )"
            @click="emit('select', section.id)"
          >
            <!-- Expand Toggle -->
            <button
              v-if="section.children && section.children.length > 0"
              @click.stop="toggleExpand(section.id)"
              class="p-0 hover:bg-muted/50 rounded"
            >
              <SafeIcon
                :name="expandedSections.has(section.id) ? 'ChevronDown' : 'ChevronRight'"
                :size="16"
              />
            </button>
            <div v-else class="w-4" />

            <!-- Icon -->
            <SafeIcon
              :name="getHeadingIcon(section.level)"
              :size="16"
              class="flex-shrink-0"
            />

            <!-- Label -->
            <span class="text-sm font-medium truncate flex-1">
              {{ section.content.substring(0, 30) }}{{ section.content.length > 30 ? '...' : '' }}
            </span>
          </div>

          <!-- Children -->
          <div
            v-if="section.children && expandedSections.has(section.id)"
            :class="getIndentClass(2)"
            class="space-y-1"
          >
            <template v-for="child in section.children" :key="child.id">
              <div
                v-if="child.type === 'paragraph' || child.type === 'heading'"
                :class="cn(
                  'flex items-center gap-2 px-3 py-2 rounded-md cursor-pointer transition-colors',
                  'hover:bg-muted',
                  selectedBlockId === child.id && 'bg-primary/10 text-primary'
                )"
                @click="emit('select', child.id)"
              >
                <SafeIcon
                  :name="child.type === 'heading' ? 'Heading3' : 'Type'"
                  :size="14"
                  class="flex-shrink-0"
                />
                <span class="text-xs truncate flex-1">
                  {{ child.content.substring(0, 25) }}{{ child.content.length > 25 ? '...' : '' }}
                </span>
              </div>

              <!-- Placeholder -->
              <div
                v-else-if="child.type === 'image_placeholder'"
                :class="cn(
                  'flex items-center gap-2 px-3 py-2 rounded-md cursor-pointer transition-colors',
                  'hover:bg-muted',
                  selectedBlockId === child.id && 'bg-primary/10 text-primary'
                )"
                @click="emit('select', child.id)"
              >
                <SafeIcon name="Image" :size="14" class="flex-shrink-0" />
                <span class="text-xs truncate flex-1">{{ child.label }}</span>
              </div>
            </template>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

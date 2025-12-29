
<script setup lang="ts">
import type { DocumentTOCModel } from '@/data/generation'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  toc: DocumentTOCModel[]
}

defineProps<Props>()

const getIndentLevel = (index: string): number => {
  return (index.match(/\./g) || []).length
}

const handleNavigate = (tocId: string) => {
  if (typeof window !== 'undefined') {
    // Navigate to content view with TOC ID
    window.location.href = `./bid-document-content-view.html?tocId=${tocId}`
  }
}
</script>

<template>
  <div class="space-y-2">
    <template v-for="item in toc" :key="item.id">
      <!-- Chapter Item -->
      <div
        :style="{ paddingLeft: `${getIndentLevel(item.index) * 1.5}rem` }"
        class="group"
      >
        <button
          @click="handleNavigate(item.id)"
          class="w-full text-left px-3 py-2 rounded-lg hover:bg-muted transition-colors flex items-center gap-2"
        >
          <SafeIcon name="ChevronRight" :size="16" class="text-muted-foreground group-hover:text-foreground transition-colors" />
          <span class="text-sm font-medium text-muted-foreground group-hover:text-foreground transition-colors">
            {{ item.index }}
          </span>
          <span class="text-sm group-hover:text-primary transition-colors">
            {{ item.title }}
          </span>
        </button>

        <!-- Nested Children -->
        <template v-if="item.children && item.children.length > 0">
          <div v-for="child in item.children" :key="child.id">
            <button
              @click="handleNavigate(child.id)"
              :style="{ paddingLeft: `${(getIndentLevel(child.index) * 1.5)}rem` }"
              class="w-full text-left px-3 py-2 rounded-lg hover:bg-muted transition-colors flex items-center gap-2 group"
            >
              <SafeIcon name="ChevronRight" :size="16" class="text-muted-foreground group-hover:text-foreground transition-colors" />
              <span class="text-sm text-muted-foreground group-hover:text-foreground transition-colors">
                {{ child.index }}
              </span>
              <span class="text-sm text-muted-foreground group-hover:text-foreground transition-colors">
                {{ child.title }}
              </span>
            </button>
          </div>
        </template>
      </div>
    </template>
  </div>
</template>

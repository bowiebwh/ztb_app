
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  Sidebar,
  SidebarContent,
  SidebarProvider,
  SidebarInset,
} from '@/components/ui/sidebar'

interface Props {
  headerHeight?: string
}

const props = withDefaults(defineProps<Props>(), {
  headerHeight: '64px',
})

const isClient = ref(true)

onMounted(() => {
  isClient.value = false
  requestAnimationFrame(() => {
    isClient.value = true
  })
})
</script>

<template>
  <SidebarProvider>
    <Sidebar
      class="top-[--header-height] h-[calc(100vh-var(--header-height))]"
      :style="{ '--header-height': props.headerHeight }"
    >
      <SidebarContent>
        <slot name="sidebar" />
      </SidebarContent>
    </Sidebar>
    <SidebarInset class="flex flex-col min-h-[calc(100vh-var(--header-height))]" :style="{ '--header-height': props.headerHeight }">
      <slot />
    </SidebarInset>
  </SidebarProvider>
</template>

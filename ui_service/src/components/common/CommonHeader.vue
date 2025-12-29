
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import {
  Breadcrumb,
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface BreadcrumbItem {
  label: string
  href?: string
}

interface Props {
  breadcrumbs?: BreadcrumbItem[]
  showThemeToggle?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  breadcrumbs: () => [],
  showThemeToggle: true,
})

const isDark = ref(false)

onMounted(() => {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('theme')
    if (saved === 'dark' || saved === 'light') {
      isDark.value = saved === 'dark'
      document.documentElement.classList.toggle('dark', isDark.value)
    } else {
      isDark.value = document.documentElement.classList.contains('dark')
    }
  }
})

const toggleTheme = () => {
  if (typeof window !== 'undefined') {
    isDark.value = !isDark.value
    document.documentElement.classList.toggle('dark', isDark.value)
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  }
}
</script>

<template>
  <header class="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
    <div class="container flex h-16 items-center justify-between px-4">
      <!-- Logo & Brand -->
      <div class="flex items-center gap-6">
        <a href="./project-list.html" class="flex items-center gap-2 font-semibold text-lg hover:opacity-80 transition-opacity">
          <div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
            <SafeIcon name="FileText" :size="20" color="white" />
          </div>
          <span>智标助手</span>
        </a>

        <!-- Breadcrumbs -->
        <Breadcrumb v-if="breadcrumbs.length > 0" class="hidden md:flex">
          <BreadcrumbList>
            <template v-for="(item, index) in breadcrumbs" :key="index">
              <BreadcrumbSeparator v-if="index > 0" />
              <BreadcrumbItem>
                <BreadcrumbLink v-if="item.href && index < breadcrumbs.length - 1" :href="item.href">
                  {{ item.label }}
                </BreadcrumbLink>
                <BreadcrumbPage v-else>
                  {{ item.label }}
                </BreadcrumbPage>
              </BreadcrumbItem>
            </template>
          </BreadcrumbList>
        </Breadcrumb>
      </div>

      <!-- Actions -->
      <div class="flex items-center gap-2">
        <Button
          v-if="showThemeToggle"
          variant="ghost"
          size="icon"
          @click="toggleTheme"
          aria-label="切换主题"
        >
          <SafeIcon v-if="isDark" name="Sun" :size="20" />
          <SafeIcon v-else name="Moon" :size="20" />
        </Button>
      </div>
    </div>
  </header>
</template>

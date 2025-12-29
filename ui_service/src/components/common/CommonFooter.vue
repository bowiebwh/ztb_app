
<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'simple' | 'full'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'simple',
})

const currentYear = computed(() => {
  if (typeof window !== 'undefined') {
    return new Date().getFullYear()
  }
  return 2024
})

const footerLinks = [
  { name: '关于我们', href: '#about' },
  { name: '隐私政策', href: '#privacy' },
  { name: '服务条款', href: '#terms' },
  { name: '联系我们', href: '#contact' },
]
</script>

<template>
  <footer class="border-t bg-background mt-auto">
    <div class="container mx-auto px-4 py-6">
      <!-- Simple Footer -->
      <div v-if="variant === 'simple'" class="flex flex-col md:flex-row justify-between items-center gap-4">
        <p class="text-sm text-muted-foreground">
          © {{ currentYear }} 智标助手. 保留所有权利.
        </p>
      </div>

      <!-- Full Footer -->
      <div v-else class="space-y-6">
        <div class="flex flex-col md:flex-row justify-between items-start gap-6">
          <!-- Brand -->
          <div class="space-y-2">
            <div class="flex items-center gap-2 font-semibold">
              <div class="w-6 h-6 rounded bg-primary flex items-center justify-center">
                <span class="text-xs text-primary-foreground">智</span>
              </div>
              <span>智标助手</span>
            </div>
            <p class="text-sm text-muted-foreground max-w-xs">
              企业级招投标文档智能生成与编辑系统
            </p>
          </div>

          <!-- Links -->
          <div class="flex flex-wrap gap-x-6 gap-y-2">
            <a
              v-for="link in footerLinks"
              :key="link.name"
              :href="link.href"
              class="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              {{ link.name }}
            </a>
          </div>
        </div>

        <!-- Copyright -->
        <div class="pt-6 border-t">
          <p class="text-sm text-muted-foreground text-center">
            © {{ currentYear }} 智标助手. 保留所有权利.
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>

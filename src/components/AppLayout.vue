<template>
  <div class="app-layout h-full flex flex-col">
    <!-- 顶部菜单 -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center">
          <router-link to="/" class="text-lg font-bold text-gray-800 mr-8 hover:text-primary-500 transition-colors">
            Sweegi Tools
          </router-link>
          <el-menu
            :default-active="activeIndex"
            mode="horizontal"
            background-color="#ffffff"
            text-color="#6b7280"
            active-text-color="#d3139c"
            class="border-none flex-1"
            @select="handleSelect"
            :ellipsis="false"
          >
            <el-menu-item index="markdown-viewer" class="menu-item-custom">
              <el-icon class="mr-1"><Document /></el-icon>
              Markdown查看器
            </el-menu-item>
            <el-menu-item index="html-to-pdf" class="menu-item-custom">
              <el-icon class="mr-1"><Printer /></el-icon>
              HTML转PDF
            </el-menu-item>
          </el-menu>
        </div>
      </div>
    </header>
    
    <!-- 主内容区 -->
    <div class="flex-grow overflow-auto">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Document, Printer } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

// 根据当前路由设置活跃菜单项
const activeIndex = computed(() => {
  const path = route.path
  if (path === '/markdown-viewer') return 'markdown-viewer'
  if (path === '/html-to-pdf') return 'html-to-pdf'
  return ''
})

const handleSelect = (key) => {
  router.push(`/${key}`)
}
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
}

.flex-grow {
  flex-grow: 1;
}

:deep(.el-menu--horizontal) {
  border-bottom: none !important;
  display: flex !important;
  flex-wrap: nowrap !important;
}

:deep(.el-menu-item) {
  border-bottom: 2px solid transparent !important;
  flex-shrink: 0 !important;
  white-space: nowrap !important;
}

:deep(.menu-item-custom) {
  display: flex !important;
  align-items: center !important;
  min-width: auto !important;
  padding: 0 20px !important;
}

:deep(.el-menu-item.is-active) {
  border-bottom-color: var(--color-primary) !important;
}

:deep(.el-menu-item:hover) {
  background-color: #f9fafb !important;
  color: var(--color-primary) !important;
}

/* 确保菜单不会被省略号替换 */
:deep(.el-menu--horizontal .el-menu-item) {
  overflow: visible !important;
}

/* 防止菜单项被隐藏 */
:deep(.el-menu-overflow) {
  display: none !important;
}
</style> 
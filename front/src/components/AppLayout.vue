<template>
  <div class="app-layout h-full flex flex-col">
    <!-- 顶部菜单 -->
    <header class="bg-gray-900 shadow-lg border-b border-gray-700 h-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full">
        <div class="flex items-center justify-between h-full">
          <!-- Logo -->
          <router-link to="/" class="text-xl md:text-2xl no-underline font-bold text-white hover:text-pink-400 transition-colors">
            Sweegi Tools
          </router-link>

          <!-- 桌面端菜单 -->
          <el-menu
            :default-active="activeIndex"
            mode="horizontal"
            background-color="#111827"
            text-color="#d1d5db"
            active-text-color="#ec4899"
            class="border-none flex-1 ml-8 hidden md:flex"
            @select="handleSelect"
            :ellipsis="false"
          >
            <el-menu-item index="markdown" class="menu-item-custom">
              <el-icon class="mr-2"><Document /></el-icon>
              Markdown查看器
            </el-menu-item>
            <el-menu-item index="html-to-pdf" class="menu-item-custom">
              <el-icon class="mr-2"><Printer /></el-icon>
              HTML转PDF
            </el-menu-item>
          </el-menu>

          <!-- 移动端汉堡菜单按钮 -->
          <button
            @click="toggleMobileMenu"
            class="md:hidden p-2 rounded-md text-gray-300 hover:text-white hover:bg-gray-800 transition-colors"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- 移动端下拉菜单 -->
      <div
        v-show="mobileMenuOpen"
        class="md:hidden bg-gray-800 border-t border-gray-700 shadow-lg"
        :class="{ 'animate-slide-down': mobileMenuOpen }"
      >
        <div class="px-4 py-2 space-y-1">
          <a
            @click="handleMobileMenuSelect('markdown')"
            :class="[
              'flex items-center px-3 py-3 rounded-md text-base font-medium transition-colors cursor-pointer',
              activeIndex === 'markdown'
                ? 'bg-gray-700 text-pink-400'
                : 'text-gray-300 hover:bg-gray-700 hover:text-white'
            ]"
          >
            <el-icon class="mr-3 h-5 w-5"><Document /></el-icon>
            Markdown查看器
          </a>
          <a
            @click="handleMobileMenuSelect('html-to-pdf')"
            :class="[
              'flex items-center px-3 py-3 rounded-md text-base font-medium transition-colors cursor-pointer',
              activeIndex === 'html-to-pdf'
                ? 'bg-gray-700 text-pink-400'
                : 'text-gray-300 hover:bg-gray-700 hover:text-white'
            ]"
          >
            <el-icon class="mr-3 h-5 w-5"><Printer /></el-icon>
            HTML转PDF
          </a>
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

// 移动端菜单状态
const mobileMenuOpen = ref(false)

// 根据当前路由设置活跃菜单项
const activeIndex = computed(() => {
  const path = route.path
  if (path.startsWith('/markdown')) return 'markdown'
  if (path.startsWith('/html-to-pdf')) return 'html-to-pdf'
  return ''
})

const handleSelect = (key) => {
  router.push(`/${key}`)
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const handleMobileMenuSelect = (key) => {
  router.push(`/${key}`)
  mobileMenuOpen.value = false
}
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
}

.flex-grow {
  flex-grow: 1;
}

/* 强制深色主题样式 */
:deep(.el-menu--horizontal) {
  border-bottom: none !important;
  display: flex !important;
  flex-wrap: nowrap !important;
  background-color: #111827 !important;
}

:deep(.el-menu-item) {
  border-bottom: 2px solid transparent !important;
  flex-shrink: 0 !important;
  white-space: nowrap !important;
  background-color: #111827 !important;
  color: #d1d5db !important;
  height: 60px !important;
  line-height: 60px !important;
}

:deep(.menu-item-custom) {
  display: flex !important;
  align-items: center !important;
  min-width: auto !important;
  padding: 0 24px !important;
  font-size: 16px !important;
  font-weight: 500 !important;
  background-color: #111827 !important;
  color: #d1d5db !important;
}

:deep(.el-menu-item.is-active) {
  border-bottom-color: #ec4899 !important;
  color: #ec4899 !important;
  background-color: #1f2937 !important;
}

:deep(.el-menu-item:hover) {
  background-color: #1f2937 !important;
  color: #ec4899 !important;
}

/* 移动端下拉动画 */
@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-down {
  animation: slide-down 0.2s ease-out;
}

/* 确保菜单不会被省略号替换 */
:deep(.el-menu--horizontal .el-menu-item) {
  overflow: visible !important;
}

/* 防止菜单项被隐藏 */
:deep(.el-menu-overflow) {
  display: none !important;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .app-layout {
    font-size: 14px;
  }

  /* 强制移动端样式 */
  header {
    background-color: #111827 !important;
    border-bottom: 1px solid #374151 !important;
  }

  /* 汉堡菜单按钮样式 */
  button {
    background-color: transparent !important;
    color: #d1d5db !important;
  }

  button:hover {
    background-color: #1f2937 !important;
    color: #ffffff !important;
  }
}

/* 全局强制深色主题 */
.bg-gray-900 {
  background-color: #111827 !important;
}

.bg-gray-800 {
  background-color: #1f2937 !important;
}

.border-gray-700 {
  border-color: #374151 !important;
}

.text-white {
  color: #ffffff !important;
}

.text-gray-300 {
  color: #d1d5db !important;
}

.hover\:text-pink-400:hover {
  color: #f472b6 !important;
}

.hover\:bg-gray-700:hover {
  background-color: #374151 !important;
}

.hover\:text-white:hover {
  color: #ffffff !important;
}

.text-pink-400 {
  color: #f472b6 !important;
}

.bg-gray-700 {
  background-color: #374151 !important;
}
</style> 
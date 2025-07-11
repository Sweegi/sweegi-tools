<template>
  <div class="home-container">
    <!-- 主要内容 -->
    <main class="flex items-center justify-center min-h-screen bg-gradient-to-br from-primary-50 to-primary-100">
      <div class="text-center">
        <h1 class="text-6xl font-bold text-gray-800 mb-6 animate-bounce">
          Boom！Sweegi Tools！
        </h1>
        <p class="text-xl text-gray-600 mb-8">
          欢迎使用 Sweegi 工具集合
        </p>
        <div class="flex justify-center space-x-4">
          <el-button 
            type="primary" 
            size="large" 
            @click="goToMarkdownViewer"
            icon="Document"
          >
            开始使用 Markdown查看器
          </el-button>
          <el-button 
            type="success" 
            size="large" 
            @click="goToHtmlToPdf"
            icon="Printer"
          >
            开始使用 HTML转PDF
          </el-button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { Document, Printer } from '@element-plus/icons-vue'

const router = useRouter()

const goToMarkdownViewer = () => {
  router.push('/markdown-viewer')
}

const goToHtmlToPdf = () => {
  router.push('/html-to-pdf')
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
}
</style> 
<template>
  <div class="markdown-viewer-container">
    <!-- 主要内容 -->
    <div class="flex items-center justify-center min-h-screen bg-gray-100 p-4">
      <div class="text-center p-8 bg-white rounded-lg shadow-md max-w-2xl w-full">
        <div class="mb-6">
          <el-icon size="48" color="#d3139c"><Document /></el-icon>
        </div>
        <h1 class="text-3xl font-bold text-gray-800 mb-6">Markdown 查看器</h1>
        <p class="text-gray-600 mb-8">
          一个简单而强大的本地 Markdown 文件查看工具
        </p>
        
        <el-button 
          type="primary" 
          size="large" 
          @click="openFile"
          class="mb-4"
          icon="FolderOpened"
        >
          选择 Markdown 文件
        </el-button>
        
        <div v-if="recentFiles.length > 0" class="mt-8">
          <h2 class="text-xl font-semibold text-gray-700 mb-4">最近打开的文件</h2>
          <el-card shadow="hover" class="text-left">
            <div 
              v-for="(file, index) in recentFiles" 
              :key="index"
              class="p-3 border-b border-gray-200 last:border-b-0 hover:bg-gray-50 cursor-pointer flex items-center transition-colors"
              @click="openRecentFile(file)"
            >
              <el-icon class="mr-3 text-primary-500"><Document /></el-icon>
              <div class="flex-1">
                <div class="font-medium text-gray-900 truncate">{{ file.name }}</div>
                <div class="text-sm text-gray-500">
                  {{ new Date(file.lastModified).toLocaleString() }}
                </div>
              </div>
              <el-icon class="text-gray-400"><ArrowRight /></el-icon>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Document, FolderOpened, ArrowRight } from '@element-plus/icons-vue'
import { fileOpen } from 'browser-fs-access'

const router = useRouter()
const recentFiles = ref([])

onMounted(() => {
  // 从本地存储中获取最近文件列表
  const savedFiles = localStorage.getItem('recentFiles')
  if (savedFiles) {
    recentFiles.value = JSON.parse(savedFiles)
  }
})

const openFile = async () => {
  try {
    const file = await fileOpen({
      extensions: ['.md', '.markdown'],
      description: 'Markdown文件'
    })
    
    // 将文件添加到最近文件列表
    const fileInfo = { 
      name: file.name, 
      size: file.size,
      lastModified: file.lastModified,
      // 将文件内容转换为URL以便在Viewer中使用
      content: await file.text()
    }
    
    addToRecentFiles(fileInfo)
    
    // 导航到查看器页面
    localStorage.setItem('currentFile', JSON.stringify(fileInfo))
    router.push('/viewer')
  } catch (error) {
    console.error('打开文件失败', error)
  }
}

const addToRecentFiles = (fileInfo) => {
  // 移除旧的相同文件（如果存在）
  recentFiles.value = recentFiles.value.filter(f => f.name !== fileInfo.name)
  
  // 添加到列表开头
  recentFiles.value.unshift({
    name: fileInfo.name,
    lastModified: fileInfo.lastModified
  })
  
  // 保持列表不超过10个项目
  if (recentFiles.value.length > 10) {
    recentFiles.value = recentFiles.value.slice(0, 10)
  }
  
  // 保存到本地存储
  localStorage.setItem('recentFiles', JSON.stringify(recentFiles.value))
}

const openRecentFile = (fileInfo) => {
  // 这里我们只有文件名和修改日期，需要用户重新选择文件
  openFile()
}
</script>

<style scoped>
/* 移除之前的菜单样式 */
</style> 
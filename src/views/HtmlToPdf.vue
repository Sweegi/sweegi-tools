<template>
  <div class="html-to-pdf-container">
    <!-- 主要内容 -->
    <div class="flex items-center justify-center min-h-screen bg-gray-100 p-4">
      <div class="text-center p-8 bg-white rounded-lg shadow-md max-w-2xl w-full">
        <div class="mb-6">
          <el-icon size="48" color="#d3139c"><Printer /></el-icon>
        </div>
        <h1 class="text-3xl font-bold text-gray-800 mb-6">HTML 转 PDF</h1>
        <p class="text-gray-600 mb-8">
          将 HTML 文件或网页转换为 PDF 文档
        </p>
        
        <div class="space-y-6">
          <el-button 
            type="primary" 
            size="large" 
            @click="selectHtmlFile"
            class="w-full"
            icon="FolderOpened"
          >
            选择 HTML 文件
          </el-button>
          
          <el-divider>
            <span class="text-gray-500">或</span>
          </el-divider>
          
          <el-card shadow="hover" class="text-left">
            <template #header>
              <div class="flex items-center">
                <el-icon class="mr-2 text-primary-500"><Link /></el-icon>
                <span>从URL转换</span>
              </div>
            </template>
            <el-input
              v-model="urlInput"
              placeholder="输入网页URL (例如: https://example.com)"
              size="large"
              class="mb-4"
            >
              <template #prepend>
                <el-icon><Link /></el-icon>
              </template>
              <template #append>
                <el-button 
                  @click="convertFromUrl" 
                  :disabled="!urlInput.trim()"
                  type="primary"
                >
                  转换
                </el-button>
              </template>
            </el-input>
          </el-card>
        </div>
        
        <div v-if="isConverting" class="mt-8">
          <el-card shadow="always">
            <div class="text-center">
              <el-icon size="24" class="animate-spin mb-2 text-primary-500"><Loading /></el-icon>
              <div class="mb-4">
                <el-progress 
                  :percentage="progress" 
                  :show-text="true"
                  :stroke-width="8"
                  status="success"
                />
              </div>
              <p class="text-gray-600">正在转换中，请稍候...</p>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { fileOpen } from 'browser-fs-access'
import { ElMessage } from 'element-plus'
import { Printer, FolderOpened, Link, Loading } from '@element-plus/icons-vue'

const urlInput = ref('')
const isConverting = ref(false)
const progress = ref(0)

const selectHtmlFile = async () => {
  try {
    const file = await fileOpen({
      extensions: ['.html', '.htm'],
      description: 'HTML文件'
    })
    
    ElMessage.success(`已选择文件: ${file.name}`)
    // TODO: 实现HTML文件转PDF功能
    await convertFile(file)
  } catch (error) {
    if (error.name !== 'AbortError') {
      console.error('选择文件失败', error)
      ElMessage.error('选择文件失败')
    }
  }
}

const convertFromUrl = async () => {
  if (!urlInput.value.trim()) {
    ElMessage.warning('请输入有效的URL')
    return
  }
  
  // TODO: 实现URL转PDF功能
  ElMessage.info('URL转PDF功能开发中...')
}

const convertFile = async (file) => {
  isConverting.value = true
  progress.value = 0
  
  try {
    // 模拟转换进度
    const progressInterval = setInterval(() => {
      progress.value += 10
      if (progress.value >= 100) {
        clearInterval(progressInterval)
        isConverting.value = false
        ElMessage.success('转换完成！')
      }
    }, 200)
    
    // TODO: 实际的PDF转换逻辑
    
  } catch (error) {
    isConverting.value = false
    progress.value = 0
    console.error('转换失败', error)
    ElMessage.error('转换失败')
  }
}
</script>

<style scoped>
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style> 
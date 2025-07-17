<template>
  <div class="viewer-container h-full flex flex-col">
    <header class="bg-white border-b border-gray-200 p-4 flex items-center justify-between shadow-sm">
      <div class="flex items-center">
        <el-button @click="goBack" circle>
          <el-icon><ArrowLeft /></el-icon>
        </el-button>
        <h1 class="ml-4 text-xl font-medium">{{ currentFile?.name || '未命名文档' }}</h1>
      </div>
      <div>
        <el-button @click="openFile" type="primary">打开其他文件</el-button>
      </div>
    </header>

    <main class="flex-grow overflow-auto p-4 bg-gray-50">
      <div v-if="renderedContent" class="markdown-body bg-white p-8 max-w-4xl mx-auto rounded-lg shadow">
        <div v-html="renderedContent"></div>
      </div>
      <div v-else class="text-center p-8">
        <el-empty description="无内容或文件未能加载" />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { fileOpen } from 'browser-fs-access'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import { ArrowLeft } from '@element-plus/icons-vue'
import './markdown.css'

const router = useRouter()
const currentFile = ref(null)
const markdownContent = ref('')

// 配置markdown-it
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value
      } catch (__) {}
    }
    return '' // 使用外部默认转义
  }
})

const renderedContent = computed(() => {
  if (!markdownContent.value) return ''
  return md.render(markdownContent.value)
})

onMounted(() => {
  loadCurrentFile()
})

const loadCurrentFile = () => {
  const fileData = localStorage.getItem('currentFile')
  if (fileData) {
    try {
      currentFile.value = JSON.parse(fileData)
      markdownContent.value = currentFile.value.content
    } catch (error) {
      console.error('无法解析文件数据', error)
    }
  }
}

const openFile = async () => {
  try {
    const file = await fileOpen({
      extensions: ['.md', '.markdown'],
      description: 'Markdown文件'
    })
    
    const fileInfo = { 
      name: file.name, 
      size: file.size,
      lastModified: file.lastModified,
      content: await file.text()
    }
    
    // 更新当前文件
    currentFile.value = fileInfo
    markdownContent.value = fileInfo.content
    
    // 添加到最近文件
    const recentFiles = JSON.parse(localStorage.getItem('recentFiles') || '[]')
    const existingIndex = recentFiles.findIndex(f => f.name === fileInfo.name)
    if (existingIndex > -1) {
      recentFiles.splice(existingIndex, 1)
    }
    recentFiles.unshift({
      name: fileInfo.name,
      lastModified: fileInfo.lastModified
    })
    if (recentFiles.length > 10) {
      recentFiles.length = 10
    }
    
    localStorage.setItem('recentFiles', JSON.stringify(recentFiles))
    localStorage.setItem('currentFile', JSON.stringify(fileInfo))
  } catch (error) {
    console.error('打开文件失败', error)
  }
}

const goBack = () => {
  router.push('/')
}
</script> 
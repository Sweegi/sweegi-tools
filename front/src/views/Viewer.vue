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
import { ref, onMounted, computed, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { fileOpen } from 'browser-fs-access'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import { ArrowLeft } from '@element-plus/icons-vue'
import mermaid from 'mermaid'
import '../css/markdown.css'

const router = useRouter()
const currentFile = ref(null)
const markdownContent = ref('')

// 初始化 Mermaid
console.log('开始初始化Mermaid...')
console.log('Mermaid对象:', mermaid)
console.log('Mermaid方法:', Object.keys(mermaid))

mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
  fontFamily: 'Arial, sans-serif',
  logLevel: 'debug'
})

console.log('Mermaid初始化完成')
console.log('render方法类型:', typeof mermaid.render)

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

// 添加mermaid渲染规则
const originalFenceRule = md.renderer.rules.fence || function(tokens, idx, options, env, renderer) {
  return renderer.renderToken(tokens, idx, options)
}

md.renderer.rules.fence = (tokens, idx, options, env, renderer) => {
  const token = tokens[idx]
  const info = token.info ? md.utils.unescapeAll(token.info).trim() : ''

  if (info === 'mermaid') {
    const mermaidId = `mermaid-${Math.random().toString(36).substr(2, 9)}`
    // 使用pre标签包装，这是mermaid推荐的方式
    return `<pre class="mermaid" id="${mermaidId}">${token.content}</pre>`
  }

  // 对于代码块，使用语法高亮
  if (info && hljs.getLanguage(info)) {
    try {
      const highlighted = hljs.highlight(token.content, { language: info }).value
      return `<pre><code class="hljs language-${info}">${highlighted}</code></pre>`
    } catch (__) {}
  }

  // 使用默认的代码块渲染
  return originalFenceRule(tokens, idx, options, env, renderer)
}

const renderedContent = computed(() => {
  if (!markdownContent.value) return ''
  return md.render(markdownContent.value)
})

// 监听内容变化，渲染mermaid图表
watch(renderedContent, () => {
  nextTick(() => {
    setTimeout(() => {
      renderMermaidCharts()
    }, 100) // 延迟100ms确保DOM完全更新
  })
}, { flush: 'post' })

// 渲染mermaid图表
const renderMermaidCharts = async () => {
  const mermaidElements = document.querySelectorAll('.mermaid:not([data-processed="true"])')
  console.log('找到的未处理Mermaid元素数量:', mermaidElements.length)

  if (mermaidElements.length === 0) {
    console.log('没有找到需要处理的Mermaid元素')
    return
  }

  try {
    console.log('尝试使用mermaid.run()方法')

    // 标记元素，避免重复处理
    mermaidElements.forEach(el => el.setAttribute('data-processing', 'true'))

    // 使用mermaid.run()自动检测和渲染
    await mermaid.run()

    // 标记为已处理
    mermaidElements.forEach(el => {
      el.setAttribute('data-processed', 'true')
      el.removeAttribute('data-processing')
      console.log('图表渲染完成:', el.id)
    })
  } catch (runError) {
    console.error('mermaid.run()失败，尝试手动渲染:', runError)

    // 回退到手动渲染
    for (const element of mermaidElements) {
      try {
        const graphDefinition = element.textContent.trim()
        console.log('手动渲染图表:', element.id)

        if (!element.id) {
          element.id = `mermaid-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`
        }

        const renderResult = await mermaid.render(element.id + '_svg', graphDefinition)

        if (renderResult && renderResult.svg) {
          element.innerHTML = renderResult.svg
          console.log('手动渲染成功:', element.id)
        } else {
          throw new Error('渲染结果无效')
        }

        element.setAttribute('data-processed', 'true')
        element.removeAttribute('data-processing')
      } catch (error) {
        console.error('手动渲染失败:', element.id, error)
        element.innerHTML = `<div class="mermaid-error">
          <strong>Mermaid渲染错误:</strong><br>
          ${error.message}<br><br>
          <strong>图表内容:</strong><br>
          <pre>${element.textContent.trim()}</pre>
        </div>`
        element.setAttribute('data-processed', 'true')
        element.removeAttribute('data-processing')
      }
    }
  }
}

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
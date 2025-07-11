<template>
  <div class="html-to-pdf-container">
    <!-- 主要内容 -->
    <div class="flex items-center justify-center min-h-screen bg-gray-100 p-4">
      <div class="text-center p-8 bg-white rounded-lg shadow-md max-w-4xl w-full">
        <div class="mb-6">
          <el-icon size="48" color="#d3139c"><Printer /></el-icon>
        </div>
        <h1 class="text-3xl font-bold text-gray-800 mb-6">HTML 转 PDF</h1>
        <p class="text-gray-600 mb-8">
          将 HTML 文件或网页转换为 PDF 文档
        </p>

        <div class="flex justify-center mb-8">
          <!-- 选择HTML文件 -->
          <el-card shadow="hover" class="w-full max-w-md">
            <template #header>
              <div class="flex items-center">
                <el-icon class="mr-2 text-primary-500"><FolderOpened /></el-icon>
                <span>本地HTML文件</span>
              </div>
            </template>
            <div class="space-y-4">
              <el-button 
                type="primary" 
                size="large" 
                @click="selectHtmlFile"
                class="w-full"
                icon="FolderOpened"
                :loading="isConverting">
                选择 HTML 文件
              </el-button>
              <div v-if="selectedFile" class="text-sm text-gray-600">
                已选择: {{ selectedFile.name }}
              </div>
            </div>
          </el-card>
        </div>

        <!-- PDF配置选项 -->
        <el-card shadow="never" class="mb-6" v-if="selectedFile">
          <template #header>
            <div class="flex items-center">
              <el-icon class="mr-2 text-primary-500"><Setting /></el-icon>
              <span>PDF设置</span>
            </div>
          </template>
          <div class="grid md:grid-cols-4 gap-4 text-left">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">页面格式</label>
              <el-select v-model="pdfOptions.format" class="w-full">
                <el-option label="A4" value="a4" />
                <el-option label="A3" value="a3" />
                <el-option label="Letter" value="letter" />
                <el-option label="Legal" value="legal" />
              </el-select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">页面方向</label>
              <el-select v-model="pdfOptions.orientation" class="w-full">
                <el-option label="竖向" value="portrait" />
                <el-option label="横向" value="landscape" />
              </el-select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">图片质量</label>
              <el-select v-model="pdfOptions.imageQuality" class="w-full">
                <el-option label="高质量" :value="1.0" />
                <el-option label="中等质量" :value="0.8" />
                <el-option label="低质量" :value="0.6" />
              </el-select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">缩放比例</label>
              <el-input-number v-model="pdfOptions.scale" :min="1" :max="3" :step="0.1" class="w-full" />
            </div>
          </div>
        </el-card>

        <!-- HTML预览区域 -->
        <div v-if="htmlContent" class="mb-6">
          <el-card shadow="never">
            <template #header>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <el-icon class="mr-2 text-primary-500"><View /></el-icon>
                  <span>HTML预览 (Canvas渲染效果)</span>
                  <el-tag size="small" class="ml-2">
                    长度: {{ htmlContent.length }} 字符
                  </el-tag>
                </div>
                <div class="flex space-x-2">
                  <el-button 
                    @click="previewAsCanvas"
                    :loading="isGeneratingPreview">
                    刷新Canvas预览
                  </el-button>
                  <el-button 
                    type="primary" 
                    @click="generatePdf"
                    :loading="isConverting">
                    生成PDF
                  </el-button>
                </div>
              </div>
            </template>

            <!-- Canvas预览区域 -->
            <div class="canvas-preview-container border rounded p-4 bg-white">
              <div v-if="isGeneratingPreview" class="text-center py-8">
                <el-icon size="24" class="animate-spin mb-2 text-primary-500"><Loading /></el-icon>
                <p class="text-gray-600">正在生成Canvas预览...</p>
              </div>

              <div v-else-if="previewCanvas" class="w-full">
                <div class="mb-4 text-sm text-gray-600 text-center">
                  Canvas尺寸: {{ previewCanvas.width }} × {{ previewCanvas.height }}px
                </div>
                <div class="w-full overflow-hidden rounded border border-gray-300 shadow-sm">
                  <img 
                    :src="previewCanvas.toDataURL()" 
                    alt="Canvas预览" 
                    class="w-full h-auto"/>
                </div>
              </div>

              <div v-else class="text-center py-8">
                <el-icon size="48" class="text-gray-400 mb-4"><View /></el-icon>
                <p class="text-gray-500 mb-4">点击"刷新Canvas预览"查看渲染效果</p>
              </div>
            </div>

            <!-- 原始HTML预览 (折叠区域) -->
            <el-collapse class="mt-4">
              <el-collapse-item title="查看原始HTML内容" name="html-source">
                <div 
                  ref="previewRef"
                  class="html-preview border rounded p-4 max-h-96 overflow-auto text-left bg-gray-50"
                  v-html="htmlContent"></div>
              </el-collapse-item>
            </el-collapse>
          </el-card>
        </div>

        <!-- 如果没有内容，显示提示 -->
        <div v-if="!htmlContent" class="mb-6">
          <el-card shadow="never">
            <div class="text-center py-8">
              <el-icon size="48" class="text-gray-400 mb-4"><Document /></el-icon>
              <p class="text-gray-500">还没有选择HTML文件</p>
              <p class="text-gray-400 text-sm mt-2">请点击上方的"选择 HTML 文件"按钮来添加内容</p>
            </div>
          </el-card>
        </div>

        <!-- 转换进度 -->
        <div v-if="isConverting" class="mt-8">
          <el-card shadow="always">
            <div class="text-center">
              <el-icon size="24" class="animate-spin mb-2 text-primary-500"><Loading /></el-icon>
              <div class="mb-4">
                <el-progress 
                  :percentage="progress" 
                  :show-text="true"
                  :stroke-width="8"
                  :color="progressColor"/>
              </div>
              <p class="text-gray-600">{{ progressText }}</p>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { fileOpen } from 'browser-fs-access'
import { ElMessage, ElNotification } from 'element-plus'
import { Printer, FolderOpened, Loading, Setting, View, Download, Document } from '@element-plus/icons-vue'
import html2canvas from 'html2canvas'
import { jsPDF } from 'jspdf'

const isConverting = ref(false)
const progress = ref(0)
const progressText = ref('')
const selectedFile = ref(null)
const htmlContent = ref('')
const previewRef = ref(null)
const previewCanvas = ref(null)
const isGeneratingPreview = ref(false)

const pdfOptions = ref({
  format: 'a4',
  orientation: 'portrait',
  filename: 'converted.pdf',
  imageQuality: 1.0,
  scale: 2
})

const pageSizes = {
  a4: { width: 210, height: 297 },
  a3: { width: 297, height: 420 },
  letter: { width: 216, height: 279 },
  legal: { width: 216, height: 356 }
}

const progressColor = computed(() => {
  if (progress.value < 30) return '#d3139c'
  if (progress.value < 70) return '#e6a23c'
  return '#67c23a'
})

const selectHtmlFile = async () => {
  try {
    const file = await fileOpen({
      extensions: ['.html', '.htm'],
      description: 'HTML文件'
    })

    selectedFile.value = file
    await loadHtmlFile(file)
    ElMessage.success(`已选择文件: ${file.name}`)
  } catch (error) {
    if (error.name !== 'AbortError') {
      console.error('选择文件失败', error)
      ElMessage.error('选择文件失败')
    }
  }
}

const loadHtmlFile = async (file) => {
  try {
    let content = await file.text()

    if (!content.includes('<!DOCTYPE') && !content.includes('<html')) {
      content = `
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>${file.name}</title>
        </head>
        <body>
          ${content}
        </body>
        </html>
      `
    }

    htmlContent.value = content
    pdfOptions.value.filename = file.name.replace(/\.(html|htm)$/i, '.pdf')

    console.log('HTML文件加载完成:', {
      filename: file.name,
      size: file.size,
      contentLength: content.length,
      hasDoctype: content.includes('<!DOCTYPE'),
      hasHtmlTag: content.includes('<html')
    })

  } catch (error) {
    console.error('读取HTML文件失败', error)
    ElMessage.error('读取HTML文件失败')
  }
}

const preprocessHtmlContent = (content) => {
  if (content.includes('<!DOCTYPE') || content.includes('<html')) {
    return content
  }

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: Arial, "Microsoft YaHei", sans-serif;
      font-size: 14px;
      line-height: 1.5;
      color: #333;
      background: #fff;
      margin: 0;
      padding: 20px;
    }
  </style>
</head>
<body>
  ${content}
</body>
</html>`
}

const generatePdf = async () => {
  if (!htmlContent.value) {
    ElMessage.warning('请先选择HTML文件或输入URL')
    return
  }

  isConverting.value = true
  progress.value = 0
  progressText.value = '正在预处理HTML内容...'

  try {
    const processedHtml = preprocessHtmlContent(htmlContent.value)
    console.log('预处理HTML完成，长度:', processedHtml.length)

    progress.value = 20
    progressText.value = '正在创建临时容器...'

    const tempContainer = document.createElement('div')

    const pageSize = pageSizes[pdfOptions.value.format]
    const isLandscape = pdfOptions.value.orientation === 'landscape'
    const pageWidth = isLandscape ? pageSize.height : pageSize.width
    const pageHeight = isLandscape ? pageSize.width : pageSize.height

    const containerWidth = pageWidth * 3.779527559
    const containerHeight = pageHeight * 3.779527559

    tempContainer.innerHTML = processedHtml

    tempContainer.style.cssText = `
      position: absolute;
      top: -9999px;
      left: 0;
      width: ${containerWidth}px;
      background: #ffffff;
      overflow: visible;
      border: none;
      margin: 0;
      padding: 0;
    `

    document.body.appendChild(tempContainer)

    console.log('临时容器创建完成:', {
      width: containerWidth,
      height: containerHeight,
      scrollWidth: tempContainer.scrollWidth,
      scrollHeight: tempContainer.scrollHeight,
      innerHTML: tempContainer.innerHTML.substring(0, 200) + '...'
    })

    progress.value = 40
    progressText.value = '正在等待内容渲染...'

    await new Promise(resolve => {
      requestAnimationFrame(() => {
        setTimeout(resolve, 1500)
      })
    })

    tempContainer.offsetHeight

    const images = tempContainer.querySelectorAll('img')
    console.log('发现图片数量:', images.length)

    if (images.length > 0) {
      progressText.value = '正在加载图片...'
      await Promise.all(Array.from(images).map((img, index) => {
        return new Promise(resolve => {
          console.log(`图片 ${index + 1}:`, img.src, `完成状态:`, img.complete, `尺寸:`, img.naturalWidth, 'x', img.naturalHeight)

          if (img.complete && img.naturalHeight !== 0) {
            resolve()
          } else {
            img.onload = () => {
              console.log(`图片 ${index + 1} 加载完成`)
              resolve()
            }
            img.onerror = () => {
              console.log(`图片 ${index + 1} 加载失败`)
              resolve()
            }
            setTimeout(() => {
              console.log(`图片 ${index + 1} 加载超时`)
              resolve()
            }, 8000)
          }
        })
      }))
    }

    progress.value = 60
    progressText.value = '正在转换为高清Canvas...'

    console.log('开始html2canvas转换, 容器最终状态:', {
      scrollWidth: tempContainer.scrollWidth,
      scrollHeight: tempContainer.scrollHeight,
      offsetWidth: tempContainer.offsetWidth,
      offsetHeight: tempContainer.offsetHeight,
      clientWidth: tempContainer.clientWidth,
      clientHeight: tempContainer.clientHeight,
      computedStyle: window.getComputedStyle(tempContainer).visibility,
      background: window.getComputedStyle(tempContainer).backgroundColor
    })

    const canvas = await html2canvas(tempContainer, {
      scale: pdfOptions.value.scale,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff',
      logging: true,
      removeContainer: false
    })

    console.log('Canvas生成完成:', {
      width: canvas.width,
      height: canvas.height,
      scale: pdfOptions.value.scale,
      dataURL: canvas.toDataURL('image/jpeg', 0.1).substring(0, 100) + '...'
    })

    progress.value = 80
    progressText.value = '正在生成PDF文档...'

    const pdf = new jsPDF({
      orientation: pdfOptions.value.orientation,
      unit: 'mm',
      format: pdfOptions.value.format,
      compress: true
    })

    const canvasWidth = canvas.width
    const canvasHeight = canvas.height
    const pdfPageWidth = pdf.internal.pageSize.getWidth()
    const pdfPageHeight = pdf.internal.pageSize.getHeight()

    const widthRatio = pdfPageWidth / canvasWidth * 72 / 96
    const heightRatio = pdfPageHeight / canvasHeight * 72 / 96
    const ratio = Math.min(widthRatio, heightRatio)

    const imgWidth = canvasWidth * ratio
    const imgHeight = canvasHeight * ratio

    if (imgHeight > pdfPageHeight) {
      let yPosition = 0
      let pageCount = 0

      while (yPosition < canvasHeight) {
        if (pageCount > 0) {
          pdf.addPage()
        }

        const sourceY = yPosition
        const sourceHeight = Math.min(pdfPageHeight / ratio, canvasHeight - yPosition)

        const pageCanvas = document.createElement('canvas')
        const pageCtx = pageCanvas.getContext('2d')
        pageCanvas.width = canvasWidth
        pageCanvas.height = sourceHeight * pdfOptions.value.scale

        pageCtx.drawImage(
          canvas,
          0, sourceY * pdfOptions.value.scale,
          canvasWidth, sourceHeight * pdfOptions.value.scale,
          0, 0,
          canvasWidth, sourceHeight * pdfOptions.value.scale
        )

        const pageImgData = pageCanvas.toDataURL('image/jpeg', pdfOptions.value.imageQuality)
        pdf.addImage(pageImgData, 'JPEG', 0, 0, imgWidth, sourceHeight * ratio)

        yPosition += sourceHeight
        pageCount++
      }
    } else {
      const imgData = canvas.toDataURL('image/jpeg', pdfOptions.value.imageQuality)
      const xOffset = (pdfPageWidth - imgWidth) / 2
      const yOffset = (pdfPageHeight - imgHeight) / 2

      pdf.addImage(imgData, 'JPEG', Math.max(0, xOffset), Math.max(0, yOffset), imgWidth, imgHeight)
    }

    progress.value = 95
    progressText.value = '正在保存PDF文件...'

    pdf.save(pdfOptions.value.filename)

    if (document.body.contains(tempContainer)) {
      document.body.removeChild(tempContainer)
    }

    progress.value = 100
    progressText.value = 'PDF生成完成！'

    setTimeout(() => {
      isConverting.value = false
      progress.value = 0
      ElMessage.success('PDF生成成功！')
      ElNotification({
        title: '转换完成',
        message: `PDF文件 "${pdfOptions.value.filename}" 已成功生成`,
        type: 'success',
        duration: 5000
      })
    }, 1000)

  } catch (error) {
    console.error('PDF生成失败:', error)
    ElMessage.error(`PDF生成失败: ${error.message || '未知错误'}`)
    ElNotification({
      title: '转换失败',
      message: '请检查HTML内容或降低图片质量后重试',
      type: 'error',
      duration: 8000
    })
    isConverting.value = false
    progress.value = 0

    const containers = document.querySelectorAll('div[style*="position: absolute"][style*="top: -9999px"]')
    containers.forEach(container => {
      if (document.body.contains(container)) {
        document.body.removeChild(container)
      }
    })
  }
}

const previewAsCanvas = async () => {
  if (!htmlContent.value) {
    ElMessage.warning('请先选择HTML文件或输入URL')
    return
  }
  isGeneratingPreview.value = true
  previewCanvas.value = null

  try {
    const processedHtml = preprocessHtmlContent(htmlContent.value)
    console.log('预览：预处理HTML完成，长度:', processedHtml.length)

    const tempContainer = document.createElement('div')

    const pageSize = pageSizes[pdfOptions.value.format]
    const isLandscape = pdfOptions.value.orientation === 'landscape'
    const pageWidth = isLandscape ? pageSize.height : pageSize.width
    const pageHeight = isLandscape ? pageSize.width : pageSize.height

    const containerWidth = pageWidth * 3.779527559
    const containerHeight = pageHeight * 3.779527559

    tempContainer.innerHTML = processedHtml

    tempContainer.style.cssText = `
      position: absolute;
      top: -9999px;
      left: 0;
      width: ${containerWidth}px;
      background: #ffffff;
      overflow: visible;
      border: none;
      margin: 0;
      padding: 0;
    `

    document.body.appendChild(tempContainer)

    console.log('预览：临时容器创建完成:', {
      width: containerWidth,
      height: containerHeight,
      scrollWidth: tempContainer.scrollWidth,
      scrollHeight: tempContainer.scrollHeight,
      innerHTML: tempContainer.innerHTML.substring(0, 200) + '...'
    })

    await new Promise(resolve => {
      requestAnimationFrame(() => {
        setTimeout(resolve, 1500)
      })
    })

    tempContainer.offsetHeight

    const images = tempContainer.querySelectorAll('img')
    console.log('预览：发现图片数量:', images.length)

    if (images.length > 0) {
      await Promise.all(Array.from(images).map((img, index) => {
        return new Promise(resolve => {
          console.log(`预览：图片 ${index + 1}:`, img.src, `完成状态:`, img.complete, `尺寸:`, img.naturalWidth, 'x', img.naturalHeight)

          if (img.complete && img.naturalHeight !== 0) {
            resolve()
          } else {
            img.onload = () => {
              console.log(`预览：图片 ${index + 1} 加载完成`)
              resolve()
            }
            img.onerror = () => {
              console.log(`预览：图片 ${index + 1} 加载失败`)
              resolve()
            }
            setTimeout(() => {
              console.log(`预览：图片 ${index + 1} 加载超时`)
              resolve()
            }, 8000)
          }
        })
      }))
    }

    console.log('预览：开始html2canvas转换, 容器最终状态:', {
      scrollWidth: tempContainer.scrollWidth,
      scrollHeight: tempContainer.scrollHeight,
      offsetWidth: tempContainer.offsetWidth,
      offsetHeight: tempContainer.offsetHeight,
      clientWidth: tempContainer.clientWidth,
      clientHeight: tempContainer.clientHeight,
      computedStyle: window.getComputedStyle(tempContainer).visibility,
      background: window.getComputedStyle(tempContainer).backgroundColor
    })

    previewCanvas.value = await html2canvas(tempContainer, {
      scale: pdfOptions.value.scale,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff',
      logging: true,
      removeContainer: false
    })

    console.log('预览：Canvas生成完成:', {
      width: previewCanvas.value.width,
      height: previewCanvas.value.height,
      scale: pdfOptions.value.scale,
      dataURL: previewCanvas.value.toDataURL('image/jpeg', 0.1).substring(0, 100) + '...'
    })

    if (document.body.contains(tempContainer)) {
      document.body.removeChild(tempContainer)
    }

  } catch (error) {
    console.error('Canvas预览生成失败:', error)
    ElMessage.error('无法生成Canvas预览，请检查HTML内容或降低图片质量后重试')
  } finally {
    isGeneratingPreview.value = false
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

.html-preview {
  background: #fafafa;
  font-family: Arial, sans-serif;
  line-height: 1.6;
}

.html-preview img {
  max-width: 100%;
  height: auto;
}

.html-preview table {
  border-collapse: collapse;
  width: 100%;
}

.html-preview th,
.html-preview td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.html-preview th {
  background-color: #f2f2f2;
}

.canvas-preview-container {
  min-height: 200px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: center;
  width: 100%;
}

.canvas-preview-container img {
  background: white;
  transition: transform 0.2s ease-in-out;
  display: block;
}

.canvas-preview-container img:hover {
  transform: scale(1.01);
}
</style> 
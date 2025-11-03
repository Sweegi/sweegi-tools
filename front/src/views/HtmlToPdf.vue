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
                :loading="isConverting">
                <el-icon class="mr-1"><FolderOpened /></el-icon>
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
              <label class="block text-sm font-medium text-gray-700 mb-2">DPI质量</label>
              <el-select v-model="pdfOptions.dpi" class="w-full">
                <el-option label="默认 (96 DPI)" :value="96" />
                <el-option label="中等 (120 DPI)" :value="120" />
                <el-option label="标准 (150 DPI)" :value="150" />
                <el-option label="高清 (300 DPI)" :value="300" />
                <el-option label="超高清 (600 DPI)" :value="600" />
              </el-select>
            </div>
          </div>
          <div class="mt-4">
            <el-checkbox v-model="pdfOptions.enhanceStyles" size="small">
              <span class="text-sm text-gray-700">增强文字对比度 (推荐，解决Canvas渲染字体过淡问题)</span>
            </el-checkbox>
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
                <div class="mb-4 text-sm text-gray-600 text-center space-y-1">
                  <div>Canvas尺寸: {{ previewCanvas.width }} × {{ previewCanvas.height }}px</div>
                  <div class="text-blue-600 font-medium">
                    预计PDF页数: {{ estimatedPages }} 页
                    <el-tag size="small" type="info" class="ml-2">
                      {{ pdfOptions.format.toUpperCase() }} {{ pdfOptions.orientation === 'portrait' ? '竖向' : '横向' }}
                    </el-tag>
                  </div>
                  <div v-if="pdfOptions.enhanceStyles" class="text-green-600 text-xs">
                    ✓ 已启用文字对比度增强
                  </div>
                  <div v-else class="text-orange-600 text-xs">
                    ⚠ 文字对比度增强已关闭，可能出现字体过淡问题
                  </div>
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
import { ref, computed, watch } from 'vue'
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
const estimatedPages = ref(1)

const pdfOptions = ref({
  format: 'a4',
  orientation: 'portrait',
  filename: 'converted.pdf',
  imageQuality: 1.0,
  dpi: 96,
  enhanceStyles: true
})

const pageSizes = {
  a4: {
    width: 210, height: 297,
    pixelWidth: { 96: 794, 120: 1487, 150: 1240, 300: 2480, 600: 4960 },
    pixelHeight: { 96: 1123, 120: 2105, 150: 1754, 300: 3508, 600: 7016 }
  },
  a3: {
    width: 297, height: 420,
    pixelWidth: { 96: 1123, 120: 1404, 150: 1754, 300: 3508, 600: 7016 },
    pixelHeight: { 96: 1587, 120: 1984, 150: 2480, 300: 4960, 600: 9920 }
  },
  letter: {
    width: 216, height: 279,
    pixelWidth: { 96: 816, 120: 1020, 150: 1275, 300: 2550, 600: 5100 },
    pixelHeight: { 96: 1056, 120: 1320, 150: 1650, 300: 3300, 600: 6600 }
  },
  legal: {
    width: 216, height: 356,
    pixelWidth: { 96: 816, 120: 1020, 150: 1275, 300: 2550, 600: 5100 },
    pixelHeight: { 96: 1344, 120: 1680, 150: 2100, 300: 4200, 600: 8400 }
  }
}

const progressColor = computed(() => {
  if (progress.value < 30) return '#d3139c'
  if (progress.value < 70) return '#e6a23c'
  return '#67c23a'
})

// 计算预计页数
const calculateEstimatedPages = (canvasHeight) => {
  if (!canvasHeight) return 1

  const pageSize = pageSizes[pdfOptions.value.format]
  const isLandscape = pdfOptions.value.orientation === 'landscape'
  const dpi = pdfOptions.value.dpi

  const pageWidth = isLandscape ? pageSize.pixelHeight[dpi] : pageSize.pixelWidth[dpi]
  const pageHeight = isLandscape ? pageSize.pixelWidth[dpi] : pageSize.pixelHeight[dpi]

  // 使用与PDF生成相同的计算方式
  const widthScale = (isLandscape ? pageSize.height : pageSize.width) / pageWidth
  const pageCapacity = (isLandscape ? pageSize.width : pageSize.height) / widthScale
  const sourcePageHeight = pageCapacity / widthScale

  return Math.ceil(canvasHeight / sourcePageHeight)
}

// 监听PDF设置变化，重新计算页数
watch([() => pdfOptions.value.format, () => pdfOptions.value.orientation, () => pdfOptions.value.dpi], () => {
  if (previewCanvas.value) {
    estimatedPages.value = calculateEstimatedPages(previewCanvas.value.height)
  }
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
  // 如果已经是完整的HTML文档，进行样式增强
  if (content.includes('<!DOCTYPE') || content.includes('<html')) {
    // 只有启用样式增强时才添加优化样式
    if (!pdfOptions.value.enhanceStyles) {
      return content
    }

    // 添加Canvas渲染优化样式
    const canvasOptimizedCSS = `
    <style>
    /* Canvas渲染优化样式 - 增强文字对比度 */
    body {
      -webkit-font-smoothing: antialiased !important;
      -moz-osx-font-smoothing: grayscale !important;
      text-rendering: optimizeLegibility !important;
      font-synthesis: none !important;
    }

    /* 增强淡色文字的对比度 */
    .summary, .summary p,
    .achievements li,
    .skill-list li,
    .certifications-list li,
    [style*="color: #555"],
    [style*="color: #666"],
    [style*="color:#555"],
    [style*="color:#666"] {
      color: #333 !important;
      font-weight: 400 !important;
    }

    /* 增强更淡的文字 */
    .position, .date, .education-date,
    [style*="color: #999"],
    [style*="color:#999"] {
      color: #555 !important;
      font-weight: 400 !important;
    }

    /* 确保图标可见 */
    .contact-icon {
      fill: #333 !important;
    }

    /* 增强边框可见性 */
    .achievements li,
    .skill-list li,
    .certifications-list li {
      border-bottom-color: #ddd !important;
    }

    /* 禁用动画避免Canvas渲染问题 */
    *, *::before, *::after {
      animation-duration: 0s !important;
      animation-delay: 0s !important;
      transition-duration: 0s !important;
      transition-delay: 0s !important;
    }

    /* 确保所有元素完全不透明 */
    .section {
      opacity: 1 !important;
      transform: none !important;
    }
    </style>
    `

    // 在</head>前插入优化样式
    if (content.includes('</head>')) {
      return content.replace('</head>', canvasOptimizedCSS + '\n</head>')
    } else if (content.includes('<head>')) {
      // 如果有head标签但没有结束标签，在head标签后插入
      return content.replace('<head>', '<head>' + canvasOptimizedCSS)
    } else if (content.includes('<html')) {
      // 如果没有head标签，在html标签后插入
      const htmlMatch = content.match(/<html[^>]*>/i)
      if (htmlMatch) {
        return content.replace(htmlMatch[0], htmlMatch[0] + '\n<head>' + canvasOptimizedCSS + '\n</head>')
      }
    }

    // 如果以上都不匹配，直接返回原内容
    return content
  }

  // 对于片段HTML，使用增强的基础样式
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
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-rendering: optimizeLegibility;
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
    console.log('预处理HTML完成:', {
      原始长度: htmlContent.value.length,
      处理后长度: processedHtml.length,
      样式增强: pdfOptions.value.enhanceStyles ? '已启用' : '已关闭',
      包含DOCTYPE: processedHtml.includes('<!DOCTYPE'),
      包含body: processedHtml.includes('<body'),
      前100字符: processedHtml.substring(0, 100)
    })

    progress.value = 20
    progressText.value = '正在创建临时容器...'

    const tempContainer = document.createElement('div')

    const pageSize = pageSizes[pdfOptions.value.format]
    const isLandscape = pdfOptions.value.orientation === 'landscape'
    const dpi = pdfOptions.value.dpi

    // 根据DPI获取对应的像素尺寸
    const canvasWidth = isLandscape ? pageSize.pixelHeight[dpi] : pageSize.pixelWidth[dpi]
    const canvasHeight = isLandscape ? pageSize.pixelWidth[dpi] : pageSize.pixelHeight[dpi]

    tempContainer.innerHTML = processedHtml

    tempContainer.style.cssText = `
      position: absolute;
      top: -9999px;
      left: 0;
      width: ${canvasWidth}px;
      height: auto;
      min-height: 100px;
      background: #ffffff;
      overflow: visible;
      border: none;
      margin: 0;
      padding: 20px;
      box-sizing: border-box;
      font-family: Arial, "Microsoft YaHei", sans-serif;
      font-size: 14px;
      line-height: 1.5;
      color: #333;
    `

    document.body.appendChild(tempContainer)

    console.log('临时容器创建完成:', {
      width: canvasWidth,
      height: canvasHeight,
      scrollWidth: tempContainer.scrollWidth,
      scrollHeight: tempContainer.scrollHeight,
      有内容: tempContainer.innerHTML.length > 100,
      内容长度: tempContainer.innerHTML.length,
      前200字符: tempContainer.innerHTML.substring(0, 200),
      子元素数量: tempContainer.children.length
    })

    progress.value = 40
    progressText.value = '正在等待内容渲染...'

    // 等待内容渲染和布局稳定
    await new Promise(resolve => {
      requestAnimationFrame(() => {
        setTimeout(() => {
          // 强制重新计算布局
          tempContainer.offsetHeight
          tempContainer.scrollHeight
          resolve()
        }, 2000) // 增加等待时间确保内容完全渲染
      })
    })

    console.log('内容渲染完成后的尺寸:', {
      offsetHeight: tempContainer.offsetHeight,
      scrollHeight: tempContainer.scrollHeight,
      clientHeight: tempContainer.clientHeight
    })

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

    // 获取实际内容高度，确保捕获完整内容
    const actualContentHeight = Math.max(
      tempContainer.scrollHeight,
      tempContainer.offsetHeight,
      tempContainer.clientHeight
    )

    console.log('内容高度分析:', {
      canvasWidth,
      expectedCanvasHeight: canvasHeight,
      actualContentHeight,
      scrollHeight: tempContainer.scrollHeight,
      offsetHeight: tempContainer.offsetHeight,
      clientHeight: tempContainer.clientHeight
    })

    const canvas = await html2canvas(tempContainer, {
      scale: 1, // 固定scale为1，使用准确的像素尺寸
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff',
      logging: true, // 启用日志输出帮助调试
      removeContainer: false
    })

    console.log('Canvas生成完成:', {
      width: canvas.width,
      height: canvas.height,
      expectedWidth: canvasWidth,
      expectedContentHeight: actualContentHeight,
      实际像素总数: canvas.width * canvas.height,
      Canvas不为空: canvas.width > 0 && canvas.height > 0,
      dataURL长度: canvas.toDataURL('image/jpeg', 0.1).length,
      dataURL前缀: canvas.toDataURL('image/jpeg', 0.1).substring(0, 50)
    })

    // 检查Canvas是否真的包含内容
    const ctx = canvas.getContext('2d')
    const imageData = ctx.getImageData(0, 0, Math.min(canvas.width, 100), Math.min(canvas.height, 100))
    const pixels = imageData.data
    let hasNonWhitePixels = false
    for (let i = 0; i < pixels.length; i += 4) {
      if (pixels[i] !== 255 || pixels[i + 1] !== 255 || pixels[i + 2] !== 255) {
        hasNonWhitePixels = true
        break
      }
    }
    console.log('Canvas内容检查:', {
      检查区域: `${Math.min(canvas.width, 100)}x${Math.min(canvas.height, 100)}`,
      包含非白色像素: hasNonWhitePixels
    })

    progress.value = 80
    progressText.value = '正在生成PDF文档...'

    const pdf = new jsPDF({
      orientation: pdfOptions.value.orientation,
      unit: 'mm',
      format: pdfOptions.value.format,
      compress: true
    })

    const actualCanvasWidth = canvas.width
    const actualCanvasHeight = canvas.height
    const pdfPageWidth = pdf.internal.pageSize.getWidth()
    const pdfPageHeight = pdf.internal.pageSize.getHeight()

    console.log('PDF分页参数:', {
      canvasSize: `${actualCanvasWidth}x${actualCanvasHeight}`,
      pdfPageSize: `${pdfPageWidth}x${pdfPageHeight}mm`,
      orientation: pdfOptions.value.orientation,
      format: pdfOptions.value.format
    })

    // 计算最佳缩放比例，确保宽度充分利用页面空间
    const widthScale = pdfPageWidth / actualCanvasWidth

    // 计算在此缩放比例下，每页能容纳的Canvas高度
    const scaledCanvasHeight = actualCanvasHeight * widthScale
    const pageCapacity = pdfPageHeight // 每页的最大高度

    console.log('分页计算:', {
      widthScale: widthScale.toFixed(4),
      scaledCanvasHeight: scaledCanvasHeight.toFixed(2),
      pageCapacity: pageCapacity.toFixed(2),
      estimatedPages: Math.ceil(scaledCanvasHeight / pageCapacity)
    })

    // 多页分页处理
    let currentY = 0
    let pageCount = 0
    const sourcePageHeight = pageCapacity / widthScale // 在原始Canvas中每页对应的高度

    while (currentY < actualCanvasHeight) {
      if (pageCount > 0) {
        pdf.addPage()
      }

      // 计算当前页面要截取的Canvas区域
      const remainingHeight = actualCanvasHeight - currentY
      const currentPageHeight = Math.min(sourcePageHeight, remainingHeight)

      console.log(`第${pageCount + 1}页:`, {
        sourceY: currentY.toFixed(2),
        sourceHeight: currentPageHeight.toFixed(2),
        remainingHeight: remainingHeight.toFixed(2)
      })

      // 创建当前页面的Canvas
      const pageCanvas = document.createElement('canvas')
      const pageCtx = pageCanvas.getContext('2d')
      pageCanvas.width = actualCanvasWidth
      pageCanvas.height = Math.ceil(currentPageHeight)

      // 设置白色背景
      pageCtx.fillStyle = '#ffffff'
      pageCtx.fillRect(0, 0, pageCanvas.width, pageCanvas.height)

      // 绘制当前页面的内容
      pageCtx.drawImage(
        canvas,
        0, currentY,                    // 源图像的起始位置
        actualCanvasWidth, currentPageHeight,  // 源图像的尺寸
        0, 0,                          // 目标Canvas的起始位置
        actualCanvasWidth, currentPageHeight   // 目标Canvas的尺寸
      )

      // 将页面Canvas转换为图片并添加到PDF
      const pageImgData = pageCanvas.toDataURL('image/jpeg', pdfOptions.value.imageQuality)
      const scaledPageHeight = currentPageHeight * widthScale

      pdf.addImage(pageImgData, 'JPEG', 0, 0, pdfPageWidth, scaledPageHeight)

      console.log(`第${pageCount + 1}页添加完成:`, {
        pdfSize: `${pdfPageWidth}x${scaledPageHeight.toFixed(2)}mm`
      })

      currentY += currentPageHeight
      pageCount++

      // 更新进度
      const progressValue = 80 + (currentY / actualCanvasHeight) * 15
      progress.value = Math.min(95, progressValue)
      const totalPages = Math.ceil(actualCanvasHeight / sourcePageHeight)
      progressText.value = `正在生成PDF文档... (第${pageCount}页/共${totalPages}页)`

      // 让UI有机会更新
      await new Promise(resolve => setTimeout(resolve, 10))
    }

    console.log(`PDF生成完成，共${pageCount}页`)

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
    const dpi = pdfOptions.value.dpi

    // 根据DPI获取对应的像素尺寸（预览用）
    const previewWidth = isLandscape ? pageSize.pixelHeight[dpi] : pageSize.pixelWidth[dpi]
    const previewHeight = isLandscape ? pageSize.pixelWidth[dpi] : pageSize.pixelHeight[dpi]

    tempContainer.innerHTML = processedHtml

    tempContainer.style.cssText = `
      position: absolute;
      top: -9999px;
      left: 0;
      width: ${previewWidth}px;
      height: auto;
      min-height: 100px;
      background: #ffffff;
      overflow: visible;
      border: none;
      margin: 0;
      padding: 20px;
      box-sizing: border-box;
      font-family: Arial, "Microsoft YaHei", sans-serif;
      font-size: 14px;
      line-height: 1.5;
      color: #333;
    `

    document.body.appendChild(tempContainer)

    console.log('预览：临时容器创建完成:', {
      width: previewWidth,
      height: previewHeight,
      scrollWidth: tempContainer.scrollWidth,
      scrollHeight: tempContainer.scrollHeight,
      innerHTML: tempContainer.innerHTML.substring(0, 200) + '...'
    })

    // 等待内容渲染和布局稳定
    await new Promise(resolve => {
      requestAnimationFrame(() => {
        setTimeout(() => {
          // 强制重新计算布局
          tempContainer.offsetHeight
          tempContainer.scrollHeight
          resolve()
        }, 2000) // 增加等待时间确保内容完全渲染
      })
    })

    console.log('预览：内容渲染完成后的尺寸:', {
      offsetHeight: tempContainer.offsetHeight,
      scrollHeight: tempContainer.scrollHeight,
      clientHeight: tempContainer.clientHeight
    })

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

    // 获取实际内容高度，确保预览也能显示完整内容
    const actualPreviewHeight = Math.max(
      tempContainer.scrollHeight,
      tempContainer.offsetHeight,
      tempContainer.clientHeight
    )

    console.log('预览：内容高度分析:', {
      previewWidth,
      expectedPreviewHeight: previewHeight,
      actualPreviewHeight,
      scrollHeight: tempContainer.scrollHeight,
      offsetHeight: tempContainer.offsetHeight,
      clientHeight: tempContainer.clientHeight
    })

    previewCanvas.value = await html2canvas(tempContainer, {
      scale: 1, // 固定scale为1，使用准确的像素尺寸
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff',
      logging: true, // 启用日志输出帮助调试
      removeContainer: false
    })

    // 计算预计页数
    estimatedPages.value = calculateEstimatedPages(previewCanvas.value.height)

    console.log('预览：Canvas生成完成:', {
      width: previewCanvas.value.width,
      height: previewCanvas.value.height,
      expectedWidth: previewWidth,
      expectedContentHeight: actualPreviewHeight,
      estimatedPages: estimatedPages.value,
      isComplete: previewCanvas.value.height >= actualPreviewHeight * 0.9, // 检查是否捕获了足够的内容
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
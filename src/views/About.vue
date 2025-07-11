<template>
  <div class="about-container p-8">
    <div class="max-w-3xl mx-auto bg-white p-8 rounded-lg shadow-md">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">关于 Markdown 查看器</h1>
      <p class="text-gray-600 mb-4">
        这是一个简单而强大的本地 Markdown 文件查看工具，基于Vue3、Element Plus和TailwindCSS构建。
      </p>
      
      <h2 class="text-xl font-semibold text-gray-700 mt-6 mb-4">主要功能</h2>
      <ul class="list-disc pl-6 space-y-2 text-gray-600">
        <li>打开本地 Markdown 文件</li>
        <li>高性能渲染 Markdown 内容</li>
        <li>代码高亮显示</li>
        <li>最近文件记录功能</li>
      </ul>
      
      <h2 class="text-xl font-semibold text-gray-700 mt-6 mb-4">技术栈</h2>
      <div class="flex flex-wrap gap-2 mb-6">
        <el-tag>Vue 3</el-tag>
        <el-tag>Element Plus</el-tag>
        <el-tag>TailwindCSS</el-tag>
        <el-tag>Markdown-it</el-tag>
        <el-tag>Highlight.js</el-tag>
      </div>
      
      <div class="mt-8 text-center">
        <el-button type="primary" @click="goHome">返回首页</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script> 
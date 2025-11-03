import { defineConfig } from 'vite'
import legacy from '@vitejs/plugin-legacy'
import htmlPostBuildPlugin from './HtmlPostBuildPlugin'
import vue from '@vitejs/plugin-vue'
import path from 'path'

const base = './'

// https://vitejs.dev/config/
export default defineConfig(() => {
  return {
    base: base,
    plugins: [
      vue(),
      // 配置以下两个插件
      legacy({
        targets:["defaults","not IE 11"],
      }),
      htmlPostBuildPlugin(base)
    ],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      host: '0.0.0.0',
      port: 5173,
    },
    // 报表项目打包时 @vitejs/plugin-legacy插件生成的script路径不正确，由这个配置来解决
    // 会将生成的script标签的src值由 '../../xxx/xxx' 改成 'xxx/xxx',
    // 再由插件 htmlPostBuildPlugin 将 'xxx/xxx' 改为  './xxx/xxx' 来获得正确的相对路径
    experimental: {
      renderBuiltUrl: url => {
        return url
      }
    }
  }
}) 

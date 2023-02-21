import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vitePluginImp from 'vite-plugin-imp'
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), vueJsx(), vitePluginImp({
    libList: [
      {
        libName: 'ant-design-vue',
        style: (name) => `ant-design-vue/es/${name}/style/index.less`,
      },
    ],
  })],
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true,
      }
    }
  },
  build: {
    outDir: '../backend/dist',
    chunkSizeWarningLimit: 1024,
  },
})

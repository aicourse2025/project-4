import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(),  tailwindcss(),],
  server: {
    proxy: {
      '/api': {
        target: 'https://zl2pcttxj4.execute-api.eu-central-1.amazonaws.com/dev',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})

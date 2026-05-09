import DefaultTheme from 'vitepress/theme'
import AiChat from './components/AiChat.vue'
import './custom.css'
import { onMounted } from 'vue'

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    app.component('AiChat', AiChat)
  },
  setup() {
    onMounted(() => {
      if (window.location.pathname === '/' || window.location.pathname === '') {
        document.body.classList.add('home-page')
      }
    })
  },
}

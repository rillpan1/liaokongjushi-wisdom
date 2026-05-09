import DefaultTheme from 'vitepress/theme'
import './custom.css'
import { onMounted } from 'vue'

export default {
  ...DefaultTheme,
  setup() {
    onMounted(() => {
      // Add class to homepage for CSS targeting
      if (window.location.pathname === '/' || window.location.pathname === '') {
        document.body.classList.add('home-page')
      }
    })
  }
}
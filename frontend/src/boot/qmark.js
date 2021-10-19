import Plugin from '@quasar/quasar-ui-qmarkdown'
import '@quasar/quasar-ui-qmarkdown/dist/index.css'
import { boot } from 'quasar/wrappers'

export default boot(
  /* async */ ({ app }) => {
    app.provide(Plugin)
  }
)

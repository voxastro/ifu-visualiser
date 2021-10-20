<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-10 q-mt-md">
        <div class="row">
          <q-card v-if="tocTree" class="col-2 gt-sm" flat>
            <q-card-section>
              <TocContent :tocTree="tocTree" :denseLevel="2" />
            </q-card-section>
          </q-card>
          <q-markdown
            ref="markdown"
            :src="md_docs"
            toc
            @data="onToc"
            class="col"
          />
          <div class="col-2 gt-sm"></div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, watchEffect } from 'vue'
import md_docs from '../markdown/docs.md'
import TocContent from '../components/TocContent.vue'

export default defineComponent({
  name: 'Docs',
  components: { TocContent },
  setup() {
    const markdown = ref(null)
    const toc = ref(null)
    const tocTree = ref(null)

    const { getScrollTarget, setVerticalScrollPosition } = scroll

    function scrollToElement(id) {
      const el = document.getElementById(id)
      const target = getScrollTarget(el)
      const offset = el.offsetTop
      const duration = 500
      setVerticalScrollPosition(target, offset, duration)
    }

    const onToc = (tc) => {
      toc.value = tc
    }

    watchEffect(() => {
      if (markdown.value) {
        tocTree.value = markdown.value.makeTree(toc.value)
      }
    })

    return {
      md_docs: md_docs,
      markdown,
      onToc,
      toc,
      tocTree,
      scrollToElement,
    }
  },
})
</script>

<style lang="scss">
// Override some styles

.q-markdown--token {
  background: #a91c571a;
  color: $grey-9;
  border: $grey-2 solid 1px;
  padding: 0px 4px;
  border-radius: 7px;
}
</style>

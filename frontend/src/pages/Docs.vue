<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-1"></div>
      <div class="gt-md col-2">
        <q-card v-if="tocTree" class="fixed" flat>
          <q-card-section>
            <TocContent :tocTree="tocTree" :denseLevel="2" />
          </q-card-section>
        </q-card>
      </div>
      <div class="col">
        <q-markdown
          ref="markdown"
          :src="md_docs"
          toc
          @data="onToc"
          class="col"
        />

        <DocsTablesInfo />
      </div>
      <div class="col-1"></div>
      <div class="col-2 gt-md"></div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, watchEffect, computed } from 'vue'
import md_docs from '../markdown/docs.md'
import TocContent from '../components/TocContent.vue'
import DocsTablesInfo from '../components/DocsTablesInfo.vue'
import { useStore } from 'vuex'

export default defineComponent({
  name: 'Docs',
  components: { TocContent, DocsTablesInfo },
  setup() {
    const store = useStore()
    const markdown = ref(null)
    const toc = ref(null)
    const tocTree = ref(null)
    const tableColumns = computed(() => store.state.tableColumnsObject)

    const { getScrollTarget, setVerticalScrollPosition } = scroll

    function scrollToElement(id) {
      const el = document.getElementById(id)
      const target = getScrollTarget(el)
      const offset = el.offsetTop
      const duration = 500
      setVerticalScrollPosition(target, offset, duration)
    }

    const tableColumnsSorted = [
      ...tableColumns.value.filter((e) => e.label == 'cube'),
      ...tableColumns.value.filter((e) => e.label != 'cube'),
    ]

    const onToc = (tc) => {
      // Manually extend TOC by table description
      const tcExt = tableColumnsSorted.map((e) => ({
        id: e.label,
        label: e.label,
        level: 2,
        children: [],
      }))
      toc.value = [...tc, ...tcExt]
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
  color: $purple-9;
  border: $grey-6 solid 1px;
  padding: 0px 4px;
  border-radius: 7px;
}
</style>

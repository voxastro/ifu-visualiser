<template>
  <q-list>
    <template v-for="item in tocTree.slice(1)">
      <q-item
        v-if="!item.children.length"
        :key="item.id"
        clickable
        :dense="item.level >= denseLevel"
        @click="scrollToElement(item.id)"
        :class="
          item.level >= denseLevel
            ? 'text-grey-7 text-weight-regular'
            : 'text-grey-9 text-weight-medium'
        "
      >
        <q-item-section>{{ item.label }}</q-item-section>
      </q-item>

      <q-expansion-item
        v-else
        :key="item.id"
        default-opened
        expand-icon-toggle
        :dense="item.level >= denseLevel"
        :label="item.label"
        :content-inset-level="item.level / 7"
        @click="scrollToElement(item.id)"
        :class="
          item.level >= denseLevel
            ? 'text-grey-7 text-weight-regular'
            : 'text-grey-9 text-weight-medium'
        "
      >
        <TocContent :tocTree="item.children" :denseLevel="denseLevel" />
      </q-expansion-item>
    </template>
  </q-list>
</template>

<script>
import { defineComponent, ref, watchEffect } from 'vue'
import { scroll } from 'quasar'
export default defineComponent({
  name: 'TocContent',
  props: {
    // 'tocTree' will be provided by the component using QmToc (vmd components)
    tocTree: {
      type: Array,
      default() {
        return []
      },
    },
    denseLevel: { default: 1 },
  },
  setup() {
    const { getScrollTarget, setVerticalScrollPosition } = scroll

    function scrollToElement(id) {
      const el = document.getElementById(id)
      const target = getScrollTarget(el)
      const offset = el.offsetTop
      const duration = 500
      setVerticalScrollPosition(target, offset, duration)
    }
    return { scrollToElement }
  },
})
</script>

<!-- <style lang="sass">
// When navigating (scrolling) to an anchor and to avoid that the anchor gets
// hidden by the fixed page header we offset the scrolling by the header height.
.q-markdown [class^="q-markdown--heading-h"]
  scroll-margin-top: $toolbar-min-height
</style> -->

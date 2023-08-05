<template>
  <div class="solara-tree">
    <h4 class="pa-2">
      <span class="solara-tree__path-item" @click="path = path.slice(0,1)"> home </span>
      <span v-for="(p, i) in path_without_leaf.slice(1)">
        /
        <span class="solara-tree__path-item" @click="path = path.slice(0, i+2)">{{ p.label }}</span>
      </span>
      <v-btn icon @click="refresh_count += 1">
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
    </h4>
    <v-sheet class="solara-tree-scroll pa-2" ref="scrollpane">
      <v-list>
        <v-list-item v-if="path_without_leaf.length > 1" @click.stop="path = path_without_leaf.slice(0, -1)">
          <v-list-item-icon>
            <v-icon>mdi-keyboard-backspace</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>
              ..
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item
            v-for="item in items"
            :key="item.id"
            @click.stop="path = [...path_without_leaf, item]"
            :class="(path.slice(-1)[0].id === item.id) ? 'solara-tree-selected': ''"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title :class="'solara-tree-' + (item.leaf ? 'file' : 'dir')">
              {{ item.label }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-sheet>
  </div>
</template>

<script>
module.exports = {
  mounted() {
    const element = this.$refs.scrollpane.$el
    element.scrollTop = this.scroll_pos

    this._scrollListener = _.debounce((e) => {
      this.scroll_pos = Math.round(element.scrollTop)
    }, 50)
    element.addEventListener('scroll', this._scrollListener)
  },
  computed: {
    path_without_leaf() {
      return this.path.slice(-1)[0].leaf ? this.path.slice(0, -1) : this.path
    }
  },
  watch: {
    scroll_pos(v) {
      this.$nextTick(() => this.$refs.scrollpane.$el.scrollTop = v);
    }
  }
}
</script>

<style id="solara-tree">
.solara-tree {
  height: 100%;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.solara-tree-scroll {
  overflow: auto;
  flex-grow: 1;
}

.solara-tree__path-item {
  cursor: pointer;
}

.solara-tree-dir {
  font-weight: bold;
}

.solara-tree-selected {
  background-color: #3333;

}

.solara-tree .v-list-item__icon,
.solara-tree .v-list-item__list {
  margin-top: 0;
  margin-bottom: 0;
}

.v-application--is-ltr .solara-tree .v-list-item__icon {
  margin-right: 8px;
}

.solara-tree .v-list-item {
  height: 28px;
  min-height: 0;
  padding-left: 0;
}
</style>

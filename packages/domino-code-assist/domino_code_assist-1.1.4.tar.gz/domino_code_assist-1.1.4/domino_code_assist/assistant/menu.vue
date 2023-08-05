<template>
  <div>
  <div v-if="overlay_open" style="position: fixed; top: 0; bottom: 0; left: 0; right: 0"></div>
  <v-menu open-on-hover bottom>
    <template v-slot:activator="{ on }">
      <v-btn v-on="on" color="primary" rounded small style="min-width: 28px; padding: 0; margin: 2px" :disabled="disabled">
        <v-img :src="logo" style="height: 16px; max-width: 16px; border-radius: 8px"/>
      </v-btn>
    </template>
    <v-list flat dense>
      <v-list-item-group
          v-model="selected"
          @change="(item) => {if (item) {overlay_open = true}}"
          color="primary"
      >
        <template v-for="item in items">
          <v-list-item
              :key="item.action"
              :value="item"
          >
            <v-list-item-icon>
              <v-icon v-text="item.icon"></v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>
                {{ item.title }}
              </v-list-item-title>
            </v-list-item-content>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                    v-if="item.action === 'snippets'"
                    icon
                    :color="snippet_edit_mode ? 'primary' : ''"
                    @click.stop="snippet_edit_mode = !snippet_edit_mode"
                    @mousedown.stop=""
                    style="margin-left: 16px"
                    v-bind="attrs"
                    v-on="on"
                >
                  <v-icon>
                    {{ snippet_edit_mode ? 'mdi-pencil' : 'mdi-pencil-off'}}
                  </v-icon>
                </v-btn>
              </template>
              <span v-if="snippet_edit_mode">Snippet editing enabled. Click to disable.</span>
              <span v-else>Snippet editing disabled. Click to enable.</span>
            </v-tooltip>
          </v-list-item>
          <v-divider v-if="item.divider" :key="'div'+item"></v-divider>
        </template>
      </v-list-item-group>
    </v-list>
  </v-menu>
  </div>
</template>

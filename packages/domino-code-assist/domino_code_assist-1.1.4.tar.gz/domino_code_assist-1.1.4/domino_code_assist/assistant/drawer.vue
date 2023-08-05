<template>
  <div>
    <v-bottom-sheet v-model="is_open" :width="width" transition="right-sheet-transition">
      <v-card :class="['domino-right-sheet', inIframe && 'domino-right-sheet--in-iframe']">
        <v-card-title class_="text-h5" style="background-color: #2d71c7; color: white">
          <span>{{ title }}</span>
          <v-spacer></v-spacer>
          <v-btn icon dark @click="is_open = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="overflow-auto domino-right-sheet--content">
          <jupyter-widget v-if="content" :widget="content"></jupyter-widget>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-text-field v-if="show_var_out" v-model="var_out" hide-details class="mr-8 dense" style="max-width: 250px; margin-top: -7px;"
                        :label="`Output variable${valid_variable_name ? '' : ' *invalid'}`" :error-messages="valid_variable_name ? [] : ['invalid']"></v-text-field>
          <v-btn outlined color="primary" @click="is_open = !is_open">
            <v-icon>mdi-close</v-icon>
            Cancel
          </v-btn>
          <v-btn v-if="show_default_buttons" @click="apply()" color="primary" :elevation="0" :disabled="apply_disabled">
            <v-icon left>mdi-play</v-icon>
            Run
          </v-btn>
          <v-menu v-if="warning_widget" open-on-hover>
            <template v-slot:activator="{ on }">
              <v-icon v-on="on" color="orange" class="ml-2">mdi-alert</v-icon>
            </template>
            <v-sheet>
              <jupyter-widget :widget="warning_widget"></jupyter-widget>
            </v-sheet>
          </v-menu>
        </v-card-actions>
      </v-card>
    </v-bottom-sheet>
  </div>
</template>
<script>
module.exports = {
  watch: {
    is_open: (val) => {
      if (!window['Jupyter']) {
        return;
      }
      /* workaround for notebook stealing paste events of the image input of the markdown editor */
      if (val) {
        Jupyter.keyboard_manager.disable();
      } else {
        Jupyter.keyboard_manager.enable();
      }
    }
  },
  computed: {
    inIframe() {
      try {
        return window.self !== window.top;
      } catch (e) {
        return true;
      }
    },
  },
}
</script>
<style id="domino_code_assist-drawer">
.vuetify-styles .v-bottom-sheet.v-dialog:not(.v-dialog--fullscreen) {
  margin: 0 0 0 auto;
  max-height: 100vh;
  align-self: center;
  height: 100vh;
}

.vuetify-styles .v-card.domino-right-sheet:not(.v-sheet--tile):not(.v-card--shaped) {
  border-radius: 0;
}

.v-card.domino-right-sheet {
  height: 100%;
  max-height: 100%;
  display: flex;
  flex-direction: column;
  min-width: 600px;
}

.domino-right-sheet--content {
  max-width: 100vw;
}
.vuetify-styles .v-dialog>.v-card>div.domino-right-sheet--content.v-card__text {
  padding-top: 0;
  padding-bottom: 0;
}

.v-card.domino-right-sheet .v-card__text {
  flex-grow: 1;
}

.right-sheet-transition-enter {
  transform: translateX(100%);
}

.right-sheet-transition-leave-to {
  transform: translateX(100%)
}

.domino-right-sheet .solara-file-list {
  height: unset;
  flex-grow: 1;
}

.domino-right-sheet .solara-file-browser {
  display: flex;
  flex-direction: column;
  height: 100%;
  max-height: 100%;
}
.v-card.v-sheet.domino-right-sheet--in-iframe .v-card__actions{
  padding-right: 104px;
}
</style>

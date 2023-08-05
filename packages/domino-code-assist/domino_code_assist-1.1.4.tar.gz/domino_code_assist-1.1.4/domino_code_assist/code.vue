<template>
  <div :class="['solara-code-highlight', 'solara-code-highlight__box', no_controls && 'solara-code-highlight--no_controls' ]">
    <div v-for="(chunk, index) in highlighted_chunks" class="domino_code_assist-code__chunk">
      <div v-html="chunk"></div>
      <div v-if="error && error[0] == index">
        <v-menu open-on-hover bottom left offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-icon color="red" v-on="on">mdi-bug</v-icon>
          </template>
          <v-card>
            <v-card-text>
              {{ error[1] }}
            </v-card-text>
          </v-card>
        </v-menu>
      </div>
      <div v-if="!no_controls" :class="index < highlighted_chunks.length - 1 ? 'domino_code_assist-code__controls' : ''">
        <span v-if="index < highlighted_chunks.length - 1">
          <v-btn icon @click="send_event('insert', index)">
            <v-icon>mdi-subdirectory-arrow-left</v-icon>
          </v-btn>
          <v-btn icon @click="send_event('edit', index)">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn icon @click="send_event('delete', index)" :disabled="!assistant_mode && index == 0">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </span>
      </div>
    </div>
  </div>
</template>

<style id="domino_code_assist-code">
.domino_code_assist-code__chunk {
  position: relative;
  display: flex;
  flex-direction: row;
}

.domino_code_assist-code__controls {
  position: absolute;
  right: -7px;
  top: -7px;
  opacity: 0;
  background-color: #00000033;
  border-radius: 4px;
  transition: opacity .5s;
  display: flex;
  flex-direction: row-reverse;
}

:not(.solara-code-highlight--no_controls) .domino_code_assist-code__chunk:hover {
  border-bottom: 1px solid grey;
}

.domino_code_assist-code__chunk:hover .domino_code_assist-code__controls {
  opacity: 1;
  z-index: 1;
}

.highlight pre {
  border-width: 0px;
}
</style>

<script>
module.exports = {
  methods: {
    send_event(name, index) {
      this.event = {
        name,
        index,
        id: Math.random().toString(16)
      }
    }
  }
}
</script>

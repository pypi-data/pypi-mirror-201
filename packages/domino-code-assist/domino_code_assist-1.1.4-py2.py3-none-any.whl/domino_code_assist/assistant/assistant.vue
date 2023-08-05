<template>
  <div>
    <div style="display: flex">
      <div class="mx-2">
        <jupyter-widget :widget="tour"></jupyter-widget>
      </div>
      <v-btn v-if="sample_project.length === 0" small class="mx-2" color="primary" @click="insert_sample_project">
        <v-icon left small>mdi-format-color-fill</v-icon>
        CREATE SAMPLE NOTEBOOK
      </v-btn>
      <div style="white-space: nowrap; margin-top: 4px">Domino Code Assist initialized. (v{{ version }})</div>
    </div>
    <div style="display: none">
      <div ref="domino_code_assistAssistantMenu" class="domino_code_assist-assistant-menu vuetify-styles" style="display: none">
        <div class="v-application v-application--is-ltr theme--light" style="background: unset" data-app>
          <v-btn v-if="snippet_edit_mode" class="domino_code_assist-assistant__add-snippet-btn" outlined color="primary" small @click="snippet_add_dialog_open = true">
            <v-icon left>mdi-plus</v-icon>
            Save as snippet
          </v-btn>
          <v-btn class="domino_code_assist-assistant__save-snippet-btn" outlined color="primary" small @click="saveSnippet">
            <v-icon left>mdi-content-save</v-icon>
            Save
          </v-btn>
          <jupyter-widget :widget="menu"></jupyter-widget>
        </div>
      </div>
    </div>
    <v-snackbar v-model="snippet_saved_snackbar">
      Snippet saved.
    </v-snackbar>
  </div>
</template>
<script>
module.exports = {
  destroyed() {
    this.cleanUpDOM();
  },
  created() {
    if (this.in_user_install_mode) {
      const labConfigData = document.getElementById('jupyter-config-data');
      const base_url = labConfigData ? JSON.parse(labConfigData.textContent).baseUrl : document.body.dataset.baseUrl;
      window.solara_cdn = `${base_url}nbextensions/_solara/cdn`;
    }
  },
  mounted() {
    window.lastLcaAsistant = this
    this.assistantDOM = this.$refs.domino_code_assistAssistantMenu;
    this.notebookId = test = DCA.getNotebookId(this.$el);

    this.cleanUpDOM()

    this.cleanups = [];
    DCA.assistants[this.notebookId] = this;
    this.isAttached = true;

    const update = () => {
      if (this.isAttached) {
        this.injectCells();
        this.notebook_path = DCA.getNotebookPath(this.notebookId);
        const cells = DCA.getCells(this.notebookId);
        cells.filter(cell => cell.model.type === "markdown" && cell.model.id == null)
             .forEach(cell => cell.model.id = this.generate_id())
          this.markdown_cells = Object.fromEntries(
              cells.filter(cell => cell.model.type === "markdown")
                   .map(cell => [cell.model.id, cell.model.value.text])
              )
        if (this._cell && this.snippet_edit_mode && this._cell.model.type === "code") {
          this.syncStyle(this._cell);
        }
        setTimeout(update, 1000);
      }
    }
    update();
  },
  watch: {
    code(value) {
      if (value == null) {
        return;
      }
      const isEdit = !!this._cell.model.value.text;

      if (value.modifier && value.modifier === "insert-above") {
        DCA.insertCellAbove(this.notebookId, this._cell, value);
        return;
      }
      this._cell.model.value.text = value.code;
      if (value.meta) {
        this._cell.model.metadata.set("assistant", value.meta);
      }
      DCA.activate(this.notebookId, this._cell);

      if (value.type_ && value.type_ === "markdown") {
        DCA.changeCellType(this.notebookId, this._cell, "markdown")
      } else {
        DCA.changeCellType(this.notebookId, this._cell, "code")
      }
      DCA.runAndAdvance(this.notebookId);
      this.injectCells();
      this.code = null;
    },
    snippet_add_header(v) {
      if (!v) {
        return;
      }
      this._cell.model.value.text = v + this._cell.model.value.text;
      this.save_snippet(this._cell.model.value.text);
      this.snippet_path = null;
      this.snippet_add_dialog_open = false;
      this.snippet_saved_snackbar=true;
    },
    sample_project(v) {
      if (!v) {
        return;
      }
      const firstLcaInitCell = DCA.getCells(this.notebookId).filter(cell => cell.model.type === "code" && cell.model.value.text.includes("dca.init()"))[0];
      DCA.insertCellsBelow(this.notebookId, firstLcaInitCell, v);
    },
  },
  methods: {
    syncStyle(cell) {
      if (cell.model.type === "code" && cell.model.value.text.startsWith(this.snippet_prefix)) {
        this.assistantDOM.classList.add("domino_code_assist-assistant-snippet-edit")
      } else {
        this.assistantDOM.classList.remove("domino_code_assist-assistant-snippet-edit")
      }
    },
    show(cell) {
      this.cell_id = cell.model.id
      this._cell = cell

      cell.node.prepend(this.assistantDOM)
      this.syncStyle(cell)
      this.code_up = {
        code: cell.model.value.text,
        meta: cell.model.metadata.get("assistant") || null,
        type_: cell.model.type,
      }
    },
    cleanup() {
      this.cleanups.forEach(cleanup => cleanup());
      this.cleanups = [];
    },
    injectCells() {
      const cells = DCA.getCells(this.notebookId);
      cells.forEach(cell => {
        const input = cell.node;

        if (input.dataset && input.dataset.visited !== "true") {
          const onMouseEnter = () => {
            if(!this.isAttached) {
              console.error("failed to remove mouseenter")
              return;
            }
            this.show(cell)
          };
          input.addEventListener("mouseenter", onMouseEnter);
          input.dataset.visited = true;
          this.cleanups.push(() => {
            input.dataset.visited = false;
            input.removeEventListener("mouseenter", onMouseEnter)}
          );
        }
      })
    },
    async jupyter_save_notebook() {
      const response = await DCA.saveNotebook(this.notebookId);
      this.notebook_saved(response);
    },
    generate_id() {
      const cells = DCA.getCells(this.notebookId);
      const usedIds = cells.filter(cell => cell.model.id).map(cell => cell.model.id)
      while (true) {
        const id = Math.random().toString(16).slice(2,10);
        if (!usedIds.includes(id)) {
          return id
        }
      }
    },
    saveSnippet() {
      this.save_snippet(this._cell.model.value.text);
      this.snippet_saved_snackbar=true;
    },
    cleanUpDOM() {
      if(DCA.assistants[this.notebookId]) {
        // remove old one from DOM
        DCA.assistants[this.notebookId].isAttached = false;
        DCA.assistants[this.notebookId].assistantDOM.remove()
        DCA.assistants[this.notebookId].cleanup()
      }
    }
  }
}
</script>
<style id="domino_code_assist-assistant">
  .domino_code_assist-assistant-menu {
    display: block !important;
    position: absolute;
    top: 0;
    right: 0;
    z-index: 3;
  }

  .markdown-drawer .solara-milkdown .milkdown .ProseMirror {
    min-height: 400px;
  }

  .domino_code_assist-assistant__add-snippet-btn, .domino_code_assist-assistant__save-snippet-btn {
    margin-right: 32px;
    margin-top: 2px;
    backdrop-filter: blur(2px);
  }

  .domino_code_assist-assistant-menu.domino_code_assist-assistant-snippet-edit .domino_code_assist-assistant__add-snippet-btn {
    display: none;
  }

  .domino_code_assist-assistant-menu:not(.domino_code_assist-assistant-snippet-edit) .domino_code_assist-assistant__save-snippet-btn {
    display: none;
  }
  .jp-Toolbar.jp-cell-toolbar {
    right: 232px;
  }
  .output_area > .output_subarea > .jupyter-widgets > .lm-Widget > .vuetify-styles{
      padding-top: 11px;
      padding-bottom: 11px;
  }
</style>

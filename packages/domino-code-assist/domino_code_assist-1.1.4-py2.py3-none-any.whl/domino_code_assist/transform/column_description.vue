<template>
  <div class="domino-column-description__info-main">
    <strong>Column info:</strong>
    <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
    <div v-else style="display: flex;">
      <v-alert v-if="error" type="error">{{ error }}</v-alert>
      <table v-if="info && column" class="domino-column-description__info">
        <tr>
          <th>dtype</th>
          <td>{{ info.dtype }}</td>
        </tr>
        <tr v-for="(value, label) in info.description">
          <th v-if="label === 'data_type'">effective dtype</th>
          <th v-else>{{ label }}</th>
          <td v-if="label === 'unique'">
            <v-tooltip v-if="value" bottom>
              <template v-slot:activator="{ on }">
                <span v-on="on" class="domino-column-description__uniques">{{ value.length }}</span>
              </template>
              <div>{{ value }}</div>
            </v-tooltip>
            <span v-else> > 1000 </span>
          </td>
          <td v-else>{{ value }}</td>
        </tr>
      </table>
      <div v-if="histogram && column" class="domino-column-description__column_histogram">
        <jupyter-widget :widget="histogram"></jupyter-widget>
      </div>
    </div>
  </div>
</template>

<style id="domino-column-description">
.domino-column-description__info-main {
  width: 448px;
  padding-left: 8px;
  padding-right: 8px;
  min-height: 180px;
}

.domino-column-description__info {
  width: 228px;
}

.domino-column-description__info td,
.domino-column-description__info th {
  padding: 0 10px;
}

.domino-column-description__info th {
  opacity: 0.7;
  vertical-align: top;
}

.domino-column-description__column_histogram {
  height: 100px;
  width: 200px;
  margin-right: 4px;
}

.domino-column-description__column_histogram .js-plotly-plot {
  height: 100%;
}
.domino-column-description__uniques {
  text-decoration: underline;
}
</style>

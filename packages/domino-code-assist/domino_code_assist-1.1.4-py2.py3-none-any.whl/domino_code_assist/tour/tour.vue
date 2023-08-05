<template>
  <v-menu :close-on-content-click="false" v-model="opened">
    <template v-slot:activator="{ on }">
      <v-btn
        v-on="on"
        color="primary"
        dark
        small
      >
        <v-icon small left>mdi-information-outline</v-icon>
        Take the tour
      </v-btn>
    </template>
    <v-card>
      <v-carousel v-model="step" class="dca-tour" style="height: unset">
        <v-carousel-item
            v-for="(text, i) in texts"
            :key="text"
            style="height: unset"
        >
          <div style="height: 550px; width: 1050px; display: flex; flex-direction: column">
            <div style="flex-grow: 1; overflow: auto; display: flex; justify-content: center;">
              <img style="align-self: center;" :src="images[i]" :width="widths[i]"/>
            </div>
            <div style="margin-bottom: 50px; display: flex; justify-content: center;">
              <div style="max-width: 1050px; font-weight: bold; font-size: 24px; text-align: center; color: var(--jp-ui-font-color0); opacity: 0.65;">
                {{ text }}
              </div>
            </div>
          </div>
        </v-carousel-item>
      </v-carousel>
    </v-card>
  </v-menu>
</template>

<script>
modules.exports = {
  name: "tour"
}
</script>

<style id="dca-tour">
.dca-tour .v-responsive.v-image.v-carousel__item {
  height: unset !important;
}
</style>

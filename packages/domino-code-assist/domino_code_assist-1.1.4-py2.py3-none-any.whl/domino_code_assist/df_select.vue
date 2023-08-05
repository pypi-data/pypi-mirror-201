<template>
  <v-select :items="items" :label="label" v-model="value">
    <template v-slot:item="{item}">
      <v-list-item-icon>
        <v-icon v-if="item == 'Load more data'">mdi-database-plus</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title>
          {{ item }}
        </v-list-item-title>
      </v-list-item-content>
    </template>
  </v-select>
</template>

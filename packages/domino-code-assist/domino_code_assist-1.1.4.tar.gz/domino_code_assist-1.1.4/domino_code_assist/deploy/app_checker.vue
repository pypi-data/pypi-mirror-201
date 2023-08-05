<template>
</template>

<script>
module.exports = {
  methods: {
    async checkAppOnline() {
      const result = await fetch(this.url);
      if (result.status === 200) {
        const text = await result.text();
        if (text.includes("solara.production = true;")) {
          return true
        }

      }
      return false
    },
    async loop() {
      if (this.running && !this.online) {
        this.online = await this.checkAppOnline()
        if (!this.online) {
          setTimeout(this.loop, 1000)
        }
      }
    }
  },
  watch: {
    async running(value) {
      if (value) {
        if (this.dev) {
          setTimeout(() => this.online = true, 3000)
        } else {
          this.loop()
        }
      } else {
        this.online = false
      }
    }
  }
}
</script>

<template>
</template>
<script>
module.exports = {
  created() {
    this.project_token = window._dca_mixpanel_token
    this.mixpanel_enabled = window._dca_mixpanel_enabled

    const browser = (function (agent) { switch (true) {
      case agent.indexOf("edge") > -1: return "MS Edge";
      case agent.indexOf("edg/") > -1: return "Edge ( chromium based)";
      case agent.indexOf("opr") > -1 && !!window.opr: return "Opera";
      case agent.indexOf("chrome") > -1 && !!window.chrome: return "Chrome";
      case agent.indexOf("trident") > -1: return "MS IE";
      case agent.indexOf("firefox") > -1: return "Mozilla Firefox";
      case agent.indexOf("safari") > -1: return "Safari";
      default: return "other";
    }
    })(window.navigator.userAgent.toLowerCase());

    this.frontend_props = {
      "domain": location.host,
    }

    const set_unreachable = () => {
      this.frontend_props = {
        "domain": location.host,
        "$os": navigator.platform,
        "$browser": browser,
        "$screen_height": screen.height,
        "$screen_width": screen.width,
      }
      this.unreachable_in_frontend = true;
    }

    if (typeof mixpanel === 'undefined' || !window._dca_mixpanel_enabled) {
      set_unreachable();
    } else {
      (async () => {
        try {
          const data = await fetch("https://api-js.mixpanel.com/track/", {method: "POST"})
          this.initialized = true;
          if (data.status !== 200) {
            set_unreachable();
          }
        } catch (e) {
          set_unreachable();
        }
      })()
    }
  },
  methods: {
    jupyter_track(event, props) {
      mixpanel.track(event, {...props, ...this.frontend_props});
    },
    jupyter_identify(unique_id) {
      mixpanel.identify(unique_id);
    }
  }
}
</script>

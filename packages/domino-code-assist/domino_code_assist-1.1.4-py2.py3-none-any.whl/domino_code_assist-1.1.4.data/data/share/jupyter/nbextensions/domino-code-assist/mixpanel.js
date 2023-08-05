const labConfigData = document.getElementById('jupyter-config-data');

function initMixpanel() {
    const base_url = labConfigData ? JSON.parse(labConfigData.textContent).baseUrl : document.body.dataset.baseUrl;
    const Jupyter_version = labConfigData ? JSON.parse(labConfigData.textContent).appVersion : Jupyter.version;

    (async () => {
        let mixpanelEnabled = false;
        try {
            const resp = await fetch(`/v4/auth/principal`);
            if (resp.status === 200) {
                const principal = await resp.json();
                mixpanelEnabled = principal && principal.mixpanelSettings && principal.mixpanelSettings.frontendClientEnabled;
            }
        } catch(e) {
            console.warn(e)
        }
        window._dca_mixpanel_enabled = mixpanelEnabled;
    if (typeof mixpanel === 'undefined' && mixpanelEnabled) {
        let project_token = 'a442c4dbf420b59cdac95cfb07f57cbb'
        if (['localhost', '127.0.', '0.0.0.0'].find(url => location.host.startsWith(url))
            || ['.dominodatalab.com', 'team-sandbox.domino.tech', 'eval.domino.tech', 'domino-eval.com', 'domino-pilot.com',
                'dominohackathon.com', 'dominodata.science', 'gurudomino.com', 'dominoai1.com'].find(url => location.host.endsWith(url))) {
            console.log("in test environment")
            project_token = '3aef1937b53691cfad358cbe583c0aa6'
        }
        window._dca_mixpanel_token = project_token;
        try {
            (function(f,b){if(!b.__SV){var e,g,i,h;window.mixpanel=b;b._i=[];b.init=function(e,f,c){function g(a,d){var b=d.split(".");2==b.length&&(a=a[b[0]],d=b[1]);a[d]=function(){a.push([d].concat(Array.prototype.slice.call(arguments,0)))}}var a=b;"undefined"!==typeof c?a=b[c]=[]:c="mixpanel";a.people=a.people||[];a.toString=function(a){var d="mixpanel";"mixpanel"!==c&&(d+="."+c);a||(d+=" (stub)");return d};a.people.toString=function(){return a.toString(1)+".people (stub)"};i="disable time_event track track_pageview track_links track_forms track_with_groups add_group set_group remove_group register register_once alias unregister identify name_tag set_config reset opt_in_tracking opt_out_tracking has_opted_in_tracking has_opted_out_tracking clear_opt_in_out_tracking start_batch_senders people.set people.set_once people.unset people.increment people.append people.union people.track_charge people.clear_charges people.delete_user people.remove".split(" ");
                for(h=0;h<i.length;h++)g(a,i[h]);var j="set set_once union unset remove delete".split(" ");a.get_group=function(){function b(c){d[c]=function(){call2_args=arguments;call2=[c].concat(Array.prototype.slice.call(call2_args,0));a.push([e,call2])}}for(var d={},e=["get_group"].concat(Array.prototype.slice.call(arguments,0)),c=0;c<j.length;c++)b(j[c]);return d};b._i.push([e,f,c])};b.__SV=1.2;e=f.createElement("script");e.type="text/javascript";e.async=!0;e.src="undefined"!==typeof MIXPANEL_CUSTOM_LIB_URL?
                MIXPANEL_CUSTOM_LIB_URL:"file:"===f.location.protocol&&"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js".match(/^\/\//)?"https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js":"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js";g=f.getElementsByTagName("script")[0];g.parentNode.insertBefore(e,g)}})(document,window.mixpanel||[]);

            mixpanel.init(project_token, {
                'property_blacklist': ['$current_url', '$referrer', '$initial_referrer'],
                'ignore_dnt' : true
            });

            const result = await fetch(`${base_url}mixpanel/`)
            const r = await result.json()
            const { id, LCA_version, Domino_version, event_name } = r
            mixpanel.identify(id)
            mixpanel.track(event_name, {
                LCA_version,
                Domino_version,
                jupyter: labConfigData ? 'lab' : 'notebook',
                Jupyter_version,
                LCA_language: 'python'
            })

        } catch (e) {
        }

        const set_unreachable = async () => {
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

            const matches = document.cookie.match('\\b_xsrf=([^;]*)\\b');
            const _xsrf = (matches && matches[1]) || '';

            const frontend_props = {
                "token": project_token,
                "domain": location.host,
                "$referring_domain": location.host,
                "$os": navigator.platform,
                "$browser": browser,
                "$screen_height": screen.height,
                "$screen_width": screen.width,
                jupyter: labConfigData ? 'lab' : 'notebook',
                Jupyter_version,
                LCA_language: 'python'
            }
            const result = await fetch(`${base_url}mixpanel/`, {
                method: 'POST',
                headers: {
                    'X-XSRFToken': _xsrf,
                    'content-type': 'application/json',
                },
                body: JSON.stringify(frontend_props)
            })
        }

        if (typeof mixpanel === 'undefined') {
            set_unreachable();
        } else {
            try {
                const data = await fetch("https://api-js.mixpanel.com/track/", {method: "POST"})
                if (data.status !== 200) {
                    set_unreachable();
                }
            } catch (e) {
                set_unreachable();
            }
        }
    }
    })();

}

if (labConfigData) {
    module.exports.initMixpanel = initMixpanel
} else {
    define([], () => initMixpanel)
}

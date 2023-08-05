<template>
    <div></div>
</template>

<script>
module.exports = {
    mounted() {
        if(this.dev) {
            this.mounted = true;
            sendLoop = () => {
                if(this.mounted) {
                    this.devSendClean();
                    setTimeout(sendLoop, 1000);
                }
            }
            setTimeout(() => {
                this.on_connected(true);
                setTimeout(sendLoop, 1000);
            }, 1000);
        } else {
            const protocol = location.protocol.replace('http', 'ws');
            const url = `${protocol}//${location.host}${this.server_path}`
            console.log("connecting to " + url);
            this.ws = new WebSocket(url);
            this.ws.onopen = (event) => {
                this.on_connected(true);
            };
            this.ws.onclose = (event) => {
                this.on_connected(false);
            };
            this.ws.onmessage = (event) => {
                this.on_message(JSON.parse(event.data));
            };
        }
    },
    destroyed() {
        if(this.dev) {
            console.log("destroyed")
            this.mounted = false;
        } else {
            this.ws.close();
        }
    },
    methods: {
        devSendClean() {
            let msg = {"type":"RunResourcesStatusChangedEvent","runId":"63a44822ab92a65b16f1473b","status":{"repositories":[{"name":"Domino Files","isUntrackedBranch":false,"status":{"Clean":{}},"mergeConflictsStatus":{"NoMergeConflictResolutionInProgress":{}}},{"name":"low-code-assistant-snippets","branchName":"main","isUntrackedBranch":false,"branchLink":"https://github.com/dominodatalab/low-code-assistant-snippets/tree/main","status":{"Unpushed":{"commitsAhead":0,"commitsBehind":8}},"mergeConflictsStatus":{"NoMergeConflictResolutionInProgress":{}}},{"name":"personal-lca-snippets","branchName":"main","isUntrackedBranch":false,"branchLink":"https://github.com/maartenbreddels-demo/lca-snippets/tree/main","status":{"Clean":{}},"mergeConflictsStatus":{"NoMergeConflictResolutionInProgress":{}}}]},"key":"run.resources.status","timestamp":1671806186232};
            console.log("Sending clean file system message")
            this.on_message(msg)
        },
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

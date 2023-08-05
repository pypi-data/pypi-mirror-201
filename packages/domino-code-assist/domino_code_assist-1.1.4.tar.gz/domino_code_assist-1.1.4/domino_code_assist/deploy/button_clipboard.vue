<template>
    <div>
        <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
                <v-tooltip v-model="show_clipboard_message" bottom>
                    <template v-slot:activator="{ on2, attrs2 }">
                        <v-btn color="primary" @click="copyText" class="ma-1" icon v-bind="attrs" v-on="{...on, ...on2}" :disabled="disabled">
                            <v-icon>mdi-content-copy</v-icon>
                        </v-btn>
                    </template>
                    <v-icon color="green" class="ma-1">mdi-check</v-icon>Copied to clipboard
                </v-tooltip>
            </template>
            Copy {{ url }} to clipboard
        </v-tooltip>
    </div>
</template>
<script>
modules.export = {
    computed: {
        url() {
            return `${location.host}${this.pathname}`
        }
    },
    methods: {
        copyText() {
            this.show_clipboard_message = true
            let text_to_copy = `${location.host}${this.pathname}`
            console.log("copying", text_to_copy)
            navigator.clipboard.writeText(text_to_copy)
            setTimeout(() => this.show_clipboard_message = false, 1000)
        }
    }
}

</script>

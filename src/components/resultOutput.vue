<template>
        <table>
            <tr v-for='(segment, index) in segments'>
                <td class="number">{{ index + 1 }}</td>
                <td v-html="segment.original"></td>
                <td class="warnings"><span title="It is recommended to use preposition 'та' if a sentence already contains preposition 'й\і!'" v-if="segment.warnings">/!\</span></td>
                <td v-html="segment.reviewed"></td>
                <td class="corrections">{{ segment.corrections }}</td>
            </tr>
        </table>
</template>

<script>
    import { eventBus } from '../main'
    export default {
        data () {
            return {
                segments: ''
            }
        },
        created () {
            eventBus.$on('textWasSubmitted', (txt) => {
                this.segments = JSON.parse(text.value)
            })
        }
    }
</script>

<style scoped>
    table {
        table-layout: auto;
    }

    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }

    th {
        background-color: #C71585;
        color: white
    }

    td {
        color: #000;
        padding: 5px;
    }

    .number, .warnings, .corrections {
        text-align: center;
    }
</style>
<template>
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <transition name="fade" mode="out-in">
                    <component :is="selectedComponent"></component>
                </transition>
            </div>
        </div>
    </div>
</template>

<script>
    import TextInput from './workpanel/textInput.vue';
    import ResultOutput from './workpanel/resultOutput.vue';

    export default {
        methods: {
            createNew() {
                this.$store.dispatch('createNew');
            }
        },
        computed: {
            selectedComponent() {
                return this.$store.getters.getComponent;
            }
        },
        components: {
            'text-input': TextInput,
            'result-output': ResultOutput
        }
    }
</script>

<style scoped>
    .container {
        margin-top: 100px;
        min-height: calc(100vh - 170px);
    }
    .fade-enter-active, .fade-leave-active {
        transition: opacity .5s ease;
    }
    .fade-enter, .fade-leave-to
        /* .component-fade-leave-active below version 2.1.8 */ {
        opacity: 0;
    }
</style>
<template>
  <div id="app">
      <app-header></app-header>
      <app-workpanel></app-workpanel>
      <app-footer></app-footer>
  </div>
</template>

<script>
    import Workpanel from './components/workpanel.vue';
    import Header from './components/header.vue';
    import Footer from './components/footer.vue';

    export default {
        name: 'app',
        computed: {
            selectedComponent() {
                return this.$store.getters.getComponent;
            }
        },
        components: {
            'app-header': Header,
            'app-workpanel': Workpanel,
            'app-footer': Footer
        }
    }
</script>

<style>
    .correct {
        background-color: #98FB98;
    }
    .wrong {
        background-color: #FF6347;
    }
</style>

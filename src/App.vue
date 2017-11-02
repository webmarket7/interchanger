<template>
  <div id="app">
      <div class="container">
          <main-menu></main-menu>
          <div class="row">
              <div class="col-md-12">
                  <transition name="fade" mode="out-in">
                      <component :is="selectedComponent"></component>
                  </transition>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
  import TextInput from './components/textInput.vue';
  import ResultOutput from './components/resultOutput.vue';
  import MainMenu from './components/mainMenu.vue';

  export default {
      name: 'app',
      computed: {
        selectedComponent() {
            return this.$store.getters.getComponent;
        }
      },
      components: {
          'text-input': TextInput,
          'result-output': ResultOutput,
          'main-menu': MainMenu
      }
  }
</script>

<style>

    #app {
        margin: 50px 0;
    }

    .correct {
        background-color: #98FB98;
    }

    .wrong {
        background-color: #FF6347;
    }

    .fade-enter-active, .fade-leave-active {
        transition: opacity .5s ease;
    }
    .fade-enter, .fade-leave-to
        /* .component-fade-leave-active below version 2.1.8 */ {
        opacity: 0;
    }


</style>

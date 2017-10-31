<template>
  <div id="app">
      <div class="wrapper">
          <main-menu></main-menu>
          <div class="container">
              <div class="row">
                  <div class="col-md-12">
                      <text-input></text-input>
                      <result-output></result-output>
                  </div>
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
    data () {
      return {

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

    .wrapper {
        margin: 50px 0;
    }

    .correct {
        background-color: #98FB98;
    }

    .wrong {
        background-color: #FF6347;
    }

</style>

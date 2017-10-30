<template>
  <div id="app">
      <div class="wrapper">
          <text-input></text-input>
          <result-output></result-output>
      </div>
  </div>
</template>

<script>
  import TextInput from './components/textInput.vue';
  import ResultOutput from './components/resultOutput.vue';
  export default {
    name: 'app',
    data () {
      return {

      }
    },
      components: {
        'text-input': TextInput,
        'result-output': ResultOutput
      }
  }
</script>

<style>
    .wrapper {
        display: block;
        width: 50%;
        margin: 2% auto;
    }
    .correct {
        background-color: #98FB98;
    }

    .wrong {
        background-color: #FF6347;
    }
</style>

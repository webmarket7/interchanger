<template>
    <form v-if="isSubmitted">
        <div class="form-group">
                <textarea name="text" id="text" rows="20" placeholder="Please input text here…" v-model.lazy="text"></textarea>
                <div class="cpanel">
                    <button class="btn btn-success button" @click.prevent="submitted">Submit</button>
                    <button type="reset" class="btn btn-warning button">Clear</button>
                </div>
        </div>
        <p>{{ text }}</p>
    </form>
</template>

<script>
    import { eventBus } from '../main';

    export default {
        data: function() {
            return {
                isSubmitted: true,
                text: ''
            }
        },
        methods: {
            submitted: function () {
                this.isSubmitted = false;
                eventBus.$emit('textWasSubmitted', this.text)
            }
        }
    }
</script>

<style scoped>
    textarea {
        display: block;
        width: 100%;
        resize: none;
        padding: 10px;
        margin-bottom: 20px;
    }
    .cpanel {
        display: block;
        width: 50%;
        margin: 0 auto;
    }
    .button {
        width: 48%;
    }

</style>
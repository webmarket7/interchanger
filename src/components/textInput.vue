<template>
        <form>
            <div class="form-group" v-if="isDisplayed">
                <textarea name="text" id="text" rows="20" placeholder="Please input text here…" v-model.lazy="text"></textarea>
                <div class="cpanel">
                    <button class="btn btn-primary button" @click.prevent="submitted">Submit</button>
                    <button type="reset" class="btn btn-warning button">Clear</button>
                </div>
            </div>
        </form>
</template>

<script>
    import { eventBus } from '../main';

    export default {
        data: function() {
            return {
                isDisplayed: true,
                text: ''
            }
        },
        methods: {
            submitted: function () {
                this.isDisplayed = false;
                eventBus.$emit('textWasSubmitted', this.text);
                text = ''
            }
        },
        created() {
            eventBus.$on('newDocument', (isCreated) => {
                this.isDisplayed = true;
            });
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
        height: 50px;
        min-width: 70px;
    }

</style>
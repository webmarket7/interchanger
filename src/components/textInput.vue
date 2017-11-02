<template>
        <form>
            <div class="form-group">
                <textarea name="text" id="text" rows="20" placeholder="Please input text here…" v-model.lazy="text"></textarea>
                <div class="cpanel">
                    <button class="btn btn-primary button" @click.prevent="check(text)">Check</button>
                    <button type="reset" class="btn btn-warning button">Clear</button>
                </div>
            </div>
        </form>
</template>

<script>
    export default {
        data: function() {
            return {
                isDisplayed: true,
                text: ''
            }
        },
        methods: {
            check(text) {
                this.$store.dispatch('check', text)
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
        height: 50px;
        min-width: 70px;
    }

</style>
<template>
        <form>
            <div class="form-group flex-container">
                <div class="edge left-edge"></div>
                <textarea class="flex-element"
                        name="text"
                        id="text"
                        rows="25"
                        placeholder="Please input text here…"
                        v-model.lazy="text"></textarea>
                <div class="edge right-edge">
                    <menu class="flex-container">
                        <button type="submit"
                                title="Check for interchanges"
                                @click.prevent="check(text)">
                            <img src="../../assets/check-button.png"
                                 alt="Check">
                        </button>
                        <button type="reset"
                                title="Clear">
                            <img src="../../assets/clear-button.png"
                                 alt="Check">
                        </button>
                    </menu>
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
                if (text.length > 0) {
                    this.$store.dispatch('check', text)
                }
                else {
                    alert('Error! No text was entered!')
                }
            }
        }
    }
</script>

<style scoped>
    .flex-container {
        display: flex;
    }

    .flex-element {
        flex-grow: 1;
    }

    .edge {
        width: 75px;
        border: 1px solid;
        background-color: #d9edf7;
    }

    .left-edge {
        border-right: none;
        border-top-left-radius: 20px;
        border-bottom-left-radius: 20px;
    }

    textarea {
        resize: none;
        padding: 15px;
        border-top: 1px solid black;
        border-bottom: 1px solid black;
    }

    textarea:focus {
        outline: none;
    }

    .right-edge {
        border-left: none;
        border-top-right-radius: 20px;
        border-bottom-right-radius: 20px;
    }

    menu {
        justify-content: flex-start;
        flex-direction: column;
        margin: 0;
        padding: 15px 10px;
    }

    menu button {
        border: 0;
        background: transparent;
        margin-bottom: 5px;
        width: 60px;
        height: 50px;
    }

    menu button:focus {
        outline: none;
    }

     menu button img {
        width: 45px;
        height: 45px;
    }

</style>
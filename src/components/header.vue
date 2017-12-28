<template>
    <div class="header fixed">
        <div class="container">
            <div class="row">
                <div class="col-md-5"></div>
                <div class="col-md-2 flex-container">
                    <div class="flex-element menu-option">
                        <img src="../assets/add_new.png"
                             alt="Add new"
                             @click="createNew">
                    </div>
                    <div class="flex-element">
                        <img class="logo"
                             src="../assets/logo.png"
                             alt="Logo">
                    </div>
                    <div class="flex-element menu-option">
                        <img src="../assets/settings.png"
                             alt="Settings">
                    </div>
                </div>
                <div class="col-md-5"></div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        methods: {
            createNew() {
                this.$store.dispatch('createNew');
            }
        }
    }
</script>

<style scoped>
    .header {
        width: 100%;
        height: 56px;
        border-bottom: 1px solid black;
        background-color: #f3f3f4;
    }
    .fixed {
        position: fixed;
        top:0;
        left:0;
        z-index:10;
    }
    .flex-container {
        display: flex;
        justify-content: center;
    }
    .flex-element {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 56px;
        height: 55px;
    }
    .menu-option {
        border-right: 1px solid #bbbbc0;
        border-left: 1px solid #bbbbc0;
    }
    .menu-option img {
        cursor: pointer;
        height: 35px;
    }
</style>
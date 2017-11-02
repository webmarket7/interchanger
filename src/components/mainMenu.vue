<template>
    <div class="row">
        <div class="col-md-4">
            <img src="../assets/logo.png" alt="Logo">
        </div>
        <div class="col-md-6"></div>
        <div class="col-md-2">
            <menu>
                <img src="../assets/add_new.png" alt="Add new" @click="createNew">
                <img src="../assets/settings.png" alt="Settings">
            </menu>
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

    .container {
        margin-bottom: 20px;
    }

    menu {
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
    }

    img {
        margin: 0 0 0 15px;
        cursor: pointer;
    }

</style>
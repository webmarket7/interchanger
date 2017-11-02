<template>
    <div class="footer">
        <div class="container">
            <div class="row">
                <div class="col-md-4"></div>
                 <div class="col-md-4">
                    <div class="flex-container">
                        <p>© Oleksanr Ryzhyk, 2017</p>
                        <p>All rights reserved</p>
                    </div>
                </div>
                <div class="col-md-4"></div>
            </div>
        </div>
    </div>
</template>



<style scoped>

    .flex-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 70px;
        font-weight: bold;
    }

    .footer {
        width: 100%;
        border-top: 1px solid black;
        background-color: #f3f3f4;
        height: 70px;
        bottom: 0;
    }
</style>
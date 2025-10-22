<div class="cams">
    <div class="camWrapper">
        <img src="img\placeHolder.jpg" alt="">
        <button> Activate </button>
    </div>

    <div class="camWrapper">
        <img src="img\placeHolder.jpg" alt="">
        <button> Activate </button>
    </div>
</div>

<style>

    img {
        display: flex;
        border-radius: 5px;
    }

    .camWrapper {
        background-color: var(--foregroundColor);
        scale: 80%;
        border-radius: 5px;
        box-shadow: 5px 5px 5px 5px rgba(0, 0, 0, 0.2);
        border: solid 1px;
        border-color: var(--foregroundColor);

        padding: 10px;


        transition: 0.5s;
    }

    .camWrapper:hover {
        border-color: var(--borderColor);
    }
    
    button {
        display: flex;
        margin-left: auto; margin-right: auto;
    }

</style>
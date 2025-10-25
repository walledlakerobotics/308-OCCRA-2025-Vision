<div class="cams">
    <div class="camWrapper">
        <img src="img\placeHolder.jpg" alt="">
        <p>Name Cam</p>
        <button> Activate </button>
    </div>

    <div class="camWrapper">
        <img src="img\placeHolder.jpg" alt="">
        <p>Name Cam</p>
        <button> Activate </button>
    </div>

    <div class="camWrapper">
        <img src="img\placeHolder.jpg" alt="">
        <p>Name Cam</p>
        <button> Activate </button>
    </div>

    <div class="camWrapper">
        <img src="img\placeHolder.jpg" alt="">
        <p>Name Cam</p>
        <button> Activate </button>
    </div>
</div>

<style>

    
    
    img {
        border-radius: 5px;

        width: 95%;
        height: auto;

        margin-top: 5px;


    }

    p {
        scale: 120%;
        padding: 5px;
    }

    .cams {
        padding: 1rem;
        display: grid;
        gap: 15px;
        grid-template-columns: repeat(auto-fit, minmax(20rem, 0.9fr));
    }

    .camWrapper {
        background-color: var(--foregroundColor);
        display: flex;

        flex-direction: column;
        align-items: center;

        border-radius: 10px;
        border: solid 2px;
        border-color: var(--borderColor);
        box-shadow: 0 0 5px 2.5px var(--borderGlow);

        padding: 20px;
        transition: 0.5s;
    }



    
    button {
        background-color: var(--buttonColor);

        border: solid;
        border-color: var(--borderColorUnhover);
        border-width: 1.5px;
        border-radius: 5px;

        margin-top: 5px;
        margin-bottom: 5px;

        width: 100%;
        padding: 10px;

        color: var(--borderColorUnhover);

        transition: 0.5s;
    }

    button:hover {
        border-color: var(--borderColor);
        color: var(--borderColor);
    }

    button:active {
        border-color: var(--activeButton);
        color: var(--activeButton);
    }
</style>

<script lang="ts">

</script>
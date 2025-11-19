

<script lang="ts">
    import placeholder from "./img/placeHolder.jpg"

    var cameras = 
    [
        // this will auto detect the cameras 
        
    ]
</script>

<div class="veiws">
    <img src={placeholder} alt="">
    <img src={placeholder} alt="">
</div>

<div class="camList">

    <select name="options" id=""> 
        <!-- This is where all the cameras go -->
        <option value="camera 121"> ;3</option>
        <option value="camera 128">;3</option>

    </select> 
</div>




<style>


    img {
        border: 2px solid var(--borderColor);
        border-radius: 5px;
    }
    .camList {
        background-color: rgb(15, 13, 34);
        
        overflow: hidden;

        

        /* margin-top: 1rem; */
    }

    .veiws {


        background-color: var(--foregroundColor);

        padding: 20px;

        justify-content: center;
        gap: 20px;
        display: flex;
        flex-direction: row;
        padding: 1rem;
        
    }

    select {
        color: var(--borderColor);

        background-color: var(--droupDownMenuColor);
        display: flex;

        margin-bottom: 1rem;
        margin-top: 1rem;
        margin-left: auto; margin-right: auto;

        border-radius: 5px;
        border: solid var(--borderColor) 1.5px;
        
        
        padding-bottom: 5px; padding-top: 5px;
        padding-left: 25rem; padding-right: 25rem;

        border-width: 1.5px;
        border: none;
        border-color: var(--borderColor);
        

        transition: 0.1s;
        
    }

    
</style>
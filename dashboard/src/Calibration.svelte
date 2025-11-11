<script lang="ts">

</script>

<div class="cameraContainer">
    <img src="img/placeHolder.jpg" alt="">
</div>

<div class="propertieSettings">

</div>

<select name="Camera" id="">
    <option value="camera 121"> ;3</option>
</select>


<style>
    select {
        color: var(--borderColor);

        background-color: var(--foregroundColor);
        display: flex;
        position: absolute;

        margin-bottom: 1rem;
        margin-top: 1rem;
        margin-left: auto; margin-right: auto;

        border-radius: 5px;
        border: solid var(--borderColor) 1.5px;
        
        
        padding-bottom: 5px; padding-top: 5px;
        padding-left: 15rem; padding-right: 15rem;

        border-width: 1.5px;
        border: none;
        border-color: var(--borderColor);
        

        transition: 0.1s;
        
    }

    img {
        border-radius: 5px;

        width: 45%;
        height: auto;

        margin-top: 5px;


    }

    .cameraContainer {
        justify-content: center;
        gap: 20px;
        display: flex;
        flex-direction: row;
        padding: 1rem;
        

    }
    .propertieSettings {

    }
</style>
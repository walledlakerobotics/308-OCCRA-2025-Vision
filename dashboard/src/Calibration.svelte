<script lang="ts">
    import placeholder from "./img/placeHolder.jpg";
</script>

<div class="cameraContainer">
    <img src="{placeholder}" alt="">
</div>

<div class="propertieSettings">
    <select name="CameraList">
        <option value="camera 121"> ;3</option>
    </select>
</div>

<style>
    .propertieSettings {
        background-color: var(--foregroundColor);


        height: 100%;
        padding: 10px;

        margin: 0%;
        display: flex;
    }

    .cameraContainer  {
        background-color: var(--foregroundColor);

        position: fixed;
        border-radius: 5px;

        margin: auto;

        padding: 15px;

        border: solid 2px;

        border-color: var(--borderColor);
        box-shadow: 0 0 5px 2.5px var(--borderGlow);

        justify-content: center;
        display: flex;
        

    }

    select {
        color: var(--borderColor);
        background-color: rgb(11, 1, 28);
        margin-left: auto; margin-right: auto;

        border-radius: 5px;
        border: solid var(--borderColor) 1.5px;
        
        
        padding-bottom: 5px; padding-top: 5px;
        padding-left: 5rem; padding-right: 5rem;

        border-width: 1.5px;
        border: none;
        border-color: var(--borderColor);
        

        transition: 0.1s;
        
    }

    img {
        border-radius: 5px;

    }

    
</style>
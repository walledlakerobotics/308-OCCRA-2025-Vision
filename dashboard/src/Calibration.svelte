    <script lang="ts">
        import placeholder from "./img/placeHolder.jpg";
    </script>

    <div class="cameraContainer">
        <div class="camImage">
            <img src="{placeholder}" alt="">
        </div>
    </div>

    <div class="propertieSettings">
        <select name="CameraList">
            <option value="camera 121"> ;3</option>
        </select>
    </div>

    <style>
        .propertieSettings {
            background-color: var(--foregroundColor);

        padding: 10px;

            height: 100%;
            padding: 10px;

            margin: 0%;
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

        .cameraContainer {
            display: flex;
        }

        .camImage {
            /* position: fixed; */
            margin-left: auto;
            margin-right: auto;
        }

        
    </style>
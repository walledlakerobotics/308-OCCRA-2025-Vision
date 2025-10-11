

<script lang="ts">
    var cameras = 
    [
        // this will auto detect the cameras 
        
    ]
</script>


<div class="veiws">
    <img src="img/placeHolder.jpg" alt="">
    <img src="img/placeHolder.jpg" alt="">
</div>

<div class="navbar">
    <nav>
        <select name="options" id=""> 
            <!-- This is where all the cameras go -->
            <option value="camera 121"> ;3</option>
            <option value="camera 128">;3</option>

        </select> 
    </nav>
</div>


<style>
    img {
        border-radius: 5px;
        box-shadow: 5px 5px 5px 5px rgba(0, 0, 0, 0.2);
    }


    .veiws {
        justify-content: center;
        gap: 5px;
        display: flex;
        flex-direction: row;
    }

    select {
        color: var(--borderColor);
        background-color: var(--foregroundColor);
        display: flex;

        margin-top: 1rem;
        margin-left: auto; margin-right: auto;

        border-radius: 5px;
        
        
        padding-bottom: 5px; padding-top: 5px;
        padding-left: 25rem; padding-right: 25rem;

        border-width: 1.5px;
        border: none;
        border-color: var(--borderColor);
        

        transition: 0.1s;
        
    }

    option {

    }

    
</style>
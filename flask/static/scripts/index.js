function show_hide_inputs() {
    let inputs = document.getElementById("devices");
    let inputs_button = document.getElementById("show_hide_inputs");
    if (inputs.style.display === "none") {
        inputs.style.display = "block";
        inputs_button.innerHTML = "Cacher le menu 'périphériques'";

    } else {
        inputs.style.display = "none";
        inputs_button.innerHTML = "Afficher le menu 'périphériques'";
    }
}

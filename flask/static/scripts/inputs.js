// Check that the browser has the Gamepad API
const hasGamepadAPI = () => "getGamepads" in navigator;
console.log(`Has gamepad API: ${hasGamepadAPI()}`)


// If a controller is connected, gamepadIndex takes the value 
// of the port where the controller is connected
// else gamepadIndex is undefined
let gamepadIndex;
window.addEventListener('gamepadconnected', (event) => {
	gamepadIndex = event.gamepad.index;
});


function select_device(device) {
    ` Selects the device to use for the game controller.

    Args:
        device (str): The device to use. Either 'keyboard' or 'controller'. `

    // Retrieves the images of the controller and keyboard image
    let header_controller = document.getElementById("header_controller");
    let header_keyboard = document.getElementById("header_keyboard");

    // If no controller is connected and the user has selected it
    if (gamepadIndex === undefined && device === 'controller') {
        window.alert("Aucune manette n'est connectée. Veuillez connecter une manette et réessayer.");
        return;
    }

    // Starting of the animation of devices div
    document.getElementById("devices").classList.add("animation");

    // If the user chooses the controller
    if (device === 'controller') {
        setInterval(() => {
            // A controller is connected and has an index
            if(gamepadIndex !== undefined) {
                // Get the currently connected controller
                const controller = navigator.getGamepads()[gamepadIndex];

                // Create a list containing all inputs
                let result = [];

                if (controller.buttons[0].pressed) {
                    result.push("reculer");
                } if (controller.buttons[1].pressed) {
                    result.push("droite");
                } if (controller.buttons[2].pressed) {
                    result.push("gauche");
                } if (controller.buttons[3].pressed) {
                    result.push("avancer");
                }
                // Send request to the Python file if there is an input
                if (result.length != 0) {
                    fetch('/my_route', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(result)
                        })
                        .then(response => response.json())
                        .then(data => console.log(data))
                        .catch(error => console.error(error));
                    console.log(result);
                }
            }
        }, 100) // 100ms = 10Hz

        console.log('Controller selected');
        header_controller.style.backgroundColor = "#424558"
        header_keyboard.style.backgroundColor = ""
    } 
    // If the user chooses the keyboard
    else if (device === 'keyboard') {
        console.log('Keyboard selected');
        header_keyboard.style.backgroundColor = "#424558"
        header_controller.style.backgroundColor = ""


        let result = "";
        // Event listener for each keydown
        document.addEventListener('keydown', function(event) {
            if (event.repeat) {return}
            console.log(event.key);
            // Create a list containing all inputs

            if (event.key === "ArrowUp") {
                result = "avancer";
            } if (event.key === "ArrowLeft") {
                result = "gauche"
            } if (event.key === "ArrowDown") {
                result ="reculer";
            } if (event.key === "ArrowRight") {
                result = "droite";
            }
            // Send request to the Python file if there is an input
            fetch('http://10.229.253.46:2005', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(result)
                })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error(error));
        });

        // Event listener for each keyup
        document.addEventListener("keyup", function(event) {
            if (event.repeat) {return}
            console.log(event.key)
            if (event.key === "ArrowUp") {
                result = "stop_avancer";
            } if (event.key === "ArrowLeft") {
                result = "stop_gauche";
            } if (event.key === "ArrowDown") {
                result = "stop_reculer";
            } if (event.key === "ArrowRight") {
                result = "stop_droite";
            }

            // Send request to the Python file if there is an input
            fetch('http://10.229.253.46:2005', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(result)
                })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error(error));
        });
        
    }
}
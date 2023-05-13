// Check that the browser has the Gamepad API
const hasGamepadAPI = () => "getGamepads" in navigator;
console.log(`Has gamepad API: ${hasGamepadAPI()}`)


//Gamepad Object
let gamepadIndex;
window.addEventListener('gamepadconnected', (event) => {
	gamepadIndex = event.gamepad.index;
});


// Read Controller Inputs
function read_controller_inputs(controller, leftStick=false, rightStick=false, backside=false, start_back=false, dPad=false, buttons=false) {
    ` Reads the input from the game controller and returns the requested buttons/triggers.

    Args:
        controller (Gamepad): The game controller object.
        leftStick (bool): Whether to include data for the left joystick.
        rightStick (bool): Whether to include data for the right joystick.
        backside (bool): Whether to include data for the backside buttons/triggers.
        start_back (bool): Whether to include data for the start and back buttons.
        dPad (bool): Whether to include data for the D-pad.
        buttons (bool): Whether to include data for the A, B, X, and Y buttons.

    Returns:
        dict: A dictionary containing the requested buttons/triggers, with keys for each button/trigger 
        and values being their corresponding values from the game controller. If a requested button/trigger 
        was not included, its corresponding value will be None.`

    let result = [];

    if (controller.buttons[0].pressed) {
        result.push("reculer");
    }
    if (controller.buttons[1].pressed) {
        result.push("gauche");
    }
    if (controller.buttons[2].pressed) {
        result.push("avancer");
    }
    if (controller.buttons[0].pressed) {
        result.push("droite");
    }

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
    }
    

    /*
    if (leftStick) {
        result['leftStick'] = {"x": controller.axes[0], "y": controller.axes[1], "thumb": controller.buttons[10].pressed};
    } 
    if (rightStick) {
        result['rightStick'] = {"x": controller.axes[2] , "y": controller.axes[3], "thumb": controller.buttons[11].pressed};
    }
    if (backside) {
        result['backside'] = {"leftBumper": controller.buttons[4].pressed, "rightBumper": controller.buttons[5].pressed, "leftTrigger": controller.buttons[6].pressed, "rightTrigger": controller.buttons[7].pressed};
    }
    if (start_back) {
        result['start_back'] = {"back": controller.buttons[8].pressed, "start": controller.buttons[9].pressed};
    }
    if (dPad) {
        result['dPad'] = {"left": controller.buttons[13].pressed, "right": controller.buttons[14].pressed, "up": controller.buttons[12].pressed, "down": controller.buttons[15].pressed};
    }
    if (buttons) {
        result['buttons'] = {"A": controller.buttons[0].pressed, "B": controller.buttons[1].pressed, "X": controller.buttons[2].pressed, "Y": controller.buttons[3].pressed};
    }*/


    return result;

}




function select_device(device) {
    ` Selects the device to use for the game controller.

    Args:
        device (str): The device to use. Either 'keyboard' or 'controller'. `

    
    let header_controller = document.getElementById("header_controller");
    let header_keyboard = document.getElementById("header_keyboard");

    if (gamepadIndex === undefined && device === 'controller') {
        window.alert("Aucune manette n'est connectée. Veuillez connecter une manette et réessayer.");
        return;
    }

    document.getElementById("devices").classList.add("animation");
    
    
    
    


    if (device === 'controller') {
        // Exevute the read_controller_inputs function every 100ms if a controller is connected
        setInterval(() => {
            if(gamepadIndex !== undefined) {
                // A controller is connected and has an index
                const controller = navigator.getGamepads()[gamepadIndex];
                //controller_inputs = read_controller_inputs(controller=myGamepad, leftStick=true, rightStick=false, backside=true, start_back=false, dPad=false, buttons=true);
                
                
                
                let result = [];

                if (controller.buttons[0].pressed) {
                    result.push("reculer");
                }
                if (controller.buttons[1].pressed) {
                    result.push("droite");
                }
                if (controller.buttons[2].pressed) {
                    result.push("gauche");
                }
                if (controller.buttons[3].pressed) {
                    result.push("avancer");
                }

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

    } else if (device === 'keyboard') {
        console.log('Keyboard selected');
        header_keyboard.style.backgroundColor = "#424558"
        header_controller.style.backgroundColor = ""
        

        document.addEventListener('keydown', function(event) {
            console.log(event.key);
            result = [];
            if (event.key === "ArrowUp") {
                result.push("avancer");
            }
            if (event.key === "ArrowLeft") {
                result.push("gauche");
            }
            if (event.key === "ArrowDown") {
                result.push("reculer");
            }
            if (event.key === "ArrowRight") {
                result.push("droite");
            }
            

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
                
        });

    }
}
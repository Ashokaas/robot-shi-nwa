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
        leftStick (bool): Whether to include data for the left joystick.
        rightStick (bool): Whether to include data for the right joystick.
        backside (bool): Whether to include data for the backside buttons/triggers.
        start_back (bool): Whether to include data for the start and back buttons.
        dPad (bool): Whether to include data for the D-pad.
        buttons (bool): Whether to include data for the A, B, X, and Y buttons.

    Returns:
        dict: A dictionary containing the requested buttons/triggers, with keys for each button/trigger 
        and values being their corresponding values from the game controller. If a requested button/trigger 
        was not included, its corresponding value will be None. `

    let result = {};

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
    }
    return result;

}

// Exevute the read_controller_inputs function every 100ms if a controller is connected
setInterval(() => {
	if(gamepadIndex !== undefined) {
		// A controller is connected and has an index
		const myGamepad = navigator.getGamepads()[gamepadIndex];
        controller_inputs = read_controller_inputs(controller=myGamepad, leftStick=true, rightStick=false, backside=true, start_back=false, dPad=false, buttons=true);
        console.log(controller_inputs);
	}
}, 100) // 100ms = 10Hz

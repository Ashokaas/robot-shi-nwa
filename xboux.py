import inputs
import math
import threading

# This class is used to read the inputs from an Xbox controller
class XboxController():
    # Constants for the controller inputs (these are the max values for each input) allowing to normalize the values between 0 and 1
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self, rounding:int=0):
        #Select the rounding used for the joysticks and the pressure of the triggers
        self.rounding = rounding
        
        # Joysticks
            # Left Joystick
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
            # Right Joystick
        self.RightJoystickY = 0
        self.RightJoystickX = 0
            # Thumbsticks
        self.LeftThumb = 0
        self.RightThumb = 0
        
        # Backside
            # Triggers
        self.LeftTrigger = 0
        self.RightTrigger = 0
            # Bumpers
        self.LeftBumper = 0
        self.RightBumper = 0
        
        # Buttons
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        
        # Start/Back
        self.Back = 0
        self.Start = 0
        
        # D-pad
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self, leftStick=False, rightStick=False, backside=False, start_back=False, dPad=False, buttons=False):
        """ Reads the input from the game controller and returns the requested buttons/triggers.

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
            was not included, its corresponding value will be None.
        """
        result = {}
        
        if leftStick:
            result['leftStick'] = {"x": self.LeftJoystickX, "y": self.LeftJoystickY, "thumb": self.LeftThumb}
            
        if rightStick:
            result['rightStick'] = {"x": self.RightJoystickX, "y": self.RightJoystickY, "thumb": self.RightThumb}
        
        if backside:
            result['backside'] = {"leftBumper": self.LeftBumper, "rightBumper": self.RightBumper, "leftTrigger": self.LeftTrigger, "rightTrigger": self.RightTrigger}
        
        if start_back:
            result['start_back'] = {"back": self.Back, "start": self.Start}
        
        if dPad:
            result['dPad'] = {"left": self.LeftDPad, "right": self.RightDPad, "up": self.UpDPad, "down": self.DownDPad}
        
        if buttons:
            result['buttons'] = {"A": self.A, "B": self.B, "X": self.X, "Y": self.Y}
            
        return result


    def _monitor_controller(self):
        while True:
            events = inputs.get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = round(event.state / XboxController.MAX_JOY_VAL, self.rounding) 
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = round(event.state / XboxController.MAX_JOY_VAL, self.rounding)
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = round(event.state / XboxController.MAX_JOY_VAL, self.rounding)
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = round(event.state / XboxController.MAX_JOY_VAL, self.rounding)
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = round(event.state / XboxController.MAX_TRIG_VAL, self.rounding)
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = round(event.state / XboxController.MAX_TRIG_VAL, self.rounding)
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state
                elif event.code == 'BTN_WEST':
                    self.X = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state



if __name__ == '__main__':
    joy = XboxController(rounding=1)
    while True:
        print(joy.read(buttons=True, leftStick=True))




from gpiozero import AngularServo
import time

class servomotor:
    
    def __init__(self, pin = 18, position = 0, 
                 min_angle = -90, max_angle = 90, 
                 min_pulse_width = 0.0005, max_pulse_width = 0.0025):
        self.position = position
        self.start_pos = position
        self.min_angle = min_angle
        self.max_angle = max_angle
        
        self.motor = AngularServo(pin, initial_angle=position, 
                                    min_angle=min_angle, max_angle=max_angle, 
                                    min_pulse_width=min_pulse_width, 
                                    max_pulse_width=max_pulse_width)
        
    def setDirection(self, set_pos, speed = 5):
        """
        moves servomotor to a specified position with a specified speed
        
        :param set_pos: set_pos (-90 to 90 / right to left)
        :param speed: speed (1 to 5 / slow to fast)
        """
        # catch values out of the intervall
        set_pos = max(self.min_angle, min(set_pos, self.max_angle))
        speed = max(1, min(speed, 5))

        # map speed to motion profile
        step_deg = {1: 1.0, 2: 2.0, 3: 3.0, 4: 5.0, 5: 8.0}[speed]
        delay_s  = {1: 0.03, 2: 0.02, 3: 0.015, 4: 0.01, 5: 0.008}[speed]

        # define direction
        direction = 1 if set_pos > self.position else -1
        # setup cariable with current position
        current_position = self.position

        # turn from current position to set_pos with a certain speed      
        while True:
            # check if servo is in right position or overshooted then end loop
            if (direction == 1 and self.position >= set_pos) or (direction == -1 and self.position <= set_pos):
                break
            # calculate next angular step
            current_position += direction * step_deg

            # check if servo would overshoot target
            if direction == 1: current_position = min(current_position, set_pos)
            else: current_position = max(current_position, set_pos)

            # set servo to calculated position
            self.motor.angle = current_position
            self.position = current_position

            # delay to controll speed of turning
            time.sleep(delay_s)
        # ensure that position of servo is right
        self.motor.angle = set_pos
        self.position = set_pos
    

    def setPosition(self, pos):
        """
        set angular position of servomotor
        
        :param pos: angle to which the servomotor moves min = -90 and max = 90
        """
        self.motor.angle = pos
        self.position = pos

    def setHome(self):
        """
        set servo back to start position
        """
        self.setDirection(self.start_pos)
        
    def getPosition(self):
        """
        returns the position of the servomotor
        """
        return self.position
    
    def end(self):
        """
        moves servo to start position, stops PWM communication and cleans up
        """
        self.setHome()
        self.motor.close()
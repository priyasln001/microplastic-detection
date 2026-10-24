import time
import logging

logger = logging.getLogger(__name__)

# Check if we are on a Raspberry Pi
try:
    import RPi.GPIO as GPIO
    from picamera import PiCamera # Note: Newer RPi uses libcamera
    RASPBERRY_PI = True
except (ImportError, RuntimeError):
    RASPBERRY_PI = False
    logger.warning("Not running on a Raspberry Pi. Hardware features will be simulated.")

class HardwareController:
    def __init__(self, uv_pin=17, white_pin=27, ir_pin=22):
        self.uv_pin = uv_pin
        self.white_pin = white_pin
        self.ir_pin = ir_pin
        
        if RASPBERRY_PI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.uv_pin, GPIO.OUT)
            GPIO.setup(self.white_pin, GPIO.OUT)
            GPIO.setup(self.ir_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
            # Initial state: Lights Off
            GPIO.output(self.uv_pin, GPIO.LOW)
            GPIO.output(self.white_pin, GPIO.LOW)
            self.camera = PiCamera()
        else:
            self.camera = None

    def set_lighting(self, mode):
        """
        Set lighting mode: 'uv', 'white', or 'off'
        """
        if RASPBERRY_PI:
            if mode == 'uv':
                GPIO.output(self.uv_pin, GPIO.HIGH)
                GPIO.output(self.white_pin, GPIO.LOW)
            elif mode == 'white':
                GPIO.output(self.uv_pin, GPIO.LOW)
                GPIO.output(self.white_pin, GPIO.HIGH)
            else:
                GPIO.output(self.uv_pin, GPIO.LOW)
                GPIO.output(self.white_pin, GPIO.LOW)
        else:
            logger.info(f"SIMULATED: Lighting set to {mode}")

    def capture_image(self, filename='capture.jpg'):
        """
        Capture image from Pi Camera or fallback to OpenCV for USB webcams.
        """
        if RASPBERRY_PI:
            self.camera.capture(filename)
            logger.info(f"Image captured to {filename}")
            return filename
        else:
            import cv2
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(filename, frame)
                cap.release()
                return filename
            cap.release()
            return None

    def wait_for_ir_trigger(self, timeout=None):
        """
        Wait until IR sensor is triggered (Solid Waste mode).
        """
        if RASPBERRY_PI:
            logger.info("Waiting for IR sensor trigger...")
            triggered = GPIO.wait_for_edge(self.ir_pin, GPIO.FALLING, timeout=timeout)
            return triggered is not None
        else:
            time.sleep(2) # Simulate delay
            logger.info("SIMULATED: IR Sensor Triggered!")
            return True

    def cleanup(self):
        if RASPBERRY_PI:
            GPIO.cleanup()
            self.camera.close()

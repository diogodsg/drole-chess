import RPi.GPIO as GPIO
from threading import Thread
import time


class DisplayModule:
    def __init__(self):
        # GPIO to LCD mapping
        self.LCD_RS = 7
        self.LCD_E = 8
        self.LCD_D4 = 25
        self.LCD_D5 = 24
        self.LCD_D6 = 23
        self.LCD_D7 = 18

        # Constants
        self.LCD_CHR = True  # Character mode
        self.LCD_CMD = False  # Command mode
        self.LCD_CHARS = 16  # Characters per line (16 max)
        self.LCD_LINE_1 = 0x80  # LCD memory location for 1st line
        self.LCD_LINE_2 = 0xC0  # LCD memory location 2nd line

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LCD_E, GPIO.OUT)  # Set GPIO's to output mode
        GPIO.setup(self.LCD_RS, GPIO.OUT)
        GPIO.setup(self.LCD_D4, GPIO.OUT)
        GPIO.setup(self.LCD_D5, GPIO.OUT)
        GPIO.setup(self.LCD_D6, GPIO.OUT)
        GPIO.setup(self.LCD_D7, GPIO.OUT)

        # Initialize display
        self.lcd_init()

        self.top_text = ""
        self.bottom_text = ""

        self.top_display_text = ""
        self.bottom_display_text = ""

        self.top_pos = 0
        self.top_pos_max = 0

        self.bottom_pos = 0
        self.bottom_pos_max = 0

        self.running = False

    def lcd_init(self):
        self.lcd_write(0x33, self.LCD_CMD)  # Initialize
        self.lcd_write(0x32, self.LCD_CMD)  # Set to 4-bit mode
        self.lcd_write(0x06, self.LCD_CMD)  # Cursor move direction
        self.lcd_write(0x0C, self.LCD_CMD)  # Turn cursor off
        self.lcd_write(0x28, self.LCD_CMD)  # 2 line display
        self.lcd_write(0x01, self.LCD_CMD)  # Clear display
        time.sleep(0.0005)  # Delay to allow commands to process

    def lcd_write(self, bits, mode):
        # High bits
        GPIO.setmode(GPIO.BCM)
        GPIO.output(self.LCD_RS, mode)  # RS

        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits & 0x10 == 0x10:
            GPIO.output(self.LCD_D4, True)
        if bits & 0x20 == 0x20:
            GPIO.output(self.LCD_D5, True)
        if bits & 0x40 == 0x40:
            GPIO.output(self.LCD_D6, True)
        if bits & 0x80 == 0x80:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

        # Low bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits & 0x01 == 0x01:
            GPIO.output(self.LCD_D4, True)
        if bits & 0x02 == 0x02:
            GPIO.output(self.LCD_D5, True)
        if bits & 0x04 == 0x04:
            GPIO.output(self.LCD_D6, True)
        if bits & 0x08 == 0x08:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

    def lcd_toggle_enable(self):
        time.sleep(0.0005)
        GPIO.output(self.LCD_E, True)
        time.sleep(0.0005)
        GPIO.output(self.LCD_E, False)
        time.sleep(0.0005)

    def lcd_text(self, message, line):
        # Send text to display
        # print(f"writing {message} on display")
        message = message.ljust(self.LCD_CHARS, " ")

        self.lcd_write(line, self.LCD_CMD)

        for i in range(self.LCD_CHARS):
            self.lcd_write(ord(message[i]), self.LCD_CHR)

    def display(self, line, text):
        print("\tEntered")
        if self.running:
            self.running = False
            print("\tWaiting Thread stop")
            if hasattr(self, "update_thread") and self.update_thread.is_alive():
                self.update_thread.join()
        print("\tThread stopped")
        self.top_pos = 0
        self.bottom_pos = 0

        if line == 0:
            self.top_pos = 0
            if len(text) <= 16:
                self.top_text = text
                self.top_pos_max = 0
            else:
                self.top_text = "   " + text + "   "  # pad the text with spaces
                self.top_pos_max = len(self.top_text) - 16
        else:
            self.bottom_pos = 0
            if len(text) <= 16:
                self.bottom_text = text
                self.bottom_pos_max = 0
            else:
                self.bottom_text = "   " + text + "   "  # pad the text with spaces
                self.bottom_pos_max = len(self.bottom_text) - 16
        print("\tStarting thread")
        self.running = True
        self.update_thread = Thread(target=self.update, args=())
        self.update_thread.start()
        print("\tdisplay done")

    def update(self):
        while self.running:
            if self.top_pos >= self.top_pos_max:
                self.top_pos = 0
            else:
                self.top_pos += 1

            if self.bottom_pos >= self.bottom_pos_max:
                self.bottom_pos = 0
            else:
                self.bottom_pos += 1

            # lcd display lcdstring
            self.lcd_text(
                self.top_text[self.top_pos : self.top_pos + 16], self.LCD_LINE_1
            )
            self.lcd_text(
                self.bottom_text[self.bottom_pos : self.bottom_pos + 16],
                self.LCD_LINE_2,
            )

            time.sleep(0.3)

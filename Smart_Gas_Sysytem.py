import RPi.GPIO as GPIO
import Adafruit_DHT
import time

# Pin setup
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 17
GAS_PIN = 27
RELAY_PIN = 22

GPIO.setmode(GPIO.BCM)   # Use BCM GPIO numbering
GPIO.setup(GAS_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)

try:
    # Run 50 cycles (about 100 seconds at 2 sec delay)
    for i in range(50):
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        gas_detected = GPIO.input(GAS_PIN) == GPIO.LOW  # Active LOW

        print(f"Cycle {i+1}")
        print(f"Temp: {temperature}°C, Humidity: {humidity}%, Gas: {'YES' if gas_detected else 'NO'}")

        if gas_detected or (temperature is not None and temperature > 35):
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn relay ON
            print("⚠️ ALERT: Ventilation ON")
        else:
            GPIO.output(RELAY_PIN, GPIO.LOW)   # Turn relay OFF
            print("✅ Safe: Ventilation OFF")

        print("-" * 40)
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up. Program ended.")

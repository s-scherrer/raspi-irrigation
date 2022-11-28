#include <LiquidCrystal.h>
#include <cactus_io_AM2302.h>

# define MINUTE 60000
# define SECOND 1000

#define LCD_SWITCH 2
#define LCD_REGISTER_SELECT 3
#define LCD_ENABLE 4
#define LCD_DATA4 5
#define LCD_DATA5 6
#define LCD_DATA6 7
#define LCD_DATA7 8
#define LCD_BRIGHTNESS 9
#define AM2302_PIN 10
#define STATUS_PIN 13

#define HUMIDITY_ID 1
#define TEMPERATURE_ID 2
// with 8 bytes per measurement and 2 observations, 10s correspond
// to 50MB of data per year
#define AM2302_INTERVAL 10*SECOND


/*
 * Function and type definitions
 */

struct observation_t {
  unsigned short observable_id;
  float value;
};

void measure_dht(AM2302 *dht, observation_t *humidity_obs_ptr, observation_t *temperature_obs_ptr) {
  dht->readHumidity();
  dht->readTemperature();
  (*humidity_obs_ptr).value = dht->humidity;
  (*temperature_obs_ptr).value = dht->temperature_C;
}

void blink_led(int pin, int ntimes = 4, int delay_time = 250) {
  for (int i = 0; i < ntimes; i++) {
    digitalWrite(pin, HIGH);
    delay(delay_time);
    digitalWrite(pin, LOW);
    delay(delay_time);
  }
}


/*
 * Initializations
 */

// initialize display
LiquidCrystal lcd(
  LCD_REGISTER_SELECT, 
  LCD_ENABLE, 
  LCD_DATA4,
  LCD_DATA5,
  LCD_DATA6,
  LCD_DATA7
);
char line1[17];
char line2[17];
volatile int lcdOn = 1;


void toggle_lcd(){
  Serial.println("toggling lcd");
  if (lcdOn) {
    digitalWrite(LCD_BRIGHTNESS, LOW);
    lcdOn = 0;
  } else {
    digitalWrite(LCD_BRIGHTNESS, HIGH);
    lcdOn = 1;
  }
}

// initialize T+RH sensor
AM2302 dht(AM2302_PIN);
observation_t humidity_obs = {HUMIDITY_ID, -9999.0f};
observation_t temperature_obs = {TEMPERATURE_ID, -9999.0f};
unsigned long previousMeasTime = -1000 * MINUTE;

void setup() {
  Serial.begin(9600);
  pinMode(STATUS_PIN, OUTPUT); // LED
  pinMode(LCD_BRIGHTNESS, OUTPUT);
  digitalWrite(LCD_BRIGHTNESS, HIGH);
  pinMode(LCD_SWITCH, INPUT);
  attachInterrupt(digitalPinToInterrupt(LCD_SWITCH), toggle_lcd, FALLING);
  pinMode(AM2302_PIN, INPUT);

  
  lcd.begin(16, 2);  // cols, rows
  lcd.print("Hello");
  lcd.setCursor(0, 1);  // col, row
  lcd.print("World");
  blink_led(STATUS_PIN);
  Serial.println("Finished setup");
}

void measure(){
  blink_led(STATUS_PIN, 2, 100);
  measure_dht(&dht, &humidity_obs, &temperature_obs);

  // send results via serial
  Serial.write((byte *) &humidity_obs, sizeof(humidity_obs)); Serial.write("\n");
  Serial.write((byte *) &temperature_obs, sizeof(temperature_obs)); Serial.write("\n");

  // write results to LCD
  char rh [8];
  char t [8];
  dtostrf(humidity_obs.value, 6, 1, rh);
  dtostrf(temperature_obs.value, 6, 1, t);
  sprintf(line1, "RH [%%]:   %s", rh);
  sprintf(line2, "T [*C]:   %s", t);
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2); 
}

void loop(){
  unsigned long currentTime = millis();
  if (currentTime - previousMeasTime > AM2302_INTERVAL) {
    measure();
    previousMeasTime = currentTime;
  }
}

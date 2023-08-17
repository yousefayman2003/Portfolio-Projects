 // Used modules
#include <ESP32Servo.h>
#include <Keypad.h>
//#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include <addons/TokenHelper.h>
#include <addons/RTDBHelper.h>
#include <time.h>

#define WIFI_SSID ""
#define WIFI_PASSWORD ""

#define API_KEY "AIzaSyAzkKax2O0i-2b2r8U13HjayCipQmChB3E"
#define DATABASE_URL "https://esp-firebase-641b5-default-rtdb.firebaseio.com/"

#define USER_EMAIL "test@gmail.com"
#define USER_PASSWORD "123456"

#define TIME_DELAY 100

#define PARENT_PATH "sensor"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

// variables
const char* ntpServer = "pool.ntp.org";
unsigned long sendDataPrevMillis = 0;
int timestamp;
bool ultrasonicValue = false;
bool fireValue = false;
bool pirValue = false;
int ldrValue;
int gasValue;

// Function Declartion
unsigned long getTime();
void writeDataInt(String path, int data);
void writeDataFloat(String path, float data);
int readDataInt(String path);
float readDataFloat(String path);
void deleteData(String path);
void initWiFi();
void setPinsMode();
bool valid_password();
bool is_there_someone();
void emergency();

// Used variables
byte pir_pin = 34;
byte flame_pin = 5;
const byte rows = 4;
const byte cols = 4;
byte gas_pin = 35;
byte echo_pin = 23, trig_pin = 18;
byte motor_pin = 15;
byte leds_pin = 19;
byte ldr_pin = 2;
char password[] = "2382023";
byte row_pins[] = {13, 12, 14, 27}, col_pins[] = {26, 25, 33, 32};
char keys[4][4] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'},
};

// Objects
//LiquidCrystal_I2C lcd(0x27, 16, 2);
Keypad keypad = Keypad(makeKeymap(keys), row_pins, col_pins, rows, cols);
Servo motor;

void setup() {
    Serial.begin(115200);
    setPinsMode();
//  lcd.init();
//  lcd.backlight();
//  lcd.print("The home is safe");

    // Connecting to WiFi
    initWiFi();
  
    //Configure times
    configTime(0, 0, ntpServer);
    
    // Assign the api key (required) 
    config.api_key = API_KEY;
    // Assign the RTDB URL 
    config.database_url = DATABASE_URL;
    // Assign the callback function for the long running token generation task 
    config.token_status_callback = tokenStatusCallback;
  
    // Assign the user sign in credentials 
    auth.user.email = USER_EMAIL;
    auth.user.password = USER_PASSWORD;
    
    // Connecting to FireBase
    Firebase.begin(&config, &auth);
    Firebase.reconnectWiFi(true);
}

void loop() {
    // The smart door with keypad and ultrasonic authentication 
    if (Firebase.ready() && millis() - sendDataPrevMillis > TIME_DELAY || sendDataPrevMillis == 0)
    {
  
        // Serial.println("----------------Successfully connected to FireBase---------------");
        // sending data rate millis value
        sendDataPrevMillis = millis();
  
        ldrValue = analogRead(ldr_pin);
        gasValue = analogRead(gas_pin);
        ultrasonicValue = is_there_someone();
        fireValue = digitalRead(flame_pin);
        pirValue = digitalRead(pir_pin);
        
        
        
        Serial.println("Is there someone " + String(is_there_someone()));
        Serial.println("LDR value: " + String(ldrValue));
        Serial.println("GAS value: " + String(gasValue));
        Serial.println("Flame value: " + String(fireValue));
        Serial.println("PIR value: " + String(ultrasonicValue));
        Serial.println("Flame value: " + String(pirValue));
        
        // Writing to RTDB
        writeDataInt(String(PARENT_PATH)+ String("/ldr"), ldrValue);
        writeDataInt(String(PARENT_PATH)+ String("/gas"), gasValue);
        writeDataBool(String(PARENT_PATH)+ String("/fire"), fireValue);
        writeDataBool(String(PARENT_PATH)+ String("/ultrasonic"), ultrasonicValue);
        writeDataBool(String(PARENT_PATH)+ String("/pir"), pirValue);
    
              
    }

       
         
//  if (is_there_someone())
//  {
//    if (keypad.getKey() == '#')
//    {
//      lcd.clear();
//      lcd.print("Enter Your Password");
//      Serial.println("Enter Your Password");
//      if (valid_password())
//        {
//          lcd.clear();
//          lcd.print("Correct Password");
//          Serial.print("Correct Password");
//          motor.write(180);
//          delay(3000);
//          motor.write(0);
//        }
//      else
//      {
//        lcd.clear();
//        lcd.print("Wrong Password");
//        Serial.println("Wrong Password");
//        delay(1000);
//      }
//      lcd.clear();
//      lcd.print("The home is safe");
//      Serial.println("The home is safe");
//    }
//  }
//
//  
//
//  // Control home lighting using PIR sensor and LDR sensor 
//  if (analogRead(ldr_pin) < 2000 || digitalRead(pir_pin))
//    digitalWrite(leds_pin, HIGH);
//  else
//    digitalWrite(leds_pin, LOW);
//
//   
//  // Declare an emergency when there is a fire or gas leak
//  if (analogRead(gas_pin) > 1200 || analogRead(flame_pin < 3000))
//  {
//    emergency();
//  }
  
}



/**
 * Description: emergency- turn on the buzzer and turn off the lamps when fire or gas is detected
 * Input:
 *      buzzer_pin[byte]: location of buzzer pin in esp32
 *      leds_pin[byte]: location of leds pins in esp32
 * Return: NULL
 */
// void emergency()
// {
//   lcd.clear();
//   lcd.print("Emergency");
//   digitalWrite(leds_pin, LOW);
//   while (analogRead(gas_pin) > 1200 || analogRead(flame_pin < 3000))
//   {
//      tone(buzzer_pin, 100);
//      delay(100);
//      noTone(buzzer_pin);
//   }
//   lcd.clear();
//   lcd.print("The Home is safe");
// }



/**
 * Description: vaild_password - cheack the entered password by user
 * Input: NULL
 * Return: 
 *      true if the entered password is correct 
 *      false otherwise
 */
//bool valid_password()
//{
//  byte i = 0;
//  bool condition = true;
//  char key;
//  
//  // take the password from the user
//  while(1)
//  {
//    key = keypad.getKey();
//    if (key)
//    {
//      // display the entered keys password
//      lcd.setCursor(i, 1);
//      lcd.print(key); 
//      Serial.print(key);
//      if (key == '#' or i == 16)
//        break;
//      else if (i >= strlen(password) || key != password[i])
//        condition = false;
//      i++;
//    }
//  }
//  return condition;
//}


/**
 * Description: is_there_someone - cheack if there someone in front of the door or not
 * Input:NULL 
 * Return:
 *      true if there is someone in front of the door and the distance between them is grater or equal 5
 *      false otherwise
 */
bool is_there_someone()
{
  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse
  digitalWrite(trig_pin, LOW);
  delay(2);
  digitalWrite(trig_pin, HIGH);
  delay(5);
  digitalWrite(trig_pin, LOW);

  // Read the echo PW signals
  int duration = pulseIn(echo_pin, HIGH);

  // Calculate the distance in centimeters
  int distance = duration * 0.034 / 2;

  if (distance <= 10)
    return true;
  else
    return false;
}

/**
 * setPinsMode - Set pins mode for  esp32
 * 
 * Return: NULL
*/
void setPinsMode()
{
  pinMode(echo_pin, INPUT);
  pinMode(trig_pin, OUTPUT);
  pinMode(ldr_pin, INPUT);
  pinMode(gas_pin, INPUT);
  pinMode(flame_pin, INPUT);
  pinMode(pir_pin, INPUT);  
  motor.attach(motor_pin);
}

/**
 * getTime - Function that gets current epoch time
 * 
 * Return: 0 if failed to get time, else returns current time
*/
unsigned long getTime() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return (0);
  }
  time(&now);
  return now;
}

/*
 void setLocalTime() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("No time available (yet)");
    return;
  }
  Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
*/

/**
 * writeDataInt - Writes data of type int to firebase
 * 
 * @path [String]: database path to write data for
 * 
 * @data [int]: data to write
 * 
 * Return: NULL
*/
void writeDataInt(String path, int data)
{
  // Getting current time
  timestamp = getTime();
  // Writing to RTDB
  if (Firebase.RTDB.setIntAsync(&fbdo, path, data))
  {
    Serial.printf("%i - SuccessFully Saved to : %s (%s) at %i\n", data, fbdo.dataPath().c_str(), fbdo.dataType(), timestamp);          
  }
  // if writing fails
  else
  {
    Serial.println("FAILED TO WRITE: " + fbdo.errorReason());  
  }
}

/**
 * writeDataBool - Writes data of type boolean to firebase
 * 
 * @path [String]: database path to write data for
 * 
 * @data [bool]: data to write
 * 
 * Return: NULL
*/
void writeDataBool(String path, bool data)
{
  // Getting current time
  timestamp = getTime();
  // Writing to RTDB
  if (Firebase.RTDB.setBoolAsync(&fbdo, path, data))
  {
    Serial.printf("%i - SuccessFully Saved to : %s (%s) at %i\n", data, fbdo.dataPath(), fbdo.dataType(), timestamp);          
  }
  // if writing fails
  else
  {
    Serial.println("FAILED TO WRITE: " + fbdo.errorReason());  
  }
}

/**
 * readDataInt - Reads data of type int from firebase
 * 
 * @path [String]: database path to read data from
 * 
 * Return: data
*/
int readDataInt(String path)
{
    // storing the value of the data
    int value;
    // Reading from RTDB
    if (Firebase.RTDB.getInt(&fbdo, path))
    {
      value = fbdo.intData();
      Serial.println("Successfull READ from " + fbdo.dataPath() + ": " + value + "(" + fbdo.dataType() + ")");
    }
    // if failed to read
    else
    {
      Serial.println("FAILED TO READ: " + fbdo.errorReason());   
    } 
    return (value);
}

/**
 * readDataBool - Reads data of type boolean from firebase
 * 
 * @path [String]: database path to read data from
 * 
 * Return: data
*/
float readDataFloat(String path)
{
    // storing the value of the data
    float value;
    // Reading from RTDB
    if (Firebase.RTDB.getFloat(&fbdo, path))
    {
      value = fbdo.boolData();
      Serial.println("Successfull READ from " + fbdo.dataPath() + ": " + value + "(" + fbdo.dataType() + ")");
    }
    // if failed to read
    else
    {
      Serial.println("FAILED TO READ: " + fbdo.errorReason());   
    } 

    return (value);
}

/**
 * deleteData - Deletes data from a specific path
 * 
 * Return: NULL
*/
void deleteData(String path)
{
    if (Firebase.RTDB.deleteNode(&fbdo, path)) {
    Serial.println("Data deleted successfully! at " + fbdo.dataPath());
  } else {
    Serial.println("Failed to delete data from " + fbdo.dataPath() + "  at Firebase RTDB!");
  }
}

/**
 * initWiFi - Initializes a wifi connection with esp32
 * 
 * Return: NULL
*/
void initWiFi()
{
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting To WiFi");
  while (WiFi.status() != WL_CONNECTED)
  {
      Serial.print(".");
      delay(250);  
  }
  Serial.println();
  Serial.printf("Connected with IP: %s\n\n", String(WiFi.localIP()));
}

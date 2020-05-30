#define LED_RED 13
#define LED_YELLOW 12
#define LED_GREEN 11
#define FAKE_VCC 6
#define BUTTON1 7
#define BUTTON2 5

bool red_to_green = true;
bool green_to_red = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_RED, OUTPUT);
  digitalWrite(LED_RED, HIGH); 

  pinMode(LED_YELLOW, OUTPUT);
  digitalWrite(LED_YELLOW, HIGH);

  pinMode(LED_GREEN, OUTPUT);
  digitalWrite(LED_GREEN, HIGH);

  pinMode(FAKE_VCC, OUTPUT);
  digitalWrite(FAKE_VCC, HIGH);

  pinMode(BUTTON1, INPUT);
  digitalWrite(BUTTON1, LOW);

  pinMode(BUTTON2, INPUT);
  digitalWrite(BUTTON2, LOW);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

    if(digitalRead(BUTTON1) == LOW && red_to_green)
  {
    digitalWrite(LED_RED, LOW);
    digitalWrite(LED_YELLOW, LOW);
    delay(1000);
    digitalWrite(LED_RED, HIGH);
    digitalWrite(LED_YELLOW, HIGH);
    digitalWrite(LED_GREEN, LOW);
    red_to_green = false;
    green_to_red = true;
    
  }

  if(digitalRead(BUTTON1) == HIGH && green_to_red)
  {
    digitalWrite(LED_GREEN, HIGH);
    digitalWrite(LED_YELLOW, LOW);
    delay(4000);
    digitalWrite(LED_YELLOW, HIGH);
    digitalWrite(LED_RED, LOW);
    
    red_to_green = true;
    green_to_red = false;
  }
}

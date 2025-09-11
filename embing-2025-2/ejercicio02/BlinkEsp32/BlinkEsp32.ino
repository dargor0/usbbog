/**
  @brief Blink (modified for ESP32)
*/

// these are the colors available in my board. 
// Change them according to your needs.
#define LED_RED 2
#define LED_GREEN 4
#define LED_YELLOW 27

// Task handles
TaskHandle_t blinkred_task_handle;
TaskHandle_t blinkyellow_task_handle;

// blinker parameters: put inside the array
// {<pin_number>, <half period in ms>}
int red_param[2] = {LED_RED, 1000};
int yellow_param[2] = {LED_YELLOW, 200};

// calculator by JohanSanchez
void parpadear(int veces);
char leerOperacion();
int leerNumero();

// Calculator LED
#define LED_CALCULATOR LED_GREEN

// generic blinker task code
void blinker_generic(void * param)
{
  // local parameters
  int pin = 0;
  int delaynum = 0;

  // extract from parameters
  int * paramarray = (int *) param;

  pin = paramarray[0];
  delaynum = paramarray[1];

  // init the pin
  pinMode(pin, OUTPUT);

  // show parameters
  Serial.print("Start blink task pin=");
  Serial.print(pin);
  Serial.print(" delay=");
  Serial.println(delaynum);

  // loop
  while(1)
  {
    digitalWrite(pin, HIGH);  // turn the LED on (HIGH is the voltage level)
    delay(delaynum);          // wait for half period
    digitalWrite(pin, LOW);   // turn the LED off by making the voltage LOW
    delay(delaynum);          // wait for another half period
  }
}

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_CALCULATOR as an output for the calculator.
  pinMode(LED_CALCULATOR, OUTPUT);
  // other pins are initialized on the task code

  // Configure serial console
  Serial.begin(115200);
  Serial.println("ESP32 demo");

  // task creation
  xTaskCreate(blinker_generic, "BRed", 2048, red_param, 2, &blinkred_task_handle);
  Serial.println("Task red created");
  xTaskCreate(blinker_generic, "BYel", 2048, yellow_param, 2, &blinkyellow_task_handle);
  Serial.println("Task yellow created");
}

// the loop function runs over and over again forever
void loop() {
  // run calculator
  Serial.println("=== CALCULADORA SIMPLE ===");
  Serial.println("Escribe la operacion: + , - , * , /");

  // wait for serial
  while (Serial.available() == 0)
  {
    delay(500);
  }

  if (Serial.available() > 0) {
    char operacion = leerOperacion(); ///< Leer operación (+, -, *, /)

    int num1 = leerNumero();  ///< Primer número
    int num2 = leerNumero();  ///< Segundo número
    int resultado = 0;

    // Realizar operación
    switch (operacion) {
      case '+': resultado = num1 + num2; break;
      case '-': resultado = num1 - num2; break;
      case '*': resultado = num1 * num2; break;
      case '/': resultado = num1 / num2; break;
      default:
        Serial.println("Operacion no valida.");
        return; ///< Sale de loop en esta iteración
    }

    // Mostrar resultado
    Serial.print("Resultado: ");
    Serial.println(resultado);

    // Parpadear según el signo
    if (resultado > 0) parpadear(1);
    else if (resultado < 0) parpadear(2);
    else parpadear(3);

    Serial.println("Operacion terminada.");
  }
}

/**
 * @brief Hace parpadear el LED integrado.
 * @param veces Número de parpadeos.
 */
void parpadear(int veces) {
  for (int i = 0; i < veces; i++) {
    digitalWrite(LED_CALCULATOR, HIGH);
    delay(300);
    digitalWrite(LED_CALCULATOR, LOW);
    delay(300);
  }
}

/**
 * @brief Lee la operación desde el Serial, ignorando saltos de línea.
 * @return char Carácter de la operación (+, -, *).
 */
char leerOperacion() {
  String linea = Serial.readStringUntil('\n'); // lee hasta Enter
  linea.trim(); // elimina espacios y saltos
  if (linea.length() > 0) {
    return linea.charAt(0); // primer carácter
  }
  return '?'; // valor por defecto si está vacío
}

/**
 * @brief Lee un número entero desde el Serial.
 * @return int Número introducido por el usuario.
 */
int leerNumero() {
  Serial.println("Ingresa un numero y presiona Enter:");
  while (Serial.available() == 0); // esperar entrada
  String linea = Serial.readStringUntil('\n');
  linea.trim();
  return linea.toInt(); // convierte la cadena a entero
}

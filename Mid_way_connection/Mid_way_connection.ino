

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
  Serial.setTimeout(1);
}

void loop() {
  //Vendt til at der modtages noget på den seriale forbindelse
  while (!Serial.available()) 
  {
    
  }
  String msgFromPC = ""; //Vaiable til at genne beskeden i mens den kommer ind fra pc
  while (Serial.available()) 
  {
     
    // Læs det indkommende data
    char c = Serial.read();
    if (c == '\n') 
      {
       /*Stop med at læse til når at der er '\n' modtaget dette kommer de
       da for hver besked skrives der på en ny linje og derfor er '\n' brugt som stopper.*/
       break; 
      }
    msgFromPC += c;
    delay(2); //For at give tid til at alle characters bliver modtaget.  
  }
  String msgFromDynamixel = "";
  while (Serial1.available()) 
  {
     
    // Læs det indkommende data
    char c = Serial1.read();
    if (c == '\n') 
      {
       /*Stop med at læse til når at der er '\n' modtaget dette kommer de
       da for hver besked skrives der på en ny linje og derfor er '\n' brugt som stopper.*/
       break; 
      }
    msgFromDynamixel += c;
    delay(2); //For at give tid til at alle characters bliver modtaget.  
  }
  Serial.print(msgFromDynamixel);
  Serial1.print(msgFromPC);
}

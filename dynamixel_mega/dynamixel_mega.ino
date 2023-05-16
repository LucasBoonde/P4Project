void setup() {
  //Åbne serial forbindelse
  Serial.begin(115200);
  Serial1.begin(115200);
  Serial.setTimeout(1);
}

void loop() 
{ 
  //Vendt til at der modtages noget på den seriale forbindelse
  while (!Serial1.available()) 
  {
    
  }
  String message = ""; //Vaiable til at genne beskeden i mens den kommer ind fra pc
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
    message += c;
    delay(2); //For at give tid til at alle characters bliver modtaget.
  }
  double Tau[2];
  //Sæt opdelings tegnet til ',' og hvis der er flere end 0 ',' i beskeden opdeles beskeden så alt der er før bliver til en og alt der er efter bliver til en anden besked.
  int OpdelingsIndex = message.indexOf(',');
  if (OpdelingsIndex >= 0) 
  {
    
    Tau[0] = message.substring(0,OpdelingsIndex).toDouble();
    Tau[1] = message.substring(OpdelingsIndex+1).toDouble();
    //Serial1.print(String(Tau1));
  }
  Serial.print(String(Tau[0]));
  String output = "#" +String(Tau[0])+"og"+String(Tau[1])+"#Modtaget";
  Serial1.print(message);
  Serial1.println(output);
}

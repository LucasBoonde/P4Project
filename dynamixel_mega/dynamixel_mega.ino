#include <DynamixelShield.h>

const uint8_t ID1 = 1;
const uint8_t ID2 = 2;

const float DXL_PROTOCOL_VERSION = 2.0;

DynamixelShield dxl;

//This namespace is required to use Control table item names
using namespace ControlTableItem;



void setup() {
  //Åbne serial forbindelse
  Serial.begin(115200);
  Serial1.begin(115200);
  Serial.setTimeout(1);


  // Set Port baudrate to 57600bps. This has to match with DYNAMIXEL baudrate.
  dxl.begin(57600);
  // Set Port Protocol Version. This has to match with DYNAMIXEL protocol version.
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  // Get DYNAMIXEL information
  dxl.ping(ID1);

  // Turn off torque when configuring items in EEPROM area - Jeg ved faktisk ikke om man skal sætte den i position mode for at aflæse positionen, men det tror jeg
  dxl.torqueOff(ID1);
  dxl.setOperatingMode(ID1, OP_CURRENT);
  dxl.torqueOn(ID1);

  dxl.ping(ID2);

  // Turn off torque when configuring items in EEPROM area
  dxl.torqueOff(ID2);
  dxl.setOperatingMode(ID2, OP_CURRENT);
  dxl.torqueOn(ID2);




}

void loop() 
{ 
  //Vendt til at der modtages noget på den seriale forbindelse
  while (!Serial1.available()) 
  {
    
  }
  String message = ""; //Variabel til at genne beskeden i mens den kommer ind fra pc
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
    //Serial1.print(message);
  }
  //Serial1.print(message+ "#");
  char indicator;
  double Current[2];
  //Serial1.print(message);
  int OpdelingsIndexIndicator = message.indexOf('#');
  if (OpdelingsIndexIndicator >= 0)
  {
    String indicatorString = message.substring(0,OpdelingsIndexIndicator);
    message = message.substring(OpdelingsIndexIndicator+1);
    if (indicatorString.equals("I"))
    {
      
      //Sæt opdelings tegnet til ',' og hvis der er flere end 0 ',' i beskeden opdeles beskeden så alt der er før bliver til en og alt der er efter bliver til en anden besked.
      int OpdelingsIndex = message.indexOf(',');
      
      if (OpdelingsIndex >= 0) 
        {
          Current[0] = message.substring(0,OpdelingsIndex).toDouble();
          Current[1] = message.substring(OpdelingsIndex+1).toDouble();          
          //Kør robotten til de givne Tau* værdier (Vi prøver først lige med positions værdier i grader) 
          
          dxl.setGoalCurrent(ID1, Current[0], UNIT_MILLI_AMPERE);
          dxl.setGoalCurrent(ID2, Current[1], UNIT_MILLI_AMPERE);

          Serial1.println("I#"+String(dxl.getPresentPosition(ID1, UNIT_DEGREE))+","+String(dxl.getPresentPosition(ID2, UNIT_DEGREE))+"#"+String(dxl.getPresentVelocity(ID1, UNIT_RPM))+","+String(dxl.getPresentVelocity(ID2, UNIT_RPM))+"#M");
          
        }
      
    }
  }
  
  

  
  
  
 


  


  
  


}

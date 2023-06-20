#include <DynamixelShield.h>

const uint8_t DXL_ID = 1;
const uint8_t DXL_ID2 = 2;

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
  dxl.ping(DXL_ID);

  // Turn off torque when configuring items in EEPROM area - Jeg ved faktisk ikke om man skal sætte den i position mode for at aflæse positionen, men det tror jeg
  dxl.torqueOff(DXL_ID);
  dxl.setOperatingMode(DXL_ID, OP_CURRENT);
  dxl.torqueOn(DXL_ID);

  dxl.ping(DXL_ID2);

  // Turn off torque when configuring items in EEPROM area
  dxl.torqueOff(DXL_ID2);
  dxl.setOperatingMode(DXL_ID2, OP_CURRENT);
  dxl.torqueOn(DXL_ID2);




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
    //Serial1.print(message);
  }
  //Serial1.print(message+ "#");
  char indicator;
  double Tau[2];
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
          double Ref[2];
          Ref[0] = message.substring(0,OpdelingsIndex).toDouble();
          Ref[1] = message.substring(OpdelingsIndex+1).toDouble();
          Serial1.println("I#"+String(dxl.getPresentPosition(DXL_ID, UNIT_DEGREE))+","+String(dxl.getPresentPosition(DXL_ID2, UNIT_DEGREE))+"#M");
          Ref[0] = (Ref[0]*180)/PI;
          Ref[1] = (Ref[1]*180)/PI;
          double Tau[2];
          double pos[2];
          double vel[2];
          double corr_cnst = 100.0;

          pos[0] = dxl.getPresentPosition(DXL_ID, UNIT_DEGREE);
          pos[1] = dxl.getPresentPosition(DXL_ID2, UNIT_DEGREE);

          vel[0] = dxl.getPresentVelocity(DXL_ID, UNIT_RPM);
          vel[1] = dxl.getPresentVelocity(DXL_ID2, UNIT_RPM);

          Tau[0] = 2.0 * (Ref[0] - pos[0]) - 5 * vel[0];
          if (Tau[0] > 0) 
           Tau[0] += corr_cnst;
          if (Tau[0] < 0)
           Tau[0] -= corr_cnst;

          Tau[1] = 2.0 * (Ref[1] - pos[1]) - 5 * vel[1];
           if (Tau[1] > 0)
          Tau[1] += corr_cnst;
           if (Tau[1] < 0)
          Tau[1] -= corr_cnst;
          

          
          //Kør robotten til de givne Tau* værdier (Vi prøver først lige med positions værdier i grader) 
          
          dxl.setGoalCurrent(DXL_ID, Tau[0], UNIT_MILLI_AMPERE);
          dxl.setGoalCurrent(DXL_ID2, 0, UNIT_MILLI_AMPERE);
          
        }
      
    }
    if (indicatorString.equals("P"))
    {       
       String positionNow = "P#"+String(dxl.getPresentPosition(DXL_ID, UNIT_DEGREE))+","+String(dxl.getPresentPosition(DXL_ID2, UNIT_DEGREE))+message+"#M";
       Serial1.print(positionNow);
    }
  }
  
  

  
  
  
 


  


  
  


}

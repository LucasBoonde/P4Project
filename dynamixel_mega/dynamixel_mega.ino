/*******************************************************************************
* Copyright 2016 ROBOTIS CO., LTD.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

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
  dxl.setOperatingMode(DXL_ID, OP_POSITION);
  dxl.torqueOn(DXL_ID);

  dxl.ping(DXL_ID2);

  // Turn off torque when configuring items in EEPROM area
  dxl.torqueOff(DXL_ID2);
  dxl.setOperatingMode(DXL_ID2, OP_POSITION);
  dxl.torqueOn(DXL_ID2);



  // Set velocity and acceleration (ONLY RELEVANT FOR TESTING IN POSITION CONTROL MODE, OUTCOMMENT FOR CURRENT MODE)
  dxl.writeControlTableItem(PROFILE_ACCELERATION, DXL_ID, 50);
  dxl.writeControlTableItem(PROFILE_VELOCITY, DXL_ID, 1000);
  
  dxl.writeControlTableItem(PROFILE_ACCELERATION, DXL_ID2, 50);
  dxl.writeControlTableItem(PROFILE_VELOCITY, DXL_ID2, 1000);

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


  //Kør robotten til de givne Tau* værdier (Vi prøver først lige med positions værdier i grader) 
  dxl.setGoalPosition(DXL_ID, Tau[0], UNIT_DEGREE);
  dxl.setGoalPosition(DXL_ID2, Tau[1], UNIT_DEGREE);
  delay(1000);


  //Print nuværende position til Serial1 linjen
  Serial1.print("Present Position 1(degree) : ");
  Serial1.println(dxl.getPresentPosition(DXL_ID, UNIT_DEGREE));

  Serial1.print("Present Position 2(degree) : ");
  Serial1.println(dxl.getPresentPosition(DXL_ID2, UNIT_DEGREE));


  Serial1.print(message);
  Serial1.println(output);
}

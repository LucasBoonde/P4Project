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
  //  Serial1.begin(115200);
  //  Serial.setTimeout(1);


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


  double Tau[2];
  double pos[2];
  double vel[2];
  double corr_cnst = 100.0;

  pos[0] = dxl.getPresentPosition(DXL_ID, UNIT_DEGREE);
  pos[1] = dxl.getPresentPosition(DXL_ID2, UNIT_DEGREE);

  vel[0] = dxl.getPresentVelocity(DXL_ID, UNIT_RPM);
  vel[1] = dxl.getPresentVelocity(DXL_ID2, UNIT_RPM);

  float th1[] = {1.44, 1.53,  1.64,  1.80,  1.83,  1.95,  2.03,  1.92,  1.98,  2.067,  2.05};
  float th2[] = {1.69, 1.53,  1.38,  1.39,  1.28,  1.31,  1.32,  1.15,  1.13,  1.16,  1.08}; 

  for ( int i : th1)
  {
    th1[i] = (th1[i]*180)/PI;
          
    for( int j : th2)
    {
      th2[j] = (th2[j]*180)/PI;
      Tau[0] = 2.0 * (th1[i] - pos[0]) - 5 * vel[0];
        if (Tau[0] > 0)
          Tau[0] += corr_cnst;
        if (Tau[0] < 0)
          Tau[0] -= corr_cnst;

      Tau[1] = 2.0 * (th2[j] - pos[1]) - 5 * vel[1];
        if (Tau[1] > 0)
          Tau[1] += corr_cnst;
        if (Tau[1] < 0)
          Tau[1] -= corr_cnst;
       dxl.setGoalCurrent(DXL_ID, Tau[0], UNIT_MILLI_AMPERE);
       dxl.setGoalCurrent(DXL_ID2, Tau[1], UNIT_MILLI_AMPERE);

       if(th1[i]-pos[0]<20 and th1[i]-pos[0]>-20 and th2[j]-pos[1]<20 and th2[j]-pos[1]>-20)
         i = i+1;
         j = j+1;
       
    }
  }


}

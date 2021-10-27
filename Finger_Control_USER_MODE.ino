
#define USER_MODE


//OKAY  ({999044})
//0    ({000009}) 
//1    ({000909})
//2    ({009909})
//3    ({099909})
//4    ({999909})
//5     ({999999})

//OPEN ({000009})
#include <Servo.h>

Servo LittleFinger;
Servo RingFinger;
Servo MiddleFinger;
Servo IndexFinger;
Servo ThumbFinger;
Servo ThumbFingerRot;// create servo object to control a servo

char Buffer[40];
int index = 0;
char PrevChar = ' ';
char Prev2Char = ' ';
int DataFlag = 0;
int MoveServoFlag = 0;
int UpdateServoPosFkag = 0;

int PosLittleFinger = 180;
int PosRingFinger = 0;
int PosMiddleFinger = 0;
int PosIndexFinger = 0;
int PosThumbFinger = 0;
int PosThumbFingerRot = 0;  // variable to store the servo position


void setup()
{
  Serial.begin(9600);
  LittleFinger.attach(3); //180 open
  RingFinger.attach(5);//0 open
  MiddleFinger.attach(6);//0 open
  IndexFinger.attach(9);//O is open
  ThumbFinger.attach(10);//0 is open
  ThumbFingerRot.attach(11); //Zero = thumb low

}

void loop()
{
  MoveServoToPos();

}

void MoveServoToPos()
{
  LittleFinger.write(PosLittleFinger);
  RingFinger.write(PosRingFinger);
  MiddleFinger.write(PosMiddleFinger);
  IndexFinger.write(PosIndexFinger);
  ThumbFinger.write(PosThumbFinger);
  ThumbFingerRot.write(PosThumbFingerRot);
}

void UpdateServoPosUSER()
{
  //Serial.println("insideswitch");   
  String NewBuffer[40];
  switch(Buffer[0])
  {
    case '0':
    {
      strcpy(Buffer,"000009");   
      break;
    }
        case '1':
    {
      strcpy(Buffer,"000909");
      break;
    }
        case '2':
    {
      strcpy(Buffer,"009909");
      break;
    }
        case '3':
    {
      strcpy(Buffer,"099909");
    
      break;
    }
            case '4':
    {
      strcpy(Buffer,"999909");
      break;
    }
                case '5':
    {
      strcpy(Buffer,"999999");
      break;
    }
                    case 'O':
    {
      strcpy(Buffer,"999143");
      break;
    }
     case 'N':
    { 
      strcpy(Buffer,"000009" );
     break;
    }
  }
  
  PosLittleFinger = (Buffer[0] - '0') * 180 / 9;
  PosRingFinger = (Buffer[1] - '0') * 180 / 9;
  PosRingFinger = (PosRingFinger * (-1)) + 180;
  PosMiddleFinger = (Buffer[2] - '0') * 180 / 9;
  PosMiddleFinger = (PosMiddleFinger * (-1)) + 180;
  PosIndexFinger = (Buffer[3] - '0') * 180 / 9;
  PosIndexFinger = (PosIndexFinger * (-1)) + 180;
  PosThumbFinger = (Buffer[4] - '0') * 180 / 9;
  PosThumbFinger = (PosThumbFinger * (-1)) + 180;
  PosThumbFingerRot = (Buffer[5] - '0') * 180 / 9;
  PosThumbFingerRot = (PosThumbFingerRot * (-1)) + 180;
}

void serialEvent()
{
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:

    if (PrevChar == '{' && Prev2Char == '(')
    {
      //   Serial.println("Start");
      DataFlag = 1;
      index = 0;
    }


    if (PrevChar == '}' && inChar == ')' && DataFlag == 1)
    {
      DataFlag = 0;
      UpdateServoPosUSER();
      //Serial.println("end");
      //Serial.println(Buffer);
    }
    Prev2Char = PrevChar;
    PrevChar = inChar;
    Buffer[index] = inChar;
    index++;

  }

}

#define rwb 11   //RW
#define mr 10
#define en 12
#define clk 9

//uint8_t switch_table[16] = {};

const char switchnum[] = {2, 3, 4, 5, 6, 7, 8, 13};
const char addrnum[] = {A0, A1, A2, A4, A3};

uint8_t rcvbuffer[256] = {};

int state = 0;

uint8_t readPin(uint8_t addr)
{
  uint8_t i = 0, res = 0;
  digitalWrite(rwb, 1);
  for (i = 0; i <= 4; i++)
  {
    digitalWrite(addrnum[i], addr & 0x01 ? HIGH : LOW);
    addr >>= 1;
  }
  digitalWrite(en, 0);
  delayMicroseconds(10);
  for (i = 0; i < 8; i++)
  {
//    pinMode(switchnum[i], INPUT_PULLUP);
//    delayMicroseconds(10);
    res += digitalRead(switchnum[i]) << i;
  }
  digitalWrite(en, 1);
  return res;
}

void writePin(uint8_t addr, uint8_t n)
{
  uint8_t i = 0;
  digitalWrite(rwb, 0);
  for (i = 0; i <= 4; i++)
  {
    digitalWrite(addrnum[i], addr & 0x01 ? HIGH : LOW);
    Serial.println(addr & 0x01 ? HIGH : LOW);
    addr = addr >> 1;
  }
  for (i = 0; i < 8; i++)
  {
    pinMode(switchnum[i], OUTPUT);
    Serial.print(n & 0x01 ? HIGH : LOW);
    digitalWrite(switchnum[i], n & 0x01 ? HIGH : LOW);
    n = n >> 1;
  }
  digitalWrite(en, 0);
  //delay(100);
  delayMicroseconds(400);
  digitalWrite(en, 1);
  for (i = 0; i < 8; i++)
  {
    pinMode(switchnum[i], INPUT_PULLUP);
    delayMicroseconds(10);
  }
}

void setup() {
  // put your setup code here, to run once:
  int i = 0;

  DDRC = 0xff; //端口C设置为输出,A0~A5,in fact 0x3F will be OK because there are only six PINs while 0x3F is B00111111
  PORTC = 0x00; //端口C初始值设置为0

  pinMode(en, OUTPUT);
  pinMode(mr, OUTPUT);
  pinMode(rwb, OUTPUT);
  pinMode(clk, OUTPUT);

  for (i = 0; i < 8; i++)
  {
    pinMode(switchnum[i], INPUT_PULLUP);
    delayMicroseconds(10);
  }

  digitalWrite(en, 1);
  digitalWrite(mr, 0);
  digitalWrite(rwb, 1);
  digitalWrite(clk, 1);

  delay(1);
  digitalWrite(mr, 1);

  for (i = 0; i < 32; i++)writePin(i, 0);
  //Considering add self-check programme.

  Serial.begin(115200);
  //while (Serial.available() > 0)Serial.read();
  //Serial.println("Initialization Completed.");
}

void loop() {
  // put your main code here, to run repeatedly:
  uint8_t readbuf = 0;
  int readlen = 0;

  if (Serial.available())
  {
        switch (state)
        {
          case 0:
            Serial.print("Readbuf = ");
            readbuf = Serial.read();
    
            Serial.println(readbuf);
            if (readbuf == 0x01)state = 1; //0x01 for read
            else if (readbuf == 0x02)state = 2; //0x02 for write
            else if (readbuf == 0x03)state = 3; //0x03 for control
            else state = 0;
            break;
          case 1://Read Mode
            readlen = Serial.read();
            Serial.print("Length = ");
            Serial.println(readlen);
            while (Serial.available() < readlen);
            Serial.readBytes(rcvbuffer, readlen);
            for(int i=0;i<readlen;i++)
            {
              Serial.print("Switch ");
              Serial.print((int)rcvbuffer[i]);
              Serial.print(" = ");
              Serial.println(readPin(rcvbuffer[i]&0x1F));
            }
            state = 0;
            break;
          case 2://Write Mode
            readlen = Serial.read();
            Serial.print("Length = ");
            Serial.println(readlen);
            while (Serial.available() < readlen);
            Serial.readBytes(rcvbuffer, readlen);
            for(int i=0;i<(readlen>>1);i++)
            {
              writePin(rcvbuffer[i<<1]&0x1F,rcvbuffer[(i<<1)+1]);
              Serial.print("Switch ");
              Serial.print((int)rcvbuffer[i<<1]);
              Serial.print(" to ");
              Serial.println((int)rcvbuffer[(i<<1)+1]);
            }
            state = 0;
            break;
          case 3:
            readlen = Serial.read();
            Serial.print("Length = ");
            Serial.println(readlen);
            while (Serial.available() < readlen);
            Serial.readBytes(rcvbuffer, readlen);

            state = 0;
            break;
          default:
            Serial.print("State = ");
            Serial.println(state);
            state = 0;
        }
  }

  delay(10);
}

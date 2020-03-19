#include <string.h>
#include <Wire.h>

#define I2C_ADDRESS 0x68
#define ACCEL_XOUT_H 0x3B
#define PWR_MGMT_1 0x6B
#define ACCEL_CONFIG 0x1C
#define GYRO_CONFIG 0x1B
#define ACCEL_SCALE 0
#define GYRO_SCALE 0
#define PERIOD 100
#define NUM_SENSORS 6

bool handshakeBool = false;
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;
char msg;
char output[NUM_SENSORS*10] = "";
char sensorString[10] = "";
double sensorValues[NUM_SENSORS];
void setup() {
  Serial.begin(115200);
  Wire.begin();
  sensor_write_reg(PWR_MGMT_1, 0); // set to 0 to wakes up the MPU-6050
  sensor_write_reg(ACCEL_CONFIG, ACCEL_SCALE);
  sensor_write_reg(GYRO_CONFIG, GYRO_SCALE); 
}
void sensor_write_reg(int reg, uint8_t data){
  Wire.beginTransmission(I2C_ADDRESS);
  Wire.write(reg);
  Wire.write(data);
  Wire.endTransmission(true); // release the I2C-bus
}

void sensor_read_reg(int reg, uint8_t *storage){
  Wire.beginTransmission(I2C_ADDRESS);
  Wire.write(reg);
  Wire.endTransmission(false); // hold the I2C-bus
  Wire.requestFrom(I2C_ADDRESS, 1, true); // relase the I2C-bus after data is read
  *storage = Wire.read();
}
void loop() {
  while(!handshakeBool) {
    if(Serial.available()) {
      msg = Serial.read();
      msg = (char) msg;
      if(msg == 'H') {
        Serial.write("ACK");
        delay(500);
        handshakeBool = true;      
      }
    }
  }

  while(true) {
    getData();
    pushData();
    delay(100);
  }
}

void getData() {
  Wire.beginTransmission(I2C_ADDRESS);
  Wire.write(ACCEL_XOUT_H);  // starting with register ACCEL_XOUT_H
  Wire.endTransmission(false);
  Wire.requestFrom(I2C_ADDRESS, 14, true);  // request a total of 14 registers
  AcX = Wire.read() << 8 | Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
  AcY = Wire.read() << 8 | Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ = Wire.read() << 8 | Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  Tmp = Wire.read() << 8 | Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  GyX = Wire.read() << 8 | Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  GyY = Wire.read() << 8 | Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  GyZ = Wire.read() << 8 | Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
  sensorValues[0] = accel_preproc(AcX);
  sensorValues[1] = accel_preproc(AcY);
  sensorValues[2] = accel_preproc(AcZ);
  sensorValues[3] = gyro_preproc(GyX);
  sensorValues[4] = gyro_preproc(GyY);
  sensorValues[5] = gyro_preproc(GyZ);
}
double accel_preproc(int16_t AcIn){
  double AcOut, g = 9.80665; // in unit of m/s^2
  AcOut = AcIn / (double) 32767 * 2 * g;
  AcOut = AcOut * pow(2, ACCEL_SCALE);
  return AcOut;
}

double gyro_preproc(int16_t GyIn){
  double GyOut, r = 250; // in unit of degree/s
  GyOut = GyIn / (double) 32767 * r;
  GyOut = GyOut * pow(2, GYRO_SCALE);
  return GyOut;
}
void pushData() {
//  char output[NUM_SENSORS*10] = "";
  memset(output,0,sizeof(output));
//  char sensorString[10] = "";
  memset(sensorString,0,sizeof(sensorString));
  char final2Bytes[3] = " z";
  for(int i=0;i<NUM_SENSORS;i++) {
    dtostrf(sensorValues[i],0,2,sensorString);
    strcat(output, sensorString);
    strcat(output," ");
  }
  final2Bytes[0] = calcChecksum2(output);
  strcat(output,final2Bytes);
  Serial.print(output);
}

char calcChecksum2(char dataArr[]) {
  int len = strlen(dataArr);
  char checksum = 0;
  for(int i=0;i<len;i++) {
    checksum ^= dataArr[i];
  }
  checksum = (((int)checksum)%95) + 33;
  return checksum;
}

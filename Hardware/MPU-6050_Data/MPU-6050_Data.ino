/* MPU-6050 usage with connections to Arduino board
*/
#include <Wire.h>
#define I2C_ADDRESS 0x68
#define ACCEL_XOUT_H 0x3B
#define PWR_MGMT_1 0x6B
#define ACCEL_CONFIG 0x1C
#define GYRO_CONFIG 0x1B
#define ACCEL_SCALE 0
#define GYRO_SCALE 0
#define PERIOD 50
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;
int ctrl = 1;
void setup(){
  Wire.begin();
  sensor_write_reg(PWR_MGMT_1, 0); // set to 0 to wakes up the MPU-6050
  sensor_write_reg(ACCEL_CONFIG, ACCEL_SCALE);
  sensor_write_reg(GYRO_CONFIG, GYRO_SCALE);
  Serial.begin(9600);
}
void loop(){
  unsigned long long current_time = millis();
  do {
    int c = Serial.read();
    if (c != -1 && c != 10) ctrl = c - 48;
  } while (!ctrl);
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
  Serial.print(accel_preproc(AcX));
  Serial.print("\t");
  Serial.print(accel_preproc(AcY));
  Serial.print("\t");
  Serial.print(accel_preproc(AcZ));
  Serial.print("\t");
  Serial.print(gyro_preproc(GyX));
  Serial.print("\t");
  Serial.print(gyro_preproc(GyY));
  Serial.print("\t");
  Serial.print(gyro_preproc(GyZ));
  Serial.print("\n");
  while(millis() < current_time + PERIOD) {
    ; // wait until PERIOD ms
  }
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

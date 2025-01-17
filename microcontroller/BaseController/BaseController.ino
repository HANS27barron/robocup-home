#include "Movement.h"
#include "RosBridge.h"
#include "BNO.h"
#include "Plot.h"

Movement *robot = nullptr;
bool ROS_ENABLE = true;
bool CHECK_PID = false;
bool CHECK_MOTORS = false;
bool CHECK_ENCODERS = false;

void setup() {
    Serial.begin(57600);
    Serial2.begin(57600);

    Movement initRobot;
    robot = &initRobot;
    robot->initEncoders();

    if (!ROS_ENABLE) {
        loop();
    }
    
    BNO bno;
    Plot plot(robot, ROS_ENABLE);
    // plot.startSequence();
    
    RosBridge bridge(robot, &bno, &plot);
    
    bridge.run();
}

// Used if ROS disabled.
void loop() {
    if (CHECK_PID) {
        Serial.begin(57600);
        // Check PID
        while(1) {
            Plot plot(robot, !ROS_ENABLE);
            delay(2000);
            plot.startSequence();
            // List of x Velocities
            double xVelocities[] = {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7};
            long long time = 0.0;
            int i = 0;
            bool sign = false;
            while(1) {
                if (millis() - time > 6000) {
                    time = millis();
                    if (sign) {
                      i++;
                      if (i == 7) {
                          i = 0;
                      }
                      sign = false;
                    }else {
                      sign = true;
                    }
                }
                robot->cmdVelocity(0.5, 0, 0);
                plot.plotTargetandCurrent();
            }
        }
    }
    if (CHECK_ENCODERS) {
        Serial.begin(9600);
        bool direction = false;
        long long start_time = millis();
        while(1) {
          if (millis() - start_time > 10*1000) {
            start_time = millis();
            direction = !direction;
            Serial.println("Direction Changed");
          }
          if (direction) {
            robot->back_left_motor_.changePwm(150);
            robot->back_left_motor_.forward();
            robot->front_left_motor_.changePwm(150);
            robot->front_left_motor_.forward();
            robot->back_right_motor_.changePwm(150);
            robot->back_right_motor_.forward();
            robot->front_right_motor_.changePwm(150);
            robot->front_right_motor_.forward();
          } else {
            robot->back_left_motor_.changePwm(150);
            robot->back_left_motor_.backward();
            robot->front_left_motor_.changePwm(150);
            robot->front_left_motor_.backward();
            robot->back_right_motor_.changePwm(150);
            robot->back_right_motor_.backward();
            robot->front_right_motor_.changePwm(150);
            robot->front_right_motor_.backward();
          }
               
          Serial.print("BL ");
          Serial.println( (robot->back_left_motor_.getEncodersDir()));
          Serial.print("FL ");
          Serial.println( (robot->front_left_motor_.getEncodersDir()));
          Serial.print("BR ");
          Serial.println( (robot->back_right_motor_.getEncodersDir()));
          Serial.print("FR ");
          Serial.println( (robot->front_right_motor_.getEncodersDir()));
          Serial.println("\n");
        }
    }
    
    if (CHECK_MOTORS) {
        Serial.begin(9600);
        // Check Motors
        while(1) {
          long long start = millis();
          robot->back_left_motor_.setPidTicks(0);
          robot->front_left_motor_.setPidTicks(0);
          robot->back_right_motor_.setPidTicks(0);
          robot->front_right_motor_.setPidTicks(0);
          while(millis()-start < 1000) {
              robot->back_left_motor_.changePwm(255);
              robot->back_left_motor_.forward();
              robot->front_left_motor_.changePwm(255);
              robot->front_left_motor_.forward();
              robot->back_right_motor_.changePwm(255);
              robot->back_right_motor_.forward();
              robot->front_right_motor_.changePwm(255);
              robot->front_right_motor_.forward();
          }
          robot->back_left_motor_.changePwm(0);
          robot->back_right_motor_.changePwm(0);
          robot->front_left_motor_.changePwm(0);
          robot->front_right_motor_.changePwm(0);
          Serial.print("BL");
          Serial.println( (robot->back_left_motor_.getPidTicks() / Motor::kPulsesPerRevolution) * 60 );
          Serial.print("FL");
          Serial.println( (robot->front_left_motor_.getPidTicks() / Motor::kPulsesPerRevolution) * 60 );
          Serial.print("BR");
          Serial.println( (robot->back_right_motor_.getPidTicks() / Motor::kPulsesPerRevolution) * 60 );
          Serial.print("FR");
          Serial.println( (robot->front_right_motor_.getPidTicks() / Motor::kPulsesPerRevolution) * 60 );
          delay(1000);
        }
    }
}

# Motion Detection using Raspberry Pi and Camera Module

## Introduction

This project demonstrates a lightweight motion detection system using the **Raspberry Pi Zero 2 W** and an **OV5647 camera module**. The motion detection is implemented using **background subtraction**, making it efficient enough to run on the limited resources of the Pi Zero.

### Potential Applications

- Motion detection sensor
- DIY security camera (expandable with notifications and local network storage)

---

## Hardware Requirements

- Raspberry Pi Zero 2 W
- Arducam 5MP OV5647 Camera Module (or compatible)

---

## Software Dependencies

- Python 3
- [Picamera2](https://github.com/raspberrypi/picamera2)
- [OpenCV](https://github.com/opencv/opencv-python)

Make sure to enable the camera interface on your Raspberry Pi (`raspi-config`) and install the required packages before running the project.


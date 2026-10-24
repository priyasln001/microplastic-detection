# Hardware Setup & Circuit Diagram

This document explains the hardware requirements and connections for building the Smart Microplastic Detection System.

## Main Control Unit (MCU)
- **Raspberry Pi 4 Model B (4GB/8GB)** OR **NVIDIA Jetson Nano (4GB)**. 
- *Note:* Jetson Nano is preferred for faster on-edge YOLOv8 inference, though RPi 4 is sufficient if processing via the cloud or using lower framerates.

## Hardware Components Required
1. **Camera Unit:** Raspberry Pi HQ Camera (with 16mm telephoto / macro lens) OR a Digital USB Microscope (e.g., 1000x magnification).
2. **Illumination:**
   - 365nm UV LED Strip / UV Ring Light (for Nile Red fluorescence).
   - 6000K White LED Ring Light (for standard sludge/waste imaging).
3. **Sensors (For Solid Waste Module):**
   - IR Breakbeam Sensor (Transmitter & Receiver).
4. **Relay Control:** 
   - 5V 2-Channel Relay Board (used to toggle UV and White LEDs programmatically).
5. **Sample Prep:**
   - Mini vacuum pump (for membrane filtration).
   - Heating plate (for sludge drying).

## Circuit Connections (Raspberry Pi Example)

### 1. Camera
- **Pi HQ Camera:** Connect the ribbon cable to the `CAMERA` CSI port on the Raspberry Pi.

### 2. Relay Module (Lighting Control)
The relay toggles between White LED and UV LED modes based on the software dashboard selection.
- **Relay VCC** -> Pi 5V (Pin 2 or 4)
- **Relay GND** -> Pi GND (Pin 6)
- **Relay IN1** (Controls UV LED) -> Pi GPIO 17 (Pin 11)
- **Relay IN2** (Controls White LED) -> Pi GPIO 27 (Pin 13)

*Powering LEDs:* Connect the positive terminal of the 12V external power supply to the COM terminal of the relays. Connect the NO (Normally Open) terminals to the respective LED positive leads. Ground the LEDs to the external power supply ground.

### 3. IR Breakbeam Sensor (Solid Waste Trigger)
- **Transmitter (Tx):** Connect to a 5V power source and Ground.
- **Receiver (Rx):** 
  - VCC -> Pi 3.3V (Pin 1) or 5V (depending on sensor logic level, use level shifter if 5V Rx sends 5V signals to 3.3V Pi GPIO).
  - GND -> Pi GND (Pin 9)
  - Data / OUT -> Pi GPIO 22 (Pin 15)

## Simulated 3D Structure Design
Due to the optical nature of the system, a darkroom enclosure is necessary for the **Water Module**.
1. **Housing:** An opaque, matte-black acrylic box (approx. 20x20x30 cm) to block external light.
2. **Sample Stage:** A motorized or manual multi-axis stage at the bottom to hold the 47mm membrane filter.
3. **Optics Mount:** The Pi HQ Camera is mounted facing straight down (nadir view) onto the filter.
4. **Lighting:** The RGB/White ring light and UV strip are mounted in a circular array around the camera lens, angled inwards at 45 degrees to prevent harsh specular reflection on the filter surface.

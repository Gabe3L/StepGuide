# StepGuide

StepGuide is an AI-powered wearable assistant designed as an innovative replacement for traditional guide dogs. Built during SpurHacks 2025 (Startup Track), StepGuide empowers individuals with visual impairments to navigate their environments and daily tasks independently, reliably, and affordably.

## Inspiration

Guide dogs are life-changing for many, but they are expensive, require training and care, and aren't accessible to everyone. StepGuide aims to democratize mobility assistance through modern AI and embedded computing.

---

## What It Does

StepGuide is a real-time AI assistant that:

- Detects and identifies objects (cars, people, toothbrushes, etc.) using YOLOv8
- Reads text aloud using OCR and Text-To-Speech (TTS)
- Provides real-time spatial and situational guidance via a wireless earbud
- Enables users to navigate unfamiliar environments safely and confidently

---

## Tech Stack

### Hardware:
- Jetson Orin Nano (edge AI computing)
- 30,000mAh Battery Pack (12–18 hrs runtime)
- Wireless Bluetooth Earbud (audio output)

### Software:
- YOLOv11 for real-time object detection
- OCR for text recognition
- Coqui TTS for speech synthesis
- Python, PyTorch, OpenCV, NumPy

---

## Features

- Object Detection:
  - Trained to recognize 80+ objects including:
    - Vehicles (cars, buses)
    - People
    - Household items (toothbrushes, bottles, doors, etc.)
- Natural Language Descriptions:
  - Spatial context (e.g., "Car approaching from the left")
- OCR + TTS:
  - Reads signs, menus, and labels aloud
- Efficient Power Design:
  - Optimized for low-latency and low-power inference

---

## Team

Made with at SpurHacks 2025 by:

- Gabe Lynch
- Alex
- Owen Ramsey
- Yasin

---

## Installation (For Development)

1. Flash Jetson Orin Nano with JetPack 6
2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install torch torchvision opencv-python pytesseract coqui-tts ultralytics
   ```
3. Clone the repo and run:
   ```bash
   python3 -m main
   ```

---

## Future Plans

- Add navigation with GPS and SLAM
- Integrate with smartphones for UI and settings
- Expand dataset for more specific object classes

---

## License

This project is open-source under the MIT License.

---

## Acknowledgements

Special thanks to SpurHacks 2025 organizers and for hosting an amazing event.
# System Architecture & Workflow Diagrams

This document contains visual representations of the system logic.

## 1. Physical Hardware Layout
```mermaid
graph LR
    subgraph Enclosure
        CAM[Pi HQ Camera]
        UV[UV LED 365nm]
        WHT[White LED]
        SMP[Filter Sample]
    end
    
    subgraph Processing Unit
        PI[Raspberry Pi 4 / Jetson Nano]
        RLY[Relay Board]
    end
    
    PI -->|GPIO Trigger| RLY
    RLY -->|12V Power| UV
    RLY -->|12V Power| WHT
    CAM -->|CSI Ribbon Cable| PI
    SMP -.->|Photon Feed| CAM
```

## 2. Software Execution Sequence
```mermaid
sequenceDiagram
    participant User
    participant Streamlit
    participant Hardware
    participant AI_Model
    
    User->>Streamlit: Configure Lighting (UV)
    Streamlit->>Hardware: GPIO toggle (Relay 1 ON)
    User->>Streamlit: Trigger "Capture"
    Hardware->>Streamlit: Image Frame (CSI/USB)
    Streamlit->>AI_Model: Preprocessed Image (640x640)
    AI_Model->>AI_Model: YOLOv8 Forward Pass
    AI_Model->>Streamlit: BBox Coords + Class IDs
    Streamlit->>User: Display Heatmap & Particle Count
```

## 3. Solid Waste Detection Logic
```mermaid
flowchart TD
    A[Start Conveyor] --> B{IR Beam Broken?}
    B -- No --> B
    B -- Yes --> C[Capture RGB Frame]
    C --> D[Identify Material Type]
    D --> E{Plastic Detected?}
    E -- No --> A
    E -- Yes --> F[Assess Degradation Pattern]
    F --> G[Calculate Shedding Risk Score]
    G --> H[Update IoT Dashboard]
    H --> A
```

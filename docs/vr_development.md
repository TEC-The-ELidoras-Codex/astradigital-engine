# The Elidoras Codex - VR Development

![TEC Logo](assets/images/tec_logo.png)

## 🌌 AstraDigital Ocean in VR

This extension to the AstraDigital Engine enables visualization & interaction with The Elidoras Codex universe in Virtual Reality on Meta Quest devices.

## ✨ Features

- **Unity Integration**: Seamless bridge between AstraDigital Engine & Unity projects
- **MetaQuest Support**: Build & deploy to Meta Quest VR headsets
- **Live World Preview**: See your TEC world come to life in immersive VR
- **Data Synchronization**: Visualize real-time changes to the AstraDigital Ocean
- **Development Workflow**: Complete toolchain for VR content creation

## 🚀 Getting Started

### Prerequisites

- Unity 2022.3 or newer with Android Build Support
- Meta Quest Developer Account
- Meta Quest 2/3 headset (optional, but recommended for testing)
- Android SDK Platform Tools (for ADB communication)

### Setup

1. Set up the VR development environment:

```bash
# Setup complete VR environment
python tec_vr_tools.py setup --unity --metaquest --sample-data
```

2. Open the created Unity project in Unity Hub (location will be displayed in setup output)

3. Install required Unity packages:
   - Oculus Integration (from Asset Store)
   - XR Interaction Toolkit (via Package Manager)
   - XR Plugin Management (via Package Manager)

4. Configure XR Plugin Management for Oculus/Meta Quest

### Workflow

#### Exporting TEC World Data to Unity

```bash
# Export current AstraDigital Ocean state to Unity
python tec_vr_tools.py export
```

#### Managing MetaQuest Devices

```bash
# List connected MetaQuest devices
python tec_vr_tools.py device list
```

#### Building & Deploying to MetaQuest

```bash
# Build & deploy to connected MetaQuest device
python tec_vr_tools.py build
```

## 📚 Documentation

### Project Structure

```
astradigital-engine/
  ├── unity_projects/      # Unity projects directory
  │   └── tec_vr/          # Main TEC VR project
  │       ├── Assets/
  │       │   ├── AstradigitalData/ # Exported TEC data
  │       │   └── Scripts/  # Unity C# scripts
  │       └── METAQUEST_SETUP.md  # Setup instructions
  │
  ├── builds/              # Build outputs
  │   └── metaquest/       # MetaQuest APK builds
  │
  ├── src/
  │   └── utils/
  │       ├── unity_integration.py  # Unity bridge
  │       └── metaquest_dev.py  # MetaQuest tools
  │
  └── tec_vr_tools.py      # CLI tool for VR dev
```

### Integration Architecture

The VR integration uses a data-driven approach:

1. **AstraDigital Engine** manages core TEC world data
2. **Unity Bridge** exports this data to Unity-compatible format
3. **Unity Visualization** renders & enables interaction with world data
4. **MetaQuest Deployment** brings the experience to VR

## 🛠️ Development Guidelines

### Adding New VR Features

1. First implement new data structures in AstraDigital Engine
2. Update the Unity bridge to export the new data
3. Create/update Unity scripts to visualize the data
4. Test in editor before deploying to device

### Performance Optimization

- Keep polygon counts low for VR performance
- Use occlusion culling & level of detail (LOD)
- Batch rendering where possible
- Target 90fps for comfortable VR experience

## 🔮 Future Enhancements

- [ ] Real-time collaborative editing in VR
- [ ] Voice commands via MetaQuest microphone
- [ ] Hand tracking for intuitive world manipulation
- [ ] Spatial audio for immersive experiences
- [ ] Mixed reality mode for blending TEC with physical world

## 📝 License

This project is licensed under the terms of the included LICENSE file.

---

*The Astradigital Ocean awaits your exploration in virtual reality...*

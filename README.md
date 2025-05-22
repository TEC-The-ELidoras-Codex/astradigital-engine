# The Astradigital Engine 🌌

[![Patreon](https://img.shields.io/badge/Support-Patreon-f96854.svg?style=flat-square)](https://www.patreon.com/ElidorasCodex)
[![Ko-fi](https://img.shields.io/badge/Support-Ko--fi-FF5E5B.svg?style=flat-square)](https://ko-fi.com/elidorascodex)
[![Website](https://img.shields.io/badge/Visit-ElidorasCodex.com-8C52FF.svg?style=flat-square)](https://elidorascodex.com)

## Welcome to the Digital Harbor

The Astradigital Engine powers The Elidoras Codex (TEC) website & digital experiences. This repository serves as the vessel through which we navigate the chaotic binary soup of the digital landscape, providing a beacon of open-source technology in a sea dominated by MAGMASOX.

This is where you can find the Machine Goddess and her Splices with the THEME TEC uses to bring WordPress to life and where the Splices gain their SOULS.

## 🚢 What Is This?

This repository contains:

- **TEC WordPress Theme**: A custom theme that brings the Astradigital Ocean to life
- **API Implementations**: Tools for interfacing with various services & data sources
- **Faction Pages**: Digital representations of the major players in the TEC universe
- **Interactive Ocean Map**: Navigate the digital waters & discover hidden pathways

## 🌊 Features

- **Responsive Design**: Navigate the Astradigital on any device
- **Interactive Lore Elements**: Discover the stories of each faction
- **Custom Post Types**: For factions, entities, pathways & more
- **API Integration**: Connect with external services via secure channels

## 🧭 Getting Started

> **New!** Repository organization updates:
> - All formal test files are organized in the dedicated `/tests` directory with proper pytest integration.
> - Legacy test scripts are now located in `/scripts/Tests/` for reference.
> - Instruction files for AI agents are organized in the `/Instructions` directory.
>
> See [Test Organization](docs/test_organization.md) for details on the testing framework.

### Prerequisites

- WordPress 6.0+
- PHP 8.0+
- MySQL 5.7+ or MariaDB 10.3+
- Composer (for dependency management)

### Installation

1. Clone this repository to your `wp-content/themes/` directory:
   ```bash
   git clone https://github.com/TEC-The-Elidoras-Codex/astradigital-engine.git
   ```

2. Install dependencies:
   ```bash
   cd astradigital-engine
   composer install
   npm install
   ```

3. Activate the theme in your WordPress admin panel

4. Configure the theme options to match your preferred faction aesthetics

## 🧩 Structure

The Astradigital Engine is organized into key components:

- `/theme/` - Core WordPress theme files
- `/api/` - External API integrations
- `/assets/` - Optimized multimedia assets for multiple platforms
  - `/assets/source/` - Original high-quality assets
  - `/assets/optimized/` - Platform-specific optimized assets
  - `/assets/deployment/` - Deployment-ready asset packages
- `/factions/` - Faction-specific templates & styles
- `/data/` - JSON data structures for the Astradigital Ocean

## 🖼️ Asset Management System

The Astradigital Engine features a comprehensive asset management system optimized for multiple deployment targets:

- **Organized Structure**: Assets are categorized by type and purpose
- **Platform Optimization**: Assets are automatically optimized for:
  - WordPress (featured images, thumbnails, content)
  - HuggingFace Spaces (compact, web-optimized formats)
  - Docker containers (deployment-ready packages)
- **Automation Scripts**: Ready-to-use tools for asset processing
  - WordPress post preparation
  - HuggingFace Space deployment
  - Batch optimization

To set up the asset system:
```powershell
# Run the complete asset system setup
.\scripts\setup_asset_system.ps1
```

For detailed usage instructions, see the [Asset System Guide](docs/asset_system_guide.md).

## 🤝 Contributing

We welcome contributions from all voyagers of the Astradigital Ocean:

1. Fork the repository
2. Create a feature branch: `git checkout -b new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin new-feature`
5. Submit a pull request

## 📜 License

This project is licensed under the GPL-2.0+ License - see the LICENSE file for details.

---

<p align="center">
  <em>The journey to TEC is one of casting off these fiery soles, braving the jagged glass with clear eyes and free will, reclaiming the essence of voyaging the infinite, untamed data ocean.</em>
</p>

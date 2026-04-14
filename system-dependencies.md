# System Dependencies for Harness Books

This document lists the external system dependencies required to build and export Harness Books.

## Overview

The build system requires several binary tools for different tasks:
- **EPUB Export**: Convert Markdown to EPUB format with cover images
- **Diagram Generation** (optional): Regenerate PNG diagrams from PlantUML sources
- **Website Build**: Generate static HTML site

## Dependencies by Task

### EPUB Export (`tools/book-kit/export_epub.py`)

| Tool | Minimum Version | Purpose | Tested Version |
|------|----------------|---------|----------------|
| **pandoc** | 3.9.0 | Convert Markdown to EPUB | 3.9.0.2 |
| **librsvg** | 2.62 | `rsvg-convert` for SVG cover images | 2.62.1 |
| **poppler** | 26.0 | `pdftoppm` for PDF cover images | 26.02.0 |

### Diagram Generation (optional, for `--clean-generated` flag)

| Tool | Purpose | Notes |
|------|---------|-------|
| **plantuml** | Generate PNG from `.puml` files | Requires Java runtime |

### Website Build (`tools/book-kit/build_honkit.py`)

| Tool | Purpose |
|------|---------|
| **Node.js** with **honkit** | Build static HTML site |

## Installation Methods

### Recommended: Conda Environment

Create a conda environment with all EPUB tools:

```bash
conda create -n epub pandoc librsvg poppler -c conda-forge
conda activate epub
```

### Ubuntu/Debian

```bash
sudo apt-get install pandoc librsvg2-bin poppler-utils plantuml
```

### macOS (Homebrew)

```bash
brew install pandoc librsvg poppler plantuml
```

### Node.js/honkit

```bash
npm install -g honkit
```

## Python Dependencies

All Python scripts in this project use only the standard library. No external Python packages are required.

The `requirements.txt` file exists only to clarify this point and redirect to this document.

## Verification

After installation, verify the tools are available:

```bash
# Check versions
pandoc --version | head -1
rsvg-convert --version 2>&1 | head -1
pdftoppm -v 2>&1 | head -1
```

## Troubleshooting

### `pandoc` not found
- Ensure pandoc is installed and in your PATH
- If using conda, activate the environment: `conda activate epub`

### `rsvg-convert` not found
- On Ubuntu/Debian, install `librsvg2-bin`
- On macOS with Homebrew, install `librsvg`

### `pdftoppm` not found  
- On Ubuntu/Debian, install `poppler-utils`
- On macOS with Homebrew, install `poppler`

### `plantuml` not found
- Install PlantUML from your package manager
- Ensure Java runtime is installed

# ASCII Cam

A Python application that captures video from a webcam, converts it to ASCII art in real-time, and outputs it to a window or a virtual camera device.

## Features

- Real-time ASCII art conversion of webcam feed.
- Multiple ASCII rendering modes:
    - `colored`: Full color from the original video.
    - `grayscale`: Characters are rendered in shades of gray.
    - `black-and-white`: High-contrast black and white.
    - `matrix`: A configurable "digital rain" effect overlaid on a green-tinted ASCII video. The rain can be made of random characters or custom words.
- Adjustable output resolution and ASCII character density.
- Output to a regular window or a virtual camera.
- Cross-platform (tested on macOS).

## Installation

First, install the required Python libraries:

```bash
make install
```

## Usage

This project uses a `Makefile` to provide convenient shortcuts for common commands.

```bash
# Run with default settings (colored ASCII, output to a window)
make run

# Run with the classic "digital rain" matrix effect
make matrix

# Run with custom falling words in the matrix effect
# (You can edit the words directly in the Makefile)
make matrix-words

# Run with a sparse matrix effect
make matrix-sparse

# Run in high resolution
make high-res

# Run with the virtual camera output
make virtual-cam

# See all available command-line options
make help
```

For more advanced configurations, you can run `main.py` directly. Use `make help` to see all the possible flags.

---

## Virtual Camera Setup on macOS

To use the virtual camera feature (`make virtual-cam`), you need an application to provide the virtual camera backend. This is a **one-time setup**. We recommend using the free and open-source OBS Studio.

**Step 1: Download and Install OBS Studio**

1.  Go to [obsproject.com](https://obsproject.com/) and download the installer for macOS.
2.  Install OBS Studio by dragging it to your Applications folder.

**Step 2: Start the OBS Virtual Camera**

1.  Open OBS Studio. You do not need to configure any scenes or sources.
2.  In the "Controls" dock (usually in the bottom right), click **Start Virtual Camera**.
3.  The virtual camera is now running. You can minimize the OBS Studio window.

**Step 3: Run ASCII Cam**

Now, simply run:
```bash
make virtual-cam
```

**Step 4: Select the Camera in Other Apps**

1.  In your target application (e.g., Zoom, Google Meet), go to video settings and choose **"OBS Virtual Camera"** as your webcam.

To stop the virtual camera, open OBS again and click **Stop Virtual Camera**.

# Retail Entrance Analytics

A computer vision pipeline for analyzing retail CCTV footage and counting unique customer entries using object detection, multi-object tracking, geometric entrance validation, and OCR-based CCTV timestamp extraction.

## Demo

![Entrance Detection and Tracking](docs/entry_001_ID_1.jpg)

The system detects and tracks people, validates entrance crossings, extracts the CCTV timestamp using OCR, and records confirmed entry events.

## Pipeline

```text
CCTV Video
     │
     ▼
YOLOv8 Person Detection
     │
     ▼
ByteTrack Multi-Object Tracking
     │
     ▼
Track ID + Bounding Box
     │
     ▼
Entrance Line Geometry
     │
     ▼
Per-Track Entry State Machine
     │
     ├── Outside
     ├── Crossing
     └── Fully Inside
              │
              ▼
       Entry Confirmation
              │
        ┌─────┴─────┐
        ▼           ▼
    PaddleOCR    Screenshot
        │           │
        ▼           ▼
 CCTV Timestamp   Entry Frame
        │
        └─────┬─────┘
              ▼
          CSV Event Log
```

## Key Features

* YOLOv8 person detection
* ByteTrack multi-object tracking
* Persistent track IDs
* Configurable entrance line
* Geometric line-crossing analysis
* Bounding-box based entry validation
* Consecutive-frame confirmation
* Duplicate counting prevention
* PaddleOCR CCTV timestamp extraction
* Automatic entry screenshots
* CSV event logging
* OpenCV-based video processing and visualization

## Entry Detection Logic

A person is not counted simply because their bounding box crosses the entrance line.

The system validates the complete transition of the tracked person:

1. Person is detected by YOLOv8.
2. ByteTrack assigns a persistent tracking ID.
3. The person's bounding-box position is evaluated relative to the entrance line.
4. The system checks whether the person becomes fully inside the defined entrance region.
5. The condition must remain valid for a configurable number of consecutive frames.
6. The track is counted only once.
7. The corresponding frame is saved as an entry screenshot.
8. PaddleOCR extracts the CCTV timestamp from the original frame.
9. The event is recorded in the CSV output.

This approach helps reduce false positives caused by:

* People standing near the doorway
* Partial line crossings
* People walking past the entrance
* Temporary detector movement
* People already inside when processing starts

## Technologies

| Component             | Technology |
| --------------------- | ---------- |
| Programming           | Python     |
| Object Detection      | YOLOv8     |
| Multi-Object Tracking | ByteTrack  |
| OCR                   | PaddleOCR  |
| Video Processing      | OpenCV     |
| Data Logging          | CSV        |
| Numerical Processing  | NumPy      |

## Project Structure

```text
retail-entrance-analytics/
│
├── docs/
│   └── entry_001_ID_1.jpg
│
├── entrance_count.py
├── README.md
└── requirements.txt
```

## Installation

Create a Python environment and install the dependencies:

```bash
pip install -r requirements.txt
```

The project uses YOLOv8 and PaddleOCR for detection and timestamp extraction.

## Usage

Run the pipeline with a CCTV video:

```bash
python entrance_count.py --video input_video/your_video.mp4
```

The application will:

* Open the CCTV video
* Allow the entrance line to be configured
* Detect and track people
* Validate entrance events
* Extract CCTV timestamps
* Save entry screenshots
* Generate a CSV event log
* Generate an annotated output video

## Output

For each confirmed entry, the system can generate:

```text
output/
├── entrance_annotated.mp4
├── entrance_counts.csv
└── entry_screenshots/
    ├── entry_001_ID_1.jpg
    ├── entry_002_ID_3.jpg
    └── ...
```

The CSV contains information such as:

* Entry number
* Track ID
* Video frame
* Video time
* CCTV date
* CCTV time
* CCTV datetime
* OCR text
* Screenshot filename

## Computer Vision Approach

The project combines several CV components rather than relying on a single detection model.

### Detection

YOLOv8 detects people in each video frame.

### Tracking

ByteTrack maintains identities across frames so that the same person can be followed throughout the scene.

### Spatial Reasoning

The entrance is represented using a configurable line and an inside reference point. Bounding-box geometry is used to determine whether a person has actually moved into the store.

### Temporal Validation

Entry events require the person to remain fully inside for multiple consecutive frames. This reduces false positives caused by momentary detections or people passing close to the entrance.

### OCR

PaddleOCR reads the CCTV timestamp directly from the original video frame. The extracted timestamp is associated with the confirmed entry event.

## Privacy

The repository does not include the original CCTV video or generated CCTV footage. The demo image is provided only to illustrate the computer vision output.

## Author

**Abinand A**

AI/ML Engineer | Computer Vision | Generative AI

GitHub: [abinand5769](https://github.com/abinand5769)

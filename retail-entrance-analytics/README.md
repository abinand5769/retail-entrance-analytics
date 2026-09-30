# Retail Entrance People Counter (CCTV)

Counts **unique people who fully enter a shop** from CCTV footage, and logs the **on-screen CCTV date/time** for every entry.

Built with **YOLOv8 + ByteTrack + PaddleOCR + OpenCV**.

## What it does

- Detects people in every frame (YOLOv8) and gives each one a persistent ID (ByteTrack).
- You draw a virtual **entrance line** once, with mouse clicks.
- A person is counted **only when their whole body is inside the shop** (head *and* feet past the line) for several frames in a row - not when they are just standing in the doorway.
- People who are already inside at the start, or walking past outside, are **not** counted.
- Each entry is counted **once per person**.
- For every entry it reads the **CCTV timestamp** burned into the video with OCR and saves:
  - an annotated video,
  - a CSV log,
  - a screenshot of the entry moment.

## How it works

| Stage | Technique |
|---|---|
| Person detection | YOLOv8 (`yolov8s.pt`, COCO class 0) |
| Multi-object tracking | ByteTrack (via Ultralytics) |
| Line crossing | Signed distance from each bounding-box corner to the line (cross product) |
| Entry decision | Per-track state machine: *armed* (seen outside/crossing) then *fully inside for N frames* then count once |
| CCTV time | Crop timestamp region, upscale 2x, PaddleOCR (DB text detection + recognition), regex parsing |
| OCR fallback | First-frame timestamp + elapsed video time |

### Entry logic

```
fully_inside  = every corner of the person's box is past the line
fully_outside = every corner is before the line

first seen fully inside                  -> never counted
first seen outside / crossing            -> armed
armed AND fully_inside for 5 frames      -> COUNT (once per track ID)
```

Main settings (top of `entrance_count.py`):

| Setting | Meaning |
|---|---|
| `FULL_INSIDE_MARGIN` | Pixels past the line every corner must be |
| `CONFIRM_FRAMES` | Consecutive fully-inside frames needed |
| `CONF_THRES` | YOLO detection confidence |
| `TIMESTAMP_ROI` | Where the CCTV timestamp is on screen |

## Setup

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
```

`yolov8s.pt` is downloaded automatically on first run.

## Usage

1. Put your video in `input_video/` (footage is not included in this repo for privacy).
2. Run:

```bash
python entrance_count.py input_video/your_video.mp4
```

3. In the window that opens:
   1. Click **2 points** along the shop entrance (threshold) to define the line.
   2. Click **1 point inside the shop**.
   3. Press **ENTER** to start. (`R` = reset, `ESC` = cancel.)

## Output

Written to `output/`:

- `entrance_annotated.mp4` - video with boxes, IDs, `IN/OUT/CROSSING` status, live counter
- `entrance_counts.csv` - one row per entry
- `entry_screenshots/` - one image per entry

CSV columns: `Entry Number, Track ID, Video Frame, Video Time, CCTV Date, CCTV Time, CCTV DateTime, OCR Text, Screenshot`

## Project structure

```
.
├── entrance_count.py     # main script
├── requirements.txt
├── input_video/          # put your videos here (git-ignored)
├── output/               # generated results (git-ignored)
└── docs/                 # demo GIF / screenshots for this README
```

## Demo

Add a short GIF or screenshot here (faces blurred - see the note below):

```
![demo](docs/demo.gif)
```

## Limitations

- Accuracy depends on where the entrance line is drawn (draw it at the shop threshold).
- Heavy occlusion can cause a track ID switch; the "armed" rule limits false counts from this.
- Counts entries only, not exits.
- The OCR region (`TIMESTAMP_ROI`) must match the timestamp position of your camera.

## Privacy note

CCTV footage shows real people. The raw video and generated screenshots are **not** included in this repository. If you add a demo, blur faces first.

## Tech stack

Python, OpenCV, Ultralytics YOLOv8, ByteTrack, PaddleOCR, NumPy

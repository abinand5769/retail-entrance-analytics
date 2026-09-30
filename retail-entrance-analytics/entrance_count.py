# import os
# import csv
# import re
# import cv2
# import numpy as np

# from ultralytics import YOLO
# from paddleocr import PaddleOCR


# # ============================================================
# # CONFIG
# # ============================================================

# INPUT_VIDEO = r"C:\Users\user\Desktop\task_1\input video\cropped_03m02s_to_03m20s.mp4"

# OUTPUT_DIR = r"C:\Users\user\Desktop\task_1\output"

# OUTPUT_VIDEO = os.path.join(
#     OUTPUT_DIR,
#     "entrance_annotated.mp4"
# )

# OUTPUT_CSV = os.path.join(
#     OUTPUT_DIR,
#     "entrance_counts.csv"
# )

# SCREENSHOT_DIR = os.path.join(
#     OUTPUT_DIR,
#     "entry_screenshots"
# )

# # YOLO model
# MODEL_PATH = "yolov8s.pt"

# # Detection confidence
# CONF_THRES = 0.40

# # COCO class 0 = person
# PERSON_CLASS_ID = 0


# # ============================================================
# # CREATE OUTPUT DIRECTORIES
# # ============================================================

# os.makedirs(OUTPUT_DIR, exist_ok=True)
# os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# # ============================================================
# # INITIALIZE OCR
# # ============================================================

# print("Loading PaddleOCR...")

# ocr = PaddleOCR(
#     use_angle_cls=True,
#     lang="en",
#     ocr_version="PP-OCRv4",
#     use_space_char=True,
#     det_db_thresh=0.1,
#     det_db_box_thresh=0.1
# )

# print("PaddleOCR loaded.")


# # ============================================================
# # LINE SELECTION VARIABLES
# # ============================================================

# line_points = []

# inside_point = None


# # ============================================================
# # MOUSE CALLBACK
# # ============================================================

# def mouse_callback(event, x, y, flags, param):

#     global line_points
#     global inside_point

#     if event == cv2.EVENT_LBUTTONDOWN:

#         # First two clicks = entrance line
#         if len(line_points) < 2:

#             line_points.append((x, y))

#             print(
#                 f"Line point {len(line_points)}: "
#                 f"({x}, {y})"
#             )

#         # Third click = inside point
#         elif inside_point is None:

#             inside_point = (x, y)

#             print(
#                 f"Inside point: "
#                 f"({x}, {y})"
#             )


# # ============================================================
# # SELECT ENTRANCE LINE
# # ============================================================

# def select_line(video_path):

#     global line_points
#     global inside_point

#     cap = cv2.VideoCapture(video_path)

#     if not cap.isOpened():
#         raise RuntimeError(
#             f"Could not open video:\n{video_path}"
#         )

#     ret, first_frame = cap.read()

#     cap.release()

#     if not ret:
#         raise RuntimeError(
#             "Could not read first frame."
#         )

#     original_frame = first_frame.copy()

#     window_name = (
#         "ENTRANCE LINE | "
#         "2 clicks=line | "
#         "3rd click=INSIDE | "
#         "ENTER=confirm | "
#         "R=reset | "
#         "ESC=cancel"
#     )

#     cv2.namedWindow(window_name)

#     cv2.setMouseCallback(
#         window_name,
#         mouse_callback
#     )

#     print()
#     print("=" * 60)
#     print("DRAW ENTRANCE LINE")
#     print("=" * 60)
#     print("1. Click first point of entrance line")
#     print("2. Click second point of entrance line")
#     print("3. Click somewhere INSIDE the shop")
#     print("4. Press ENTER")
#     print("5. Press R to reset")
#     print("6. Press ESC to cancel")
#     print("=" * 60)
#     print()

#     while True:

#         display = original_frame.copy()

#         # Draw line points
#         for point in line_points:

#             cv2.circle(
#                 display,
#                 point,
#                 6,
#                 (0, 0, 255),
#                 -1
#             )

#         # Draw entrance line
#         if len(line_points) == 2:

#             cv2.line(
#                 display,
#                 line_points[0],
#                 line_points[1],
#                 (0, 255, 255),
#                 3
#             )

#             cv2.putText(
#                 display,
#                 "ENTRANCE LINE",
#                 (
#                     line_points[0][0],
#                     max(30, line_points[0][1] - 10)
#                 ),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7,
#                 (0, 255, 255),
#                 2
#             )

#         # Draw inside point
#         if inside_point is not None:

#             cv2.circle(
#                 display,
#                 inside_point,
#                 8,
#                 (255, 0, 0),
#                 -1
#             )

#             cv2.putText(
#                 display,
#                 "INSIDE",
#                 (
#                     inside_point[0] + 10,
#                     inside_point[1]
#                 ),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7,
#                 (255, 0, 0),
#                 2
#             )

#         # Instructions
#         cv2.putText(
#             display,
#             "2 clicks = LINE | 3rd click = INSIDE | ENTER = CONFIRM | R = RESET",
#             (10, 30),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.55,
#             (0, 255, 0),
#             2
#         )

#         cv2.imshow(
#             window_name,
#             display
#         )

#         key = cv2.waitKey(20) & 0xFF

#         # Reset
#         if key == ord("r"):

#             line_points = []
#             inside_point = None

#             print("Points reset.")

#         # Enter
#         elif key in (13, 10):

#             if (
#                 len(line_points) == 2
#                 and inside_point is not None
#             ):

#                 print("Line confirmed.")

#                 break

#             else:

#                 print(
#                     "Please select 2 line points "
#                     "and 1 inside point."
#                 )

#         # ESC
#         elif key == 27:

#             cv2.destroyWindow(window_name)

#             raise SystemExit(
#                 "Cancelled by user."
#             )

#     cv2.destroyWindow(window_name)

#     return (
#         line_points[0],
#         line_points[1],
#         inside_point
#     )


# # ============================================================
# # SIDE OF LINE
# # ============================================================

# def side_of_line(
#     point,
#     line_a,
#     line_b
# ):

#     ax, ay = line_a
#     bx, by = line_b

#     px, py = point

#     value = (
#         (bx - ax) * (py - ay)
#         -
#         (by - ay) * (px - ax)
#     )

#     return value


# # ============================================================
# # DRAW DASHED LINE
# # ============================================================

# def draw_dashed_line(
#     image,
#     pt1,
#     pt2,
#     color,
#     thickness=2,
#     dash_len=15
# ):

#     distance = int(
#         np.hypot(
#             pt2[0] - pt1[0],
#             pt2[1] - pt1[1]
#         )
#     )

#     if distance == 0:
#         return

#     for i in range(
#         0,
#         distance,
#         dash_len * 2
#     ):

#         r0 = i / distance

#         r1 = min(
#             i + dash_len,
#             distance
#         ) / distance

#         p0 = (
#             int(
#                 pt1[0]
#                 +
#                 (pt2[0] - pt1[0]) * r0
#             ),
#             int(
#                 pt1[1]
#                 +
#                 (pt2[1] - pt1[1]) * r0
#             )
#         )

#         p1 = (
#             int(
#                 pt1[0]
#                 +
#                 (pt2[0] - pt1[0]) * r1
#             ),
#             int(
#                 pt1[1]
#                 +
#                 (pt2[1] - pt1[1]) * r1
#             )
#         )

#         cv2.line(
#             image,
#             p0,
#             p1,
#             color,
#             thickness
#         )


# # ============================================================
# # DRAW CORNER BOX
# # ============================================================

# def draw_corner_box(
#     image,
#     x1,
#     y1,
#     x2,
#     y2,
#     color,
#     thickness=2
# ):

#     width = x2 - x1
#     height = y2 - y1

#     lw = int(width * 0.25)
#     lh = int(height * 0.25)

#     # Top left
#     cv2.line(
#         image,
#         (x1, y1),
#         (x1 + lw, y1),
#         color,
#         thickness
#     )

#     cv2.line(
#         image,
#         (x1, y1),
#         (x1, y1 + lh),
#         color,
#         thickness
#     )

#     # Top right
#     cv2.line(
#         image,
#         (x2, y1),
#         (x2 - lw, y1),
#         color,
#         thickness
#     )

#     cv2.line(
#         image,
#         (x2, y1),
#         (x2, y1 + lh),
#         color,
#         thickness
#     )

#     # Bottom left
#     cv2.line(
#         image,
#         (x1, y2),
#         (x1 + lw, y2),
#         color,
#         thickness
#     )

#     cv2.line(
#         image,
#         (x1, y2),
#         (x1, y2 - lh),
#         color,
#         thickness
#     )

#     # Bottom right
#     cv2.line(
#         image,
#         (x2, y2),
#         (x2 - lw, y2),
#         color,
#         thickness
#     )

#     cv2.line(
#         image,
#         (x2, y2),
#         (x2, y2 - lh),
#         color,
#         thickness
#     )


# # ============================================================
# # OCR
# # ============================================================

# def run_ocr_on_frame(frame):

#     """
#     Run PaddleOCR on the exact frame where
#     the person entered.
#     """

#     try:

#         result = ocr.ocr(
#             frame,
#             cls=True
#         )

#         if not result or not result[0]:

#             return []

#         extracted_text = []

#         for item in result[0]:

#             try:

#                 text_value = item[1][0]
#                 confidence = float(item[1][1])

#                 extracted_text.append(
#                     (
#                         text_value,
#                         confidence
#                     )
#                 )

#             except Exception:

#                 continue

#         return extracted_text

#     except Exception as e:

#         print(
#             "OCR error:",
#             e
#         )

#         return []


# # ============================================================
# # EXTRACT CCTV DATE / TIME
# # ============================================================

# def extract_datetime(ocr_results):

#     """
#     Try to find date and time from OCR text.

#     Supports common CCTV formats such as:

#     2026-09-30 12:35:42
#     30-09-2026 12:35:42
#     30/09/2026 12:35:42
#     2026/09/30 12:35:42
#     30.09.2026 12:35:42
#     12:35:42
#     """

#     all_text = " ".join(
#         text for text, confidence in ocr_results
#     )

#     # Normalize OCR mistakes
#     normalized = all_text

#     normalized = normalized.replace(
#         "O",
#         "0"
#     )

#     normalized = normalized.replace(
#         "o",
#         "0"
#     )

#     normalized = normalized.replace(
#         "|",
#         "1"
#     )

#     # --------------------------------------------------------
#     # Date + time
#     # --------------------------------------------------------

#     datetime_patterns = [

#         r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}"
#         r"\s+"
#         r"\d{1,2}:\d{2}:\d{2}\b",

#         r"\b\d{1,2}[-/.]\d{1,2}[-/.]\d{4}"
#         r"\s+"
#         r"\d{1,2}:\d{2}:\d{2}\b",

#         r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}"
#         r"\s+"
#         r"\d{1,2}:\d{2}\b",

#         r"\b\d{1,2}[-/.]\d{1,2}[-/.]\d{4}"
#         r"\s+"
#         r"\d{1,2}:\d{2}\b",
#     ]

#     for pattern in datetime_patterns:

#         match = re.search(
#             pattern,
#             normalized
#         )

#         if match:

#             value = match.group(0)

#             # Separate date/time
#             parts = value.split()

#             if len(parts) >= 2:

#                 return (
#                     parts[0],
#                     parts[1],
#                     value
#                 )

#     # --------------------------------------------------------
#     # Time only
#     # --------------------------------------------------------

#     time_pattern = (
#         r"\b"
#         r"(?:[01]?\d|2[0-3])"
#         r":"
#         r"[0-5]\d"
#         r":"
#         r"[0-5]\d"
#         r"\b"
#     )

#     time_match = re.search(
#         time_pattern,
#         normalized
#     )

#     if time_match:

#         return (
#             "",
#             time_match.group(0),
#             ""
#         )

#     return (
#         "",
#         "",
#         ""
#     )


# # ============================================================
# # FORMAT OCR TEXT
# # ============================================================

# def get_ocr_text(ocr_results):

#     return " | ".join(
#         text
#         for text, confidence in ocr_results
#     )


# # ============================================================
# # MAIN
# # ============================================================

# def main():

#     print()
#     print("=" * 70)
#     print("ENTRANCE LINE COUNTING")
#     print("=" * 70)

#     print()
#     print("Input:")
#     print(INPUT_VIDEO)

#     print()
#     print("Output:")
#     print(OUTPUT_DIR)

#     # --------------------------------------------------------
#     # Select line
#     # --------------------------------------------------------

#     line_a, line_b, inside_pt = select_line(
#         INPUT_VIDEO
#     )

#     # Determine inside side
#     raw_inside = side_of_line(
#         inside_pt,
#         line_a,
#         line_b
#     )

#     if raw_inside >= 0:

#         inside_sign = 1

#     else:

#         inside_sign = -1

#     print()
#     print("Entrance line:")
#     print(line_a, "->", line_b)

#     print("Inside point:")
#     print(inside_pt)

#     # --------------------------------------------------------
#     # Load YOLO
#     # --------------------------------------------------------

#     print()
#     print("Loading YOLO model...")

#     model = YOLO(
#         MODEL_PATH
#     )

#     print("YOLO loaded.")

#     # --------------------------------------------------------
#     # Open video
#     # --------------------------------------------------------

#     cap = cv2.VideoCapture(
#         INPUT_VIDEO
#     )

#     if not cap.isOpened():

#         raise RuntimeError(
#             "Could not open input video."
#         )

#     width = int(
#         cap.get(
#             cv2.CAP_PROP_FRAME_WIDTH
#         )
#     )

#     height = int(
#         cap.get(
#             cv2.CAP_PROP_FRAME_HEIGHT
#         )
#     )

#     fps = cap.get(
#         cv2.CAP_PROP_FPS
#     )

#     if fps <= 0:

#         fps = 25

#     total_frames = int(
#         cap.get(
#             cv2.CAP_PROP_FRAME_COUNT
#         )
#     )

#     print()
#     print("Video information")
#     print("-" * 40)
#     print("Width:", width)
#     print("Height:", height)
#     print("FPS:", fps)
#     print("Total frames:", total_frames)

#     # --------------------------------------------------------
#     # Video writer
#     # --------------------------------------------------------

#     fourcc = cv2.VideoWriter_fourcc(
#         *"mp4v"
#     )

#     out = cv2.VideoWriter(
#         OUTPUT_VIDEO,
#         fourcc,
#         fps,
#         (width, height)
#     )

#     # --------------------------------------------------------
#     # Tracking variables
#     # --------------------------------------------------------

#     previous_side = {}

#     # Track IDs already counted
#     entered_ids = set()

#     entered_count = 0

#     frame_idx = 0

#     # --------------------------------------------------------
#     # CSV
#     # --------------------------------------------------------

#     csv_file = open(
#         OUTPUT_CSV,
#         "w",
#         newline="",
#         encoding="utf-8-sig"
#     )

#     csv_writer = csv.writer(
#         csv_file
#     )

#     csv_writer.writerow([
#         "Entry Number",
#         "Track ID",
#         "Video Frame",
#         "Video Time",
#         "CCTV Date",
#         "CCTV Time",
#         "CCTV DateTime",
#         "OCR Text",
#         "Screenshot"
#     ])

#     # --------------------------------------------------------
#     # PROCESS VIDEO
#     # --------------------------------------------------------

#     while True:

#         ret, frame = cap.read()

#         if not ret:

#             break

#         frame_idx += 1

#         # Video elapsed time
#         video_seconds = frame_idx / fps

#         minutes = int(
#             video_seconds // 60
#         )

#         seconds = int(
#             video_seconds % 60
#         )

#         milliseconds = int(
#             (video_seconds % 1) * 1000
#         )

#         video_time = (
#             f"{minutes:02d}:"
#             f"{seconds:02d}."
#             f"{milliseconds:03d}"
#         )

#         # ----------------------------------------------------
#         # YOLO TRACKING
#         # ----------------------------------------------------

#         results = model.track(
#             frame,
#             persist=True,
#             classes=[PERSON_CLASS_ID],
#             conf=CONF_THRES,
#             tracker="bytetrack.yaml",
#             verbose=False
#         )

#         # Draw entrance line
#         draw_dashed_line(
#             frame,
#             line_a,
#             line_b,
#             (0, 255, 255),
#             3
#         )

#         cv2.putText(
#             frame,
#             "ENTRANCE LINE",
#             (
#                 line_a[0],
#                 max(
#                     25,
#                     line_a[1] - 10
#                 )
#             ),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.65,
#             (0, 255, 255),
#             2
#         )

#         # ----------------------------------------------------
#         # PERSON TRACKING
#         # ----------------------------------------------------

#         for result in results:

#             if (
#                 result.boxes is None
#                 or result.boxes.id is None
#             ):

#                 continue

#             boxes = (
#                 result.boxes.xyxy
#                 .cpu()
#                 .numpy()
#             )

#             ids = (
#                 result.boxes.id
#                 .cpu()
#                 .numpy()
#                 .astype(int)
#             )

#             for box, track_id in zip(
#                 boxes,
#                 ids
#             ):

#                 x1, y1, x2, y2 = map(
#                     int,
#                     box
#                 )

#                 # Centroid
#                 cx = int(
#                     (x1 + x2) / 2
#                 )

#                 cy = int(
#                     (y1 + y2) / 2
#                 )

#                 # Current side
#                 raw_side = side_of_line(
#                     (cx, cy),
#                     line_a,
#                     line_b
#                 )

#                 current_side = (
#                     1
#                     if raw_side >= 0
#                     else -1
#                 )

#                 is_inside = (
#                     current_side
#                     == inside_sign
#                 )

#                 # ------------------------------------------------
#                 # ENTRY DETECTION
#                 # ------------------------------------------------

#                 if track_id in previous_side:

#                     previous = previous_side[
#                         track_id
#                     ]

#                     crossed_into_store = (
#                         previous != current_side
#                         and
#                         current_side == inside_sign
#                     )

#                     # Unique-only counting
#                     if (
#                         crossed_into_store
#                         and
#                         track_id not in entered_ids
#                     ):

#                         # ----------------------------------------
#                         # PERSON ENTERED
#                         # ----------------------------------------

#                         entered_count += 1

#                         entered_ids.add(
#                             track_id
#                         )

#                         print()
#                         print("=" * 70)
#                         print(
#                             f"PERSON ENTERED "
#                             f"#{entered_count}"
#                         )
#                         print(
#                             f"Track ID: {track_id}"
#                         )
#                         print(
#                             f"Frame: {frame_idx}"
#                         )
#                         print(
#                             f"Video time: {video_time}"
#                         )
#                         print("=" * 70)

#                         # ----------------------------------------
#                         # Draw entry information
#                         # ----------------------------------------

#                         cv2.rectangle(
#                             frame,
#                             (
#                                 x1,
#                                 y1
#                             ),
#                             (
#                                 x2,
#                                 y2
#                             ),
#                             (0, 255, 0),
#                             4
#                         )

#                         cv2.putText(
#                             frame,
#                             "ENTRY!",
#                             (
#                                 x1,
#                                 max(
#                                     30,
#                                     y1 - 35
#                                 )
#                             ),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             0.9,
#                             (0, 255, 0),
#                             3
#                         )

#                         # ----------------------------------------
#                         # OCR
#                         # ----------------------------------------

#                         print(
#                             "Reading CCTV date/time..."
#                         )

#                         ocr_results = (
#                             run_ocr_on_frame(
#                                 frame.copy()
#                             )
#                         )

#                         ocr_text = get_ocr_text(
#                             ocr_results
#                         )

#                         cctv_date, cctv_time, cctv_datetime = (
#                             extract_datetime(
#                                 ocr_results
#                             )
#                         )

#                         print(
#                             "OCR:",
#                             ocr_text
#                         )

#                         print(
#                             "CCTV Date:",
#                             cctv_date
#                         )

#                         print(
#                             "CCTV Time:",
#                             cctv_time
#                         )

#                         # ----------------------------------------
#                         # Add information to screenshot
#                         # ----------------------------------------

#                         cv2.rectangle(
#                             frame,
#                             (10, 90),
#                             (430, 190),
#                             (0, 0, 0),
#                             -1
#                         )

#                         cv2.putText(
#                             frame,
#                             f"ENTRY #{entered_count}",
#                             (20, 120),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             0.65,
#                             (0, 255, 0),
#                             2
#                         )

#                         cv2.putText(
#                             frame,
#                             f"TRACK ID: {track_id}",
#                             (20, 145),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             0.55,
#                             (255, 255, 255),
#                             2
#                         )

#                         cv2.putText(
#                             frame,
#                             f"VIDEO: {video_time}",
#                             (20, 170),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             0.55,
#                             (255, 255, 255),
#                             2
#                         )

#                         if cctv_datetime:

#                             cv2.putText(
#                                 frame,
#                                 f"CCTV: {cctv_datetime}",
#                                 (20, 195),
#                                 cv2.FONT_HERSHEY_SIMPLEX,
#                                 0.55,
#                                 (0, 255, 255),
#                                 2
#                             )

#                         elif cctv_time:

#                             cv2.putText(
#                                 frame,
#                                 f"CCTV TIME: {cctv_time}",
#                                 (20, 195),
#                                 cv2.FONT_HERSHEY_SIMPLEX,
#                                 0.55,
#                                 (0, 255, 255),
#                                 2
#                             )

#                         # ----------------------------------------
#                         # SAVE SCREENSHOT
#                         # ----------------------------------------

#                         screenshot_name = (
#                             f"entry_"
#                             f"{entered_count:03d}_"
#                             f"ID_{track_id}.jpg"
#                         )

#                         screenshot_path = os.path.join(
#                             SCREENSHOT_DIR,
#                             screenshot_name
#                         )

#                         cv2.imwrite(
#                             screenshot_path,
#                             frame
#                         )

#                         print(
#                             "Screenshot saved:"
#                         )

#                         print(
#                             screenshot_path
#                         )

#                         # ----------------------------------------
#                         # CSV
#                         # ----------------------------------------

#                         csv_writer.writerow([
#                             entered_count,
#                             track_id,
#                             frame_idx,
#                             video_time,
#                             cctv_date,
#                             cctv_time,
#                             cctv_datetime,
#                             ocr_text,
#                             screenshot_path
#                         ])

#                         csv_file.flush()

#                 # Save current side
#                 previous_side[
#                     track_id
#                 ] = current_side

#                 # --------------------------------------------
#                 # DRAW PERSON
#                 # --------------------------------------------

#                 if is_inside:

#                     box_color = (
#                         0,
#                         200,
#                         0
#                     )

#                 else:

#                     box_color = (
#                         0,
#                         165,
#                         255
#                     )

#                 draw_corner_box(
#                     frame,
#                     x1,
#                     y1,
#                     x2,
#                     y2,
#                     box_color,
#                     2
#                 )

#                 cv2.circle(
#                     frame,
#                     (cx, cy),
#                     4,
#                     box_color,
#                     -1
#                 )

#                 status = (
#                     "IN"
#                     if is_inside
#                     else "OUT"
#                 )

#                 cv2.putText(
#                     frame,
#                     f"ID {track_id} {status}",
#                     (
#                         x1,
#                         max(
#                             20,
#                             y1 - 8
#                         )
#                     ),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.5,
#                     box_color,
#                     2
#                 )

#         # ----------------------------------------------------
#         # COUNTER PANEL
#         # ----------------------------------------------------

#         overlay = frame.copy()

#         cv2.rectangle(
#             overlay,
#             (10, 10),
#             (300, 75),
#             (0, 0, 0),
#             -1
#         )

#         frame = cv2.addWeighted(
#             overlay,
#             0.55,
#             frame,
#             0.45,
#             0
#         )

#         cv2.rectangle(
#             frame,
#             (10, 10),
#             (300, 75),
#             (255, 255, 255),
#             1
#         )

#         cv2.putText(
#             frame,
#             "ENTERED STORE",
#             (20, 38),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.6,
#             (255, 255, 255),
#             2
#         )

#         cv2.putText(
#             frame,
#             str(entered_count),
#             (20, 67),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.9,
#             (0, 255, 0),
#             2
#         )

#         # Video time
#         cv2.putText(
#             frame,
#             f"Video: {video_time}",
#             (
#                 width - 190,
#                 30
#             ),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.5,
#             (255, 255, 255),
#             2
#         )

#         # ----------------------------------------------------
#         # WRITE VIDEO
#         # ----------------------------------------------------

#         out.write(frame)

#         # Show processing
#         cv2.imshow(
#             "Entrance Counting",
#             frame
#         )

#         key = cv2.waitKey(1) & 0xFF

#         if key == 27:

#             print(
#                 "Processing stopped by user."
#             )

#             break

#     # --------------------------------------------------------
#     # CLEANUP
#     # --------------------------------------------------------

#     cap.release()

#     out.release()

#     csv_file.close()

#     cv2.destroyAllWindows()

#     # --------------------------------------------------------
#     # FINAL RESULTS
#     # --------------------------------------------------------

#     print()
#     print("=" * 70)
#     print("PROCESSING COMPLETE")
#     print("=" * 70)

#     print()
#     print(
#         f"Total unique people entered: "
#         f"{entered_count}"
#     )

#     print()
#     print(
#         "Annotated video:"
#     )

#     print(
#         OUTPUT_VIDEO
#     )

#     print()
#     print(
#         "CSV:"
#     )

#     print(
#         OUTPUT_CSV
#     )

#     print()
#     print(
#         "Entry screenshots:"
#     )

#     print(
#         SCREENSHOT_DIR
#     )

#     print()
#     print("=" * 70)


# # ============================================================
# # START
# # ============================================================

# if __name__ == "__main__":

#     main()






import os
import csv
import re
from datetime import datetime, timedelta

import cv2
import numpy as np

from ultralytics import YOLO
from paddleocr import PaddleOCR


# ============================================================
# CONFIG
# ============================================================

INPUT_VIDEO = r"C:\Users\user\Desktop\task_1\input video\cropped_03m02s_to_03m20s.mp4"
OUTPUT_DIR = r"C:\Users\user\Desktop\task_1\output"

OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "entrance_annotated.mp4")
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "entrance_counts.csv")
SCREENSHOT_DIR = os.path.join(OUTPUT_DIR, "entry_screenshots")

MODEL_PATH = "yolov8s.pt"
CONF_THRES = 0.35
IMG_SIZE = 960            # larger = better for small / far people
PERSON_CLASS_ID = 0

# ---- Entry rule -------------------------------------------------
# A person is counted ONLY when the WHOLE body box (all 4 corners:
# head and feet) is on the inside of the line, for CONFIRM_FRAMES
# frames in a row.
FULL_INSIDE_MARGIN = 5    # px past the line that every corner must be
FULL_OUTSIDE_MARGIN = 5   # px before the line to be considered "outside"
CONFIRM_FRAMES = 5        # consecutive fully-inside frames needed
LINE_EXTENT_PAD = 0.15    # allow crossing slightly beyond line ends (fraction)

# Where the CCTV timestamp is on screen: (x1, y1, x2, y2)
TIMESTAMP_ROI = (0, 0, 420, 55)

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# ============================================================
# OCR
# ============================================================

print("Loading PaddleOCR...")
ocr = PaddleOCR(
    use_angle_cls=True,
    lang="en",
    ocr_version="PP-OCRv4",
    use_space_char=True,
    det_db_thresh=0.1,
    det_db_box_thresh=0.1,
)
print("PaddleOCR loaded.")


def run_ocr(image):
    try:
        result = ocr.ocr(image, cls=True)
        if not result or not result[0]:
            return []
        out = []
        for item in result[0]:
            try:
                out.append((item[1][0], float(item[1][1])))
            except Exception:
                continue
        return out
    except Exception as e:
        print("OCR error:", e)
        return []


def parse_datetime(ocr_results):
    """Return (date, time, datetime_string) or ("", "", "")."""
    text = " ".join(t for t, _ in ocr_results)
    text = text.replace("O", "0").replace("o", "0").replace("|", "1")
    text = re.sub(r"\s*([:\-/.])\s*", r"\1", text)

    m = re.search(
        r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})\s*(\d{1,2}):(\d{2}):(\d{2})", text
    )
    if m:
        y, mo, d, h, mi, s = m.groups()
        date = f"{y}-{int(mo):02d}-{int(d):02d}"
        tm = f"{int(h):02d}:{mi}:{s}"
        return date, tm, f"{date} {tm}"

    m = re.search(
        r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})\s*(\d{1,2}):(\d{2}):(\d{2})", text
    )
    if m:
        d, mo, y, h, mi, s = m.groups()
        date = f"{int(d):02d}-{int(mo):02d}-{y}"
        tm = f"{int(h):02d}:{mi}:{s}"
        return date, tm, f"{date} {tm}"

    m = re.search(r"(\d{1,2}):(\d{2}):(\d{2})", text)
    if m:
        h, mi, s = m.groups()
        return "", f"{int(h):02d}:{mi}:{s}", ""

    return "", "", ""


def read_cctv_datetime(clean_frame):
    """OCR the timestamp area of an UNANNOTATED frame."""
    x1, y1, x2, y2 = TIMESTAMP_ROI
    roi = clean_frame[y1:y2, x1:x2]
    roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    results = run_ocr(roi)
    date, tm, dt = parse_datetime(results)
    if not tm:
        results = run_ocr(clean_frame)
        date, tm, dt = parse_datetime(results)
    text = " | ".join(t for t, _ in results)
    return date, tm, dt, text


# ============================================================
# LINE SELECTION (mouse)
# ============================================================

line_points = []
inside_point = None


def mouse_callback(event, x, y, flags, param):
    global line_points, inside_point
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(line_points) < 2:
            line_points.append((x, y))
            print(f"Line point {len(line_points)}: ({x}, {y})")
        elif inside_point is None:
            inside_point = (x, y)
            print(f"Inside point: ({x}, {y})")


def select_line(video_path):
    global line_points, inside_point

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video:\n{video_path}")
    ret, first = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError("Could not read first frame.")

    win = "ENTRANCE LINE | 2 clicks=line | 3rd click=INSIDE | ENTER | R=reset | ESC"
    cv2.namedWindow(win)
    cv2.setMouseCallback(win, mouse_callback)

    print("\nClick 2 points for the entrance line (along the shop threshold),")
    print("then 1 point INSIDE the shop, then press ENTER. R = reset, ESC = cancel.\n")

    while True:
        disp = first.copy()
        for p in line_points:
            cv2.circle(disp, p, 6, (0, 0, 255), -1)
        if len(line_points) == 2:
            cv2.line(disp, line_points[0], line_points[1], (0, 255, 255), 3)
        if inside_point is not None:
            cv2.circle(disp, inside_point, 8, (255, 0, 0), -1)
            cv2.putText(disp, "INSIDE", (inside_point[0] + 10, inside_point[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(disp, "2 clicks = LINE | 3rd click = INSIDE | ENTER = CONFIRM | R = RESET",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
        cv2.imshow(win, disp)

        key = cv2.waitKey(20) & 0xFF
        if key == ord("r"):
            line_points, inside_point = [], None
        elif key in (13, 10):
            if len(line_points) == 2 and inside_point is not None:
                break
            print("Please select 2 line points and 1 inside point.")
        elif key == 27:
            cv2.destroyWindow(win)
            raise SystemExit("Cancelled by user.")

    cv2.destroyWindow(win)
    return line_points[0], line_points[1], inside_point


# ============================================================
# GEOMETRY
# ============================================================

class EntranceLine:
    def __init__(self, a, b, inside_pt):
        self.a = a
        self.b = b
        self.dx = b[0] - a[0]
        self.dy = b[1] - a[1]
        self.length = float(np.hypot(self.dx, self.dy))
        raw = self._cross(inside_pt)
        self.sign = 1 if raw >= 0 else -1

    def _cross(self, p):
        return self.dx * (p[1] - self.a[1]) - self.dy * (p[0] - self.a[0])

    def dist(self, p):
        """Signed distance in pixels. POSITIVE = inside the shop."""
        return self.sign * self._cross(p) / self.length

    def along(self, p):
        """Position along the line, 0 = point A, 1 = point B."""
        return ((p[0] - self.a[0]) * self.dx + (p[1] - self.a[1]) * self.dy) / (self.length ** 2)


def body_distances(line, x1, y1, x2, y2):
    corners = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
    d = [line.dist(c) for c in corners]
    return min(d), max(d)


# ============================================================
# DRAWING
# ============================================================

def draw_dashed_line(img, p1, p2, color, thickness=2, dash=15):
    dist = int(np.hypot(p2[0] - p1[0], p2[1] - p1[1]))
    if dist == 0:
        return
    for i in range(0, dist, dash * 2):
        r0 = i / dist
        r1 = min(i + dash, dist) / dist
        a = (int(p1[0] + (p2[0] - p1[0]) * r0), int(p1[1] + (p2[1] - p1[1]) * r0))
        b = (int(p1[0] + (p2[0] - p1[0]) * r1), int(p1[1] + (p2[1] - p1[1]) * r1))
        cv2.line(img, a, b, color, thickness)


def draw_corner_box(img, x1, y1, x2, y2, color, t=2):
    lw = int((x2 - x1) * 0.25)
    lh = int((y2 - y1) * 0.25)
    for (px, py, sx, sy) in [(x1, y1, 1, 1), (x2, y1, -1, 1), (x1, y2, 1, -1), (x2, y2, -1, -1)]:
        cv2.line(img, (px, py), (px + sx * lw, py), color, t)
        cv2.line(img, (px, py), (px, py + sy * lh), color, t)


# ============================================================
# MAIN
# ============================================================

def main():
    line_a, line_b, inside_pt = select_line(INPUT_VIDEO)
    line = EntranceLine(line_a, line_b, inside_pt)

    print("Loading YOLO...")
    model = YOLO(MODEL_PATH)

    cap = cv2.VideoCapture(INPUT_VIDEO)
    if not cap.isOpened():
        raise RuntimeError("Could not open input video.")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    print(f"Video: {width}x{height} @ {fps:.2f} fps")

    out = cv2.VideoWriter(OUTPUT_VIDEO, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    csv_file = open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig")
    writer = csv.writer(csv_file)
    writer.writerow([
        "Entry Number", "Track ID", "Video Frame", "Video Time",
        "CCTV Date", "CCTV Time", "CCTV DateTime", "OCR Text", "Screenshot",
    ])

    # per-track state:
    #   armed   -> the person has been seen NOT fully inside (outside/crossing)
    #              so a later "fully inside" is a real entry
    #   streak  -> consecutive frames fully inside
    #   counted -> already counted (each ID counted once)
    states = {}
    flash = {}                 # track_id -> frame until which "ENTRY!" is shown
    entered_count = 0
    frame_idx = 0
    base_dt = None             # CCTV time read from first frame (fallback)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1
        clean = frame.copy()   # untouched copy for OCR

        elapsed = (frame_idx - 1) / fps
        video_time = f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d}.{int((elapsed % 1) * 1000):03d}"

        if frame_idx == 1:
            d, t, dt, _ = read_cctv_datetime(clean)
            try:
                base_dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                print("CCTV start time:", base_dt)
            except Exception:
                base_dt = None

        results = model.track(
            frame,
            persist=True,
            classes=[PERSON_CLASS_ID],
            conf=CONF_THRES,
            imgsz=IMG_SIZE,
            tracker="bytetrack.yaml",
            verbose=False,
        )

        draw_dashed_line(frame, line_a, line_b, (0, 255, 255), 3)
        cv2.putText(frame, "ENTRANCE LINE", (line_a[0], max(25, line_a[1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)

        new_entries = []       # (entry_no, track_id)

        for result in results:
            if result.boxes is None or result.boxes.id is None:
                continue
            boxes = result.boxes.xyxy.cpu().numpy()
            ids = result.boxes.id.cpu().numpy().astype(int)

            for box, tid in zip(boxes, ids):
                x1, y1, x2, y2 = map(int, box)
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                foot = (cx, y2)

                min_d, max_d = body_distances(line, x1, y1, x2, y2)
                fully_inside = min_d >= FULL_INSIDE_MARGIN     # whole body past line
                fully_outside = max_d <= -FULL_OUTSIDE_MARGIN  # whole body before line

                st = states.get(tid)
                if st is None:
                    # People who first appear already fully inside are NOT entries.
                    st = {"armed": not fully_inside, "streak": 0, "counted": False}
                    states[tid] = st

                if fully_outside:
                    st["armed"] = True

                if not st["counted"]:
                    if fully_inside and st["armed"]:
                        st["streak"] += 1
                    else:
                        st["streak"] = 0

                    if st["streak"] >= CONFIRM_FRAMES:
                        t = line.along(foot)
                        if -LINE_EXTENT_PAD <= t <= 1 + LINE_EXTENT_PAD:
                            st["counted"] = True
                            entered_count += 1
                            flash[tid] = frame_idx + int(fps * 1.5)
                            new_entries.append((entered_count, tid))
                            print(f"\nPERSON ENTERED #{entered_count} | ID {tid} | "
                                  f"frame {frame_idx} | {video_time}")

                # ---- drawing ----
                if st["counted"] or fully_inside:
                    color, status = (0, 200, 0), "IN"
                elif fully_outside:
                    color, status = (0, 165, 255), "OUT"
                else:
                    color, status = (0, 255, 255), "CROSSING"

                draw_corner_box(frame, x1, y1, x2, y2, color, 2)
                cv2.circle(frame, (cx, cy), 4, color, -1)
                cv2.putText(frame, f"ID {tid} {status}", (x1, max(20, y1 - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                if flash.get(tid, 0) >= frame_idx:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
                    cv2.putText(frame, "ENTRY!", (x1, max(30, y1 - 30)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)

        # ---- counter panel ----
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (300, 75), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.55, frame, 0.45, 0)
        cv2.rectangle(frame, (10, 10), (300, 75), (255, 255, 255), 1)
        cv2.putText(frame, "ENTERED STORE", (20, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, str(entered_count), (20, 67), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(frame, f"Video: {video_time}", (width - 190, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # ---- log new entries (OCR on the CLEAN frame) ----
        for entry_no, tid in new_entries:
            date, tm, dt, ocr_text = read_cctv_datetime(clean)

            if not dt and base_dt is not None:          # fallback: start time + elapsed
                calc = base_dt + timedelta(seconds=elapsed)
                date, tm = calc.strftime("%Y-%m-%d"), calc.strftime("%H:%M:%S")
                dt = f"{date} {tm}"
                ocr_text = (ocr_text + " | " if ocr_text else "") + "(time computed from video start)"

            shot = frame.copy()
            cv2.rectangle(shot, (10, 90), (430, 200), (0, 0, 0), -1)
            cv2.putText(shot, f"ENTRY #{entry_no}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
            cv2.putText(shot, f"TRACK ID: {tid}", (20, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
            cv2.putText(shot, f"VIDEO: {video_time}", (20, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
            if dt or tm:
                cv2.putText(shot, f"CCTV: {dt or tm}", (20, 195), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

            shot_path = os.path.join(SCREENSHOT_DIR, f"entry_{entry_no:03d}_ID_{tid}.jpg")
            cv2.imwrite(shot_path, shot)

            writer.writerow([entry_no, tid, frame_idx, video_time, date, tm, dt, ocr_text, shot_path])
            csv_file.flush()
            print(f"  CCTV: {dt or tm or 'not read'} | screenshot: {shot_path}")

        out.write(frame)
        cv2.imshow("Entrance Counting", frame)
        if (cv2.waitKey(1) & 0xFF) == 27:
            print("Stopped by user.")
            break

    cap.release()
    out.release()
    csv_file.close()
    cv2.destroyAllWindows()

    print("\n" + "=" * 60)
    print(f"Total unique people entered: {entered_count}")
    print("Video:", OUTPUT_VIDEO)
    print("CSV:", OUTPUT_CSV)
    print("Screenshots:", SCREENSHOT_DIR)
    print("=" * 60)


if __name__ == "__main__":
    main()
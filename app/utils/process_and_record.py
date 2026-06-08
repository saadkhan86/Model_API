import imageio
from ultralytics import YOLO
import cv2
import time
import os
import uuid
import math
from collections import deque
from app.constants.constants import CLASS_COLORS, CLASS_NAMES, WEAPON_CLASSES, VALUABLE_CLASSES, CONF_THRESHOLD, FLEEING_MIN_RATIO, FLEEING_MAX_RATIO, PRE_ROLL_SECONDS, CLIP_DURATION_SECONDS
from app.utils.ai_utils import check_overlap, calculate_centroid, annotate_frame
# Load YOLO model
model = YOLO("yolov8n.pt")


def process_and_record(video_path):
    """Processes video file, checks for theft/suspicious activity, and saves 20s clips."""
    reader = imageio.get_reader(video_path, 'ffmpeg')
    meta = reader.get_meta_data()
    fps = meta['fps']
    width, height = meta.get('size', (640, 480))
    diagonal = math.sqrt(width**2 + height**2)

    # Recording constraints
    clip_frame_count = int(CLIP_DURATION_SECONDS * fps)
    pre_roll_count = int(PRE_ROLL_SECONDS * fps)

    # State variables
    pre_roll_frames = deque(maxlen=pre_roll_count)
    current_clip_frames = []
    saved_clips = []
    recording_active = False
    frames_remaining = 0

    # Tracking variable for speed detection
    prev_centroids = []

    target_classes = list(CLASS_NAMES.keys())

    for frame in reader:
        # Get frame in BGR for OpenCV
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Optimize YOLO: specify target classes and turn off verbose console spam
        results = model(frame_bgr, conf=CONF_THRESHOLD,
                        classes=target_classes, verbose=False)

        person_boxes = []
        weapon_boxes = []
        item_boxes = []
        all_detections = []

        # Parse YOLO outputs
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                coords = [x1, y1, x2, y2]

                all_detections.append((coords, cls_id, conf))

                if cls_id == 0:
                    person_boxes.append(coords)
                elif cls_id in WEAPON_CLASSES:
                    weapon_boxes.append((coords, cls_id, conf))
                elif cls_id in VALUABLE_CLASSES:
                    item_boxes.append((coords, cls_id, conf))

        # Check Suspicion Triggers
        suspicious_reasons = []

        # 1. Weapon Detection
        if weapon_boxes:
            weapon_names = {CLASS_NAMES[c] for (_, c, _) in weapon_boxes}
            suspicious_reasons.append(f"Weapon: {', '.join(weapon_names)}")

        # 2. Theft / Valuable Interaction Detection
        for p_box in person_boxes:
            for i_box, cls_id, _ in item_boxes:
                if check_overlap(p_box, i_box) > 0:
                    suspicious_reasons.append(
                        f"Theft Interaction ({CLASS_NAMES[cls_id]})")

        # 3. Running / Fleeing Speed Detection
        curr_centroids = [calculate_centroid(box) for box in person_boxes]
        fleeing_detected = False
        if prev_centroids and curr_centroids:
            for curr_c in curr_centroids:
                min_dist = float('inf')
                for prev_c in prev_centroids:
                    dist = math.sqrt(
                        (curr_c[0] - prev_c[0])**2 + (curr_c[1] - prev_c[1])**2)
                    if dist < min_dist:
                        min_dist = dist

                # Check fleeing limits
                min_flee_pixels = FLEEING_MIN_RATIO * diagonal
                max_flee_pixels = FLEEING_MAX_RATIO * diagonal
                if min_flee_pixels <= min_dist <= max_flee_pixels:
                    fleeing_detected = True
                    break

        if fleeing_detected:
            suspicious_reasons.append("Fleeing/Running")

        prev_centroids = curr_centroids

        # De-duplicate suspicion reasons
        suspicious_reasons = list(set(suspicious_reasons))

        # Draw annotations and overlays
        annotate_frame(frame_bgr, all_detections, suspicious_reasons)

        # Convert back to RGB for imageio writer
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        # Handle Clip Recording
        if suspicious_reasons:
            if not recording_active:
                recording_active = True
                # Start recording with pre-roll buffer
                current_clip_frames = list(pre_roll_frames)
                frames_remaining = clip_frame_count - len(current_clip_frames)

        if recording_active:
            current_clip_frames.append(frame_rgb)
            frames_remaining -= 1
            if frames_remaining <= 0:
                clip_path = save_clip_imageio(current_clip_frames, fps)
                saved_clips.append(clip_path)
                recording_active = False
                current_clip_frames = []
        else:
            pre_roll_frames.append(frame_rgb)

    # Save remaining frames if video finished during an active recording
    if recording_active and current_clip_frames:
        clip_path = save_clip_imageio(current_clip_frames, fps)
        saved_clips.append(clip_path)

    reader.close()
    return saved_clips


def save_clip_imageio(frames, fps):
    """Saves a list of frames to an mp4 file using imageio."""
    os.makedirs("clips", exist_ok=True)
    # Use unique timestamp + uuid to prevent file collision
    unique_id = uuid.uuid4().hex[:6]
    output_path = f"clips/suspicious_{int(time.time())}_{unique_id}.mp4"

    writer = imageio.get_writer(
        output_path, fps=fps, codec='libx264', quality=8)
    for frame in frames:
        writer.append_data(frame)
    writer.close()
    print(f"Successfully saved suspicious clip: {output_path}")
    return output_path

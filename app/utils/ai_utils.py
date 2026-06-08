import cv2
from app.constants.constants import CLASS_COLORS, CLASS_NAMES, WEAPON_CLASSES, VALUABLE_CLASSES, CONF_THRESHOLD, FLEEING_MIN_RATIO, FLEEING_MAX_RATIO, PRE_ROLL_SECONDS, CLIP_DURATION_SECONDS


def calculate_centroid(box):
    """Calculates centroid of a bounding box [x1, y1, x2, y2]."""
    return ((box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0)


def check_overlap(box1, box2):
    """Checks intersection area between box1 and box2."""
    x1_max = max(box1[0], box2[0])
    y1_max = max(box1[1], box2[1])
    x2_min = min(box1[2], box2[2])
    y2_min = min(box1[3], box2[3])

    if x1_max < x2_min and y1_max < y2_min:
        return (x2_min - x1_max) * (y2_min - y1_max)
    return 0


def annotate_frame(frame, detections, suspicious_reasons=None):
    """Draws premium bounding boxes, labels, and optional alerts on the frame."""
    # Draw object detections
    for box, cls_id, conf in detections:
        x1, y1, x2, y2 = box
        color = CLASS_COLORS.get(cls_id, (0, 255, 0))
        label_text = f"{CLASS_NAMES.get(cls_id, 'Item')}: {conf:.2f}"

        # Draw smooth bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Draw filled label text background
        (w, h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        label_y = max(y1, h + 10)
        cv2.rectangle(frame, (x1, label_y - h - 10),
                      (x1 + w + 10, label_y), color, -1)

        # Draw text
        cv2.putText(frame, label_text, (x1 + 5, label_y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)

    # Draw top-level suspicious alert overlay if triggered
    if suspicious_reasons:
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (frame.shape[1], 45), (0, 0, 255), -1)
        cv2.addWeighted(overlay, 0.35, frame, 0.65, 0, frame)

        reasons_str = ", ".join(suspicious_reasons)
        warning_text = f"ALERT: SUSPICIOUS ACTIVITY ({reasons_str})"
        cv2.putText(frame, warning_text, (15, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2, cv2.LINE_AA)

        # Red border around the screen
        cv2.rectangle(
            frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 4)

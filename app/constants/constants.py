CLASS_COLORS = {
    0: (235, 206, 135),     # Sky Blue for Person
    24: (0, 165, 255),      # Orange/Amber for Backpack
    26: (0, 165, 255),      # Orange/Amber for Handbag
    28: (0, 165, 255),      # Orange/Amber for Suitcase
    34: (0, 0, 255),        # Red for Baseball bat (Weapon)
    39: (200, 200, 0),      # Cyan/Yellow-Green for Bottle
    40: (200, 200, 0),      # Wine glass
    41: (200, 200, 0),      # Cup
    43: (0, 0, 255),        # Red for Knife (Weapon)
    63: (255, 128, 0),      # Blue/Orange for Laptop
    67: (255, 128, 0),      # Blue/Orange for Cell phone
    73: (128, 0, 128),      # Purple for Book
    76: (0, 0, 255),        # Red for Scissors (Weapon)
}
# Target classes mapping (COCO class IDs)
CLASS_NAMES = {
    0: "Person",
    24: "Backpack",
    26: "Handbag",
    28: "Suitcase",
    34: "Baseball bat",
    39: "Bottle",
    40: "Wine glass",
    41: "Cup",
    43: "Knife",
    63: "Laptop",
    67: "Cell phone",
    73: "Book",
    76: "Scissors"
}

WEAPON_CLASSES = {34, 43, 76}

VALUABLE_CLASSES = {24, 26, 28, 39, 40, 41, 63, 67, 73}

# Constants for analytics and recording
CONF_THRESHOLD = 0.35

FLEEING_MIN_RATIO = 0.04   # 4% of diagonal per frame (fleeing speed)

FLEEING_MAX_RATIO = 0.20   # 20% of diagonal per frame (avoiding mismatches)

PRE_ROLL_SECONDS = 5

CLIP_DURATION_SECONDS = 30

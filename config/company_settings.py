from pathlib import Path

STATIC_DIR = Path("static")
TEMPLATES_DIR = STATIC_DIR / "templates"
FONTS_DIR = STATIC_DIR / "fonts"

COMPANY_SETTINGS = {
    "dewise": {
        "template_path": TEMPLATES_DIR / "dewise" / "Dewise-Certificate_01.jpg",
        # "template_path": TEMPLATES_DIR / "dewise" / "Dewise-Certificate.jpg",
        "fonts": {
            "title": FONTS_DIR / "dewise" / "ProximaNova-Bold.otf",
            "text": FONTS_DIR / "dewise" / "ProximaNova-Bold.otf",
        },
        "text_positions": {
            "name": {"x": 0.5, "y": 0.39},  # Positions as percentage of image dimensions
            "course": {"x": 0.5, "y": 0.523},
            # "date": {"x": 0.5, "y": 0.913},
            "date": {"x": 0.528, "y": 0.913},
        },
        "font_sizes": {
            # "name": 60,
            # "course": 40/1.618,
            # "date": 30
            "name": 100,
            "course": 100/1.618,
            "date": 40
        },
        "text_colors": {
            "name": "black",
            "course": "black",
            "date": "black"
        }
    },
    "tic": {
        "template_path": TEMPLATES_DIR / "tic" / "Team_1_member.png",
        "fonts": {
            "title": FONTS_DIR / "tic" / "ProximaNova-Bold.otf",
            "text": FONTS_DIR / "tic" / "ProximaNova-Bold.otf",
        },
        "text_positions": {
            "name": {"x": 0.3303, "y": 0.5},  # Positions as percentage of image dimensions
            "course": {"x": 0.71, "y": 0.6348},
            # "date": {"x": 0.5, "y": 0.913},
            "date": {"x": 0.528, "y": 0.913}  ,
        },
        "font_sizes": {
            "name": 600,
            "course": 40/1.618,
            "date": 30
        },
        "text_colors": {
            "name": "black",
            "course": "black",
            "date": "black"
        }
    },


    # Add other companies with their specific settings
}
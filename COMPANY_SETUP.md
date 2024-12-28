# Adding New Companies

This guide explains how to add new companies to the Certificate Generator API.

## Table of Contents

- [Directory Setup](#directory-setup)
- [Asset Requirements](#asset-requirements)
- [Configuration Steps](#configuration-steps)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Directory Setup

1. Create company directories:
```bash
export COMPANY_ID="your_company_id"
mkdir -p static/templates/$COMPANY_ID
mkdir -p static/fonts/$COMPANY_ID
```

## Asset Requirements

### Certificate Template
- Format: PNG
- Recommended size: 1920x1080 pixels (16:9) or 2000x1414 pixels (√2 ratio)
- Resolution: 300 DPI
- Color mode: RGB
- File name: `certificate.png`

### Fonts
Required fonts:
- Title font (for names)
- Text font (for other content)

Supported formats:
- TrueType (.ttf)
- OpenType (.otf)

## Configuration Steps

1. Add company settings in `config/company_settings.py`:

```python
COMPANY_SETTINGS = {
    "your_company_id": {
        "template_path": TEMPLATES_DIR / "your_company_id" / "certificate.png",
        "fonts": {
            "title": FONTS_DIR / "your_company_id" / "title.ttf",
            "text": FONTS_DIR / "your_company_id" / "text.ttf"
        },
        "text_positions": {
            "name": {"x": 0.5, "y": 0.4},  # Positions as percentage
            "course": {"x": 0.5, "y": 0.5},
            "date": {"x": 0.5, "y": 0.6}
        },
        "font_sizes": {
            "name": 60,
            "course": 40,
            "date": 30
        },
        "text_colors": {
            "name": "black",
            "course": "black",
            "date": "black"
        }
    }
}
```

## Testing

1. Verify file structure:
```bash
tree static/templates/$COMPANY_ID
tree static/fonts/$COMPANY_ID
```

2. Test certificate generation:
```bash
curl -X POST "http://localhost:8000/$COMPANY_ID/generate-certificate/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Test User",
  "course_name": "Test Course",
  "created_at": "2024-10-29T12:00:00"
}'
```

## Text Positioning Guide

The text positioning uses relative coordinates (0-1) where:
- 0.0 is the left/top edge
- 1.0 is the right/bottom edge
- 0.5 is the center

Example positions:
```python
"text_positions": {
    "name": {"x": 0.5, "y": 0.4},    # Centered, slightly above middle
    "course": {"x": 0.5, "y": 0.5},   # Centered, middle
    "date": {"x": 0.5, "y": 0.6}      # Centered, slightly below middle
}
```

## Font Size Guidelines

Recommended sizes for 1920x1080 template:
- Name: 60-80px
- Course: 40-50px
- Date: 30-40px

Adjust based on your template size and design.

## Troubleshooting

### Common Issues

1. **Template not found**
   - Check file path
   - Verify file permissions
   - Ensure correct file name

2. **Font loading fails**
   - Verify font file exists
   - Check font file format
   - Confirm font file permissions

3. **Text positioning issues**
   - Use preview mode to test positions
   - Verify coordinate values are between 0 and 1
   - Check for proper scaling on different template sizes

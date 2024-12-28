from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime
import io
from pathlib import Path
from config.company_settings import COMPANY_SETTINGS
import tempfile
import os
import requests
from io import BytesIO
from typing import List



class PixelCertificateGenerator:
    def __init__(self, company_id: str):
        if company_id not in COMPANY_SETTINGS:
            raise ValueError(f"Company {company_id} not configured")
        self.settings = COMPANY_SETTINGS[company_id]
        self._validate_paths()

    def _validate_paths(self):
        """Validate that all required files exist"""
        if not self.settings["template_path"].exists():
            raise FileNotFoundError(f"Template not found: {self.settings['template_path']}")
        for font_path in self.settings["fonts"].values():
            if not font_path.exists():
                raise FileNotFoundError(f"Font not found: {font_path}")

    def generate(self, name: str, course_name: str, created_at: datetime) -> bytes:
        # Open template
        img = Image.open(self.settings["template_path"])
        draw = ImageDraw.Draw(img)
        W, H = img.size

        # Load fonts
        name_font = ImageFont.truetype(
            str(self.settings["fonts"]["title"]),
            self.settings["font_sizes"]["name"]
        )
        regular_font = ImageFont.truetype(
            str(self.settings["fonts"]["text"]),
            self.settings["font_sizes"]["course"]
        )
        date_font = ImageFont.truetype(
            str(self.settings["fonts"]["text"]),
            self.settings["font_sizes"]["date"]
        )
        # Draw text
        # Name
        pos = self.settings["text_positions"]["name"]
        draw.text(
            (W * pos["x"], H * pos["y"]),
            name,
            font=name_font,
            fill=self.settings["text_colors"]["name"],
            anchor="mm"
        )

        # Course name
        pos = self.settings["text_positions"]["course"]
        draw.text(
            (W * pos["x"], H * pos["y"]),
            course_name,
            font=regular_font,
            fill=self.settings["text_colors"]["course"],
            anchor="mm"
        )

        # Date
        pos = self.settings["text_positions"]["date"]
        draw.text(
            (W * pos["x"], H * pos["y"]),
            created_at.strftime("%B %d, %Y"),
            font=date_font,
            fill=self.settings["text_colors"]["date"],
            anchor="mm"
        )

        # Convert to bytes
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)

        return img_byte_array.getvalue()






class CertificateGenerator:
    def __init__(self, company_id: str):
        if company_id not in COMPANY_SETTINGS:
            raise ValueError(f"Company {company_id} not configured")
        self.settings = COMPANY_SETTINGS[company_id]
        self._validate_paths()

    def _validate_paths(self):
        """Validate that all required files exist"""
        if not self.settings["template_path"].exists():
            raise FileNotFoundError(f"Template not found: {self.settings['template_path']}")
        for font_path in self.settings["fonts"].values():
            if not font_path.exists():
                raise FileNotFoundError(f"Font not found: {font_path}")

    def generate(self, name: str, course_name: str, created_at: datetime) -> bytes:
        # Open template
        img = Image.open(self.settings["template_path"])
        draw = ImageDraw.Draw(img)
        W, H = img.size

        # Load fonts
        name_font = ImageFont.truetype(
            str(self.settings["fonts"]["title"]),
            self.settings["font_sizes"]["name"]
        )
        regular_font = ImageFont.truetype(
            str(self.settings["fonts"]["text"]),
            self.settings["font_sizes"]["course"]
        )
        date_font = ImageFont.truetype(
            str(self.settings["fonts"]["text"]),
            self.settings["font_sizes"]["date"]
        )
        # Draw text
        # Name
        pos = self.settings["text_positions"]["name"]
        draw.text(
            (W * pos["x"], H * pos["y"]),
            name,
            font=name_font,
            fill=self.settings["text_colors"]["name"],
            anchor="mm"
        )

        # Course name
        pos = self.settings["text_positions"]["course"]
        draw.text(
            (W * pos["x"], H * pos["y"]),
            course_name,
            font=regular_font,
            fill=self.settings["text_colors"]["course"],
            anchor="mm"
        )

        # Date
        pos = self.settings["text_positions"]["date"]
        draw.text(
            (W * pos["x"], H * pos["y"]),
            created_at.strftime("%B %d, %Y"),
            font=date_font,
            fill=self.settings["text_colors"]["date"],
            anchor="mm"
        )

        # Convert to bytes
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)

        return img_byte_array.getvalue()


class TICFlyerGenerator:
    TEMPLATE_PATHS = {
        "regional_coordinator": "./static/templates/tic/regional_coordinator.png",
        "mentor": "./static/templates/tic/mentorflyer.png",
        "team_1": "./static/templates/tic/team_1_member.png",
        "team_2": "./static/templates/tic/team_2_members.png",
        "team_3": "./static/templates/tic/team_3_members.png",
        "team_4": "./static/templates/tic/team_4_members.png",
        "team_5": "./static/templates/tic/team_5_members.png",
    }

    def __init__(self, company_id: str):
        self.company_id = company_id

    def generate(self, name: str, template_type: str, images: List[str]) -> bytes:
        # Load template based on type and number of images
        img = self._load_template(template_type, len(images))

        # Paste images onto the flyer
        for index, img_url in enumerate(images):
            overlay_img = self._fetch_and_prepare_image(img_url,template_type)
            position = self._get_position_for_image(template_type, index)
            img.paste(overlay_img, position,overlay_img)

        # Add name to the flyer if applicable
        self._add_text_to_flyer(img, name)

        return self._image_to_bytes(img)

    def _load_template(self, template_type: str, image_count: int) -> Image.Image:
        """Load the template based on the type and number of images."""
        if template_type == "regional_coordinator" and image_count == 1:
            print("team_2")
            return Image.open(self.TEMPLATE_PATHS["regional_coordinator"]).convert("RGBA")
        elif template_type == "mentors" and image_count == 1:
            print("team new")
            return Image.open(self.TEMPLATE_PATHS["mentor"]).convert("RGBA")
        elif template_type == "team1" and image_count == 1:
            print("team1")
            return Image.open(self.TEMPLATE_PATHS["team_1"]).convert("RGBA")
        elif template_type == "team2":
            print("team2")
            return Image.open(self.TEMPLATE_PATHS["team_2"]).convert("RGBA")
        elif template_type == "team3" and image_count == 3:
            return Image.open(self.TEMPLATE_PATHS["team_3"]).convert("RGBA")
        elif template_type == "team4" and image_count == 4:
            return Image.open(self.TEMPLATE_PATHS["team_4"]).convert("RGBA")
        elif template_type == "team5" and image_count == 5:
            return Image.open(self.TEMPLATE_PATHS["team_5"]).convert("RGBA")
        else:
            raise ValueError("Invalid template type or image count", template_type, image_count)

    # def _fetch_and_prepare_image(self, url: str) -> Image.Image:
    #     response = requests.get(url)
    #     response.raise_for_status()
    #     overlay_img = Image.open(BytesIO(response.content)).convert("RGBA")
    #     return overlay_img.resize((400, 400))  # Resize all images 

    # def _fetch_and_prepare_image(self, url: str) -> Image.Image:
        response = requests.get(url)
        response.raise_for_status()
        overlay_img = Image.open(BytesIO(response.content)).convert("RGBA")
        resized_img = overlay_img.resize((400, 400))  # Resize all images
    
        border_size = (resized_img.width // 2, resized_img.height // 2)
        
        # Add the border
        bordered_img = ImageOps.expand(resized_img, (200,200))
        
        return bordered_img

    
    def _fetch_and_prepare_image(self, url: str, template_type: str) -> Image.Image:
        response = requests.get(url)
        response.raise_for_status()

        # Open the image
        overlay_img = Image.open(BytesIO(response.content)).convert("RGBA")

        # Define target size based on template type
        if template_type in ['team1', 'team2', 'team3', 'team4', 'team5']:
            target_size = 400
        else:
            target_size = 700

        min_side = min(overlay_img.width, overlay_img.height)
        left = (overlay_img.width - min_side) // 2
        top = (overlay_img.height - min_side) // 2
        right = left + min_side
        bottom = top + min_side
        square_img = overlay_img.crop((left, top, right, bottom))

     
        resized_img = square_img.resize((target_size, target_size), Image.Resampling.LANCZOS)


        mask = Image.new("L", (target_size, target_size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, target_size, target_size), fill=255)

        # Apply the mask to create a rounded image
        rounded_img = Image.new("RGBA", (target_size, target_size))
        rounded_img.paste(resized_img, (0, 0), mask=mask)

        # Add a border
        border_size = 20
        bordered_img = ImageOps.expand(rounded_img, border=border_size, fill=(255, 255, 255, 0))

        return bordered_img
    
    def _get_position_for_image(self, template_type: str, index: int) -> tuple:
        """Determine positions based on template and index."""
        positions = {
        "mentor":[(160, 718)],
            "regional":[(490, 855)],
            "team_1": [(490, 855)],
            "team_2": [(121, 628), (121, 1080)],
            "team_3": [(121, 628), (121, 1080), (520, 850)],
            "team_4": [(108, 540), (108, 1000), (504, 768), (504, 1215)],
            "team_5": [(106, 640), (106, 1100), (492, 403), (495, 870), (492, 1320)],
        }
        # key = "team_1" if template_type == "mentors" and len(positions["team_4"]) == 1 else "team_4"
        # print("key", key)

        if template_type == 'mentors' or template_type == 'regional_coordinator':
            return positions.get(template_type, positions.get('mentor', [(50, 50)]))[index]
        if template_type == 'team1':
            return positions.get(template_type, positions.get('team_1', [(50, 50)]))[index]
        if template_type == 'team2':
            return positions.get(template_type, positions.get('team_2', [(50, 50)]))[index]
        if template_type == 'team3':
            return positions.get(template_type, positions.get('team_3', [(50, 50)]))[index]
        if template_type == 'team4':
            return positions.get(template_type, positions.get('team_4', [(50, 50)]))[index]
        if template_type == 'team5':
            return positions.get(template_type, positions.get('team_5', [(50, 50)]))[index]
        
        return positions.get(template_type, positions.get('team_1', [(50, 50)]))[index]

    def _add_text_to_flyer(self, img: Image.Image, name: str):
        
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("./static/fonts/tic/ProximaNova-Bold.otf", 85)
        
        
        draw.text((1190, 1320), name, fill="black", font=font)

    def _image_to_bytes(self, img: Image.Image) -> bytes:
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()









# curl -X POST "http://localhost:8000/tic/generate-new-flyer/" \
# -H "Content-Type: application/json" \
# -d '{
#   "name": "New Flyer Sample",
#   "template_type": "team",
#   "images": ["https://utfs.io/f/f8d5d4f6-1578-41c0-b8cb-e4ddc7c5a065-4kalwz.jpg"]
# }'



# curl -X POST "http://localhost:8000/tic/generate-new-flyer/" -H "Content-Type: application/json" -d '{
#   "name": "Foghab Ulrich",
#   "template_type": "mentors",
#   "images": ["https://utfs.io/f/f8d5d4f6-1578-41c0-b8cb-e4ddc7c5a065-4kalwz.jpg"]
# }' --output new.png
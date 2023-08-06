import sys
from PIL import Image

class img2array:
    """Converts an image to an array"""

    image_path = ""
    item_prefix = ""
    item_postfix = ""
    color_format = ""
    image_file: Image.Image

    image_height = 0
    image_width = 0

    def __init__(
        self, image_path: str, item_prefix: str, item_postfix: str, color_format="RGB"
    ):
        self.image_path = image_path
        self.item_prefix = item_prefix
        self.item_postfix = item_postfix
        self.color_format = color_format

    def open_file(self, image_path: str):
        self.image_file = Image.open(image_path)
        self.image_height = self.image_file.height
        self.image_width = self.image_file.width

    def print_file(self):
        print("{")
        for y in range(self.image_height):
            print("{", end="")
            for x in range(self.image_width):
                comma = ", "
                if x >= self.image_width - 1:
                    comma = ""
                print(f"{self.create_item(self.image_file.getpixel(tuple([x, y])))}{comma}", end="")
            comma = ","
            if y >= self.image_height - 1:
                comma = ""
            print("}" + comma)
        print("}")

    def set_color_format(self, pixel_value: tuple | str) -> str:
        # Default pixel_value is RGBA
        if self.color_format == "RGB":
            return f"{pixel_value[0]}, {pixel_value[1]}, {pixel_value[2]}"
        elif self.color_format == "RGBA":
            return f"{pixel_value[0]}, {pixel_value[1]}, {pixel_value[2]}, {pixel_value[3]}"
        elif self.color_format == "Hex":
            return f"#{0:02x}{1:02x}{2:02x}".format(
                pixel_value[0], pixel_value[1], pixel_value[2]
            )
        elif self.color_format == "HexAlpha":
            return f"#{0:02x}{1:02x}{2:02x}{3:02x}".format(
                pixel_value[0], pixel_value[1], pixel_value[2], pixel_value[3]
            )
        elif self.color_format == "" or self.color_format == None:
            print("No color format set, using RGB as a fallback.")
            self.color_format = "RGB"
            return self.create_item(pixel_value)
        print(f"Unknown color format {self.color_format}, exiting.")
        sys.exit(1)

    def create_item(self, pixel_value: tuple | str) -> str:
        val = self.set_color_format(pixel_value)
        return f"{self.item_prefix}{val}{self.item_postfix}"

    def close_file(self):
        self.image_file.close()

    def run(self):
        self.open_file(self.image_path)
        self.print_file()
        self.close_file()
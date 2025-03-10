import json
import base64
from pathlib import Path


def load_json_data(file_path: str) -> dict:
    """Load and parse JSON data from file."""
    with open(file_path, "r") as file:
        return json.load(file)


def extract_base64_image(data: dict) -> str | None:
    """Extract base64 encoded image string from data."""
    return data.get("plots", {}).get("image", "")


def save_decoded_image(base64_image: str, output_path: str) -> None:
    """Decode base64 string and save as image file."""
    image_data = base64.b64decode(base64_image)
    with open(output_path, "wb") as image_file:
        image_file.write(image_data)


def main(input_path: Path | str, output_path: Path | str):
    data = load_json_data(input_path)
    base64_image = extract_base64_image(data)

    if base64_image:
        save_decoded_image(base64_image, output_path)
        print(f"Image saved as {output_path}")
    else:
        print("No image data found in response.json")


if __name__ == "__main__":
    input_path = "" # add input path here
    output_path = "plots/plot.png" # add output path here

    main(input_path, output_path)

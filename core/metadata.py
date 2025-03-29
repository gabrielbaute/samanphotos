"""Extract metadata from image files."""

import exifread
from flask import current_app
from datetime import datetime


def extract_metadata(filepath):
    """Extract metadata from an image file.
    Args:
        filepath (str): Path to the image file
    Returns:
        dict: Metadata extracted from the image
    """
    with open(filepath, "rb") as f:
        tags = exifread.process_file(f)

    metadata = {}
    try:
        if "EXIF DateTimeOriginal" in tags:
            date_taken = tags["EXIF DateTimeOriginal"].values
            metadata["date_taken"] = datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")

        if "Image Make" in tags:
            metadata["camera_make"] = tags["Image Make"].values

        if "Image Model" in tags:
            metadata["camera_model"] = tags["Image Model"].values

        if "EXIF FocalLength" in tags:
            metadata["focal_length"] = str(tags["EXIF FocalLength"].values)

        if "EXIF FNumber" in tags:
            metadata["aperture"] = str(tags["EXIF FNumber"].values)

        if "EXIF ISOSpeedRatings" in tags:
            metadata["iso"] = str(tags["EXIF ISOSpeedRatings"].values)

        if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags:
            lat_ref = tags.get("GPS GPSLatitudeRef").values
            lon_ref = tags.get("GPS GPSLongitudeRef").values
            lat = convert_to_degrees(tags["GPS GPSLatitude"])
            lon = convert_to_degrees(tags["GPS GPSLongitude"])
            if lat_ref != "N":
                lat = -lat
            if lon_ref != "E":
                lon = -lon
            metadata["gps_latitude"] = str(lat)
            metadata["gps_longitude"] = str(lon)

        return metadata
    except Exception as e:
        current_app.logger.error(f"Error extracting metadata: {e}")


def convert_to_degrees(value):
    """Convert GPS coordinates to decimal degrees.
    Args:
        value (exifread.utils.Ratio): GPS coordinates
    Returns:
        float: GPS coordinates in decimal degrees
    """
    d, m, s = [float(x.num) / float(x.den) for x in value.values]
    return d + (m / 60.0) + (s / 3600.0)

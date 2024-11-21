import csv
import os
import sys
import django
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings.development")
django.setup()

from artwork.models import Artwork


def clean_boolean(value):
    """Convert various string representations to boolean"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "t", "yes", "y", "1")
    return bool(value)


def load_artworks_from_csv(csv_path):
    default_status = "unavailable"
    default_year_created = 2024
    """
    Load artworks from CSV file.

    Expected CSV columns:
    painting_number, title, medium, paper, width_inches, height_inches, price_cents, category

    Args:
        csv_path (str): Path to CSV file
    """
    successful_imports = []
    failed_imports = []

    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                artwork = Artwork.objects.create(
                    painting_number=int(row["painting_number"]),
                    title=row["title"] or "",
                    medium=row["medium"],
                    paper=clean_boolean(row["paper"]),
                    width_inches=Decimal(row["width_inches"]),
                    height_inches=Decimal(row["height_inches"]),
                    price_cents=int(row["price_cents"]),
                    category=row["category"],
                    status=default_status,
                    painting_year=default_year_created,
                )
                successful_imports.append(artwork.title)

            except Exception as e:
                failed_imports.append(
                    {"title": row.get("title", "Unknown"), "error": str(e)}
                )

    print(f"\nSuccessfully imported {len(successful_imports)} artworks:")
    for title in successful_imports:
        print(f"✓ {title}")

    if failed_imports:
        print(f"\nFailed to import {len(failed_imports)} artworks:")
        for fail in failed_imports:
            print(f"✗ {fail['title']}: {fail['error']}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load artworks from CSV file")
    parser.add_argument("csv_path", help="Path to CSV file")

    args = parser.parse_args()

    print(f"Loading artworks from {args.csv_path}")

    load_artworks_from_csv(args.csv_path)

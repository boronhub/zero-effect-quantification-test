from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable

from translate import Translator
from deep_translator import GoogleTranslator


def parse_args() -> argparse.Namespace:
    base_dir = Path(__file__).resolve().parent
    default_input = base_dir / "stimulus_table_all_exps.csv"
    default_output = base_dir / "stimulus_table_all_exps_zh.csv"
    default_reference = Path(__file__).resolve().parent.parent / "mandarin_exp" / "stimulus_table_all_exps_zh_bak.csv"

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=default_input,
        help=f"Input CSV path (default: {default_input})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output,
        help=f"Output CSV path (default: {default_output})",
    )
    parser.add_argument(
        "--reference",
        type=Path,
        default=default_reference,
        help=f"Reference CSV path for Filler Image lookups (default: {default_reference})",
    )
    return parser.parse_args()


def translate(text: str) -> str:
    try:
        translator = Translator(from_lang="de", to_lang="zh")
        result = translator.translate(text)
        return result if result is not None else text
    except Exception:
        # Fallback to GoogleTranslator if translate library fails
        try:
            translator = GoogleTranslator(source="de", target="zh-CN")
            result = translator.translate(text)
            return result if result is not None else text
        except Exception:
            # If all else fails, return the original text
            return text


def translate_rows(
    rows: Iterable[dict[str, str]],
    reference_images: Dict[str, str],
) -> list[dict[str, str]]:
    cache: Dict[str, str] = {}
    out_rows: list[dict[str, str]] = []

    def tr(text: str) -> str:
        key = (text or "").strip()
        if not key:
            return ""
        if key in cache:
            return cache[key]

        translated = translate(key)
        cache[key] = translated
        return translated

    for row in rows:
        row = dict(row)
        row["Sentence_german"] = tr(row.get("Sentence_german", ""))
        row["Expected_answer"] = tr(row.get("Expected_answer", ""))
        row["color_adjective1"] = tr(row.get("color_adjective1", ""))
        row["color_adjective2"] = tr(row.get("color_adjective2", ""))
        
        # Add Image column based on Experiment type
        experiment = row.get("Experiment", "")
        if experiment == "Filler":
            # For Filler, look up Image from reference file
            item = row.get("Item", "")
            condition = row.get("Condition", "")
            key = f"{experiment}_{item}_{condition}"
            row["Image"] = reference_images.get(key, "")
        else:
            # For other experiments, generate from Item and scenario
            item = row.get("Item", "")
            scenario = row.get("scenario", "")
            row["Image"] = f"pic{item}_{scenario}.svg"
        
        # Add Type column
        row["Type"] = "Trial"
        
        out_rows.append(row)

    return out_rows


def main() -> None:
    args = parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input CSV not found: {args.input}")

    # Load reference file for Filler Image lookups
    reference_images: Dict[str, str] = {}
    if args.reference.exists():
        with args.reference.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("Experiment") == "Filler":
                    experiment = row.get("Experiment", "")
                    item = row.get("Item", "")
                    condition = row.get("Condition", "")
                    image = row.get("Image", "")
                    key = f"{experiment}_{item}_{condition}"
                    reference_images[key] = image

    with args.input.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("Input CSV has no header row.")
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    translated_rows = translate_rows(rows, reference_images)

    for old, new in (
        ("Sentence_german", "Sentence_chinese"),
        ("Expected_answer", "Expected_answer_zh"),
        ("color_adjective1", "color_adjective1_zh"),
        ("color_adjective2", "color_adjective2_zh"),
    ):
        if old in fieldnames:
            fieldnames[fieldnames.index(old)] = new
        for row in translated_rows:
            if old in row:
                row[new] = row.pop(old)

    # Add Image and Type columns to fieldnames if not already present
    if "Image" not in fieldnames:
        fieldnames.append("Image")
    if "Type" not in fieldnames:
        fieldnames.append("Type")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(translated_rows)

    print(f"Wrote translated CSV to: {args.output}")


if __name__ == "__main__":
    main()
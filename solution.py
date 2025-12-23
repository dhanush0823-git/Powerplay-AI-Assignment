import json
import re
from datetime import datetime, timedelta


def detect_urgency(text):
    """
    Simple rule-based urgency detection.
    """
    text = text.lower()

    if "urgent" in text or "asap" in text or "immediately" in text:
        return "high"

    if "soon" in text or "in 7 days" in text or "next week" in text:
        return "medium"

    return "low"


def detect_deadline(text):
    """
    Extract deadline if clearly mentioned.
    If unclear, return None.
    """
    text = text.lower()

    # Example: "in 5 days"
    match = re.search(r"in (\d+) days", text)
    if match:
        days = int(match.group(1))
        deadline_date = datetime.today() + timedelta(days=days)
        return deadline_date.date().isoformat()

    # Example: "by March 30"
    match = re.search(r"by ([a-z]+ \d{1,2})", text)
    if match:
        try:
            current_year = datetime.today().year
            date_string = f"{match.group(1)} {current_year}"

            date_obj = datetime.strptime(date_string, "%B %d %Y")
            return date_obj.date().isoformat()

        except ValueError:
            return None

    return None


def extract_quantity_and_unit(text):
    """
    Extract quantity and unit together.
    """
    match = re.search(r"(\d+)\s*(units|bags|truckloads|kg|tons)", text.lower())
    if match:
        return int(match.group(1)), match.group(2)

    return None, None


def extract_material(text):
    """
    Very basic material detection.
    """
    text = text.lower()

    if "cement" in text:
        return "cement"
    if "steel" in text:
        return "steel bars"
    if "sand" in text:
        return "river sand"

    return None


def extract_project(text):
    """
    Extract project name if mentioned.
    """
    match = re.search(r"project ([a-z0-9\s]+)", text.lower())
    if match:
        return match.group(1).strip().title()

    return None


def extract_location(text):
    """
    Extract common city names.
    """
    text = text.lower()

    if "mumbai" in text:
        return "Mumbai"
    if "bangalore" in text:
        return "Bangalore"
    if "chennai" in text:
        return "Chennai"
    if "delhi" in text:
        return "Delhi"

    return None


def convert_text_to_json(text):
    """
    Main conversion function.
    Always returns valid schema.
    """
    quantity, unit = extract_quantity_and_unit(text)

    return {
        "material_name": extract_material(text),
        "quantity": quantity,
        "unit": unit,
        "project_name": extract_project(text),
        "location": extract_location(text),
        "urgency": detect_urgency(text),
        "deadline": detect_deadline(text)
    }


def run(input_file, output_file):
    """
    Reads input lines and writes structured JSON output.
    """
    results = []

    with open(input_file, "r") as file:
        for line in file:
            if line.strip():
                parsed_output = convert_text_to_json(line)
                results.append(parsed_output)

    with open(output_file, "w") as file:
        json.dump(results, file, indent=2)


if __name__ == "__main__":
    run("test_inputs.txt", "outputs.json")

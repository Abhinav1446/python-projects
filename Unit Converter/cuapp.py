from flask import Flask, render_template, request

app = Flask(__name__)

# ------------------------------
# Conversion tables / logic
# ------------------------------

# Length: all units relative to 1 meter
UNIT_TO_METER = {
    "m": 1,
    "cm": 0.01,
    "mm": 0.001,
    "km": 1000,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144
}


def convert_length(value, unit_from, unit_to):
    """
    Convert a length from unit_from to unit_to via meters.
    Raises ValueError if units are not supported.
    """
    unit_from = unit_from.lower().strip()
    unit_to = unit_to.lower().strip()

    if unit_from not in UNIT_TO_METER or unit_to not in UNIT_TO_METER:
        raise ValueError("Unsupported unit. Try: m, cm, mm, km, in, ft, yd")

    # Step 1: convert input value to meters
    value_in_meters = value * UNIT_TO_METER[unit_from]
    # Step 2: convert meters to target unit
    result = value_in_meters / UNIT_TO_METER[unit_to]
    return result


# Weight: all units relative to 1 kilogram
UNIT_TO_KG = {
    "kg": 1,
    "g": 0.001,
    "mg": 0.000001,
    "lb": 0.453592,
    "oz": 0.0283495,
}


def weight_convert(value, unit_from, unit_to):
    """
    Convert a weight from unit_from to unit_to via kilograms.
    Raises ValueError if units are not supported.
    """
    unit_from = unit_from.lower().strip()
    unit_to = unit_to.lower().strip()

    if unit_from not in UNIT_TO_KG or unit_to not in UNIT_TO_KG:
        raise ValueError("Unsupported unit. Try: kg, g, mg, lb, oz")

    # Step 1: convert to kg
    value_in_kg = value * UNIT_TO_KG[unit_from]
    # Step 2: convert kg to target unit
    result = value_in_kg / UNIT_TO_KG[unit_to]
    return result


def convert_temp(value, unit_from, unit_to):
    """
    Convert temperature between Celsius (c), Fahrenheit (f), and Kelvin (k).
    Raises ValueError if units are not supported.
    """
    unit_from = unit_from.lower().strip()
    unit_to = unit_to.lower().strip()

    # If both units are same, no conversion needed
    if unit_from == unit_to:
        return value

    # Convert from source unit to Celsius
    if unit_from == "c":
        c = value
    elif unit_from == "f":
        c = (value - 32) * (5 / 9)
    elif unit_from == "k":
        c = value - 273.15
    else:
        raise ValueError("Unsupported unit. Try: c, f, k")

    # Convert from Celsius to target unit
    if unit_to == "c":
        return c
    elif unit_to == "f":
        return c * (9 / 5) + 32
    elif unit_to == "k":
        return c + 273.15
    else:
        raise ValueError("Unsupported unit. Try: c, f, k")


# ------------------------------
# Routes
# ------------------------------

@app.route("/", methods=["GET"])
def index():
    """
    Main page.
    Uses ?type=length / ?type=weight / ?type=temp to decide which tab is active.
    """
    measurement = request.args.get("type", "length")
    return render_template(
        "index.html",
        measurement=measurement,
        result=None,
        show_result=False,   # initially, just show the form
        error=None,
        unit_to=None,
        value=None,
        unit_from=None,
    )


@app.route("/convert_length", methods=["POST"])
def do_length():
    """
    Handle length conversion form submit.
    """
    length_str = (request.form.get("length") or "").strip()
    unit_from = (request.form.get("unit_from") or "").strip()
    unit_to = (request.form.get("unit_to") or "").strip()

    error = None
    result = None
    show_result = False
    value = None

    # Validate that a value was entered
    if not length_str:
        error = "Please enter a length value."
    else:
        try:
            value = float(length_str)
            result = convert_length(value, unit_from, unit_to)
            show_result = True
        except ValueError as e:
            # This catches invalid units and invalid numbers
            error = str(e)
            show_result = False

    return render_template(
        "index.html",
        measurement="length",
        result=result,
        error=error,
        show_result=show_result,
        unit_to=unit_to,
        value=value,
        unit_from=unit_from,
    )


@app.route("/convert_weight", methods=["POST"])
def do_weight():
    """
    Handle weight conversion form submit.
    """
    weight_str = (request.form.get("weight") or "").strip()
    unit_from = (request.form.get("unit_from") or "").strip()
    unit_to = (request.form.get("unit_to") or "").strip()

    error = None
    result = None
    show_result = False
    value = None

    if not weight_str:
        error = "Please enter a weight value."
    else:
        try:
            value = float(weight_str)
            result = weight_convert(value, unit_from, unit_to)
            show_result = True
        except ValueError as e:
            error = str(e)
            show_result = False

    return render_template(
        "index.html",
        measurement="weight",
        result=result,
        unit_to=unit_to,
        error=error,
        show_result=show_result,
        value=value,
        unit_from=unit_from,
    )


@app.route("/convert_temp", methods=["POST"])
def do_temp():
    """
    Handle temperature conversion form submit.
    """
    temp_str = (request.form.get("temp") or "").strip()
    unit_from = (request.form.get("unit_from") or "").strip()
    unit_to = (request.form.get("unit_to") or "").strip()

    error = None
    result = None
    show_result = False
    value = None

    if not temp_str:
        error = "Please enter a temperature value."
    else:
        try:
            value = float(temp_str)
            result = convert_temp(value, unit_from, unit_to)
            show_result = True
        except ValueError as e:
            error = str(e)
            show_result = False

    return render_template(
        "index.html",
        measurement="temp",
        result=result,
        error=error,
        unit_to=unit_to,
        show_result=show_result,
        value=value,
        unit_from=unit_from,
    )


if __name__ == "__main__":
    app.run(debug=True)

import json


def compare_json_expected_actual(expected_json, actual_json):
    def normalize_values(data):
        """Normalizes values for comparison (e.g., handles unit variations)."""
        normalized_data = {}
        for key, value in data.items():
            normalized_value = value
            if isinstance(value, str):
                normalized_value = value.replace("percent", "%").replace("pct", "%").strip()
                if key == "maturity" and "years" in normalized_value:
                    years = int(normalized_value.split(" ")[0])
                    normalized_value = str(years * 12) + " months"
                if key == "coupon" or key == "coupon_frequency":
                    normalized_value = normalized_value.replace("cpns", "coupons")
            normalized_data[key] = normalized_value
        return normalized_data

    normalized_expected = normalize_values(expected_json)
    normalized_actual = normalize_values(actual_json)

    expected_filtered = {k: v for k, v in normalized_expected.items()
                         if k not in ("confidence", "explanation", "product", "from", "advice")}
    actual_filtered = {k: v for k, v in normalized_actual.items()
                       if k not in ("confidence", "explanation", "product", "from", "advice")}

    differences = {}
    match = True

    for key in set(expected_filtered.keys()) | set(actual_filtered.keys()):
        if expected_filtered.get(key) != actual_filtered.get(key):
            match = False
            differences[key] = {
                "expected": expected_filtered.get(key),
                "actual": actual_filtered.get(key),
            }

    return match, differences


# Example usage:
expected_str = """
{
    "underlying": "RSH.T",
    "maturity": "1 years",
    "barrier": "50 percent",
    "coupon": "semi-annually cpns",
    "coupon_rate": "15 pct",
    "autocall_frequency": "quarterly ",
    "autocall_barrier": "100 percent",
    "notional": "USD $30000",
    "from": "Henry Taylor"
}
"""

actual_str = """
{
    "product": "autocall",
    "underlying": "RSH.T",
    "maturity": "12 months",
    "barrier": "50 %",
    "coupon": "semi-annually coupons",
    "coupon_rate": "15 %",
    "autocall_frequency": "quarterly",
    "autocall_barrier": "100 %",
    "notional": "USD $30000",
    "from": "Eve",
    "confidence": "95%",
    "explanation": "The RFQ was parsed by identifying key terms and their associated values. The maturity is converted from years to months for consistency, and the autocall frequency is identified as quarterly based on the term qtr."
}
"""

expected = json.loads(expected_str)
actual = json.loads(actual_str)

match, differences = compare_json_expected_actual(expected, actual)

if match:
    print("Results match!")
else:
    print("Results do not match. Differences:")
    print(json.dumps(differences, indent=4))

from typing import Dict, List, Tuple
import json
from params import create_translation_dict


def translate(json_data: Dict,
              translation_dict: Dict,
              debug: bool = False) -> Dict:
    """Translate JSON data using the translation dictionary."""
    for key, value in json_data.items():
        translated = []
        for word in value.split():
            if word in translation_dict:
                translated.append(translation_dict[word])
            else:
                translated.append(word)
        translated_value = " ".join(translated)
        if debug:
            print(f"key: {key}, value: {value} -> translated: {translated_value}")
        json_data[key] = translated_value
        if isinstance(value, dict):
            translate(value, translation_dict)
    return json_data


def compare_json_expected_actual(expected_json,
                                 actual_json) -> Tuple[bool, Dict]:
    trans_dict = create_translation_dict()

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

    normalized_expected = normalize_values(translate(expected_json, trans_dict))
    normalized_actual = normalize_values(translate(actual_json, trans_dict))

    expected_filtered = {k: v for k, v in normalized_expected.items()
                         if k not in ("confidence", "explanation", "product", "from", "advice", "language")}
    actual_filtered = {k: v for k, v in normalized_actual.items()
                       if k not in ("confidence", "explanation", "product", "from", "advice", "language")}

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
actual_fr = """
{
    "underlying": "TPH.SW",
    "maturity": "3 ans",
    "barrier": "60 pourcentage",
    "coupon": "annuellement",
    "coupon_rate": "15 pourcentage",
    "autocall_frequency": "annuellement",
    "autocall_barrier": "100 pourcentage",
    "notional": "USD $20000",
    "from": "Alexandre Moreau",
    "language": "fr"
}
"""
actual_es = """
{
    "underlying": "VSL.T",
    "maturity": "4 a\u00f1os",
    "barrier": "70 porcentaje",
    "coupon": "semestralmente",
    "coupon_rate": "8 porcentaje",
    "autocall_frequency": "anualmente",
    "autocall_barrier": "105 porcentaje",
    "notional": "USD $25000",
    "from": "Ivonne Fern\u00e1ndez",
    "language": "es"
}
"""

if __name__ == "__main__":
    expected = json.loads(expected_str)
    actual = json.loads(actual_str)

    trans_dict = create_translation_dict()
    print("Translating English to English")
    res = translate(expected, trans_dict, debug=True)
    print("Res:", json.dumps(res, indent=4))
    print("\nTranslating French to English")
    res = translate(json.loads(actual_fr), trans_dict, debug=True)
    print("Res:", json.dumps(res, indent=4))
    print("\nTranslating Spanish to English")
    res = translate(json.loads(actual_es), trans_dict, debug=True)
    print("Res:", json.dumps(res, indent=4))

    print("\nField by field comparison, with normalization:")
    match, differences = compare_json_expected_actual(expected, actual)
    if match:
        print("Results match!")
    else:
        print("Results do not match. Differences:")
        print(json.dumps(differences, indent=4))

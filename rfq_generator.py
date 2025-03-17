import random
import uuid
import json
from util import clear_screen
from collections import namedtuple
from closing import get_colloquial_closing
from opening_request import generate_colloquial_request
from params import maturity_units_lang, percent_units_lang, frequencies_lang, coupon_types_lang, param_names_lang, names_lang
from product_def import ELN, AUTOCALL, products
from trail import log

imaginary_stocks = {
    "BQM.PA": "Bennett Quantum Mining",
    "CIF.T": "Campbell Innovative Finance",
    "FAF.MX": "Foster Advanced Finance",
    "TPH.SW": "Turner Precision Health",
    "CDM.HK": "Campbell Dynamic Mining",
    "VSL.T": "Vance Select Leisure",
    "KIF.L": "Kelly Innovative Finance",
    "ODA.T": "Owens Dynamic Automotive",
    "LZL.US": "Lambert Zenith Leisure",
    "LVL.PA": "Lambert Vanguard Leisure",
    "BSM.MX": "Bennett Synergy Mining",
    "YSR.MX": "York Superior Robotics",
    "IPR.MX": "Irwin Pinnacle Robotics",
    "TER.L": "Turner Elite Robotics",
    "EDA.US": "Edwards Dynamic Automotive",
    "SIA.PA": "Shaw Innovative Automotive",
    "RSH.T": "Reed Select Health",
    "YSL.SA": "York Superior Leisure",
    "GQM.T": "Gibson Quantum Mining",
    "TGF.PA": "Turner Global Finance"
}

underlyings = [imgs[0] for imgs in imaginary_stocks.items()]

languages = ["en", "fr", "es"]


def generate_eln_rfq():
    """Generates a random ELN RFQ email as an f-string with typos, abbreviations, and more variety."""

    # underlyings - global var
    language = random.choice(languages)
    maturities = ["6", "12", "18", "24"]
    maturity_units = maturity_units_lang
    participations = ["70", "80", "90"]
    participation_units = percent_units_lang
    barriers = ["40", "50", "60"]
    barrier_units = percent_units_lang
    coupon_frequency = frequencies_lang
    coupon_units = percent_units_lang
    coupon_types = coupon_types_lang

    underlying = random.choice(underlyings)
    maturity_val = random.choice(maturities)
    maturity_unit_full, maturity_unit_abbr = random.choice(maturity_units[language])
    participation_val = random.choice(participations)
    participation_unit_full, participation_unit_abbr = random.choice(participation_units[language])
    barrier_val = random.choice(barriers)
    barrier_unit_full, barrier_unit_abbr = random.choice(barrier_units[language])
    coupon_unit_full, coupon_unit_abbr = random.choice(coupon_units[language])
    coupon_type_full, coupon_type_abbr = random.choice(coupon_types[language])
    coupon_val = random.randint(1, 10)
    coupon_frequency_full, coupon_frequency_abbr = random.choice(coupon_frequency[language])
    notional = f"USD ${random.randint(1, 10) * 5000}"
    colloquial_request = generate_colloquial_request(product_name=products[ELN], language_code=language)
    colloquial_closing = get_colloquial_closing(language)
    first_name, family_name, nickname = random.choice(names_lang[language])

    params = {
        "underlying": underlying,
        "maturity": f"{maturity_val} {random.choice([maturity_unit_full, maturity_unit_abbr])}",
        "participation": f"{participation_val} {random.choice([participation_unit_full, participation_unit_abbr])}",
        "barrier": f"{barrier_val} {random.choice([barrier_unit_full, barrier_unit_abbr])}",
        "coupon": f"{coupon_val} {random.choice([coupon_unit_full, coupon_unit_abbr])} {random.choice([coupon_type_full, coupon_type_abbr])}",
        "coupon_frequency": f"{random.choice([coupon_frequency_full, coupon_frequency_abbr])}",
        "notional": notional
    }

    param_keys = list(params.keys())
    random.shuffle(param_keys)

    param_strings = []
    for key in param_keys:
        value = params[key]
        if key in param_names_lang[language]:
            param_name = random.choice(param_names_lang[language][key])
        else:
            param_name = ""
        value = " ".join([param_name, value])
        param_strings.append(value)

    sign_offs = [
        f"{colloquial_closing} {first_name} {family_name}",
        f"{colloquial_closing} {first_name}",
        f"{colloquial_closing} {first_name[0]}. {family_name}",
        f"{colloquial_closing} {nickname}"
    ]

    formal_params = {
        "underlying": underlying,
        "maturity": f"{maturity_val} {maturity_unit_full}",
        "participation": f"{participation_val} {participation_unit_full}",
        "barrier": f"{barrier_val} {barrier_unit_full}",
        "coupon": f"{coupon_val} {coupon_unit_full}",
        "coupon_type": f"{coupon_type_full}",
        "coupon_frequency": f"{coupon_frequency_full}",
        "notional": notional,
        "from": f"{first_name} {family_name}",
        "language": language
    }

    request = f"{colloquial_request} {', '.join(param_strings)}. {random.choice(sign_offs)}"

    result = {
        "product": "eln",
        "uuid": str(uuid.uuid4()),
        "parameters": formal_params,
        "request": request
    }
    return result


def generate_autocall_rfq():
    """Generates a random autocall RFQ email as an f-string with typos, abbreviations, and more variety."""

    # underlyings - global var
    language = random.choice(languages)
    maturities = ["1", "2", "3", "4", "5"]
    maturity_units = maturity_units_lang
    barriers = ["50", "60", "70"]
    barrier_units = percent_units_lang
    coupons = frequencies_lang
    coupon_rates = ["8", "10", "12", "15"]
    coupon_rate_units = percent_units_lang
    autocall_frequencies = frequencies_lang
    autocall_barriers = ["100", "102", "105"]
    autocall_barrier_units = percent_units_lang
    notional = f"USD ${random.randint(1, 10) * 5000}"

    underlying = random.choice(underlyings)
    maturity_val = random.choice(maturities)
    maturity_unit_full, maturity_unit_abbr = random.choice(maturity_units[language])
    barrier_val = random.choice(barriers)
    barrier_unit_full, barrier_unit_abbr = random.choice(barrier_units[language])
    coupon_full, coupon_abbr = random.choice(coupons[language])
    coupon_rate_val = random.choice(coupon_rates)
    coupon_rate_unit_full, coupon_rate_unit_abbr = random.choice(coupon_rate_units[language])
    autocall_frequency_full, autocall_frequency_abbr = random.choice(autocall_frequencies[language])
    autocall_barrier_val = random.choice(autocall_barriers)
    autocall_barrier_unit_full, autocall_barrier_unit_abbr = random.choice(autocall_barrier_units[language])
    colloquial_request = generate_colloquial_request(product_name=products[AUTOCALL], language_code=language)
    colloquial_closing = get_colloquial_closing(language)
    first_name, family_name, nickname = random.choice(names_lang[language])

    params = {
        "underlying": underlying,
        "maturity": f"{maturity_val} {random.choice([maturity_unit_full, maturity_unit_abbr])}",
        "barrier": f"{barrier_val} {random.choice([barrier_unit_full, barrier_unit_abbr])}",
        "coupon_frequency": f"{random.choice([coupon_full, coupon_abbr])}",
        "coupon": f"{coupon_rate_val} {random.choice([coupon_rate_unit_full, coupon_rate_unit_abbr])}",
        "autocall_frequency": f"{random.choice([autocall_frequency_full, autocall_frequency_abbr])}",
        "autocall_barrier": f"{autocall_barrier_val} {random.choice([autocall_barrier_unit_full, autocall_barrier_unit_abbr])}",
        "notional": notional
    }

    param_keys = list(params.keys())
    random.shuffle(param_keys)

    param_strings = []
    for key in param_keys:
        value = params[key]
        if key in param_names_lang[language]:
            param_name = random.choice(param_names_lang[language][key])
        else:
            param_name = ""
        value = " ".join([param_name, value])
        param_strings.append(value)

    sign_offs = [
        f"{colloquial_closing} {first_name} {family_name}",
        f"{colloquial_closing} {first_name}",
        f"{colloquial_closing} {first_name[0]}. {family_name}",
        f"{colloquial_closing} {nickname}"
    ]

    formal_params = {
        "underlying": underlying,
        "maturity": f"{maturity_val} {maturity_unit_full}",
        "barrier": f"{barrier_val} {barrier_unit_full}",
        "coupon_frequency": f"{coupon_full}",
        "coupon": f"{coupon_rate_val} {coupon_rate_unit_full}",
        "autocall_frequency": f"{autocall_frequency_full}",
        "autocall_barrier": f"{autocall_barrier_val} {autocall_barrier_unit_full}",
        "notional": notional,
        "from": f"{first_name} {family_name}",
        "language": language
    }

    request = f"{colloquial_request} {', '.join(param_strings)}. {random.choice(sign_offs)}"

    result = {
        "product": "autocall",
        "uuid": str(uuid.uuid4()),
        "parameters": formal_params,
        "request": request
    }
    return result


def generate_random_rfq():
    if random.random() > 0.5:
        doc = generate_eln_rfq()
    else:
        doc = generate_autocall_rfq()
    return doc


if __name__ == "__main__":
    simple = False  # False give a full dump of json
    clear_screen()
    for _ in range(5):
        if simple:
            log().debug(f"> {generate_random_rfq()['request']}\n")
        else:
            log().debug(json.dumps(generate_random_rfq(), indent=3))

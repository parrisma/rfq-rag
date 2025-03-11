import random
import uuid
import json
from collections import namedtuple

Product = namedtuple('Product', ['name'])
ELN = 0
AUTOCALL = 1
products = [None, None]
products[ELN] = Product("eln").name
products[AUTOCALL] = Product("autocall").name

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

colloquial_closings = [
    "Thx, appreciate it.",
    "Cheers, let me no.",
    "Thx in advance.",
    "Let me no wen u have a price.",
    "Appreciate the help.",
    "Thx, lookin forward to hearin back.",
    "Thx, plez advise.",
    "Let me no ur thoughts.",
    "Thx, best regards.",
    "Thx, plez reply wen u can.",
    "Cheerz, reply asap.",
    "Thx, any info is gud.",
    "Let me no wen u got it.",
    "Appreciate the quick response.",
    "Thx, let me no soon.",
    "Thx, lookin forward to ur reply.",
    "Plez advise wen u have a price.",
    "Let me no ur pricing thoughts.",
    "Thx, best wishez.",
    "Plez reply with any info.",
    "Thank you, I appreciate your assistance.",
    "Please let me know when you have the price.",
    "Thank you in advance for your prompt response.",
    "Kindly advise when you have pricing available.",
    "I look forward to hearing from you soon.",
    "Please reply at your earliest convenience.",
    "Thank you for your time and consideration.",
    "Please advise when you have an update.",
    "I appreciate your timely response.",
    "Please respond when you are able.",
]

names = [
    ('David', 'Brown', 'Dave'),
    ('Frank', 'Smith', 'Smithy'),
    ('Grace', 'Taylor', 'Gracie'),
    ('David', 'Anderson', 'Dox'),
    ('Ivy', 'Anderson', 'Ive'),
    ('Ivy', 'Brown', 'Brun'),
    ('Grace', 'Wilson', 'Wilx'),
    ('Ivy', 'Anderson', 'Andy'),
    ('Jack', 'Miller', 'Jackie'),
    ('Grace', 'Moore', 'Moe'),
    ('Henry', 'Smith', 'Hank'),
    ('Ben', 'Davis', 'Benny'),
    ('Alex', 'Anderson', 'Ali'),
    ('Jack', 'Smith', 'Bob'),
    ('Ivy', 'Williams', 'Vine'),
    ('Jack', 'Taylor', 'Taz'),
    ('Frank', 'Brown', 'Frankie'),
    ('Ben', 'Wilson', 'Benji'),
    ('Alex', 'Moore', 'Al'),
    ('David', 'Wilson', 'Davie')
]

param_names = {
    "underlying": ["Underlying", "Under", "Und", "Ticker", "Stock", ""],
    "maturity": ["Maturity", "Mat", "Expiry", "Term", ""],
    "participation": ["Participation", "Part", ""],
    "barrier": ["Barrier", "Barr", ""],
    "coupon": ["Coupon", "Cpn", "Coup", ""],
    "coupon_type": ["Coupon Type", "Cpn type", "Coup typ", ""],
    "coupon_frequency": ["Coupon Frequency", "Coupon Freq", "Cpn Freq", ""],
    "notional": ["Notional", "Amount", "Size", "Quantity", ""],
    "autocall_frequency": ["autocall frequency", "autocall freq", "auto freq", "freq", "call freq", "auto freq", "", ""],
    "autocall_barrier": ["autocall barrier", "autocall barr", "auto barr", "barrier", "call barr", "auto barr", "", ""]
}


def generate_colloquial_request(product_name: str) -> str:
    colloquial_requests = [
        "Hey, can u price ths {product_name} RFQ?",
        "Quik quote on an {product_name} note, plez.",
        "Need a price on dis {product_name} RFQ, thx.",
        "Lookin for a qoute on this {product_name}.",
        "Yo, can u get a price 4 me on this {product_name}?",
        "Any chance of gettin a qoute on this {product_name} note?",
        "Could u price this {product_name} up?",
        "Jst need a quick price on this {product_name} RFQ.",
        "Pls get a price for this {product_name}.",
        "Hey, price dis {product_name} note up.",
        "Any ideas on a price 4 dis {product_name} RFQ?",
        "Quick {product_name} price chek?",
        "Can u price dis {product_name}? Tx.",
        "Lookin for a fast qoute on this {product_name}.",
        "Yo, price dis {product_name} 1 up.",
        "Any qoutes floatin on this {product_name} note RFQ?",
        "Price this {product_name}, if u can.",
        "Quick {product_name} RFQ, plez?",
        "Get a price on dis {product_name} note, thx.",
        "Hey, any price ideaz on this {product_name} RFQ?",
        "Could you provide a quote for this {product_name} note?",
        "I require a price for the following {product_name}.",
        "Please price this {product_name}.",
        "We are seeking a quote on this {product_name} security.",
        "Kindly provide a price for this {product_name} RFQ.",
        "I would like to obtain a quote for this {product_name}.",
        "Please get back to me with a price for this {product_name} note.",
        "We need a price on this {product_name}.",
        "Could you please price this {product_name} instrument?",
        "Please provide a quotation for this {product_name}.",
    ]
    fstr_code = compile(f"f'{random.choice(colloquial_requests)}'", "<string>", "eval")
    result = eval(fstr_code)
    return result


def generate_eln_rfq():
    """Generates a random ELN RFQ email as an f-string with typos, abbreviations, and more variety."""

    # underlyings - global var
    maturities = ["6", "12", "18", "24"]
    maturity_units = [("months", "mos"), ("months", "mnth"), ("months", "mth")]
    participations = ["70", "80", "90"]
    participation_units = [("percent", "%"), ("percent", "pct")]
    barriers = ["40", "50", "60"]
    barrier_units = [("percent", "%"), ("percent", "pct")]
    coupon_frequency = [("quarterly", "qtrly"), ("semi-annually", "semi-ann"), ("annually", "ann"), ("quarterly", "qtr")]
    coupon_units = [("", ""), ("percent", "%"), ("percent", "pct")]
    coupon_types = [("fixed", "fxd"), ("fixed", "fixd")]

    underlying = random.choice(underlyings)
    maturity_val = random.choice(maturities)
    maturity_unit_full, maturity_unit_abbr = random.choice(maturity_units)
    participation_val = random.choice(participations)
    participation_unit_full, participation_unit_abbr = random.choice(
        participation_units)
    barrier_val = random.choice(barriers)
    barrier_unit_full, barrier_unit_abbr = random.choice(barrier_units)
    coupon_unit_full, coupon_unit_abbr = random.choice(coupon_units)
    coupon_type_full, coupon_type_abbr = random.choice(coupon_types)
    coupon_val = random.randint(1, 10)
    coupon_frequency_full, coupon_frequency_abbr = random.choice(coupon_frequency)
    notional = f"USD ${random.randint(1, 10) * 5000}"
    colloquial_request = generate_colloquial_request(products[ELN])
    colloquial_closing = random.choice(colloquial_closings)
    first_name, family_name, nickname = random.choice(names)

    params = {
        "underlying": underlying,
        "maturity": f"{maturity_val} {random.choice([maturity_unit_full, maturity_unit_abbr])}",
        "participation": f"{participation_val} {random.choice([participation_unit_full, participation_unit_abbr])}",
        "barrier": f"{barrier_val} {random.choice([barrier_unit_full, barrier_unit_abbr])}",
        "coupon": f"{coupon_val} {random.choice([coupon_unit_full, coupon_unit_abbr])}",
        "coupon_type": f"{random.choice([coupon_type_full, coupon_type_abbr])}",
        "coupon_frequency": f"{random.choice([coupon_frequency_full, coupon_frequency_abbr])}",
        "notional": notional
    }

    param_keys = list(params.keys())
    random.shuffle(param_keys)

    param_strings = []
    for key in param_keys:
        value = params[key]
        if key in param_names:
            param_name = random.choice(param_names[key])
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
        "from": f"{first_name} {family_name}"
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
    maturities = ["1", "2", "3", "4", "5"]
    maturity_units = [("years", "yrs")]
    barriers = ["50", "60", "70"]
    barrier_units = [("percent", "%"), ("percent", "pct")]
    coupons = [("quarterly", "qtr"), ("semi-annually", "semi"), ("annually", "annual"), ("annual", "annual"), ("annual", "ann")]
    coupon_units = [("", ""), ("coupons", "cpns")]
    coupon_rates = ["8", "10", "12", "15"]
    coupon_rate_units = [("percent", "%"), ("pct", "%")]
    autocall_frequencies = [("quarterly", "qtr"), ("semi-annually", "semi"), ("annually", "annual")]
    autocall_frequency_units = [("", "checks")]
    autocall_barriers = ["100", "102", "105"]
    autocall_barrier_units = [("percent", "%"), ("percent", "pct")]
    notional = f"USD ${random.randint(1, 10) * 5000}"

    underlying = random.choice(underlyings)
    maturity_val = random.choice(maturities)
    maturity_unit_full, maturity_unit_abbr = random.choice(
        maturity_units)[0], random.choice(maturity_units)[1]
    barrier_val = random.choice(barriers)
    barrier_unit_full, barrier_unit_abbr = random.choice(barrier_units)
    coupon_full, coupon_abbr = random.choice(coupons)
    coupon_unit_full, coupon_unit_abbr = random.choice(coupon_units)
    coupon_rate_val = random.choice(coupon_rates)
    coupon_rate_unit_full, coupon_rate_unit_abbr = random.choice(
        coupon_rate_units)
    autocall_frequency_full, autocall_frequency_abbr = random.choice(
        autocall_frequencies)
    autocall_frequency_unit_full, autocall_frequency_unit_abbr = random.choice(
        autocall_frequency_units)
    autocall_barrier_val = random.choice(autocall_barriers)
    autocall_barrier_unit_full, autocall_barrier_unit_abbr = random.choice(
        autocall_barrier_units)
    colloquial_request = colloquial_request = generate_colloquial_request(products[AUTOCALL])
    colloquial_closing = random.choice(colloquial_closings)
    first_name, family_name, nickname = random.choice(names)

    params = {
        "underlying": underlying,
        "maturity": f"{maturity_val} {random.choice([maturity_unit_full, maturity_unit_abbr])}",
        "barrier": f"{barrier_val} {random.choice([barrier_unit_full, barrier_unit_abbr])}",
        "coupon": f"{random.choice([coupon_full, coupon_abbr])} {random.choice([coupon_unit_full, coupon_unit_abbr])}",
        "coupon_rate": f"{coupon_rate_val} {random.choice([coupon_rate_unit_full, coupon_rate_unit_abbr])}",
        "autocall_frequency": f"{random.choice([autocall_frequency_full, autocall_frequency_abbr])} {random.choice([autocall_frequency_unit_full, autocall_frequency_unit_abbr])}",
        "autocall_barrier": f"{autocall_barrier_val} {random.choice([autocall_barrier_unit_full, autocall_barrier_unit_abbr])}",
        "notional": notional
    }

    param_keys = list(params.keys())
    random.shuffle(param_keys)

    param_strings = []
    for key in param_keys:
        value = params[key]
        if key in param_names:
            param_name = random.choice(param_names[key])
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
        "coupon": f"{coupon_full} {coupon_unit_full}",
        "coupon_rate": f"{coupon_rate_val} {coupon_rate_unit_full}",
        "autocall_frequency": f"{autocall_frequency_full} {autocall_frequency_unit_full}",
        "autocall_barrier": f"{autocall_barrier_val} {autocall_barrier_unit_full}",
        "notional": notional,
        "from": f"{first_name} {family_name}"
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
    for _ in range(10):
        print(json.dumps(generate_random_rfq(), indent=3))

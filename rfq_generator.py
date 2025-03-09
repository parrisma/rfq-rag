import random
import uuid
import json

products = ["eln","autocall"]

underlyings = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "JPM", "V", "UNH", "XOM",
               "NESN.SW", "ROG.SW", "ASML.AS", "SIE.DE", "SAN.MC", "600519.SS", "TTE.PA", "BP.L", "RIO.L", "TM.T"]  # Global underlyings

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

first_names = ["Alex", "Ben", "Charlie", "David",
               "Eva", "Frank", "Grace", "Henry", "Ivy", "Jack"]
family_names = ["Smith", "Jones", "Williams", "Brown",
                "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson"]
nicknames = ["Al", "Benny", "Chuck", "Dave", "Eve",
             "Frankie", "Gracie", "Hank", "Ive", "Jackie"]


def generate_eln_rfq():
    """Generates a random ELN RFQ email as an f-string with typos, abbreviations, and more variety."""

    underlyings = ["AAPL", "MSFT", "GOOG", "AMZN",
                   "TSLA", "NVDA", "JPM", "V", "UNH", "XOM"]
    maturities = ["6", "12", "18", "24"]
    maturity_units = [("months", "mos"), ("months", "mnth"),
                      ("year", "yr"), ("years", "yrs")]
    participations = ["70", "80", "90"]
    participation_units = [("percent", "%"), ("percent", "pct")]
    barriers = ["40", "50", "60"]
    barrier_units = [("percent", "%"), ("percent", "pct")]
    coupons = [("quarterly", "qtrly"), ("semi-annually",
                                        "semi-ann"), ("annually", "ann")]
    coupon_units = [("", ""), ("coupons", "cpns")]
    coupon_types = ["fixd", "var"]

    colloquial_requests = [
        "Hey, can u price ths ELN RFQ?",
        "Quik quote on an Equity Linked Note, plez.",
        "Need a price on dis ELN RFQ, thx.",
        "Lookin for a qoute on this ELN.",
        "Yo, can u get a price 4 me on this ELN?",
        "Any chance of gettin a qoute on this Equity Linked Note?",
        "Could u price this ELN up?",
        "Jst need a quick price on this ELN RFQ.",
        "Pls get a price for this ELN.",
        "Hey, price dis Equity Linked Note up.",
        "Any ideas on a price 4 dis ELN RFQ?",
        "Quick ELN price chek?",
        "Can u price dis ELN? Tx.",
        "Lookin for a fast qoute on this ELN.",
        "Yo, price dis ELN 1 up.",
        "Any qoutes floatin on this Equity Linked Note RFQ?",
        "Price this ELN, if u can.",
        "Quick ELN RFQ, plez?",
        "Get a price on dis Equity Linked Note, thx.",
        "Hey, any price ideaz on this ELN RFQ?",
        "Could you provide a quote for this Equity Linked Note?",
        "I require a price for the following ELN.",
        "Please price this Equity Linked Note.",
        "We are seeking a quote on this ELN security.",
        "Kindly provide a price for this Equity Linked Note RFQ.",
        "I would like to obtain a quote for this ELN.",
        "Please get back to me with a price for this Equity Linked Note.",
        "We need a price on this ELN.",
        "Could you please price this Equity Linked Note instrument?",
        "Please provide a quotation for this ELN.",
    ]

    underlying = random.choice(underlyings)
    maturity_val = random.choice(maturities)
    maturity_unit_full, maturity_unit_abbr = random.choice(maturity_units)
    participation_val = random.choice(participations)
    participation_unit_full, participation_unit_abbr = random.choice(
        participation_units)
    barrier_val = random.choice(barriers)
    barrier_unit_full, barrier_unit_abbr = random.choice(barrier_units)
    coupon_full, coupon_abbr = random.choice(coupons)
    coupon_unit_full, coupon_unit_abbr = random.choice(coupon_units)
    coupon_type = random.choice(coupon_types)
    colloquial_request = random.choice(colloquial_requests)
    colloquial_closing = random.choice(colloquial_closings)
    first_name = random.choice(first_names)
    family_name = random.choice(family_names)
    nickname = random.choice(nicknames)

    params = {
        "underlying": underlying,
        "maturity": f"{maturity_val} {random.choice([maturity_unit_full, maturity_unit_abbr])}",
        "participation": f"{participation_val} {random.choice([participation_unit_full, participation_unit_abbr])}",
        "barrier": f"{barrier_val} {random.choice([barrier_unit_full, barrier_unit_abbr])}",
        "coupon": f"{random.choice([coupon_full, coupon_abbr])} {random.choice([coupon_unit_full, coupon_unit_abbr])}",
        "coupon_type": coupon_type,
    }

    param_keys = list(params.keys())
    random.shuffle(param_keys)

    param_strings = []
    for key in param_keys:
        value = params[key]
        typo_chance = random.random()
        if typo_chance < 0.15:  # 15% typo chance
            value_list = list(value)
            if len(value_list) > 2:
                swap_index = random.randint(0, len(value_list) - 2)
                value_list[swap_index], value_list[swap_index +
                                                   1] = value_list[swap_index + 1], value_list[swap_index]
                value = "".join(value_list)
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
        "coupon": f"{coupon_full} {coupon_unit_full}",
        "coupon_type": coupon_type,
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

    maturities = ["1", "2", "3", "4", "5"]
    maturity_units = [("years", "yrs")]
    barriers = ["50", "60", "70"]
    barrier_units = [("percent", "%"), ("percent", "pct")]
    coupons = [("quarterly", "qtr"), ("semi-annually", "semi"),
               ("annually", "annual")]
    coupon_units = [("", ""), ("coupons", "cpns")]
    coupon_rates = ["8", "10", "12", "15"]
    coupon_rate_units = [("percent", "%"), ("pct", "%")]
    autocall_frequencies = [("quarterly", "qtr"),
                            ("semi-annually", "semi"), ("annually", "annual")]
    autocall_frequency_units = [("", "checks")]
    autocall_barriers = ["100", "102", "105"]
    autocall_barrier_units = [("percent", "%"), ("percent", "pct")]

    colloquial_requests = [
        "Hey, can u price ths autocall RFQ?",
        "Quik quote on an autocall note, plez.",
        "Need a price on dis autocall RFQ, thx.",
        "Lookin for a qoute on this autocall.",
        "Yo, can u get a price 4 me on this autocall?",
        "Any chance of gettin a qoute on this autocall note?",
        "Could u price this autocall up?",
        "Jst need a quick price on this autocall RFQ.",
        "Pls get a price for this autocall.",
        "Hey, price dis autocall note up.",
        "Any ideas on a price 4 dis autocall RFQ?",
        "Quick autocall price chek?",
        "Can u price dis autocall? Tx.",
        "Lookin for a fast qoute on this autocall.",
        "Yo, price dis autocall 1 up.",
        "Any qoutes floatin on this autocall note RFQ?",
        "Price this autocall, if u can.",
        "Quick autocall RFQ, plez?",
        "Get a price on dis autocall note, thx.",
        "Hey, any price ideaz on this autocall RFQ?",
        "Could you provide a quote for this autocall note?",
        "I require a price for the following autocall.",
        "Please price this autocall.",
        "We are seeking a quote on this autocall security.",
        "Kindly provide a price for this autocall RFQ.",
        "I would like to obtain a quote for this autocall.",
        "Please get back to me with a price for this autocall note.",
        "We need a price on this autocall.",
        "Could you please price this autocall instrument?",
        "Please provide a quotation for this autocall.",
    ]

    first_names = ["Alex", "Ben", "Charlie", "David",
                   "Eva", "Frank", "Grace", "Henry", "Ivy", "Jack"]
    family_names = ["Smith", "Jones", "Williams", "Brown",
                    "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson"]
    nicknames = ["Al", "Benny", "Chuck", "Dave", "Eve",
                 "Frankie", "Gracie", "Hank", "Ive", "Jackie"]

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

    colloquial_request = random.choice(colloquial_requests)
    colloquial_closing = random.choice(colloquial_closings)
    first_name = random.choice(first_names)
    family_name = random.choice(family_names)
    nickname = random.choice(nicknames)

    params = {
        "underlying": underlying,
        "maturity": f"{maturity_val} {random.choice([maturity_unit_full, maturity_unit_abbr])}",
        "barrier": f"{barrier_val} {random.choice([barrier_unit_full, barrier_unit_abbr])}",
        "coupon": f"{random.choice([coupon_full, coupon_abbr])} {random.choice([coupon_unit_full, coupon_unit_abbr])}",
        "coupon_rate": f"{coupon_rate_val} {random.choice([coupon_rate_unit_full, coupon_rate_unit_abbr])}",
        "autocall_frequency": f"{random.choice([autocall_frequency_full, autocall_frequency_abbr])} {random.choice([autocall_frequency_unit_full, autocall_frequency_unit_abbr])}",
        "autocall_barrier": f"{autocall_barrier_val} {random.choice([autocall_barrier_unit_full, autocall_barrier_unit_abbr])}",
    }

    param_keys = list(params.keys())
    random.shuffle(param_keys)

    param_strings = []
    for key in param_keys:
        value = params[key]
        typo_chance = random.random()
        if typo_chance < 0.15:  # 15% typo chance
            value_list = list(value)
            if len(value_list) > 2:
                swap_index = random.randint(0, len(value_list) - 2)
                value_list[swap_index], value_list[swap_index +
                                                   1] = value_list[swap_index + 1], value_list[swap_index]
                value = "".join(value_list)
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


def generate_random_rfq():
    if random.random() > 0.5:
        doc = generate_eln_rfq()
    else:
        doc = generate_autocall_rfq()
    return doc


if __name__ == "__main__":
    for _ in range(10):
        print(json.dumps(generate_random_rfq(), indent=3))

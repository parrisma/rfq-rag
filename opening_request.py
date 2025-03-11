import random


def generate_colloquial_request(product_name: str, language_code: str) -> str:
    """
    Generates a colloquial request phrase for a product in the given language.

    Args:
        product_name (str): The name of the product.
        language_code (str): The language code ("en", "fr", "es").

    Returns:
        str: A colloquial request phrase in the specified language.
    """

    colloquial_requests_en = [
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

    colloquial_requests_fr = [
        "Salut, pouvez-vous tarifer cette {product_name} RFQ?",
        "Devis rapide pour une note {product_name}, s'il vous plaît.",
        "Besoin d'un prix pour cette {product_name} RFQ, merci.",
        "Je cherche un devis pour cette {product_name}.",
        "Yo, pouvez-vous me donner un prix pour cette {product_name} ?",
        "Une chance d'obtenir un devis pour cette note {product_name} ?",
        "Pourriez-vous tarifer cette {product_name} ?",
        "J'ai juste besoin d'un prix rapide pour cette {product_name} RFQ.",
        "Veuillez me donner un prix pour cette {product_name}.",
        "Salut, tarifez cette note {product_name}.",
        "Des idées de prix pour cette {product_name} RFQ ?",
        "Vérification rapide du prix de {product_name} ?",
        "Pouvez-vous tarifer cette {product_name} ? Merci.",
        "Je cherche un devis rapide pour cette {product_name}.",
        "Yo, tarifez cette {product_name}.",
        "Des devis qui flottent pour cette note {product_name} RFQ ?",
        "Tarifez cette {product_name}, si vous pouvez.",
        "RFQ rapide pour {product_name}, s'il vous plaît ?",
        "Obtenez un prix pour cette note {product_name}, merci.",
        "Salut, des idées de prix pour cette {product_name} RFQ ?",
        "Pourriez-vous fournir un devis pour cette note {product_name} ?",
        "J'ai besoin d'un prix pour la {product_name} suivante.",
        "Veuillez tarifer cette {product_name}.",
        "Nous cherchons un devis pour ce titre {product_name}.",
        "Veuillez fournir un prix pour cette {product_name} RFQ.",
        "J'aimerais obtenir un devis pour cette {product_name}.",
        "Veuillez me donner un prix pour cette note {product_name}.",
        "Nous avons besoin d'un prix pour cette {product_name}.",
        "Pourriez-vous tarifer cet instrument {product_name} ?",
        "Veuillez fournir un devis pour cette {product_name}.",
    ]

    colloquial_requests_es = [
        "Oye, ¿puedes cotizar esta {product_name} RFQ?",
        "Cotización rápida para una nota {product_name}, por favor.",
        "Necesito un precio para esta {product_name} RFQ, gracias.",
        "Estoy buscando una cotización para esta {product_name}.",
        "Oye, ¿puedes conseguirme un precio para esta {product_name}?",
        "¿Alguna posibilidad de conseguir una cotización para esta nota {product_name}?",
        "¿Podrías cotizar esta {product_name}?",
        "Solo necesito un precio rápido para esta {product_name} RFQ.",
        "Por favor, consigue un precio para esta {product_name}.",
        "Oye, cotiza esta nota {product_name}.",
        "¿Alguna idea de precio para esta {product_name} RFQ?",
        "¿Revisión rápida del precio de {product_name}?",
        "¿Puedes cotizar esta {product_name}? Gracias.",
        "Estoy buscando una cotización rápida para esta {product_name}.",
        "Oye, cotiza esta {product_name}.",
        "¿Alguna cotización flotando para esta nota {product_name} RFQ?",
        "Cotiza esta {product_name}, si puedes.",
        "RFQ rápida para {product_name}, por favor?",
        "Consigue un precio para esta nota {product_name}, gracias.",
        "Oye, ¿alguna idea de precio para esta {product_name} RFQ?",
        "¿Podría proporcionar una cotización para esta nota {product_name}?",
        "Necesito un precio para la siguiente {product_name}.",
        "Por favor, cotiza esta {product_name}.",
        "Estamos buscando una cotización para este valor {product_name}.",
        "Por favor, proporcione un precio para esta {product_name} RFQ.",
        "Me gustaría obtener una cotización para esta {product_name}.",
        "Por favor, devuélveme un precio para esta nota {product_name}.",
        "Necesitamos un precio para esta {product_name}.",
        "¿Podría cotizar este instrumento {product_name}?",
        "Por favor, proporcione una cotización para esta {product_name}.",
    ]

    if language_code == "en":
        requests = colloquial_requests_en
    elif language_code == "fr":
        requests = colloquial_requests_fr
    elif language_code == "es":
        requests = colloquial_requests_es
    else:
        return "Language not supported."

    return random.choice(requests).format(product_name=product_name)


if __name__ == "__main__":
    prod = random.choice(["eln", "autocall"])
    print(generate_colloquial_request(product_name=prod, language_code="en"))
    print(generate_colloquial_request(product_name=prod, language_code="fr"))
    print(generate_colloquial_request(product_name=prod, language_code="es"))
    try:
        print(generate_colloquial_request(product_name=prod, language_code="de"))
    except ValueError as e:
        print("Error raised as expected")

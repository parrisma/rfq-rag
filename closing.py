import random


def get_colloquial_closing(language_code):
    """
    Returns a colloquial closing phrase based on the given language code.

    Args:
        language_code (str): The language code ("en", "fr", "es").

    Returns:
        str: A colloquial closing phrase in the specified language.
    """

    colloquial_closings_en = [
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

    colloquial_closings_fr = [
        "Merci, j'apprécie.",
        "Merci, tenez-moi au courant.",
        "Merci d'avance.",
        "Tenez-moi au courant quand vous avez un prix.",
        "J'apprécie votre aide.",
        "Merci, j'attends votre réponse avec impatience.",
        "Merci, veuillez me conseiller.",
        "Faites-moi part de vos réflexions.",
        "Merci, meilleures salutations.",
        "Merci, veuillez répondre quand vous pouvez.",
        "Merci, répondez dès que possible.",
        "Merci, toute information est bonne.",
        "Tenez-moi au courant quand vous l'avez.",
        "J'apprécie votre réponse rapide.",
        "Merci, tenez-moi au courant bientôt.",
        "Merci, j'attends votre réponse avec impatience.",
        "Veuillez me conseiller quand vous avez un prix.",
        "Faites-moi part de vos réflexions sur les prix.",
        "Merci, meilleurs vœux.",
        "Veuillez répondre avec toute information.",
        "Merci, j'apprécie votre assistance.",
        "Veuillez me faire savoir quand vous avez le prix.",
        "Merci d'avance pour votre réponse rapide.",
        "Veuillez me conseiller quand vous avez les prix disponibles.",
        "J'attends de vos nouvelles bientôt.",
        "Veuillez répondre à votre meilleure convenance.",
        "Merci pour votre temps et votre considération.",
        "Veuillez me conseiller quand vous avez une mise à jour.",
        "J'apprécie votre réponse rapide.",
        "Veuillez répondre quand vous le pouvez.",
    ]

    colloquial_closings_es = [
        "Gracias, lo aprecio.",
        "Saludos, avísame.",
        "Gracias de antemano.",
        "Avísame cuando tengas un precio.",
        "Agradezco la ayuda.",
        "Gracias, espero tu respuesta.",
        "Gracias, por favor avisa.",
        "Avísame tus pensamientos.",
        "Gracias, saludos cordiales.",
        "Gracias, por favor responde cuando puedas.",
        "Saludos, responde lo antes posible.",
        "Gracias, cualquier información es buena.",
        "Avísame cuando lo tengas.",
        "Agradezco la rápida respuesta.",
        "Gracias, avísame pronto.",
        "Gracias, espero tu respuesta.",
        "Por favor avisa cuando tengas un precio.",
        "Avísame tus pensamientos sobre el precio.",
        "Gracias, mejores deseos.",
        "Por favor responde con cualquier información.",
        "Gracias, aprecio tu asistencia.",
        "Por favor, házmelo saber cuando tengas el precio.",
        "Gracias de antemano por tu pronta respuesta.",
        "Por favor avisa cuando tengas precios disponibles.",
        "Espero tener noticias tuyas pronto.",
        "Por favor responde a tu mayor conveniencia.",
        "Gracias por tu tiempo y consideración.",
        "Por favor avisa cuando tengas una actualización.",
        "Agradezco tu pronta respuesta.",
        "Por favor responde cuando puedas.",
    ]

    if language_code == "en":
        return random.choice(colloquial_closings_en)
    elif language_code == "fr":
        return random.choice(colloquial_closings_fr)
    elif language_code == "es":
        return random.choice(colloquial_closings_es)
    else:
        raise (ValueError(f"Language [{language_code}] not supported."))


if __name__ == "__main__":
    print(get_colloquial_closing("en"))
    print(get_colloquial_closing("fr"))
    print(get_colloquial_closing("es"))
    try:
        print(get_colloquial_closing("de"))
    except ValueError as e:
        print("Error raised as expected")

import re
from datetime import datetime


def isfloat(num):
    """validate the value is float or

    Args:
        num (Any): number

    Returns:
        bool: is float or not
    """
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_valid_search_criteria(search_criteria, search_by_department=False):
    """function that accept dict object to validated every value of this object

    Args:
        search_criteria (dict): object contain as keys radius_km, start_date, end_date, longitude, latitude, address

    Returns:
        bool: valide or not valide
    """
    try:
        accented_characters = (
            "àèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÿÄËÏÖÜŸçÇßØøÅåÆæœ"
        )
        allowed_raduis = [20, 40, 60]
        if search_by_department:
            allowed_raduis.append(100)

        valide = (
            int(search_criteria["radius_km"]) in allowed_raduis
            and bool(datetime.strptime(search_criteria["start_date"], "%Y-%m-%d"))
            and bool(datetime.strptime(search_criteria["end_date"], "%Y-%m-%d"))
            and isfloat(float(search_criteria["longitude"]))
            and isfloat(float(search_criteria["latitude"]))
            and bool(
                re.match(
                    r"^[A-zÀ-ú{%s,}0-9',-.\s]{1,70}[0-9]{5}$" % accented_characters,
                    search_criteria["address"],
                )
            )
        )
    except ValueError:
        valide = False
    return valide


def capitalize_custom(name: str) -> str:
    """Capitalize the first letter of every word with some exceptions

    Args:
        name : str

    Returns:
        name : str
    """
    result = name.title()
    lower_words = ["Sur", "La", "Le", "Les", "Lès", "De", "Des", "En", "Et", "Aux"]
    for lower_word in lower_words:
        result = (
            result.replace("-" + lower_word + "-", "-" + lower_word.lower() + "-")
            .replace(" " + lower_word + "-", " " + lower_word.lower() + "-")
            .replace(" " + lower_word + " ", " " + lower_word.lower() + " ")
        )

    result = (
        result.replace(" L'", " l'")
        .replace(" D'", " d'")
        .replace("-L'", "-l'")
        .replace("-D'", "-d'")
    )

    return result

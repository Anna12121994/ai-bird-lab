bird_info = {
    "Bald Eagle": {
        "description": "Large bird of prey found mainly in North America.",
        "extra_info": "Family: Accipitridae. Diet: fish and small animals."
    },

    "Golden Eagle": {
        "description": "Large eagle with broad wings and powerful flight.",
        "extra_info": "Family: Accipitridae. Diet: small and medium-sized animals."
    },

    "House Sparrow": {
        "description": "Small bird commonly found near human settlements.",
        "extra_info": "Family: Passeridae. Diet: seeds, grains and insects."
    }
}


def get_bird_info(species):
    if species in bird_info:
        return bird_info[species]

    return {
        "description": "Інформація про цей вид відсутня.",
        "extra_info": "Додаткові відомості відсутні."
    }
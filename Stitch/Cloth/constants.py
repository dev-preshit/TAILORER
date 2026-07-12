GARMENT_TYPES = {
    # ---------- UPPER BODY ----------
    'Shirt': {
        'fields': ['length', 'shoulder', 'chest', 'waist', 'sleeves', 'biceps', 'collar', 'clothType', 'pocket', 'button', 'sleeveType'],
        'gender': 'unisex',
        'region': 'upper',
    },
    'Kurta': {
        'fields': ['length', 'shoulder', 'chest', 'waist', 'sleeveType', 'biceps', 'collar', 'clothType', 'button'],
        'gender': 'male',
        'region': 'upper',
    },
    'Kurti': {
        'fields': ['length', 'shoulder', 'bustLength', 'upperChest', 'waist', 'hips', 'sleeves', 'biceps', 'collar', 'apexGap', 'clothType', 'pocket', 'button', 'sleeveType'],
        'gender': 'female',
        'region': 'upper',
    },
    'Shrewani': {
        'fields': ['shoulder', 'chest', 'waist', 'sleeves', 'length', 'collar'],
        'gender': 'male',
        'region': 'upper',
    },
    'Coat': {
        'fields': ['shoulder', 'chest', 'waist', 'sleeves', 'length'],
        'gender': 'unisex',
        'region': 'upper',
    },
    'Jacket': {
        'fields': ['shoulder', 'chest', 'waist', 'sleeves', 'length'],
        'gender': 'unisex',
        'region': 'upper',
    },
    'Blouse': {
        'fields': ['shoulder', 'chest', 'waist', 'sleeves', 'length'],
        'gender': 'female',
        'region': 'upper',
    },
    'Gown': {
        'fields': ['shoulder', 'chest', 'waist', 'hips', 'length', 'sleeves'],
        'gender': 'female',
        'region': 'upper',
    },
    'Frock': {
        'fields': ['shoulder', 'chest', 'waist', 'hips', 'length', 'sleeves'],
        'gender': 'female',
        'region': 'upper',
    },

    # ---------- LOWER BODY ----------
    'Trouser': {
        'fields': ['hips', 'thigh', 'pantBottom', 'length'],
        'gender': 'unisex',
        'region': 'lower',
    },
    'Barmuda': {
        'fields': ['hips', 'thigh', 'length'],
        'gender': 'unisex',
        'region': 'lower',
    },
    'Paijama': {
        'fields': ['hips', 'thigh', 'length', 'pantBottom'],
        'gender': 'male',
        'region': 'lower',
    },
    'Skirt': {
        'fields': ['hips', 'length'],
        'gender': 'female',
        'region': 'lower',
    },
    'Leggings': {
        'fields': ['hips', 'thigh', 'length'],
        'gender': 'female',
        'region': 'lower',
    },
}
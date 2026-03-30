"""
Thirukanidham Porutham Engine
10-Point Tamil Marriage Compatibility Calculator
"""

# ─── Nakshatra Data ──────────────────────────────────────────────────────────

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra",
    "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula",
    "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Gana classification: Deva (0), Manushya (1), Rakshasa (2)
NAKSHATRA_GANA = [
    0, 1, 2, 0, 0, 1, 0, 0, 2,  # Ashwini to Ashlesha
    2, 1, 0, 0, 2, 0, 2, 0, 2,  # Magha to Jyeshtha
    2, 1, 0, 0, 2, 2, 1, 0, 0   # Mula to Revati
]

# Yoni classification (animal pairs)
# 0:Horse, 1:Elephant, 2:Sheep, 3:Serpent, 4:Dog, 5:Cat, 6:Rat,
# 7:Cow, 8:Buffalo, 9:Tiger, 10:Deer, 11:Monkey, 12:Mongoose, 13:Lion
NAKSHATRA_YONI = [
    0, 1, 2, 3, 3, 4, 5, 2, 5,
    6, 6, 7, 8, 9, 8, 9, 10, 10,
    4, 11, 12, 11, 13, 0, 13, 7, 1
]

# Yoni compatibility matrix (enemies = False)
YONI_ENEMIES = {
    (0, 8), (8, 0),   # Horse - Buffalo
    (1, 13), (13, 1),  # Elephant - Lion
    (3, 12), (12, 3),  # Serpent - Mongoose
    (4, 10), (10, 4),  # Dog - Deer
    (5, 6), (6, 5),    # Cat - Rat
    (7, 9), (9, 7),    # Cow - Tiger
}

# Nakshatra to Rasi (moon sign) mapping (0-11)
NAKSHATRA_RASI = [
    0, 0, 0,   # Ashwini(0), Bharani(1), Krittika-1(2) → Aries
    1, 1, 1,   # Krittika-2(3), Rohini(4), Mrigashira-1(5) → Taurus -- adjusted below
    2, 2, 2,   # Mrigashira-2, Ardra, Punarvasu-1 → Gemini
    3, 3, 3,   # Punarvasu-2, Pushya, Ashlesha → Cancer
    4, 4, 4,   # Magha, Purva Phalguni, Uttara Phalguni-1 → Leo
    5, 5, 5,   # Uttara Phalguni-2, Hasta, Chitra-1 → Virgo
    6, 6, 6,   # Chitra-2, Swati, Vishakha-1 → Libra
    7, 7, 7,   # Vishakha-2, Anuradha, Jyeshtha → Scorpio
    8, 8, 8,   # Mula, Purva Ashadha, Uttara Ashadha-1 → Sagittarius
    9, 9, 9,   # Uttara Ashadha-2, Shravana, Dhanishtha-1 → Capricorn
    10, 10, 10, # Dhanishtha-2, Shatabhisha, Purva Bhadrapada-1 → Aquarius
    11, 11, 11  # Purva Bhadrapada-2, Uttara Bhadrapada, Revati → Pisces
]

# Simplified: map each nakshatra (0-26) to its primary rasi
def nakshatra_to_rasi(nak_index):
    """Map nakshatra index to rasi index based on nakshatra pada positions."""
    # Each rasi spans 2.25 nakshatras (27 nakshatras / 12 rasis)
    rasi_map = [
        0, 0, 1, 1, 1, 2, 2, 3, 3,   # Nak 0-8
        4, 4, 5, 5, 5, 6, 6, 7, 7,   # Nak 9-17
        8, 8, 9, 9, 9, 10, 10, 11, 11  # Nak 18-26
    ]
    return rasi_map[nak_index % 27]


# Rajju groups
# 0: Pada (Feet), 1: Ooru (Thigh), 2: Nabhi (Navel),
# 3: Kanta (Neck), 4: Siro (Head)
NAKSHATRA_RAJJU = [
    0, 1, 2, 3, 4, 4, 3, 2, 1,
    0, 1, 2, 3, 4, 4, 3, 2, 1,
    0, 1, 2, 3, 4, 4, 3, 2, 1
]

# Vedha (obstruction) pairs - nakshatras that are vedha to each other
VEDHA_PAIRS = [
    (0, 17), (1, 16), (2, 15), (3, 14), (4, 13),
    (5, 22), (6, 21), (7, 20), (8, 19),
    (9, 26), (10, 25), (11, 24), (12, 23)
]

# Rasi lord mapping
RASI_LORDS = [
    4, 5, 3, 0, 1, 3, 5, 4, 6, 7, 7, 6
    # Mars, Venus, Mercury, Moon, Sun, Mercury, Venus, Mars, Jupiter, Saturn, Saturn, Jupiter
]

# Planet friendship matrix for Rasi Adhipathi
# 0:Moon, 1:Sun, 2:Mercury, 3:Venus, 4:Mars, 5:Jupiter, 6:Saturn, 7:Rahu
PLANET_FRIENDS = {
    0: {1, 3},        # Moon: friends with Sun, Mercury
    1: {0, 4, 5},     # Sun: friends with Moon, Mars, Jupiter
    2: {1, 5},        # Mercury: friends with Sun, Venus -- simplified
    3: {2, 7},        # Venus: friends with Mercury, Saturn
    4: {1, 0, 5},     # Mars: friends with Sun, Moon, Jupiter
    5: {1, 0, 4},     # Jupiter: friends with Sun, Moon, Mars
    6: {2, 3},        # Saturn: friends with Mercury, Venus
    7: {6, 3},        # Rahu: friends with Saturn, Venus
}

# Vasya classification for each rasi
# Each rasi has specific rasis that are vasya to it
VASYA_MAP = {
    0: [4, 7],      # Aries → Leo, Scorpio
    1: [3, 6],      # Taurus → Cancer, Libra
    2: [5],         # Gemini → Virgo
    3: [7, 8],      # Cancer → Scorpio, Sagittarius
    4: [6],         # Leo → Libra
    5: [2, 11],     # Virgo → Gemini, Pisces
    6: [5, 0],      # Libra → Virgo, Capricorn (adjusted)
    7: [3],         # Scorpio → Cancer
    8: [11],        # Sagittarius → Pisces
    9: [0, 10],     # Capricorn → Aries, Aquarius
    10: [0],        # Aquarius → Aries
    11: [9],        # Pisces → Capricorn
}

# Nadi classification (0: Vata, 1: Pitta, 2: Kapha)
NAKSHATRA_NADI = [
    2, 1, 0, 2, 1, 0, 2, 1, 0,
    0, 1, 2, 0, 1, 2, 0, 1, 2,
    2, 1, 0, 2, 1, 0, 2, 1, 0
]


# ─── Porutham Checks ────────────────────────────────────────────────────────

def check_dina(bride_nak, groom_nak):
    """Dina Porutham: Health & longevity compatibility."""
    count = ((groom_nak - bride_nak) % 27) + 1
    remainder = count % 9
    return remainder not in [2, 4, 6, 8, 0]


def check_gana(bride_nak, groom_nak):
    """Gana Porutham: Temperament compatibility."""
    bride_gana = NAKSHATRA_GANA[bride_nak]
    groom_gana = NAKSHATRA_GANA[groom_nak]

    if bride_gana == groom_gana:
        return True
    if bride_gana == 0 and groom_gana == 1:  # Deva-Manushya
        return True
    if bride_gana == 1 and groom_gana == 0:
        return True
    return False


def check_mahendra(bride_nak, groom_nak):
    """Mahendra Porutham: Prosperity & offspring."""
    count = ((groom_nak - bride_nak) % 27) + 1
    return count in [4, 7, 10, 13, 16, 19, 22, 25]


def check_sthree_dheerga(bride_nak, groom_nak):
    """Sthree Dheerga: Wealth & well-being of bride."""
    count = ((groom_nak - bride_nak) % 27) + 1
    return count >= 13


def check_yoni(bride_nak, groom_nak):
    """Yoni Porutham: Physical compatibility."""
    bride_yoni = NAKSHATRA_YONI[bride_nak]
    groom_yoni = NAKSHATRA_YONI[groom_nak]

    if bride_yoni == groom_yoni:
        return True
    if (bride_yoni, groom_yoni) in YONI_ENEMIES or (groom_yoni, bride_yoni) in YONI_ENEMIES:
        return False
    return True


def check_rasi(bride_rasi, groom_rasi):
    """Rasi Porutham: Moon sign compatibility."""
    diff = (groom_rasi - bride_rasi) % 12
    # Favorable positions
    favorable = [1, 2, 3, 4, 5, 7, 9, 10, 11]
    return diff in favorable or diff == 0


def check_rasi_adhipathi(bride_rasi, groom_rasi):
    """Rasi Adhipathi: Rasi lord friendship."""
    bride_lord = RASI_LORDS[bride_rasi]
    groom_lord = RASI_LORDS[groom_rasi]

    if bride_lord == groom_lord:
        return True
    return groom_lord in PLANET_FRIENDS.get(bride_lord, set()) or \
           bride_lord in PLANET_FRIENDS.get(groom_lord, set())


def check_vasya(bride_rasi, groom_rasi):
    """Vasya Porutham: Mutual attraction & control."""
    if bride_rasi == groom_rasi:
        return True
    return groom_rasi in VASYA_MAP.get(bride_rasi, []) or \
           bride_rasi in VASYA_MAP.get(groom_rasi, [])


def check_rajju(bride_nak, groom_nak):
    """Rajju Porutham: Longevity of marriage bond."""
    bride_rajju = NAKSHATRA_RAJJU[bride_nak]
    groom_rajju = NAKSHATRA_RAJJU[groom_nak]
    return bride_rajju != groom_rajju


def check_vedha(bride_nak, groom_nak):
    """Vedha Porutham: Nakshatra affliction check."""
    for pair in VEDHA_PAIRS:
        if (bride_nak == pair[0] and groom_nak == pair[1]) or \
           (bride_nak == pair[1] and groom_nak == pair[0]):
            return False
    return True


def check_nadi(bride_nak, groom_nak):
    """Nadi Porutham: Health of offspring."""
    bride_nadi = NAKSHATRA_NADI[bride_nak]
    groom_nadi = NAKSHATRA_NADI[groom_nak]
    return bride_nadi != groom_nadi


# ─── Main Matching Function ─────────────────────────────────────────────────

PORUTHAM_DETAILS = {
    "Dina": "Health and longevity compatibility",
    "Gana": "Temperament compatibility",
    "Mahendra": "Prosperity and offspring",
    "Sthree Dheerga": "Wealth and well-being of bride",
    "Yoni": "Physical and sexual compatibility",
    "Rasi": "Moon sign compatibility",
    "Rasi Adhipathi": "Rasi lord friendship",
    "Vasya": "Mutual attraction and control",
    "Rajju": "Longevity of marriage bond",
    "Vedha": "Nakshatra affliction check",
    "Nadi": "Health of offspring",
}


def calculate_porutham(bride_chart, groom_chart):
    """
    Calculate 10-point Porutham between bride and groom.

    Args:
        bride_chart: Bride's chart data from calculate_chart()
        groom_chart: Groom's chart data from calculate_chart()

    Returns:
        dict with porutham results
    """
    bride_nak = bride_chart["nakshatra"]["index"]
    groom_nak = groom_chart["nakshatra"]["index"]

    # Get rasi from moon sign index
    bride_moon = next(p for p in bride_chart["planets"] if p["name"] == "Moon")
    groom_moon = next(p for p in groom_chart["planets"] if p["name"] == "Moon")
    bride_rasi = bride_moon["sign_index"]
    groom_rasi = groom_moon["sign_index"]

    results = []

    checks = [
        ("Dina", check_dina(bride_nak, groom_nak)),
        ("Gana", check_gana(bride_nak, groom_nak)),
        ("Mahendra", check_mahendra(bride_nak, groom_nak)),
        ("Sthree Dheerga", check_sthree_dheerga(bride_nak, groom_nak)),
        ("Yoni", check_yoni(bride_nak, groom_nak)),
        ("Rasi", check_rasi(bride_rasi, groom_rasi)),
        ("Rasi Adhipathi", check_rasi_adhipathi(bride_rasi, groom_rasi)),
        ("Vasya", check_vasya(bride_rasi, groom_rasi)),
        ("Rajju", check_rajju(bride_nak, groom_nak)),
        ("Vedha", check_vedha(bride_nak, groom_nak)),
        ("Nadi", check_nadi(bride_nak, groom_nak)),
    ]

    matched = 0
    for i, (name, result) in enumerate(checks):
        results.append({
            "number": i + 1,
            "name": name,
            "matched": result,
            "description": PORUTHAM_DETAILS[name],
        })
        if result:
            matched += 1

    total = len(checks)
    score = matched

    # Determine verdict
    if score >= 8:
        verdict = "Excellent Match"
        verdict_type = "excellent"
    elif score >= 6:
        verdict = "Good Match"
        verdict_type = "good"
    elif score >= 4:
        verdict = "Average Match"
        verdict_type = "average"
    else:
        verdict = "Below Average"
        verdict_type = "poor"

    return {
        "bride": {
            "name": bride_chart["name"],
            "nakshatra": bride_chart["nakshatra"]["name"],
            "rasi": bride_moon["sign"],
        },
        "groom": {
            "name": groom_chart["name"],
            "nakshatra": groom_chart["nakshatra"]["name"],
            "rasi": groom_moon["sign"],
        },
        "results": results,
        "score": score,
        "total": total,
        "verdict": verdict,
        "verdict_type": verdict_type,
    }

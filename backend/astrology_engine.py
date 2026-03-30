"""
Thirukanidham Astrology Engine
Pure Python Vedic astrology calculations with Lahiri Ayanamsa.
Uses astronomical algorithms instead of Swiss Ephemeris C library.
"""

import math
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# ─── Constants ───────────────────────────────────────────────────────────────

ZODIAC_SIGNS = [
    "Mesha (Aries)", "Rishabha (Taurus)", "Mithuna (Gemini)",
    "Karka (Cancer)", "Simha (Leo)", "Kanya (Virgo)",
    "Tula (Libra)", "Vrischika (Scorpio)", "Dhanus (Sagittarius)",
    "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]

ZODIAC_SHORT = [
    "Mesha", "Rishabha", "Mithuna", "Karka",
    "Simha", "Kanya", "Tula", "Vrischika",
    "Dhanus", "Makara", "Kumbha", "Meena"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra",
    "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula",
    "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

PLANET_SYMBOLS = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma",
    "Mercury": "Me", "Jupiter": "Ju", "Venus": "Ve",
    "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke"
}

NAVAMSA_START = [0, 9, 6, 3, 0, 9, 6, 3, 0, 9, 6, 3]

# ─── Geocoding ───────────────────────────────────────────────────────────────

_geolocator = Nominatim(user_agent="thirukanidham_astro")
_tf = TimezoneFinder()

CITY_FALLBACK = {
    "chennai": (13.0827, 80.2707), "madurai": (9.9252, 78.1198),
    "coimbatore": (11.0168, 76.9558), "bangalore": (12.9716, 77.5946),
    "mumbai": (19.0760, 72.8777), "delhi": (28.6139, 77.2090),
    "kolkata": (22.5726, 88.3639), "hyderabad": (17.3850, 78.4867),
    "trichy": (10.7905, 78.7047), "salem": (11.6643, 78.1460),
    "tirunelveli": (8.7139, 77.7567), "kanyakumari": (8.0883, 77.5385),
    "thanjavur": (10.7870, 79.1378), "erode": (11.3410, 77.7172),
    "tiruppur": (11.1085, 77.3411), "vellore": (12.9165, 79.1325),
    "pondicherry": (11.9416, 79.8083), "mysore": (12.2958, 76.6394),
    "pune": (18.5204, 73.8567), "ahmedabad": (23.0225, 72.5714),
    "jaipur": (26.9124, 75.7873), "lucknow": (26.8467, 80.9462),
    "kanpur": (26.4499, 80.3319), "nagpur": (21.1458, 79.0882),
    "visakhapatnam": (17.6868, 83.2185), "kochi": (9.9312, 76.2673),
    "thiruvananthapuram": (8.5241, 76.9366), "bhopal": (23.2599, 77.4126),
     # --- Tamil Nadu Districts ---
    "ariyalur": (11.1401, 79.0786),
    "chengalpattu": (12.6819, 79.9888),
    "cuddalore": (11.7447, 79.7680),
    "dharmapuri": (12.1277, 78.1579),
    "dindigul": (10.3673, 77.9803),
    "kallakurichi": (11.7380, 78.9593),
    "kanchipuram": (12.8342, 79.7036),
    "karur": (10.9601, 78.0766),
    "krishnagiri": (12.5186, 78.2137),
    "mayiladuthurai": (11.1035, 79.6550),
    "nagapattinam": (10.7667, 79.8428),
    "namakkal": (11.2194, 78.1674),
    "nilgiris": (11.4064, 76.6932),
    "perambalur": (11.2333, 78.8833),
    "pudukkottai": (10.3797, 78.8208),
    "ramanathapuram": (9.3639, 78.8397),
    "ranipet": (12.9273, 79.3333),
    "sivaganga": (9.8477, 78.4836),
    "tenkasi": (8.9597, 77.3152),
    "theni": (10.0104, 77.4768),
    "thoothukudi": (8.7642, 78.1348),
    "tiruchirappalli": (10.7905, 78.7047),
    "tirupattur": (12.4973, 78.5677),
    "tiruvallur": (13.1439, 79.9084),
    "tiruvannamalai": (12.2253, 79.0747),
    "tiruvarur": (10.7722, 79.6368),
    "viluppuram": (11.9401, 79.4861),
    "virudhunagar": (9.5680, 77.9624),

    # --- Karnataka Districts ---
    "bagalkot": (16.1867, 75.6961),
    "ballari": (15.1394, 76.9214),
    "belagavi": (15.8497, 74.4977),
    "bengaluru rural": (13.2250, 77.5750),
    "bengaluru urban": (12.9716, 77.5946),
    "bidar": (17.9133, 77.5301),
    "chamarajanagar": (11.9261, 76.9437),
    "chikkaballapur": (13.4357, 77.7315),
    "chikkamagaluru": (13.3161, 75.7720),
    "chitradurga": (14.2306, 76.3980),
    "dakshina kannada": (12.9141, 74.8560),
    "davanagere": (14.4644, 75.9218),
    "dharwad": (15.4589, 75.0078),
    "gadag": (15.4315, 75.6340),
    "hassan": (13.0033, 76.1004),
    "haveri": (14.7950, 75.3991),
    "kalaburagi": (17.3297, 76.8343),
    "kodagu": (12.3375, 75.8069),
    "kolar": (13.1367, 78.1299),
    "koppal": (15.3450, 76.1548),
    "mandya": (12.5239, 76.8953),
    "mysuru": (12.2958, 76.6394),
    "raichur": (16.2076, 77.3463),
    "ramanagara": (12.7219, 77.2810),
    "shivamogga": (13.9299, 75.5681),
    "tumakuru": (13.3409, 77.1010),
    "udupi": (13.3409, 74.7421),
    "uttara kannada": (14.7937, 74.6869),
    "vijayapura": (16.8302, 75.7100),
    "yadgir": (16.7707, 77.1376),
    # --- Kerala Districts ---
    "alappuzha": (9.4981, 76.3388),
    "ernakulam": (9.9816, 76.2999),
    "idukki": (9.8490, 76.9725),
    "kannur": (11.8745, 75.3704),
    "kasaragod": (12.4996, 74.9869),
    "kollam": (8.8932, 76.6141),
    "kottayam": (9.5916, 76.5222),
    "kozhikode": (11.2588, 75.7804),
    "malappuram": (11.0732, 76.0740),
    "palakkad": (10.7867, 76.6548),
    "pathanamthitta": (9.2648, 76.7870),
    "thiruvananthapuram": (8.5241, 76.9366),
    "thrissur": (10.5276, 76.2144),
    "wayanad": (11.6854, 76.1320),

    # --- Andhra Pradesh Districts ---
    "alluri sitarama raju": (18.3273, 82.8767),
    "anakapalli": (17.6868, 83.0185),
    "ananthapuramu": (14.6819, 77.6006),
    "annamayya": (13.8020, 79.3170),
    "bapatla": (15.9047, 80.4670),
    "chittoor": (13.2172, 79.1003),
    "east godavari": (16.9891, 81.7787),
    "eluru": (16.7107, 81.0952),
    "guntur": (16.3067, 80.4365),
    "kakinada": (16.9891, 82.2475),
    "konaseema": (16.5925, 82.0165),
    "krishna": (16.1875, 81.1389),
    "kurnool": (15.8281, 78.0373),
    "nandyal": (15.4786, 78.4831),
    "nellore": (14.4426, 79.9865),
    "ntr": (16.5062, 80.6480),
    "palnadu": (16.0000, 79.7500),
    "parvathipuram manyam": (18.7785, 83.4255),
    "prakasam": (15.5090, 80.0499),
    "sri potti sriramulu nellore": (14.4426, 79.9865),
    "sri satya sai": (14.1667, 77.8167),
    "srikakulam": (18.2969, 83.8975),
    "tirupati": (13.6288, 79.4192),
    "visakhapatnam": (17.6868, 83.2185),
    "vizianagaram": (18.1067, 83.3956),
    "west godavari": (16.7107, 81.0952),

    # --- Telangana Districts ---
    "adilabad": (19.6641, 78.5320),
    "bhadradri kothagudem": (17.5500, 80.6300),
    "hanamkonda": (18.0000, 79.5800),
    "hyderabad": (17.3850, 78.4867),
    "jagtial": (18.8000, 78.9167),
    "jangaon": (17.7200, 79.1600),
    "jayashankar bhupalpally": (18.4300, 79.9500),
    "jogulamba gadwal": (16.2300, 77.8000),
    "kamareddy": (18.3200, 78.3400),
    "karimnagar": (18.4386, 79.1288),
    "khammam": (17.2473, 80.1514),
    "komaram bheem": (19.3500, 79.5000),
    "mahabubabad": (17.6000, 80.0000),
    "mahabubnagar": (16.7333, 77.9833),
    "mancherial": (18.8700, 79.4500),
    "medak": (18.0500, 78.2600),
    "medchal malkajgiri": (17.5000, 78.5000),
    "mulugu": (18.2000, 80.2000),
    "nagarkurnool": (16.4800, 78.3200),
    "nalgonda": (17.0500, 79.2700),
    "narayanpet": (16.7500, 77.5000),
    "nirmal": (19.1000, 78.3500),
    "nizamabad": (18.6725, 78.0941),
    "peddapalli": (18.6200, 79.3800),
    "rajanna sircilla": (18.3800, 78.8300),
    "rangareddy": (17.3700, 78.4700),
    "sangareddy": (17.6200, 78.0800),
    "siddipet": (18.1000, 78.8500),
    "suryapet": (17.1400, 79.6200),
    "vikarabad": (17.3300, 77.9000),
    "wanaparthy": (16.3600, 78.0600),
    "warangal": (17.9689, 79.5941),
    "yadadri bhuvanagiri": (17.6000, 78.9000),
    # --- Maharashtra Districts ---
    "ahmednagar": (19.0948, 74.7480),
    "akola": (20.7002, 77.0082),
    "amravati": (20.9374, 77.7796),
    "aurangabad": (19.8762, 75.3433),
    "beed": (18.9891, 75.7601),
    "bhandara": (21.1777, 79.6570),
    "buldhana": (20.5293, 76.1840),
    "chandrapur": (19.9615, 79.2961),
    "dhule": (20.9042, 74.7749),
    "gadchiroli": (20.1849, 80.0060),
    "gondia": (21.4624, 80.1961),
    "hingoli": (19.7176, 77.1489),
    "jalgaon": (21.0077, 75.5626),
    "jalna": (19.8347, 75.8816),
    "kolhapur": (16.7050, 74.2433),
    "latur": (18.4088, 76.5604),
    "mumbai city": (18.9388, 72.8354),
    "mumbai suburban": (19.0760, 72.8777),
    "nagpur": (21.1458, 79.0882),
    "nanded": (19.1383, 77.3210),
    "nandurbar": (21.7469, 74.1230),
    "nashik": (19.9975, 73.7898),
    "osmanabad": (18.1861, 76.0419),
    "palghar": (19.6967, 72.7699),
    "parbhani": (19.2608, 76.7748),
    "pune": (18.5204, 73.8567),
    "raigad": (18.6414, 72.8777),
    "ratnagiri": (16.9902, 73.3120),
    "sangli": (16.8524, 74.5815),
    "satara": (17.6805, 74.0183),
    "sindhudurg": (16.3492, 73.5594),
    "solapur": (17.6599, 75.9064),
    "thane": (19.2183, 72.9781),
    "wardha": (20.7453, 78.6022),
    "washim": (20.1113, 77.1330),
    "yavatmal": (20.3888, 78.1204),

    # --- Gujarat Districts ---
    "ahmedabad": (23.0225, 72.5714),
    "amreli": (21.6032, 71.2221),
    "anand": (22.5645, 72.9289),
    "aravalli": (23.3667, 73.3000),
    "banaskantha": (24.1725, 72.4380),
    "bharuch": (21.7051, 72.9959),
    "bhavnagar": (21.7645, 72.1519),
    "botad": (22.1696, 71.6667),
    "chhota udaipur": (22.3000, 74.0000),
    "dahod": (22.8359, 74.2557),
    "dang": (20.7577, 73.6860),
    "devbhoomi dwarka": (22.2394, 68.9678),
    "gandhinagar": (23.2156, 72.6369),
    "gir somnath": (20.9120, 70.3670),
    "jamnagar": (22.4707, 70.0577),
    "junagadh": (21.5222, 70.4579),
    "kachchh": (23.7337, 69.8597),
    "kheda": (22.7507, 72.6847),
    "mahisaagar": (23.0000, 73.5000),
    "mehsana": (23.5880, 72.3693),
    "morbi": (22.8173, 70.8377),
    "narmada": (21.8700, 73.5000),
    "navsari": (20.9467, 72.9520),
    "panchmahal": (22.7500, 73.6000),
    "patan": (23.8493, 72.1266),
    "porbandar": (21.6417, 69.6293),
    "rajkot": (22.3039, 70.8022),
    "sabarkantha": (23.5994, 72.9667),
    "surat": (21.1702, 72.8311),
    "surendranagar": (22.7271, 71.6486),
    "tapi": (21.1250, 73.4000),
    "vadodara": (22.3072, 73.1812),
    "valsad": (20.5992, 72.9342),

    # --- Rajasthan Districts ---
    "ajmer": (26.4499, 74.6399),
    "alwar": (27.5530, 76.6346),
    "banswara": (23.5461, 74.4340),
    "baran": (25.1000, 76.5167),
    "barmer": (25.7500, 71.3833),
    "bharatpur": (27.2152, 77.4928),
    "bhilwara": (25.3478, 74.6408),
    "bikaner": (28.0229, 73.3119),
    "bundi": (25.4381, 75.6373),
    "chittorgarh": (24.8887, 74.6269),
    "churu": (28.3042, 74.9672),
    "dausa": (26.8932, 76.3375),
    "dholpur": (26.7025, 77.8934),
    "dungarpur": (23.8431, 73.7147),
    "hanumangarh": (29.5815, 74.3294),
    "jaipur": (26.9124, 75.7873),
    "jaisalmer": (26.9157, 70.9083),
    "jalore": (25.3450, 72.6150),
    "jhalawar": (24.5967, 76.1610),
    "jhunjhunu": (28.1289, 75.3972),
    "jodhpur": (26.2389, 73.0243),
    "karauli": (26.4981, 77.0270),
    "kota": (25.2138, 75.8648),
    "nagaur": (27.2020, 73.7333),
    "pali": (25.7725, 73.3234),
    "pratapgarh": (24.0314, 74.7819),
    "rajsamand": (25.0670, 73.8790),
    "sawai madhopur": (26.0173, 76.3520),
    "sikar": (27.6094, 75.1399),
    "sirohi": (24.8887, 72.8570),
    "sri ganganagar": (29.9094, 73.8800),
    "tonk": (26.1664, 75.7885),
    "udaipur": (24.5854, 73.7125),
    # --- Uttar Pradesh Districts ---
    "agra": (27.1767, 78.0081),
    "aligarh": (27.8974, 78.0880),
    "allahabad": (25.4358, 81.8463),
    "ambedkar nagar": (26.4290, 82.5390),
    "amethi": (26.1542, 81.8142),
    "amroha": (28.9036, 78.4697),
    "auraiya": (26.4640, 79.5090),
    "azamgarh": (26.0739, 83.1859),
    "baghpat": (28.9441, 77.2186),
    "bahraich": (27.5743, 81.5946),
    "ballia": (25.7584, 84.1487),
    "balrampur": (27.4295, 82.1850),
    "banda": (25.4753, 80.3392),
    "barabanki": (26.9260, 81.1834),
    "bareilly": (28.3670, 79.4304),
    "basti": (26.8005, 82.7315),
    "bhadohi": (25.3960, 82.5665),
    "bijnor": (29.3732, 78.1367),
    "budaun": (28.0362, 79.1267),
    "bulandshahr": (28.4060, 77.8498),
    "chandauli": (25.2582, 83.2680),
    "chitrakoot": (25.2000, 80.8500),
    "deoria": (26.5020, 83.7791),
    "etah": (27.5588, 78.6626),
    "etawah": (26.7774, 79.0213),
    "faizabad": (26.7755, 82.1502),
    "farrukhabad": (27.3905, 79.5790),
    "fatehpur": (25.9270, 80.8120),
    "firozabad": (27.1591, 78.3957),
    "gautam buddha nagar": (28.5355, 77.3910),
    "ghaziabad": (28.6692, 77.4538),
    "ghazipur": (25.5840, 83.5770),
    "gonda": (27.1333, 81.9333),
    "gorakhpur": (26.7606, 83.3732),
    "hamirpur": (25.9500, 80.1500),
    "hapur": (28.7306, 77.7750),
    "hardoi": (27.3963, 80.1311),
    "hathras": (27.6000, 78.0500),
    "jalaun": (26.1451, 79.3367),
    "jaunpur": (25.7464, 82.6837),
    "jhansi": (25.4484, 78.5685),
    "kannauj": (27.0514, 79.9137),
    "kanpur dehat": (26.4499, 80.3319),
    "kanpur nagar": (26.4499, 80.3319),
    "kasganj": (27.8000, 78.6500),
    "kaushambi": (25.5300, 81.3800),
    "kheri": (27.9000, 80.8000),
    "kushinagar": (26.7400, 83.8900),
    "lalitpur": (24.6900, 78.4100),
    "lucknow": (26.8467, 80.9462),
    "maharajganj": (27.1500, 83.5700),
    "mahoba": (25.3000, 79.8700),
    "mainpuri": (27.2290, 79.0250),
    "mathura": (27.4924, 77.6737),
    "mau": (25.9417, 83.5624),
    "meerut": (28.9845, 77.7064),
    "mirzapur": (25.1460, 82.5690),
    "moradabad": (28.8386, 78.7733),
    "muzaffarnagar": (29.4727, 77.7085),
    "pilibhit": (28.6200, 79.8000),
    "pratapgarh": (25.9000, 81.9900),
    "raebareli": (26.2230, 81.2409),
    "rampur": (28.8150, 79.0250),
    "saharanpur": (29.9680, 77.5552),
    "sambhal": (28.5900, 78.5700),
    "sant kabir nagar": (26.7900, 83.0700),
    "shahjahanpur": (27.8800, 79.9100),
    "shamli": (29.4500, 77.3200),
    "shravasti": (27.5000, 81.9000),
    "siddharthnagar": (27.2800, 83.0700),
    "sitapur": (27.5700, 80.6800),
    "sonbhadra": (24.7000, 83.0700),
    "sultanpur": (26.2600, 82.0700),
    "unnao": (26.5500, 80.4900),
    "varanasi": (25.3176, 82.9739),

    # --- Bihar Districts ---
    "araria": (26.1500, 87.5200),
    "arwal": (25.2500, 84.6800),
    "aurangabad_bihar": (24.7500, 84.3700),
    "banka": (24.8800, 86.9200),
    "begusarai": (25.4200, 86.1300),
    "bhagalpur": (25.2500, 87.0000),
    "bhojpur": (25.5500, 84.6700),
    "buxar": (25.5800, 83.9800),
    "darbhanga": (26.1600, 85.9000),
    "east champaran": (26.6400, 84.9000),
    "gaya": (24.7900, 85.0000),
    "gopalganj": (26.4700, 84.4300),
    "jamui": (24.9200, 86.2200),
    "jehanabad": (25.2100, 84.9900),
    "kaimur": (25.0500, 83.6200),
    "katihar": (25.5300, 87.5800),
    "khagaria": (25.5000, 86.4800),
    "kishanganj": (26.1000, 87.9500),
    "lakhisarai": (25.1700, 86.1000),
    "madhepura": (25.9200, 86.7800),
    "madhubani": (26.3500, 86.0700),
    "munger": (25.3700, 86.4700),
    "muzaffarpur": (26.1200, 85.3800),
    "nalanda": (25.2000, 85.5200),
    "nawada": (24.8800, 85.5400),
    "patna": (25.5941, 85.1376),
    "purnia": (25.7800, 87.4700),
    "rohtas": (24.9500, 84.0200),
    "saharsa": (25.8800, 86.6000),
    "samastipur": (25.8600, 85.7800),
    "saran": (25.7800, 84.7300),
    "sheikhpura": (25.1300, 85.8500),
    "sheohar": (26.5200, 85.3000),
    "sitamarhi": (26.6000, 85.4800),
    "siwan": (26.2200, 84.3600),
    "supaul": (26.1200, 86.6000),
    "vaishali": (25.7500, 85.2200),
    "west champaran": (27.0000, 84.5000),

    # --- Madhya Pradesh Districts ---
    "agar malwa": (23.7100, 76.0100),
    "alirajpur": (22.3100, 74.3600),
    "anuppur": (23.1000, 81.7000),
    "ashoknagar": (24.5700, 77.7300),
    "balaghat": (21.8000, 80.1800),
    "barwani": (22.0300, 74.9000),
    "betul": (21.9000, 77.9000),
    "bhind": (26.5600, 78.7900),
    "bhopal": (23.2599, 77.4126),
    "burhanpur": (21.3000, 76.2300),
    "chhatarpur": (24.9100, 79.5900),
    "chhindwara": (22.0600, 78.9400),
    "damoh": (23.8300, 79.4400),
    "datia": (25.6700, 78.4600),
    "dewas": (22.9700, 76.0600),
    "dhar": (22.6000, 75.3000),
    "dindori": (22.9500, 81.0800),
    "guna": (24.6500, 77.3100),
    "gwalior": (26.2183, 78.1828),
    "harda": (22.3400, 77.1000),
    "hoshangabad": (22.7500, 77.7200),
    "indore": (22.7196, 75.8577),
    "jabalpur": (23.1800, 79.9500),
    "jhaba": (22.7700, 74.5900),
    "katni": (23.8300, 80.3900),
    "khandwa": (21.8300, 76.3500),
    "khargone": (21.8300, 75.6000),
    "mandla": (22.6000, 80.3800),
    "mandsaur": (24.0700, 75.0700),
    "morena": (26.5000, 77.9900),
    "narsinghpur": (22.9500, 79.2000),
    "neemuch": (24.4700, 74.8700),
    "panna": (24.7200, 80.1900),
    "raisen": (23.3300, 77.7800),
    "rajgarh": (23.8700, 76.7300),
    "ratlam": (23.3300, 75.0300),
    "rewa": (24.5300, 81.3000),
    "sagar": (23.8300, 78.7400),
    "satna": (24.5800, 80.8300),
    "sehore": (23.2000, 77.0800),
    "seoni": (22.0800, 79.5300),
    "shahdol": (23.3000, 81.3600),
    "shajapur": (23.4300, 76.2700),
    "sheopur": (25.6700, 76.7000),
    "shivpuri": (25.4300, 77.6500),
    "sidhi": (24.4200, 81.8800),
    "singrauli": (24.2000, 82.6700),
    "tikamgarh": (24.7400, 78.8300),
    "ujjain": (23.1793, 75.7849),
    "umaria": (23.5200, 80.8300),
    "vidisha": (23.5300, 77.8200),

    # --- Odisha Districts ---
    "angul": (20.8400, 85.1000),
    "balangir": (20.7100, 83.4900),
    "balasore": (21.4900, 86.9300),
    "bargarh": (21.3300, 83.6200),
    "bhadrak": (21.0600, 86.5000),
    "boudh": (20.8300, 84.3200),
    "cuttack": (20.4600, 85.8800),
    "deogarh": (21.5300, 84.7300),
    "dhenkanal": (20.6600, 85.6000),
    "gajapati": (18.8200, 84.1000),
    "ganjam": (19.3800, 85.0500),
    "jagatsinghpur": (20.2500, 86.1700),
    "jajpur": (20.8500, 86.3300),
    "jharsuguda": (21.8500, 84.0200),
    "kalahandi": (19.9000, 83.1700),
    "kandhamal": (20.4700, 84.2300),
    "kendrapara": (20.5000, 86.4200),
    "kendujhar": (21.6300, 85.5800),
    "khordha": (20.1800, 85.6200),
    "koraput": (18.8100, 82.7100),
    "malkangiri": (18.3600, 81.8900),
    "mayurbhanj": (21.9300, 86.7300),
    "nabarangpur": (19.2300, 82.5500),
    "nayagarh": (20.1200, 85.1000),
    "nuapada": (20.8200, 82.5300),
    "puri": (19.8100, 85.8300),
    "rayagada": (19.1700, 83.4200),
    "sambalpur": (21.4700, 83.9700),
    "subarnapur": (20.8300, 83.9000),
    "sundargarh": (22.1200, 84.0300)
    }


def get_location_data(place_name):
    """Get latitude, longitude, and timezone from a place name."""
    try:
        location = _geolocator.geocode(place_name, timeout=5)
        if location:
            lat, lon = location.latitude, location.longitude
            tz_name = _tf.timezone_at(lat=lat, lng=lon) or "Asia/Kolkata"
            return {"lat": lat, "lon": lon, "timezone": tz_name}
    except Exception:
        pass

    # Fallback for known cities
    place_lower = place_name.lower().strip()
    for key, (lat, lon) in CITY_FALLBACK.items():
        if key in place_lower:
            return {"lat": lat, "lon": lon, "timezone": "Asia/Kolkata"}

    # Default to Chennai
    return {"lat": 13.0827, "lon": 80.2707, "timezone": "Asia/Kolkata"}


# ─── Astronomical Algorithms ────────────────────────────────────────────────

def to_julian_day(year, month, day, hour_utc):
    """Convert calendar date to Julian Day Number."""
    if month <= 2:
        year -= 1
        month += 12
    A = int(year / 100)
    B = 2 - A + int(A / 4)
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + hour_utc / 24.0 + B - 1524.5
    return jd


def julian_centuries(jd):
    """Julian centuries from J2000.0."""
    return (jd - 2451545.0) / 36525.0


def normalize_degrees(deg):
    """Normalize angle to 0-360 range."""
    return deg % 360


def lahiri_ayanamsa(jd):
    """Calculate Lahiri Ayanamsa for a given Julian Day.
    Based on Lahiri's precession formula."""
    T = julian_centuries(jd)
    # Lahiri ayanamsa (Chitrapaksha) approximation
    # Based on the standard formula: ayanamsa at J2000 ≈ 23.853 degrees
    # Precession rate ≈ 50.2564"/year
    ayanamsa = 23.853 + (50.2564 / 3600.0) * (jd - 2451545.0) / 365.25
    return ayanamsa


def sun_longitude(jd):
    """Calculate tropical Sun longitude using simplified VSOP87 theory."""
    T = julian_centuries(jd)

    # Mean longitude
    L0 = normalize_degrees(280.46646 + 36000.76983 * T + 0.0003032 * T * T)

    # Mean anomaly
    M = normalize_degrees(357.52911 + 35999.05029 * T - 0.0001537 * T * T)
    M_rad = math.radians(M)

    # Equation of center
    C = (1.914602 - 0.004817 * T - 0.000014 * T * T) * math.sin(M_rad)
    C += (0.019993 - 0.000101 * T) * math.sin(2 * M_rad)
    C += 0.000289 * math.sin(3 * M_rad)

    # Sun's true longitude
    sun_lon = normalize_degrees(L0 + C)

    # Apparent longitude (with nutation correction)
    omega = 125.04 - 1934.136 * T
    sun_lon = sun_lon - 0.00569 - 0.00478 * math.sin(math.radians(omega))

    return normalize_degrees(sun_lon)


def moon_longitude(jd):
    """Calculate tropical Moon longitude using simplified ELP2000 theory."""
    T = julian_centuries(jd)

    # Moon's mean longitude
    Lp = normalize_degrees(218.3165 + 481267.8813 * T)

    # Mean elongation
    D = normalize_degrees(297.8502 + 445267.1115 * T)

    # Sun's mean anomaly
    M = normalize_degrees(357.5291 + 35999.0503 * T)

    # Moon's mean anomaly
    Mp = normalize_degrees(134.9634 + 477198.8676 * T)

    # Moon's argument of latitude
    F = normalize_degrees(93.2720 + 483202.0175 * T)

    # Convert to radians
    D_r = math.radians(D)
    M_r = math.radians(M)
    Mp_r = math.radians(Mp)
    F_r = math.radians(F)

    # Principal periodic terms for longitude
    lon = Lp
    lon += 6.289 * math.sin(Mp_r)
    lon += 1.274 * math.sin(2 * D_r - Mp_r)
    lon += 0.658 * math.sin(2 * D_r)
    lon += 0.214 * math.sin(2 * Mp_r)
    lon -= 0.186 * math.sin(M_r)
    lon -= 0.114 * math.sin(2 * F_r)
    lon += 0.059 * math.sin(2 * D_r - 2 * Mp_r)
    lon += 0.057 * math.sin(2 * D_r - M_r - Mp_r)
    lon += 0.053 * math.sin(2 * D_r + Mp_r)
    lon += 0.046 * math.sin(2 * D_r - M_r)
    lon -= 0.041 * math.sin(M_r - Mp_r)
    lon -= 0.035 * math.sin(D_r)
    lon -= 0.031 * math.sin(Mp_r + M_r)

    return normalize_degrees(lon)


def mars_longitude(jd):
    """Calculate tropical Mars longitude."""
    T = julian_centuries(jd)
    L = normalize_degrees(355.433 + 19140.2993 * T)
    M = normalize_degrees(319.513 + 19139.8585 * T)
    M_rad = math.radians(M)
    lon = L + 10.691 * math.sin(M_rad) + 0.623 * math.sin(2 * M_rad) + 0.050 * math.sin(3 * M_rad)
    return normalize_degrees(lon)


def mercury_longitude(jd):
    """Calculate tropical Mercury longitude."""
    T = julian_centuries(jd)
    L = normalize_degrees(252.251 + 149472.6746 * T)
    M = normalize_degrees(174.795 + 149472.5153 * T)
    M_rad = math.radians(M)
    lon = L + 23.440 * math.sin(M_rad) + 2.9818 * math.sin(2 * M_rad) + 0.5255 * math.sin(3 * M_rad)
    return normalize_degrees(lon)


def jupiter_longitude(jd):
    """Calculate tropical Jupiter longitude."""
    T = julian_centuries(jd)
    L = normalize_degrees(34.351 + 3034.9057 * T)
    M = normalize_degrees(225.328 + 3034.6888 * T)
    M_rad = math.radians(M)
    lon = L + 5.555 * math.sin(M_rad) + 0.168 * math.sin(2 * M_rad)
    return normalize_degrees(lon)


def venus_longitude(jd):
    """Calculate tropical Venus longitude."""
    T = julian_centuries(jd)
    L = normalize_degrees(181.979 + 58517.8157 * T)
    M = normalize_degrees(50.416 + 58517.8039 * T)
    M_rad = math.radians(M)
    lon = L + 0.7758 * math.sin(M_rad) + 0.0033 * math.sin(2 * M_rad)
    return normalize_degrees(lon)


def saturn_longitude(jd):
    """Calculate tropical Saturn longitude."""
    T = julian_centuries(jd)
    L = normalize_degrees(50.077 + 1222.1138 * T)
    M = normalize_degrees(316.967 + 1221.5515 * T)
    M_rad = math.radians(M)
    lon = L + 6.406 * math.sin(M_rad) + 0.257 * math.sin(2 * M_rad) + 0.018 * math.sin(3 * M_rad)
    return normalize_degrees(lon)


def rahu_longitude(jd):
    """Calculate Mean North Node (Rahu) longitude."""
    T = julian_centuries(jd)
    omega = normalize_degrees(125.0445 - 1934.1363 * T + 0.0020 * T * T)
    return omega


def ascendant_longitude(jd, lat, lon_geo):
    """Calculate the Ascendant (tropical)."""
    T = julian_centuries(jd)

    # Local Sidereal Time
    theta0 = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T
    lst = normalize_degrees(theta0 + lon_geo)
    lst_rad = math.radians(lst)

    # Obliquity of ecliptic
    eps = 23.4393 - 0.0130 * T
    eps_rad = math.radians(eps)
    lat_rad = math.radians(lat)

    # Ascendant formula
    y = -math.cos(lst_rad)
    x = math.sin(eps_rad) * math.tan(lat_rad) + math.cos(eps_rad) * math.sin(lst_rad)
    asc = math.degrees(math.atan2(y, x))
    asc = normalize_degrees(asc)

    return asc


# ─── Sidereal Conversion Helpers ────────────────────────────────────────────

def tropical_to_sidereal(tropical_lon, jd):
    """Convert tropical longitude to sidereal (Lahiri)."""
    ayanamsa = lahiri_ayanamsa(jd)
    return normalize_degrees(tropical_lon - ayanamsa)


def longitude_to_sign(longitude):
    return int(longitude / 30) % 12


def longitude_to_degree_in_sign(longitude):
    return longitude % 30


def longitude_to_nakshatra(longitude):
    return int(longitude / (360.0 / 27.0)) % 27


def longitude_to_pada(longitude):
    nakshatra_span = 360.0 / 27.0
    pada_span = nakshatra_span / 4.0
    pos_in_nakshatra = longitude % nakshatra_span
    return int(pos_in_nakshatra / pada_span) + 1


def longitude_to_navamsa_sign(longitude):
    sign_index = longitude_to_sign(longitude)
    degree_in_sign = longitude_to_degree_in_sign(longitude)
    navamsa_part = int(degree_in_sign / (30.0 / 9.0))
    return (NAVAMSA_START[sign_index] + navamsa_part) % 12


def format_degree(longitude):
    deg_in_sign = longitude % 30
    degrees = int(deg_in_sign)
    minutes = int((deg_in_sign - degrees) * 60)
    seconds = int(((deg_in_sign - degrees) * 60 - minutes) * 60)
    return f"{degrees}° {minutes:02d}′ {seconds:02d}″"


# ─── Main Chart Calculation ──────────────────────────────────────────────────

def calculate_chart(name, dob, time_str, place):
    """
    Calculate full Vedic birth chart.

    Args:
        name: Person's name
        dob: Date of birth (YYYY-MM-DD)
        time_str: Time of birth (HH:MM)
        place: Place of birth

    Returns:
        dict with all chart data
    """
    # Parse inputs
    year, month, day = map(int, dob.split("-"))
    parts = time_str.split(":")
    hour = int(parts[0])
    minute = int(parts[1]) if len(parts) > 1 else 0
    hour_decimal = hour + minute / 60.0

    # Get location
    loc = get_location_data(place)
    lat, lon_geo, tz = loc["lat"], loc["lon"], loc["timezone"]

    # Convert to UTC
    tz_obj = pytz.timezone(tz)
    local_dt = tz_obj.localize(datetime(year, month, day, hour, minute))
    utc_dt = local_dt.astimezone(pytz.utc)
    hour_utc = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0

    # Julian Day
    jd = to_julian_day(utc_dt.year, utc_dt.month, utc_dt.day, hour_utc)

    # Calculate tropical longitudes
    planet_funcs = {
        "Sun": sun_longitude,
        "Moon": moon_longitude,
        "Mars": mars_longitude,
        "Mercury": mercury_longitude,
        "Jupiter": jupiter_longitude,
        "Venus": venus_longitude,
        "Saturn": saturn_longitude,
        "Rahu": rahu_longitude,
    }

    # Calculate ascendant
    asc_tropical = ascendant_longitude(jd, lat, lon_geo)
    asc_sidereal = tropical_to_sidereal(asc_tropical, jd)
    asc_sign_idx = longitude_to_sign(asc_sidereal)

    # Calculate all planets
    planets_data = []
    for planet_name, func in planet_funcs.items():
        tropical_lon = func(jd)
        sid_lon = tropical_to_sidereal(tropical_lon, jd)
        sign_idx = longitude_to_sign(sid_lon)
        nak_idx = longitude_to_nakshatra(sid_lon)
        pada = longitude_to_pada(sid_lon)
        navamsa_sign_idx = longitude_to_navamsa_sign(sid_lon)

        planets_data.append({
            "name": planet_name,
            "symbol": PLANET_SYMBOLS[planet_name],
            "longitude": sid_lon,
            "sign_index": sign_idx,
            "sign": ZODIAC_SIGNS[sign_idx],
            "sign_short": ZODIAC_SHORT[sign_idx],
            "degree": format_degree(sid_lon),
            "nakshatra": NAKSHATRAS[nak_idx],
            "nakshatra_index": nak_idx,
            "pada": pada,
            "navamsa_sign_index": navamsa_sign_idx,
            "navamsa_sign": ZODIAC_SIGNS[navamsa_sign_idx],
            "navamsa_sign_short": ZODIAC_SHORT[navamsa_sign_idx],
        })

    # Ketu = Rahu + 180°
    rahu_data = next(p for p in planets_data if p["name"] == "Rahu")
    ketu_lon = normalize_degrees(rahu_data["longitude"] + 180)
    ketu_sign_idx = longitude_to_sign(ketu_lon)
    ketu_nak_idx = longitude_to_nakshatra(ketu_lon)
    ketu_pada = longitude_to_pada(ketu_lon)
    ketu_navamsa = longitude_to_navamsa_sign(ketu_lon)

    planets_data.append({
        "name": "Ketu",
        "symbol": "Ke",
        "longitude": ketu_lon,
        "sign_index": ketu_sign_idx,
        "sign": ZODIAC_SIGNS[ketu_sign_idx],
        "sign_short": ZODIAC_SHORT[ketu_sign_idx],
        "degree": format_degree(ketu_lon),
        "nakshatra": NAKSHATRAS[ketu_nak_idx],
        "nakshatra_index": ketu_nak_idx,
        "pada": ketu_pada,
        "navamsa_sign_index": ketu_navamsa,
        "navamsa_sign": ZODIAC_SIGNS[ketu_navamsa],
        "navamsa_sign_short": ZODIAC_SHORT[ketu_navamsa],
    })

    # Build Rasi Chart
    rasi_chart = {i: [] for i in range(12)}
    for p in planets_data:
        rasi_chart[p["sign_index"]].append(p["symbol"])

    # Build Navamsa Chart
    navamsa_chart = {i: [] for i in range(12)}
    for p in planets_data:
        navamsa_chart[p["navamsa_sign_index"]].append(p["symbol"])

    # Moon data
    moon_data = next(p for p in planets_data if p["name"] == "Moon")
    sun_data = next(p for p in planets_data if p["name"] == "Sun")

    return {
        "name": name,
        "dob": dob,
        "time": time_str,
        "place": place,
        "latitude": round(lat, 4),
        "longitude_geo": round(lon_geo, 4),
        "timezone": tz,
        "lagna": {
            "sign_index": asc_sign_idx,
            "sign": ZODIAC_SIGNS[asc_sign_idx],
            "sign_short": ZODIAC_SHORT[asc_sign_idx],
            "degree": format_degree(asc_sidereal),
        },
        "moon_sign": {
            "sign": moon_data["sign"],
            "sign_short": moon_data["sign_short"],
        },
        "sun_sign": {
            "sign": sun_data["sign"],
            "sign_short": sun_data["sign_short"],
        },
        "nakshatra": {
            "name": moon_data["nakshatra"],
            "pada": moon_data["pada"],
            "index": moon_data["nakshatra_index"],
        },
        "planets": planets_data,
        "rasi_chart": {str(k): v for k, v in rasi_chart.items()},
        "navamsa_chart": {str(k): v for k, v in navamsa_chart.items()},
    }

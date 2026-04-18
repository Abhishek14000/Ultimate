"""
render_premium_v2.py
Generates kundli_report_bilingual.html — a premium portfolio-style bilingual
Vedic Kundali report with rich visual components and a language toggle.
"""

import re
import sys
import markdown

# ──────────────────────────────────────────────────────────────────────────────
# 1.  READ SOURCE MARKDOWN
# ──────────────────────────────────────────────────────────────────────────────
with open("kundli_report.md", "r", encoding="utf-8") as f:
    MD_EN = f.read()

# ──────────────────────────────────────────────────────────────────────────────
# 2.  HINDI TRANSLATION (embedded, same as render_bilingual_html.py)
# ──────────────────────────────────────────────────────────────────────────────
with open("render_bilingual_html.py", "r", encoding="utf-8") as f:
    _src = f.read()
_s = _src.find('md_hi = """') + len('md_hi = """')
_e = _src.find('"""', _s)
MD_HI = _src[_s:_e]

# ──────────────────────────────────────────────────────────────────────────────
# 3.  KEYWORD HIGHLIGHTS
# ──────────────────────────────────────────────────────────────────────────────
def apply_highlights(text):
    text = re.sub(
        r'\b(exalted|own sign|strong|beneficial|yoga|Digbala|Swakshetra|ACTIVE|FULL)\b',
        r'<span class="kw-green">\1</span>', text, flags=re.IGNORECASE)
    text = re.sub(
        r'\b(debilitated|neecha|dosha|afflicted|combust|weak|Neecha|ABSENT|WEAKEST)\b',
        r'<span class="kw-red">\1</span>', text, flags=re.IGNORECASE)
    text = re.sub(
        r'\b(mixed|moderate|neutral|partial|MODERATE)\b',
        r'<span class="kw-amber">\1</span>', text, flags=re.IGNORECASE)
    return text

def md2html(text):
    return markdown.markdown(apply_highlights(text),
                             extensions=["tables", "fenced_code"])

# ──────────────────────────────────────────────────────────────────────────────
# 4.  SPLIT MARKDOWN INTO SECTIONS
# ──────────────────────────────────────────────────────────────────────────────
def split_sections(md):
    """Returns dict: {0: header_html, 1..10: section_html}"""
    chunks = re.split(r'\n(?=## (?:SECTION|खंड))', md)
    result = {'hdr': md2html(chunks[0])}
    for ch in chunks[1:]:
        m = re.match(r'## (?:SECTION\s*|खंड\s*)(\d+)', ch)
        n = int(m.group(1)) if m else 0
        result[n] = md2html(ch)
    return result

SECS_EN = split_sections(MD_EN)
SECS_HI = split_sections(MD_HI)

# ──────────────────────────────────────────────────────────────────────────────
# 5.  VISUAL DATA
# ──────────────────────────────────────────────────────────────────────────────
PLANETS = [
    {"sym":"☉","name":"Sun","name_hi":"सूर्य",     "sign":"Leo",         "sign_hi":"सिंह",    "house":3,  "deg":"16°43′","nak":"Purva Phalguni","nak_hi":"पूर्वा फाल्गुनी","pada":2,"cls":"own",   "label":"Own Sign",   "label_hi":"स्वराशि",   "role":"Mild Malefic · 3rd lord","role_hi":"सौम्य अशुभ · 3रे लग्नेश","col":"#f5a020"},
    {"sym":"☽","name":"Moon","name_hi":"चंद्र",    "sign":"Libra",        "sign_hi":"तुला",    "house":5,  "deg":"13°02′","nak":"Swati",         "nak_hi":"स्वाती",           "pada":2,"cls":"neutral","label":"Neutral",    "label_hi":"सम",         "role":"Mild Benefic · 2nd lord", "role_hi":"सौम्य शुभ · 2रे लग्नेश","col":"#a0b8e0"},
    {"sym":"♂","name":"Mars","name_hi":"मंगल",     "sign":"Cancer",       "sign_hi":"कर्क",    "house":2,  "deg":"27°08′","nak":"Ashlesha",      "nak_hi":"आश्लेषा",          "pada":4,"cls":"debil", "label":"Debilitated","label_hi":"नीचस्थ",    "role":"Functional Malefic · 6+11","role_hi":"कार्यात्मक अशुभ · 6+11","col":"#e05050"},
    {"sym":"☿","name":"Mercury","name_hi":"बुध",   "sign":"Leo",          "sign_hi":"सिंह",    "house":3,  "deg":"27°23′","nak":"U. Phalguni",   "nak_hi":"उत्तरा फाल्गुनी", "pada":1,"cls":"combust","label":"Combust",    "label_hi":"दग्ध",       "role":"Most Benefic · Lagna lord","role_hi":"परम शुभ · लग्नेश",       "col":"#40b890"},
    {"sym":"♃","name":"Jupiter","name_hi":"बृहस्पति","sign":"Taurus",    "sign_hi":"वृषभ",    "house":12, "deg":"16°11′","nak":"Rohini",        "nak_hi":"रोहिणी",           "pada":2,"cls":"neutral","label":"Neutral",    "label_hi":"सम",         "role":"Func. Malefic · 7+10",    "role_hi":"कार्यात्मक अशुभ · 7+10","col":"#f0a040"},
    {"sym":"♀","name":"Venus","name_hi":"शुक्र",   "sign":"Virgo",        "sign_hi":"कन्या",   "house":4,  "deg":"09°22′","nak":"U. Phalguni",   "nak_hi":"उत्तरा फाल्गुनी", "pada":4,"cls":"debil", "label":"Debil+Digbala","label_hi":"नीच+दिग्बल","role":"Benefic · 5+12 lord",     "role_hi":"शुभ · 5+12 लग्नेश",     "col":"#e080a0"},
    {"sym":"♄","name":"Saturn","name_hi":"शनि",    "sign":"Taurus",       "sign_hi":"वृषभ",    "house":12, "deg":"07°02′","nak":"Krittika",      "nak_hi":"कृत्तिका",         "pada":4,"cls":"friendly","label":"Friendly",  "label_hi":"मित्र",      "role":"Mixed · 8+9 lord",        "role_hi":"मिश्रित · 8+9 लग्नेश",  "col":"#9090c0"},
    {"sym":"☊","name":"Rahu","name_hi":"राहु",     "sign":"Gemini",       "sign_hi":"मिथुन",   "house":1,  "deg":"28°11′","nak":"Punarvasu",     "nak_hi":"पुनर्वसु",         "pada":3,"cls":"exalted","label":"Exalted",   "label_hi":"उच्च",       "role":"Shadow Planet · Lagna",   "role_hi":"छाया ग्रह · लग्न",       "col":"#8860d0"},
    {"sym":"☋","name":"Ketu","name_hi":"केतु",     "sign":"Sagittarius",  "sign_hi":"धनु",     "house":7,  "deg":"28°11′","nak":"Uttarashadha",  "nak_hi":"उत्तराषाढ़ा",      "pada":1,"cls":"exalted","label":"Exalted",   "label_hi":"उच्च",       "role":"Shadow Planet · 7th",     "role_hi":"छाया ग्रह · 7वाँ",       "col":"#c080b0"},
]

ASHTAKVARGA = [
    (1,"Gemini","मिथुन",29),(2,"Cancer","कर्क",26),(3,"Leo","सिंह",32),
    (4,"Virgo","कन्या",22),(5,"Libra","तुला",26),(6,"Scorpio","वृश्चिक",25),
    (7,"Sagittarius","धनु",28),(8,"Capricorn","मकर",27),(9,"Aquarius","कुंभ",25),
    (10,"Pisces","मीन",37),(11,"Aries","मेष",31),(12,"Taurus","वृषभ",29),
]

DASHAS = [
    ("Rahu","राहु","☊","2000","2010","complete","#8860d0",18),
    ("Jupiter","बृहस्पति","♃","2010","2026","complete","#f0a040",16),
    ("Saturn","शनि","♄","2026","2045","current","#c9a84c",19),
    ("Mercury","बुध","☿","2045","2062","future","#40b890",17),
    ("Ketu","केतु","☋","2062","2069","future","#c080b0",7),
    ("Venus","शुक्र","♀","2069","2089","future","#e080a0",20),
    ("Sun","सूर्य","☉","2089","2095","future","#f5a020",6),
    ("Moon","चंद्र","☽","2095","2105","future","#a0b8e0",10),
    ("Mars","मंगल","♂","2105","2112","future","#e05050",7),
]

ANTARDASHA = [
    ("Sat-Sat","2026 Jan","2029 Jan","Foundation · discipline · isolation","current"),
    ("Sat-Mer","2029 Jan","2031 Oct","Writing · research · nervous system focus","future"),
    ("Sat-Ket","2031 Oct","2032 Nov","Spiritual peak · detachment · karmic completion","future"),
    ("Sat-Ven","2032 Nov","2036 Jan","★ PEAK Marriage · career · finance · recognition","future"),
    ("Sat-Sun","2036 Jan","2036 Dec","Public recognition · solar elevation","future"),
    ("Sat-Mon","2036 Dec","2038 Jul","Dhana Yoga · prosperity · family expansion","future"),
    ("Sat-Mar","2038 Jul","2039 Sep","⚠ Health vigilance · avoid conflict","future"),
    ("Sat-Rahu","2039 Sep","2042 Jul","★ PEAK 2 · global/tech career peak","future"),
    ("Sat-Jup","2042 Jul","2045 Jan","Philosophical consolidation · mentoring","future"),
]

YOGAS = [
    ("Sarala Viparita Raja Yoga","HIGH","Saturn (8th lord in 12th)","2026–2045","active",
     "Phoenix resilience. Setbacks reverse in native's favour. The harder life pushes, the stronger the rebound."),
    ("Partial Dhana Yoga","MODERATE","Moon (2nd lord in 5th)","Sat-Moon 2036–38","active",
     "Wealth through intellect and creativity. Emotional discipline required to retain gains."),
    ("Partial Budha-Aditya Yoga","MODERATE","Sun + Mercury conjunction in Leo","Lifelong","active",
     "Recognised intellect and communication. ~40–50% strength due to Mercury combustion."),
    ("Venus Digbala in 4th","FULL","Venus (09°22′ Virgo)","Lifelong","active",
     "Directional strength overrides sign debilitation. Home becomes beautiful through personal effort."),
    ("Rahu Exaltation in Lagna","HIGH","Rahu (28°11′ Gemini)","Lifelong","active",
     "Maximum worldly ambition and unconventional drive. The world takes notice of this person."),
    ("Venus 5th lord aspects 10th","MODERATE","Venus from 4th, 7th aspect","Sat-Venus 2032–36","active",
     "Creative/artistic elements connect to career success. Pisces 10th house energised."),
]

DOSHAS = [
    ("Manglik Dosha","LOW","Mars in 2nd from Lagna only; debilitated Mars weakens it further.",
     "Manifests as harsh speech in family, not partner harm."),
    ("Kaal Sarp Dosha","ABSENT","Jupiter + Saturn on opposite side of Rahu-Ketu axis. Full KSD not present.",
     "Partial imbalance (5 vs 2 planets) gives periodic nodal disruptions — manageable."),
    ("Pitra Dosha","MILD","Rahu aspects 9th; Saturn (9th lord) in 12th; Ketu aspects Sun.",
     "Ancestral karma — tarpan on Amavasya, Gayatri Mantra, Peepal tree care."),
    ("Sade Sati","NONE NOW","Previous Sade Sati: age 9–17 (formative). Next: Oct 2038.",
     "Saturn Mahadasha (2026–45) has Sade Sati-like intensity dashawise — requires awareness."),
]

REMEDIES = [
    ("Mercury","बुध","☿","CRITICAL","Combust Lagna lord","#40b890",
     "Om Bum Budhaya Namah — 108× Wednesdays before 8 AM",
     "Daily reading + writing routine · teach others · green plants · limit screen time · emerald gemstone (trial first)"),
    ("Mars","मंगल","♂","HIGH","Debilitated 6+11 lord","#e05050",
     "Om Ang Angarakaya Namah — 108× Tuesdays · Hanuman Chalisa daily",
     "Pause 3 breaths before speaking when emotional · physical exercise Tuesdays · no Red Coral gemstone"),
    ("Venus","शुक्र","♀","MODERATE","Debilitated 5+12 lord","#e080a0",
     "Om Shum Shukraya Namah — 108× Fridays · Shri Suktam",
     "Create home beauty deliberately · white flowers to Lakshmi Fridays · no Diamond until post-2032"),
    ("Saturn","शनि","♄","HIGH","Current Mahadasha lord","#9090c0",
     "Om Sham Shanaischaraya Namah — 108× Saturdays · Mahamrityunjaya daily (2026–29)",
     "Feed crows sesame Saturdays · serve elderly · Blue Sapphire only with 3-day trial"),
    ("Pitra Dosha","पितृ दोष","☽","MODERATE","Ancestral karma","#c9a84c",
     "Gayatri Mantra 108× daily · tarpan every Amavasya · Pitru Paksha Shraddha",
     "Plant + water Peepal tree daily · feed Brahmins on Ekadashi"),
    ("Lifestyle","जीवन शैली","★","ONGOING","Structural corrections","#a0c8a0",
     "Sleep 10:30 PM–6 AM · 30 min daily exercise · 20 min meditation",
     "Weekly 4-hr digital detox · weekly financial ledger · avoid arguments Tue + Sat"),
]

LIFE_DOMAINS = [
    ("Career","करियर","💼","10th house Pisces (SAV 37 — highest) · Jupiter in 12th · Venus aspects 10th",
     "Foundation now (2026–29) → recognition peak Saturn-Venus (2032–36) → global peak Saturn-Rahu (2039–42). Domains: foreign orgs, research, writing, creative tech, law/philosophy.",
     "#f5a020"),
    ("Wealth","धन","💰","2nd house (Mars debil) · 11th house (Mars debil) · Moon 2nd lord in 5th",
     "Early leakage (pre-2026). First accumulation: Saturn-Venus 2032–36. Peak prosperity: Saturn-Moon Dec 2036–Jul 2038 (Dhana Yoga activates). Long-term: Mercury MD 2045–62.",
     "#c9a84c"),
    ("Marriage","विवाह","💍","7th house Ketu · 7th lord Jupiter in 12th · Venus debil+Digbala",
     "Most complex area. First relationship Jupiter-Venus 2017–20 (painful lessons). Primary marriage window: Saturn-Venus Nov 2032–Jan 2036. Partner: philosophical, spiritual, possibly foreign background.",
     "#e080a0"),
    ("Health","स्वास्थ्य","🌿","Gemini Lagna (respiratory, nervous) · combust Mercury · debil Mars in 2nd",
     "Key vulnerabilities: nervous system/anxiety (primary), respiratory, digestive, dental. Critical vigilance: Sat-Sat 2026–29. Caution period: Sat-Mars 2038–39. Jupiter aspects 6th — good immune protection.",
     "#40b890"),
    ("Spiritual","आध्यात्मिक","🪔","Jupiter+Saturn in 12th (moksha bhava) · Ketu in 7th · 9th lord Saturn",
     "Dark night of soul: Sat-Sat 2026–29. Most intense: Sat-Ketu 2031–32. Jupiter in Rohini: path moves from intellectual → devotional. Legacy transmission: Mercury MD 2045–62.",
     "#8860d0"),
]

STRENGTH_RANKING = [
    ("Sun","सूर्य","☉",90,"Own sign in 3rd","#f5a020"),
    ("Rahu","राहु","☊",82,"Exalted in Lagna","#8860d0"),
    ("Saturn","शनि","♄",72,"Friendly sign + Sarala Yoga","#9090c0"),
    ("Moon","चंद्र","☽",60,"Trikona, moderate Paksha Bala","#a0b8e0"),
    ("Jupiter","बृहस्पति","♃",52,"Neutral sign, 12th house","#f0a040"),
    ("Ketu","केतु","☋",48,"Possibly exalted in 7th","#c080b0"),
    ("Venus","शुक्र","♀",40,"Debilitated + Digbala (mixed)","#e080a0"),
    ("Mercury","बुध","☿",28,"Combust — severely compromised","#40b890"),
    ("Mars","मंगल","♂",15,"Debilitated, no cancellation","#e05050"),
]

# ──────────────────────────────────────────────────────────────────────────────
# 6.  HTML COMPONENT BUILDERS
# ──────────────────────────────────────────────────────────────────────────────

def planet_cards_html():
    cards = ""
    for p in PLANETS:
        cards += f"""
<div class="planet-card cls-{p['cls']}">
  <div class="pc-sym" style="color:{p['col']}">{p['sym']}</div>
  <div class="pc-body">
    <div class="pc-name">
      <span class="lang-en">{p['name']}</span>
      <span class="lang-hi" style="display:none">{p['name_hi']}</span>
    </div>
    <div class="pc-sign">
      <span class="lang-en">{p['sign']} · H{p['house']}</span>
      <span class="lang-hi" style="display:none">{p['sign_hi']} · H{p['house']}</span>
    </div>
    <div class="pc-deg">{p['deg']} · <span class="lang-en">{p['nak']} p{p['pada']}</span><span class="lang-hi" style="display:none">{p['nak_hi']} प{p['pada']}</span></div>
    <div class="pc-badge badge-{p['cls']}">
      <span class="lang-en">{p['label']}</span>
      <span class="lang-hi" style="display:none">{p['label_hi']}</span>
    </div>
    <div class="pc-role">
      <span class="lang-en">{p['role']}</span>
      <span class="lang-hi" style="display:none">{p['role_hi']}</span>
    </div>
  </div>
</div>"""
    return f'<div class="planet-grid">{cards}</div>'


def kundali_chart_html():
    # South Indian fixed-sign chart
    # Sign → house number for Gemini Lagna
    sign_to_house = {
        "Pisces":10,"Aries":11,"Taurus":12,"Gemini":1,
        "Aquarius":9,"Cancer":2,"Capricorn":8,"Leo":3,
        "Sagittarius":7,"Scorpio":6,"Libra":5,"Virgo":4,
    }
    # planets per sign
    by_sign = {s:[] for s in sign_to_house}
    for p in PLANETS:
        by_sign[p['sign']].append(p['sym'])
    # mark Lagna
    by_sign['Gemini'].insert(0,'↑')

    def cell(sign, extra_cls=""):
        h = sign_to_house[sign]
        signs_hi = {"Pisces":"मीन","Aries":"मेष","Taurus":"वृषभ","Gemini":"मिथुन",
                    "Aquarius":"कुंभ","Cancer":"कर्क","Capricorn":"मकर","Leo":"सिंह",
                    "Sagittarius":"धनु","Scorpio":"वृश्चिक","Libra":"तुला","Virgo":"कन्या"}
        ps = " ".join(by_sign[sign])
        return f"""<div class="kc {extra_cls}">
  <div class="kc-h">H{h}</div>
  <div class="kc-sign lang-en">{sign}</div>
  <div class="kc-sign lang-hi" style="display:none">{signs_hi[sign]}</div>
  <div class="kc-planets">{ps}</div>
</div>"""

    return f"""
<div class="kundali-wrap">
  <div class="kundali-grid">
    {cell("Pisces")}
    {cell("Aries")}
    {cell("Taurus")}
    {cell("Gemini","kc-lagna")}
    {cell("Aquarius")}
    <div class="kc kc-center" style="grid-area:2/2/4/4">
      <div class="kc-om">ॐ</div>
      <div class="kc-native">Abhishek Singh</div>
      <div class="kc-info lang-en">Gemini Lagna · 3 Sep 2000</div>
      <div class="kc-info lang-hi" style="display:none">मिथुन लग्न · 3 सित 2000</div>
    </div>
    {cell("Cancer")}
    {cell("Capricorn")}
    {cell("Leo")}
    {cell("Sagittarius")}
    {cell("Scorpio")}
    {cell("Libra")}
    {cell("Virgo")}
  </div>
  <p class="chart-caption lang-en">South Indian Kundali · Lahiri Ayanamsa</p>
  <p class="chart-caption lang-hi" style="display:none">दक्षिण भारतीय कुंडली · लाहिरी अयनांश</p>
</div>"""


def ashtakvarga_html():
    MAX_SCORE = 45
    rows = ""
    for h, sign, sign_hi, score in ASHTAKVARGA:
        pct = int(score / MAX_SCORE * 100)
        flag = ""
        if score == 37: flag = " ★"
        elif score == 22: flag = " ⚠"
        elif score >= 31: flag = " ↑"
        rows += f"""
<div class="avk-row">
  <div class="avk-label">
    <span class="avk-h">H{h}</span>
    <span class="avk-sign lang-en">{sign}</span>
    <span class="avk-sign lang-hi" style="display:none">{sign_hi}</span>
  </div>
  <div class="avk-bar-wrap">
    <div class="avk-bar" data-pct="{pct}" style="width:0%;background:{'#c9a84c' if score>=30 else '#6080a0' if score>=25 else '#804040'}"></div>
  </div>
  <div class="avk-score">{score}{flag}</div>
</div>"""
    return f'<div class="ashtakvarga">{rows}</div>'


def dasha_timeline_html():
    total_years = sum(d[7] for d in DASHAS[:6])
    segs = ""
    for name, name_hi, sym, start, end, status, col, dur in DASHAS:
        pct = dur / total_years * 100
        cls = f"dt-seg dt-{status}"
        segs += f"""<div class="{cls}" style="width:{pct:.1f}%;background:{'rgba(201,168,76,0.25)' if status=='current' else 'rgba(255,255,255,0.04)'};border-color:{col}">
  <div class="dt-sym" style="color:{col}">{sym}</div>
  <div class="dt-name lang-en">{name}</div>
  <div class="dt-name lang-hi" style="display:none">{name_hi}</div>
  <div class="dt-yrs">{start}–{end}</div>
</div>"""

    ad_rows = ""
    for ad, s, e, desc, st in ANTARDASHA:
        cls = "ad-current" if st == "current" else ""
        ad_rows += f"""<tr class="{cls}">
  <td><strong>{ad}</strong></td>
  <td>{s}</td><td>{e}</td>
  <td>{desc}</td>
</tr>"""

    return f"""
<div class="dasha-section">
  <h3 class="vis-title lang-en">Mahadasha Timeline (2000–2089)</h3>
  <h3 class="vis-title lang-hi" style="display:none">महादशा समयरेखा (2000–2089)</h3>
  <div class="dasha-timeline">{segs}</div>
  <h3 class="vis-title lang-en" style="margin-top:32px">Current Saturn Mahadasha — Antardasha Breakdown</h3>
  <h3 class="vis-title lang-hi" style="display:none;margin-top:32px">वर्तमान शनि महादशा — अंतर्दशा विवरण</h3>
  <div class="table-wrap">
    <table class="ad-table">
      <thead><tr>
        <th>Period</th><th>Start</th><th>End</th><th class="lang-en">Character</th><th class="lang-hi" style="display:none">स्वभाव</th>
      </tr></thead>
      <tbody>{ad_rows}</tbody>
    </table>
  </div>
</div>"""


def yoga_cards_html():
    cards = ""
    for name, strength, planets, timing, status, desc in YOGAS:
        badge_cls = {"HIGH":"badge-green","MODERATE":"badge-amber","FULL":"badge-blue"}.get(strength,"badge-amber")
        cards += f"""
<div class="yoga-card">
  <div class="yc-header">
    <div class="yc-name">{name}</div>
    <span class="badge {badge_cls}">{strength}</span>
  </div>
  <div class="yc-planet">{planets}</div>
  <div class="yc-timing">⏱ {timing}</div>
  <p class="yc-desc">{desc}</p>
</div>"""
    return f'<div class="yoga-grid">{cards}</div>'


def dosha_cards_html():
    cards = ""
    sev_cls = {"LOW":"sev-low","ABSENT":"sev-absent","MILD":"sev-mild",
               "NONE NOW":"sev-absent","MODERATE":"sev-mod"}
    for name, severity, detail, remedy in DOSHAS:
        cls = sev_cls.get(severity, "sev-mod")
        cards += f"""
<div class="dosha-card">
  <div class="dc-header">
    <span class="dc-name">{name}</span>
    <span class="badge {cls}">{severity}</span>
  </div>
  <p class="dc-detail">{detail}</p>
  <div class="dc-remedy">💊 {remedy}</div>
</div>"""
    return f'<div class="dosha-grid">{cards}</div>'


def life_domain_cards_html():
    cards = ""
    for title, title_hi, icon, config, analysis, col in LIFE_DOMAINS:
        cards += f"""
<div class="ld-card" style="border-top-color:{col}">
  <div class="ld-icon" style="background:{col}22;color:{col}">{icon}</div>
  <div class="ld-title lang-en">{title}</div>
  <div class="ld-title lang-hi" style="display:none">{title_hi}</div>
  <div class="ld-config">{config}</div>
  <p class="ld-analysis">{analysis}</p>
</div>"""
    return f'<div class="ld-grid">{cards}</div>'


def strength_bars_html():
    rows = ""
    for name, name_hi, sym, pct, reason, col in STRENGTH_RANKING:
        rows += f"""
<div class="sr-row">
  <div class="sr-label">
    <span class="sr-sym" style="color:{col}">{sym}</span>
    <span class="sr-name lang-en">{name}</span>
    <span class="sr-name lang-hi" style="display:none">{name_hi}</span>
  </div>
  <div class="sr-bar-wrap">
    <div class="sr-bar" data-pct="{pct}" style="width:0%;background:{col}aa"></div>
  </div>
  <div class="sr-pct" style="color:{col}">{pct}</div>
  <div class="sr-reason lang-en">{reason}</div>
  <div class="sr-reason lang-hi" style="display:none">{reason}</div>
</div>"""
    return f'<div class="strength-rank">{rows}</div>'


def remedy_cards_html():
    cards = ""
    pri_cls = {"CRITICAL":"badge-red","HIGH":"badge-amber","MODERATE":"badge-green","ONGOING":"badge-blue"}
    for name, name_hi, sym, priority, rationale, col, mantra, behavioral in REMEDIES:
        cls = pri_cls.get(priority,"badge-amber")
        cards += f"""
<div class="rem-card" style="border-left-color:{col}">
  <div class="rem-header">
    <span class="rem-sym" style="color:{col}">{sym}</span>
    <div>
      <div class="rem-name lang-en">{name}</div>
      <div class="rem-name lang-hi" style="display:none">{name_hi}</div>
    </div>
    <span class="badge {cls}">{priority}</span>
  </div>
  <div class="rem-rationale">{rationale}</div>
  <div class="rem-mantra"><strong>🕉 </strong>{mantra}</div>
  <div class="rem-behavioral">🌿 {behavioral}</div>
</div>"""
    return f'<div class="remedy-grid">{cards}</div>'


def hero_html():
    return """
<section class="hero" id="hero">
  <canvas id="starsCanvas"></canvas>
  <div class="hero-inner">
    <div class="hero-badge lang-en">✦ Vedic Astrology · 11 Classical Texts · Master Analysis ✦</div>
    <div class="hero-badge lang-hi" style="display:none">✦ वैदिक ज्योतिष · 11 शास्त्रीय ग्रंथ · मास्टर विश्लेषण ✦</div>
    <div class="hero-om">ॐ</div>
    <h1 class="hero-name">Abhishek Singh</h1>
    <p class="hero-sub lang-en">Premium Vedic Kundali Report · 18 April 2026</p>
    <p class="hero-sub lang-hi" style="display:none">प्रीमियम वैदिक कुंडली रिपोर्ट · 18 अप्रैल 2026</p>
    <div class="hero-stats">
      <div class="hs-pill"><span class="hs-label lang-en">Born</span><span class="hs-label lang-hi" style="display:none">जन्म</span><span class="hs-value">3 Sep 2000</span></div>
      <div class="hs-pill"><span class="hs-label lang-en">Time</span><span class="hs-label lang-hi" style="display:none">समय</span><span class="hs-value">00:00:18 IST</span></div>
      <div class="hs-pill"><span class="hs-label lang-en">Place</span><span class="hs-label lang-hi" style="display:none">स्थान</span><span class="hs-value">Ayodhya, UP</span></div>
      <div class="hs-pill"><span class="hs-label lang-en">Lagna</span><span class="hs-label lang-hi" style="display:none">लग्न</span><span class="hs-value">Gemini 01°09′</span></div>
      <div class="hs-pill"><span class="hs-label lang-en">Nakshatra</span><span class="hs-label lang-hi" style="display:none">नक्षत्र</span><span class="hs-value">Swati Pada 2</span></div>
      <div class="hs-pill hs-current"><span class="hs-label lang-en">Dasha Now</span><span class="hs-label lang-hi" style="display:none">दशा अभी</span><span class="hs-value">♄ Saturn 2026–45</span></div>
    </div>
    <a href="#section-1" class="hero-cta lang-en">Begin the Journey ↓</a>
    <a href="#section-1" class="hero-cta lang-hi" style="display:none">यात्रा शुरू करें ↓</a>
  </div>
</section>"""


def nav_html():
    links = [
        (1,"Chart Foundation","कुंडली आधार"),
        (2,"Planets","ग्रह"),
        (3,"Houses","भाव"),
        (4,"Yogas","योग"),
        (5,"Doshas","दोष"),
        (6,"Dasha","दशा"),
        (7,"Predictions","भविष्यवाणी"),
        (8,"Hierarchy","पदानुक्रम"),
        (9,"Remedies","उपाय"),
        (10,"Synthesis","संश्लेषण"),
    ]
    nav_items = ""
    for n, en, hi in links:
        nav_items += f'<a href="#section-{n}" class="nav-link" data-sec="{n}"><span class="lang-en">{en}</span><span class="lang-hi" style="display:none">{hi}</span></a>'
    return f"""
<nav class="topnav" id="topnav">
  <a href="#hero" class="nav-brand">☽ <span class="lang-en">Kundali 2026</span><span class="lang-hi" style="display:none">कुंडली 2026</span></a>
  <div class="nav-links">{nav_items}</div>
  <button class="lang-toggle" id="langBtn" onclick="toggleLang()">
    <span id="btnText">हिंदी</span> <span id="btnArrow">⇄</span>
  </button>
</nav>"""


def section_wrap(num, icon, title_en, title_hi, visuals_html, content_en, content_hi):
    return f"""
<section class="sec" id="section-{num}">
  <div class="sec-head">
    <div class="sec-num">{num:02d}</div>
    <div class="sec-title-group">
      <span class="sec-icon">{icon}</span>
      <h2 class="sec-title">
        <span class="lang-en">{title_en}</span>
        <span class="lang-hi" style="display:none">{title_hi}</span>
      </h2>
    </div>
  </div>
  <div class="sec-body">
    {visuals_html}
    <div class="sec-prose">
      <div class="lang-en prose">{content_en}</div>
      <div class="lang-hi prose" style="display:none">{content_hi}</div>
    </div>
  </div>
</section>"""


# ──────────────────────────────────────────────────────────────────────────────
# 7.  CSS
# ──────────────────────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Rajdhani:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');

:root {
  --bg:       #07071a;
  --bg2:      #0b0b22;
  --card:     rgba(10,10,28,0.96);
  --gold:     #c9a84c;
  --gold2:    #f5c842;
  --gold-dim: rgba(201,168,76,0.25);
  --gold-glow:rgba(201,168,76,0.12);
  --border:   rgba(201,168,76,0.2);
  --text:     #e8dfc8;
  --muted:    #8a7c68;
  --green:    #52c478;
  --red:      #e06060;
  --amber:    #f0c040;
  --blue:     #60a0e0;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;font-size:16px}
body{font-family:'EB Garamond',serif;background:var(--bg);color:var(--text);line-height:1.8;overflow-x:hidden}

/* ─── Hindi font ─── */
.lang-hi,.lang-hi *{font-family:'Noto Sans Devanagari',serif;line-height:2.1}

/* ─── Scrollbar ─── */
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:#07071a}
::-webkit-scrollbar-thumb{background:#3a2a0a;border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--gold)}

/* ═══════════════ HERO ═══════════════ */
.hero{position:relative;min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden;background:radial-gradient(ellipse at 50% 40%, #12123a 0%, var(--bg) 70%)}
#starsCanvas{position:absolute;inset:0;z-index:0}
.hero-inner{position:relative;z-index:1;padding:40px 20px;max-width:900px;margin:0 auto}
.hero-badge{font-family:'Rajdhani',sans-serif;font-size:.8rem;letter-spacing:3px;color:var(--gold);text-transform:uppercase;margin-bottom:20px;opacity:.85}
.hero-om{font-size:clamp(4rem,12vw,8rem);color:var(--gold);opacity:.15;line-height:1;margin-bottom:-20px;animation:pulse-om 4s ease-in-out infinite}
@keyframes pulse-om{0%,100%{opacity:.12;transform:scale(1)}50%{opacity:.22;transform:scale(1.04)}}
.hero-name{font-family:'Cinzel',serif;font-size:clamp(2.4rem,7vw,4.5rem);font-weight:700;color:#fff;letter-spacing:4px;text-shadow:0 0 40px rgba(201,168,76,0.4);margin:16px 0 8px}
.hero-sub{font-size:1rem;color:var(--muted);margin-bottom:36px;letter-spacing:1px}
.hero-stats{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-bottom:40px}
.hs-pill{background:rgba(201,168,76,0.07);border:1px solid var(--border);border-radius:40px;padding:8px 18px;display:flex;flex-direction:column;align-items:center;gap:2px;min-width:110px}
.hs-pill.hs-current{border-color:var(--gold);background:rgba(201,168,76,0.12)}
.hs-label{font-family:'Rajdhani',sans-serif;font-size:.65rem;letter-spacing:2px;text-transform:uppercase;color:var(--muted)}
.hs-value{font-family:'Rajdhani',sans-serif;font-size:.88rem;color:var(--gold);font-weight:600}
.hero-cta{display:inline-block;margin-top:8px;padding:12px 32px;border:1px solid var(--gold);border-radius:40px;color:var(--gold);text-decoration:none;font-family:'Cinzel',serif;font-size:.85rem;letter-spacing:2px;transition:all .3s}
.hero-cta:hover{background:var(--gold);color:#07071a}

/* ═══════════════ NAV ═══════════════ */
.topnav{position:fixed;top:0;left:0;right:0;z-index:999;display:flex;align-items:center;gap:8px;padding:0 24px;height:54px;background:rgba(7,7,26,0.92);backdrop-filter:blur(16px);border-bottom:1px solid var(--border);transition:all .3s;transform:translateY(-100%)}
.topnav.visible{transform:translateY(0)}
.nav-brand{font-family:'Cinzel',serif;color:var(--gold);font-size:.85rem;text-decoration:none;white-space:nowrap;letter-spacing:1px}
.nav-links{flex:1;display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;justify-content:center}
.nav-links::-webkit-scrollbar{display:none}
.nav-link{font-family:'Rajdhani',sans-serif;font-size:.7rem;letter-spacing:1px;padding:4px 10px;border-radius:20px;color:var(--muted);text-decoration:none;white-space:nowrap;transition:all .2s;text-transform:uppercase}
.nav-link:hover,.nav-link.active{color:var(--gold);background:var(--gold-glow)}
.lang-toggle{background:linear-gradient(135deg,#b8860b,var(--gold));color:#07071a;border:none;border-radius:30px;padding:7px 16px;font-size:.75rem;font-weight:700;cursor:pointer;white-space:nowrap;letter-spacing:.5px;font-family:'Rajdhani',sans-serif;transition:all .25s}
.lang-toggle:hover{background:linear-gradient(135deg,var(--gold),var(--gold2));transform:translateY(-1px)}

/* ═══════════════ SECTIONS ═══════════════ */
.sec{padding:80px 0;border-bottom:1px solid rgba(201,168,76,0.08)}
.sec-head{display:flex;align-items:flex-start;gap:20px;max-width:1100px;margin:0 auto 40px;padding:0 40px}
.sec-num{font-family:'Cinzel',serif;font-size:5rem;color:var(--gold);opacity:.08;line-height:1;font-weight:700;min-width:80px;user-select:none}
.sec-title-group{padding-top:12px}
.sec-icon{font-size:1.6rem;display:block;margin-bottom:4px}
.sec-title{font-family:'Cinzel',serif;font-size:clamp(1.5rem,3vw,2rem);color:var(--gold2);letter-spacing:2px}
.sec-body{max-width:1100px;margin:0 auto;padding:0 40px}

/* prose styling */
.prose h1,.prose h2{font-family:'Cinzel',serif;color:var(--gold2);margin:2rem 0 .8rem;letter-spacing:1px}
.prose h3{font-family:'Cinzel',serif;color:var(--gold);font-size:1.05rem;margin:1.8rem 0 .5rem;letter-spacing:.5px}
.prose h4{color:var(--gold);font-size:.95rem;margin:1.2rem 0 .4rem}
.prose p{margin-bottom:1rem;font-size:1.05rem}
.prose ul,.prose ol{margin:0 0 1rem 1.5rem}
.prose li{margin-bottom:.4rem;font-size:1.05rem}
.prose strong{color:var(--gold2);font-weight:600}
.prose em{color:#c8b070;font-style:italic}
.prose blockquote{border-left:3px solid var(--gold);padding:12px 20px;background:rgba(201,168,76,0.06);border-radius:0 6px 6px 0;margin:16px 0;font-style:italic;color:#c8b070}
.prose hr{border:none;border-top:1px solid var(--border);margin:2rem 0}
.prose table{width:100%;border-collapse:collapse;margin:16px 0;font-size:.9rem}
.prose th{background:rgba(201,168,76,0.12);color:var(--gold2);padding:10px 14px;border:1px solid var(--border);text-align:left;font-family:'Rajdhani',sans-serif;letter-spacing:.5px}
.prose td{padding:8px 14px;border:1px solid rgba(201,168,76,0.1);color:var(--text);vertical-align:top}
.prose tr:nth-child(even) td{background:rgba(255,255,255,0.02)}
.prose tr:hover td{background:rgba(201,168,76,0.04)}
.table-wrap{overflow-x:auto;margin:16px 0}

/* keyword highlights */
.kw-green{color:#52c478;font-weight:600}
.kw-red{color:#e06060;font-weight:600}
.kw-amber{color:#f0c040;font-weight:600}

/* badges */
.badge{display:inline-block;padding:2px 10px;border-radius:20px;font-size:.65rem;font-weight:700;letter-spacing:1px;font-family:'Rajdhani',sans-serif;text-transform:uppercase}
.badge-green{background:rgba(82,196,120,.15);color:#52c478;border:1px solid #52c47840}
.badge-red{background:rgba(224,96,96,.15);color:#e06060;border:1px solid #e0606040}
.badge-amber{background:rgba(240,192,64,.15);color:#f0c040;border:1px solid #f0c04040}
.badge-blue{background:rgba(96,160,224,.15);color:#60a0e0;border:1px solid #60a0e040}
.sev-low{background:rgba(82,196,120,.15);color:#52c478;border:1px solid #52c47840}
.sev-absent{background:rgba(96,160,224,.15);color:#60a0e0;border:1px solid #60a0e040}
.sev-mild{background:rgba(240,192,64,.15);color:#f0c040;border:1px solid #f0c04040}
.sev-mod{background:rgba(240,192,64,.15);color:#f0c040;border:1px solid #f0c04040}

/* ═══════════════ KUNDALI CHART ═══════════════ */
.kundali-wrap{display:flex;flex-direction:column;align-items:center;gap:12px;margin:32px 0}
.kundali-grid{display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(4,1fr);width:min(380px,100%);aspect-ratio:1;border:1.5px solid var(--gold);background:var(--bg2)}
.kc{border:1px solid var(--border);padding:8px 6px 6px;display:flex;flex-direction:column;gap:2px;background:rgba(10,10,28,0.8);transition:background .2s}
.kc:hover{background:rgba(201,168,76,0.06)}
.kc-lagna{border-color:var(--gold);background:rgba(201,168,76,0.08)!important}
.kc-center{grid-area:2/2/4/4;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(7,7,26,0.95)!important;gap:6px;border-color:var(--gold-dim)}
.kc-h{font-family:'Rajdhani',sans-serif;font-size:.6rem;color:var(--muted);line-height:1}
.kc-sign{font-size:.68rem;color:var(--muted);font-family:'Rajdhani',sans-serif;letter-spacing:.3px}
.kc-planets{font-size:.8rem;color:var(--gold);font-weight:600}
.kc-om{font-size:2.2rem;color:var(--gold);opacity:.5;line-height:1}
.kc-native{font-family:'Cinzel',serif;font-size:.72rem;color:var(--gold);text-align:center}
.kc-info{font-size:.6rem;color:var(--muted);text-align:center;font-family:'Rajdhani',sans-serif}
.chart-caption{font-size:.72rem;color:var(--muted);letter-spacing:1px;font-family:'Rajdhani',sans-serif;text-align:center}

/* ═══════════════ PLANET GRID ═══════════════ */
.planet-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin:32px 0}
.planet-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:18px;display:flex;gap:14px;transition:all .25s;cursor:default;position:relative;overflow:hidden}
.planet-card::before{content:'';position:absolute;inset:0;opacity:0;background:radial-gradient(circle at top-left,var(--gold-glow),transparent 60%);transition:opacity .3s}
.planet-card:hover{border-color:var(--gold);transform:translateY(-2px);box-shadow:0 8px 30px rgba(201,168,76,0.1)}
.planet-card:hover::before{opacity:1}
.cls-exalted{border-left:3px solid #52c478}
.cls-own{border-left:3px solid #52c478}
.cls-friendly{border-left:3px solid #60a0e0}
.cls-neutral{border-left:3px solid #8a7c68}
.cls-debil{border-left:3px solid #e06060}
.cls-combust{border-left:3px solid #f0c040}
.pc-sym{font-size:2rem;line-height:1;min-width:36px;text-align:center;margin-top:4px}
.pc-body{flex:1;display:flex;flex-direction:column;gap:4px}
.pc-name{font-family:'Cinzel',serif;font-size:.95rem;color:var(--text);font-weight:600}
.pc-sign{font-family:'Rajdhani',sans-serif;font-size:.8rem;color:var(--muted)}
.pc-deg{font-family:'Rajdhani',sans-serif;font-size:.72rem;color:var(--muted);margin-bottom:4px}
.pc-badge{margin:4px 0}
.pc-role{font-size:.7rem;color:var(--muted);border-top:1px solid var(--border);padding-top:4px;margin-top:4px}
.badge-own,.badge-exalted{background:rgba(82,196,120,.15);color:#52c478;border:1px solid #52c47840}
.badge-friendly,.badge-neutral{background:rgba(96,160,224,.15);color:#60a0e0;border:1px solid #60a0e040}
.badge-debil{background:rgba(224,96,96,.15);color:#e06060;border:1px solid #e0606040}
.badge-combust{background:rgba(240,192,64,.15);color:#f0c040;border:1px solid #f0c04040}

/* ═══════════════ ASHTAKVARGA ═══════════════ */
.ashtakvarga{margin:32px 0}
.avk-row{display:grid;grid-template-columns:140px 1fr 48px;align-items:center;gap:12px;margin-bottom:8px}
.avk-label{display:flex;gap:8px;align-items:center}
.avk-h{font-family:'Rajdhani',sans-serif;font-size:.7rem;color:var(--muted);min-width:24px}
.avk-sign{font-family:'Rajdhani',sans-serif;font-size:.8rem;color:var(--text);font-weight:600}
.avk-bar-wrap{height:20px;background:rgba(255,255,255,0.04);border-radius:10px;overflow:hidden;border:1px solid rgba(255,255,255,0.06)}
.avk-bar{height:100%;border-radius:10px;transition:width 1.2s cubic-bezier(.22,1,.36,1);position:relative}
.avk-bar::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.1))}
.avk-score{font-family:'Rajdhani',sans-serif;font-size:.82rem;color:var(--gold);font-weight:700;text-align:right;white-space:nowrap}

/* ═══════════════ DASHA TIMELINE ═══════════════ */
.dasha-section{margin:32px 0}
.vis-title{font-family:'Cinzel',serif;font-size:.95rem;color:var(--gold);letter-spacing:1px;margin-bottom:16px;text-transform:uppercase}
.dasha-timeline{display:flex;height:80px;border-radius:8px;overflow:hidden;border:1px solid var(--border);margin-bottom:24px}
.dt-seg{display:flex;flex-direction:column;justify-content:center;align-items:center;gap:2px;border-right:1px solid rgba(255,255,255,.05);padding:4px 2px;overflow:hidden;transition:all .2s;cursor:default;min-width:0}
.dt-seg:hover{filter:brightness(1.3)}
.dt-current{box-shadow:inset 0 0 0 1.5px var(--gold);animation:dasha-pulse 3s ease-in-out infinite}
@keyframes dasha-pulse{0%,100%{box-shadow:inset 0 0 0 1.5px rgba(201,168,76,0.5)}50%{box-shadow:inset 0 0 0 1.5px rgba(201,168,76,1),0 0 20px rgba(201,168,76,0.2)}}
.dt-sym{font-size:.9rem;line-height:1}
.dt-name{font-family:'Rajdhani',sans-serif;font-size:.6rem;letter-spacing:.5px;white-space:nowrap}
.dt-yrs{font-family:'Rajdhani',sans-serif;font-size:.55rem;color:var(--muted);white-space:nowrap}
.ad-table{width:100%;border-collapse:collapse;font-size:.88rem}
.ad-table th{background:rgba(201,168,76,0.1);color:var(--gold);padding:8px 12px;border:1px solid var(--border);font-family:'Rajdhani',sans-serif;letter-spacing:.5px}
.ad-table td{padding:8px 12px;border:1px solid rgba(201,168,76,0.08);vertical-align:top}
.ad-current td{background:rgba(201,168,76,0.06);color:var(--gold2)}
.ad-current td:first-child{font-weight:700}

/* ═══════════════ YOGA CARDS ═══════════════ */
.yoga-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;margin:24px 0}
.yoga-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px;transition:all .25s}
.yoga-card:hover{border-color:var(--gold);box-shadow:0 4px 20px rgba(201,168,76,0.1)}
.yc-header{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;margin-bottom:10px}
.yc-name{font-family:'Cinzel',serif;font-size:.88rem;color:var(--gold2);flex:1}
.yc-planet{font-family:'Rajdhani',sans-serif;font-size:.78rem;color:var(--muted);margin-bottom:4px}
.yc-timing{font-family:'Rajdhani',sans-serif;font-size:.72rem;color:var(--gold);opacity:.8;margin-bottom:10px}
.yc-desc{font-size:.9rem;color:var(--text);opacity:.85}

/* ═══════════════ DOSHA CARDS ═══════════════ */
.dosha-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;margin:24px 0}
.dosha-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px}
.dc-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.dc-name{font-family:'Cinzel',serif;font-size:.9rem;color:var(--gold2)}
.dc-detail{font-size:.9rem;color:var(--text);margin-bottom:12px}
.dc-remedy{font-size:.8rem;color:var(--muted);border-top:1px solid var(--border);padding-top:10px}

/* ═══════════════ LIFE DOMAIN CARDS ═══════════════ */
.ld-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;margin:24px 0}
.ld-card{background:var(--card);border:1px solid var(--border);border-top:3px solid;border-radius:10px;padding:24px;transition:all .25s}
.ld-card:hover{transform:translateY(-3px);box-shadow:0 8px 30px rgba(0,0,0,.4)}
.ld-icon{width:44px;height:44px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;margin-bottom:14px}
.ld-title{font-family:'Cinzel',serif;font-size:.95rem;font-weight:700;color:var(--gold2);margin-bottom:8px}
.ld-config{font-family:'Rajdhani',sans-serif;font-size:.75rem;color:var(--muted);margin-bottom:12px;line-height:1.6}
.ld-analysis{font-size:.88rem;color:var(--text);line-height:1.7}

/* ═══════════════ STRENGTH RANKING ═══════════════ */
.strength-rank{margin:24px 0}
.sr-row{display:grid;grid-template-columns:120px 1fr 36px 200px;align-items:center;gap:12px;margin-bottom:12px}
.sr-label{display:flex;gap:8px;align-items:center}
.sr-sym{font-size:1.1rem;min-width:24px}
.sr-name{font-family:'Rajdhani',sans-serif;font-size:.85rem;font-weight:600}
.sr-bar-wrap{height:22px;background:rgba(255,255,255,0.04);border-radius:11px;overflow:hidden;border:1px solid rgba(255,255,255,0.06)}
.sr-bar{height:100%;border-radius:11px;transition:width 1.4s cubic-bezier(.22,1,.36,1)}
.sr-pct{font-family:'Rajdhani',sans-serif;font-size:.85rem;font-weight:700;text-align:right}
.sr-reason{font-size:.78rem;color:var(--muted);font-family:'Rajdhani',sans-serif}

/* ═══════════════ REMEDY CARDS ═══════════════ */
.remedy-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px;margin:24px 0}
.rem-card{background:var(--card);border:1px solid var(--border);border-left:3px solid;border-radius:10px;padding:20px}
.rem-header{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.rem-sym{font-size:1.5rem}
.rem-name{font-family:'Cinzel',serif;font-size:.9rem;color:var(--gold2)}
.rem-header .badge{margin-left:auto}
.rem-rationale{font-family:'Rajdhani',sans-serif;font-size:.75rem;color:var(--muted);margin-bottom:10px;text-transform:uppercase;letter-spacing:.5px}
.rem-mantra{font-size:.88rem;color:var(--gold);background:rgba(201,168,76,0.06);padding:8px 12px;border-radius:6px;margin-bottom:8px}
.rem-behavioral{font-size:.85rem;color:var(--text)}

/* ═══════════════ APPENDIX ═══════════════ */
.appendix{max-width:1100px;margin:60px auto 0;padding:0 40px 60px}
.appendix h2{font-family:'Cinzel',serif;color:var(--gold);margin-bottom:20px;letter-spacing:2px}

/* ═══════════════ REVEAL ANIMATIONS ═══════════════ */
.reveal{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s ease}
.reveal.visible{opacity:1;transform:translateY(0)}

/* ═══════════════ RESPONSIVE ═══════════════ */
@media(max-width:768px){
  .sec-head,.sec-body{padding:0 16px}
  .sec-num{font-size:3rem}
  .hero-name{letter-spacing:2px}
  .hero-stats{gap:8px}
  .hs-pill{min-width:90px;padding:6px 12px}
  .nav-links{display:none}
  .sr-row{grid-template-columns:100px 1fr 36px}
  .sr-reason{display:none}
  .avk-row{grid-template-columns:120px 1fr 40px}
  .planet-grid,.yoga-grid,.ld-grid,.remedy-grid,.dosha-grid{grid-template-columns:1fr}
}
"""

# ──────────────────────────────────────────────────────────────────────────────
# 8.  JAVASCRIPT
# ──────────────────────────────────────────────────────────────────────────────
JS = """
// ─── Starfield ───
(function(){
  const c=document.getElementById('starsCanvas');
  const ctx=c.getContext('2d');
  let W,H,stars=[];
  function resize(){W=c.width=window.innerWidth;H=c.height=window.innerHeight}
  function mkStars(){stars=[];for(let i=0;i<180;i++)stars.push({x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.2+.2,a:Math.random(),da:(Math.random()-.5)*.003})}
  function draw(){
    ctx.clearRect(0,0,W,H);
    stars.forEach(s=>{s.a=Math.max(.05,Math.min(1,s.a+s.da));
      ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(255,255,240,${s.a})`;ctx.fill()});
    requestAnimationFrame(draw)}
  window.addEventListener('resize',()=>{resize();mkStars()});
  resize();mkStars();draw();
})();

// ─── Nav visibility (show after hero) ───
const nav=document.getElementById('topnav');
const hero=document.querySelector('.hero');
const heroObs=new IntersectionObserver(([e])=>{if(!e.isIntersecting)nav.classList.add('visible');else nav.classList.remove('visible')},{threshold:0.1});
heroObs.observe(hero);

// ─── Active nav section highlight ───
const secEls=document.querySelectorAll('.sec');
const navLinks=document.querySelectorAll('.nav-link');
const secObs=new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting){const id=e.target.id.replace('section-','');
    navLinks.forEach(l=>{l.classList.toggle('active',l.dataset.sec===id)})}})},{threshold:.2});
secEls.forEach(s=>secObs.observe(s));

// ─── Scroll reveal ───
const revEls=document.querySelectorAll('.reveal');
const revObs=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible')})},{threshold:.1});
revEls.forEach(el=>revObs.observe(el));

// ─── Animate bars on reveal ───
function animateBars(selector, attr){
  document.querySelectorAll(selector).forEach(bar=>{
    const obs=new IntersectionObserver(([e])=>{
      if(e.isIntersecting){bar.style.width=bar.dataset.pct+'%';obs.disconnect()}},{threshold:.1});
    obs.observe(bar)});
}
animateBars('.avk-bar');
animateBars('.sr-bar');

// ─── Language toggle ───
var LANG='en';
function toggleLang(){
  LANG=LANG==='en'?'hi':'en';
  const isHi=LANG==='hi';
  document.querySelectorAll('.lang-en').forEach(el=>el.style.display=isHi?'none':'');
  document.querySelectorAll('.lang-hi').forEach(el=>el.style.display=isHi?'':'none');
  document.getElementById('btnText').textContent=isHi?'English':'हिंदी';
  document.documentElement.lang=LANG;
  window.scrollTo({top:0,behavior:'smooth'});
}
"""

# ──────────────────────────────────────────────────────────────────────────────
# 9.  ASSEMBLE FULL HTML
# ──────────────────────────────────────────────────────────────────────────────
def assemble():
    # Section icons & titles
    icons = {1:"🔮",2:"🪐",3:"🏠",4:"✨",5:"⚠️",6:"⏳",7:"🌟",8:"📊",9:"🕉️",10:"🧬"}
    titles_en = {1:"Chart Foundation",2:"Planetary Deep Analysis",3:"House-Wise Analysis",
                 4:"Yogas — Validated Only",5:"Dosha Analysis",6:"Dasha System",
                 7:"Life Predictions — Time-Based",8:"Planetary Hierarchy",9:"Remedies",10:"Final Synthesis"}
    titles_hi = {1:"कुंडली आधार",2:"ग्रहों का गहन विश्लेषण",3:"भाव-वार विश्लेषण",
                 4:"योग — केवल प्रमाणित",5:"दोष विश्लेषण",6:"दशा प्रणाली",
                 7:"जीवन भविष्यवाणियाँ",8:"ग्रहों का पदानुक्रम",9:"उपाय",10:"अंतिम संश्लेषण"}

    # Visual component per section
    visuals = {
        1: f"""
<div class="two-col-hero reveal" style="display:grid;grid-template-columns:1fr 1fr;gap:32px;align-items:start;margin-bottom:32px">
  {kundali_chart_html()}
  <div class="lagna-card" style="background:var(--card);border:1px solid var(--border);border-radius:10px;padding:24px">
    <h3 style="font-family:Cinzel,serif;color:var(--gold);margin-bottom:12px;font-size:1rem">Lagna · मिथुन / Gemini</h3>
    <div style="display:grid;gap:10px">
      <div style="display:flex;justify-content:space-between;border-bottom:1px solid var(--border);padding-bottom:8px"><span style="color:var(--muted);font-family:Rajdhani,sans-serif;font-size:.8rem">Sign</span><span style="color:var(--gold);font-family:Rajdhani,sans-serif;font-weight:700">Gemini (Mithuna)</span></div>
      <div style="display:flex;justify-content:space-between;border-bottom:1px solid var(--border);padding-bottom:8px"><span style="color:var(--muted);font-family:Rajdhani,sans-serif;font-size:.8rem">Degree</span><span style="color:var(--gold);font-family:Rajdhani,sans-serif;font-weight:700">01°09′09″</span></div>
      <div style="display:flex;justify-content:space-between;border-bottom:1px solid var(--border);padding-bottom:8px"><span style="color:var(--muted);font-family:Rajdhani,sans-serif;font-size:.8rem">Nakshatra</span><span style="color:var(--gold);font-family:Rajdhani,sans-serif;font-weight:700">Mrigashira Pada 3</span></div>
      <div style="display:flex;justify-content:space-between;border-bottom:1px solid var(--border);padding-bottom:8px"><span style="color:var(--muted);font-family:Rajdhani,sans-serif;font-size:.8rem">Lagna Lord</span><span style="color:var(--gold);font-family:Rajdhani,sans-serif;font-weight:700">Mercury (Combust)</span></div>
      <div style="display:flex;justify-content:space-between;border-bottom:1px solid var(--border);padding-bottom:8px"><span style="color:var(--muted);font-family:Rajdhani,sans-serif;font-size:.8rem">Moon Sign</span><span style="color:var(--gold);font-family:Rajdhani,sans-serif;font-weight:700">Libra · Swati Pada 2</span></div>
      <div style="display:flex;justify-content:space-between;border-bottom:1px solid var(--border);padding-bottom:8px"><span style="color:var(--muted);font-family:Rajdhani,sans-serif;font-size:.8rem">Ayanamsa</span><span style="color:var(--gold);font-family:Rajdhani,sans-serif;font-weight:700">Lahiri 23°51′57″</span></div>
      <div style="display:flex;justify-content:space-between"><span style="color:var(--muted);font-family:Rajdhani,sans-serif;font-size:.8rem">Current Dasha</span><span style="color:var(--gold);font-family:Rajdhani,sans-serif;font-weight:700">♄ Saturn 2026–2045</span></div>
    </div>
  </div>
</div>
<h3 class="vis-title lang-en reveal" style="font-family:Cinzel,serif;font-size:.9rem;color:var(--gold);letter-spacing:2px;text-transform:uppercase;margin-bottom:16px">Planet Positions</h3>
<h3 class="vis-title lang-hi reveal" style="display:none;font-family:Noto Sans Devanagari,serif;font-size:.9rem;color:var(--gold);letter-spacing:1px;margin-bottom:16px">ग्रह स्थिति</h3>
<div class="reveal">{planet_cards_html()}</div>
<h3 class="vis-title lang-en reveal" style="font-family:Cinzel,serif;font-size:.9rem;color:var(--gold);letter-spacing:2px;text-transform:uppercase;margin:32px 0 16px">Ashtakvarga Score by House</h3>
<h3 class="vis-title lang-hi reveal" style="display:none;font-family:Noto Sans Devanagari,serif;font-size:.9rem;color:var(--gold);margin:32px 0 16px">भाव-वार अष्टकवर्ग स्कोर</h3>
<div class="reveal">{ashtakvarga_html()}</div>
""",
        4: f'<div class="reveal">{yoga_cards_html()}</div>',
        5: f'<div class="reveal">{dosha_cards_html()}</div>',
        6: f'<div class="reveal">{dasha_timeline_html()}</div>',
        7: f'<div class="reveal">{life_domain_cards_html()}</div>',
        8: f'<div class="reveal">{strength_bars_html()}</div>',
        9: f'<div class="reveal">{remedy_cards_html()}</div>',
    }

    sections_html = ""
    for n in range(1, 11):
        vis = visuals.get(n, "")
        c_en = SECS_EN.get(n, "")
        c_hi = SECS_HI.get(n, "")
        sections_html += section_wrap(
            n, icons[n], titles_en[n], titles_hi[n], vis,
            f'<div class="reveal">{c_en}</div>',
            f'<div class="reveal">{c_hi}</div>'
        )

    # Appendix
    app_en = SECS_EN.get('hdr','')
    appendix_html = f"""
<div class="appendix">
  <h2 class="lang-en">Appendix · Chart Data Summary</h2>
  <h2 class="lang-hi" style="display:none">परिशिष्ट · कुंडली डेटा सारांश</h2>
  <div class="prose lang-en">{SECS_EN.get('hdr','')}</div>
  <div class="prose lang-hi" style="display:none">{SECS_HI.get('hdr','')}</div>
</div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Abhishek Singh · Premium Vedic Kundali 2026</title>
<style>{CSS}</style>
</head>
<body>
{hero_html()}
{nav_html()}
{sections_html}
{appendix_html}
<footer style="text-align:center;padding:40px;color:var(--muted);font-family:Rajdhani,sans-serif;font-size:.75rem;letter-spacing:1px;border-top:1px solid var(--border)">
  ॐ · ABHISHEK SINGH · VEDIC KUNDALI 2026 · LAHIRI AYANAMSA · 11 CLASSICAL TEXTS
</footer>
<script>{JS}</script>
</body>
</html>"""

HTML = assemble()
with open("kundli_report_bilingual.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"Done → kundli_report_bilingual.html ({len(HTML):,} chars)")

/**
 * வ உ சி யின் உறவைத் தேடி — Translations
 * English and Tamil language support
 */

const TRANSLATIONS = {
    en: {
        // Navbar
        nav_home: "Home",
        nav_generate: "Generate Chart",
        nav_matching: "Matching",
        nav_about: "About",
        nav_contact: "Contact",
        nav_history: "History",
        nav_get_started: "Get Started",
        lang_toggle: "தமிழ்",

        // Index - Hero
        hero_badge: "Vedic Astrology · Lahiri Ayanamsa · Swiss Ephemeris",
        hero_title: "வ உ சி யின் உறவைத் தேடி",
        hero_subtitle: "Bride & Groom Horoscope Matching",
        hero_desc: "Generate precise Rasi & Navamsa charts, planetary positions, Nakshatra analysis, and 10-point Porutham compatibility — powered by authentic Sidereal calculations.",
        hero_cta1: "Generate Horoscope",
        hero_cta2: "Check Compatibility",

        // Index - Features
        feat_label: "WHAT WE OFFER",
        feat_title: "Comprehensive Vedic Astrology",
        feat_subtitle: "Every calculation you need, from birth charts to marriage matching",
        feat_rasi_title: "Rasi Chart",
        feat_rasi_desc: "South Indian style Rasi chart with accurate planetary placements using Swiss Ephemeris.",
        feat_navamsa_title: "Navamsa Chart",
        feat_navamsa_desc: "D-9 divisional chart calculated from each sign's 9-part division for deeper insight.",
        feat_nakshatra_title: "Nakshatra & Pada",
        feat_nakshatra_desc: "Complete Nakshatra identification with precise Pada calculation for both Bride and Groom.",
        feat_porutham_title: "10-Point Porutham",
        feat_porutham_desc: "Traditional Tamil marriage compatibility across Dina, Gana, Yoni, Rajju, Vedha, Nadi and more.",

        // Index - Steps
        steps_label: "HOW IT WORKS",
        steps_title: "Three Simple Steps",
        step1_title: "Enter Birth Details",
        step1_desc: "Input name, date, time and place of birth for both Bride and Groom.",
        step2_title: "Generate Charts",
        step2_desc: "Swiss Ephemeris computes planetary positions, Lagna, Nakshatra, Rasi and Navamsa charts.",
        step3_title: "View Compatibility",
        step3_desc: "Get your 10-point Porutham score with detailed analysis of each compatibility factor.",

        // Index - CTA
        cta_title: "Ready to Discover Your Stars?",
        cta_subtitle: "Generate your birth chart and find your perfect match today.",
        cta_btn: "Start Now — It's Free",

        // Footer
        footer_tagline: "Authentic Vedic Astrology powered by Swiss Ephemeris and Lahiri Ayanamsa.",
        footer_product: "Product",
        footer_birth_chart: "Birth Chart",
        footer_matching: "Matching",
        footer_rasi: "Rasi Chart",
        footer_navamsa: "Navamsa",
        footer_company: "Company",
        footer_about_us: "About Us",
        footer_contact: "Contact",
        footer_blog: "Blog",
        footer_legal: "Legal",
        footer_privacy: "Privacy Policy",
        footer_terms: "Terms of Service",
        footer_copy: "© 2026 வ உ சி யின் உறவைத் தேடி. All rights reserved.",

        // Form Page
        form_label: "GENERATE HOROSCOPE",
        form_title: "Enter Birth Details",
        form_subtitle: "Provide accurate birth details for precise chart calculations",
        bride_title: "Bride Details",
        groom_title: "Groom Details",
        label_name: "Full Name",
        label_dob: "Date of Birth",
        label_time: "Time of Birth",
        label_place: "Place of Birth",
        label_height: "Height (Optional)",
        label_weight: "Weight in kg (Optional)",
        label_salary: "Salary (Optional)",
        placeholder_bride_name: "Enter bride's name",
        placeholder_groom_name: "Enter groom's name",
        placeholder_place_bride: "e.g. Chennai, Tamil Nadu",
        placeholder_place_groom: "e.g. Madurai, Tamil Nadu",
        placeholder_height: "e.g. 5'8\"",
        placeholder_weight: "e.g. 65",
        placeholder_salary: "e.g. ₹5,00,000",
        btn_generate: "Generate Horoscope",
        form_note: "All calculations use Lahiri Ayanamsa (Sidereal Zodiac) via Swiss Ephemeris",
        loading_text: "Calculating planetary positions...",
        error_fill_all: "Please fill in all required fields for both Bride and Groom.",

        // Results Page
        results_label: "HOROSCOPE RESULTS",
        results_title: "Birth Chart",
        label_lagna: "Lagna (Ascendant)",
        label_nakshatra: "Nakshatra",
        label_moon_sign: "Moon Sign (Rasi)",
        label_sun_sign: "Sun Sign",
        chart_rasi_title: "South Indian Rasi Chart",
        chart_navamsa_title: "Navamsa Chart (D-9)",
        planet_section_title: "Planetary Positions",
        th_planet: "Planet",
        th_rasi: "Rasi (Sign)",
        th_degree: "Degree",
        th_nakshatra: "Nakshatra",
        th_pada: "Pada",
        btn_download_pdf: "Download PDF",
        btn_view_porutham: "View Porutham Results",
        btn_generate_another: "Generate Another",

        // Porutham Page
        porutham_label: "MARRIAGE COMPATIBILITY",
        porutham_title: "Porutham Analysis",
        porutham_score_label: "Porutham",
        porutham_detail_title: "Detailed Porutham Results",
        th_hash: "#",
        th_porutham: "Porutham",
        th_status: "Status",
        th_description: "Description",
        btn_download_results: "Download Results PDF",
        btn_view_charts: "View Charts",
        btn_new_matching: "New Matching",

        // Porutham verdicts
        verdict_excellent: "Excellent Match",
        verdict_good: "Good Match",
        verdict_average: "Average Match",
        verdict_poor: "Poor Match",
        verdict_excellent_desc: "This couple has outstanding compatibility. The union is considered very auspicious for a harmonious and blessed married life.",
        verdict_good_desc: "This couple has strong compatibility. The union is considered auspicious for a harmonious married life.",
        verdict_average_desc: "This couple has moderate compatibility. Further consultation with an astrologer is recommended.",
        verdict_poor_desc: "This couple has limited compatibility. Consulting with a qualified astrologer for remedies is strongly recommended.",
        badge_recommended: "Recommended for Marriage",
        badge_consult: "Consult Astrologer",
        match_yes: "✔ Match",
        match_no: "✖ No Match",

        // History Page
        history_label: "CUSTOMER RECORDS",
        history_title: "Match History",
        history_subtitle: "Browse previous compatibility analyses",
        th_id: "ID",
        th_bride: "Bride",
        th_groom: "Groom",
        th_date: "Date",
        th_score: "Score",
        th_actions: "Actions",
        btn_view: "View",
        no_records: "No records found. Generate a horoscope to create your first entry.",
        history_loading: "Loading records..."
    },

    ta: {
        // Navbar
        nav_home: "முகப்பு",
        nav_generate: "ஜாதகம் உருவாக்கு",
        nav_matching: "பொருத்தம்",
        nav_about: "பற்றி",
        nav_contact: "தொடர்பு",
        nav_history: "வரலாறு",
        nav_get_started: "தொடங்கு",
        lang_toggle: "English",

        // Index - Hero
        hero_badge: "வேத ஜோதிடம் · லஹிரி அயனாம்சம் · ஸ்விஸ் எபிமெரிஸ்",
        hero_title: "வ உ சி யின் உறவைத் தேடி",
        hero_subtitle: "மணமகள் & மணமகன் ஜாதக பொருத்தம்",
        hero_desc: "துல்லியமான ராசி & நவாம்ச கட்டங்கள், கிரக நிலைகள், நட்சத்திர பகுப்பாய்வு மற்றும் 10 பொருத்தங்கள் — உண்மையான சித்திரபக்ஷ கணக்கீடுகள்.",
        hero_cta1: "ஜாதகம் உருவாக்கு",
        hero_cta2: "பொருத்தம் பார்",

        // Index - Features
        feat_label: "நாங்கள் வழங்குவது",
        feat_title: "முழுமையான வேத ஜோதிடம்",
        feat_subtitle: "பிறப்பு ஜாதகம் முதல் திருமண பொருத்தம் வரை",
        feat_rasi_title: "ராசி கட்டம்",
        feat_rasi_desc: "ஸ்விஸ் எபிமெரிஸ் பயன்படுத்தி துல்லியமான கிரக நிலைகளுடன் தென்னிந்திய ராசி கட்டம்.",
        feat_navamsa_title: "நவாம்ச கட்டம்",
        feat_navamsa_desc: "ஆழமான நுண்ணறிவுக்காக ஒவ்வொரு ராசியின் 9 பகுதிகளிலிருந்து கணக்கிடப்பட்ட D-9 கட்டம்.",
        feat_nakshatra_title: "நட்சத்திரம் & பாதம்",
        feat_nakshatra_desc: "மணமகள் மற்றும் மணமகன் இருவருக்கும் துல்லியமான நட்சத்திர & பாத கணக்கீடு.",
        feat_porutham_title: "பத்து பொருத்தம்",
        feat_porutham_desc: "தினம், கணம், யோனி, ராஜ்ஜு, வேதை, நாடி மற்றும் பிற பொருத்தங்கள்.",

        // Index - Steps
        steps_label: "எவ்வாறு செயல்படுகிறது",
        steps_title: "மூன்று எளிய படிகள்",
        step1_title: "பிறப்பு விவரங்களை உள்ளிடவும்",
        step1_desc: "மணமகள் மற்றும் மணமகன் இருவரின் பெயர், தேதி, நேரம் மற்றும் இடம் உள்ளிடவும்.",
        step2_title: "ஜாதகம் உருவாக்கு",
        step2_desc: "கிரக நிலைகள், லக்னம், நட்சத்திரம், ராசி மற்றும் நவாம்ச கட்டங்கள் கணக்கிடப்படும்.",
        step3_title: "பொருத்தம் காண்க",
        step3_desc: "ஒவ்வொரு பொருத்த காரணியின் விரிவான பகுப்பாய்வுடன் 10 பொருத்த மதிப்பெண் பெறுங்கள்.",

        // Index - CTA
        cta_title: "உங்கள் நட்சத்திரங்களை கண்டறிய தயாரா?",
        cta_subtitle: "உங்கள் ஜாதகத்தை உருவாக்கி, சரியான பொருத்தத்தை இன்றே கண்டறியுங்கள்.",
        cta_btn: "இப்போது தொடங்கு — இலவசம்",

        // Footer
        footer_tagline: "ஸ்விஸ் எபிமெரிஸ் மற்றும் லஹிரி அயனாம்சத்தால் இயக்கப்படும் உண்மையான வேத ஜோதிடம்.",
        footer_product: "பொருள்கள்",
        footer_birth_chart: "பிறப்பு ஜாதகம்",
        footer_matching: "பொருத்தம்",
        footer_rasi: "ராசி கட்டம்",
        footer_navamsa: "நவாம்சம்",
        footer_company: "நிறுவனம்",
        footer_about_us: "எங்களைப் பற்றி",
        footer_contact: "தொடர்பு",
        footer_blog: "வலைப்பதிவு",
        footer_legal: "சட்டம்",
        footer_privacy: "தனியுரிமை கொள்கை",
        footer_terms: "சேவை விதிமுறைகள்",
        footer_copy: "© 2026 வ உ சி யின் உறவைத் தேடி. அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை.",

        // Form Page
        form_label: "ஜாதகம் உருவாக்கு",
        form_title: "பிறப்பு விவரங்களை உள்ளிடவும்",
        form_subtitle: "துல்லியமான ஜாதக கணக்கீடுகளுக்கு சரியான பிறப்பு விவரங்களை வழங்கவும்",
        bride_title: "மணமகள் விவரங்கள்",
        groom_title: "மணமகன் விவரங்கள்",
        label_name: "முழுப் பெயர்",
        label_dob: "பிறந்த தேதி",
        label_time: "பிறந்த நேரம்",
        label_place: "பிறந்த இடம்",
        label_height: "உயரம் (விருப்பத்திற்கு)",
        label_weight: "எடை கிலோவில் (விருப்பத்திற்கு)",
        label_salary: "சம்பளம் (விருப்பத்திற்கு)",
        placeholder_bride_name: "மணமகளின் பெயரை உள்ளிடவும்",
        placeholder_groom_name: "மணமகனின் பெயரை உள்ளிடவும்",
        placeholder_place_bride: "எ.கா. சென்னை, தமிழ்நாடு",
        placeholder_place_groom: "எ.கா. மதுரை, தமிழ்நாடு",
        placeholder_height: "எ.கா. 5'8\"",
        placeholder_weight: "எ.கா. 65",
        placeholder_salary: "எ.கா. ₹5,00,000",
        btn_generate: "ஜாதகம் உருவாக்கு",
        form_note: "அனைத்து கணக்கீடுகளும் லஹிரி அயனாம்சத்தை (சைடீரியல் ராசி) பயன்படுத்துகின்றன",
        loading_text: "கிரக நிலைகள் கணக்கிடப்படுகின்றன...",
        error_fill_all: "மணமகள் மற்றும் மணமகன் இருவரின் அனைத்து கட்டாய புலங்களையும் நிரப்பவும்.",

        // Results Page
        results_label: "ஜாதக முடிவுகள்",
        results_title: "பிறப்பு ஜாதகம்",
        label_lagna: "லக்னம் (உதயராசி)",
        label_nakshatra: "நட்சத்திரம்",
        label_moon_sign: "சந்திர ராசி",
        label_sun_sign: "சூரிய ராசி",
        chart_rasi_title: "தென்னிந்திய ராசி கட்டம்",
        chart_navamsa_title: "நவாம்ச கட்டம் (D-9)",
        planet_section_title: "கிரக நிலைகள்",
        th_planet: "கிரகம்",
        th_rasi: "ராசி",
        th_degree: "பாகை",
        th_nakshatra: "நட்சத்திரம்",
        th_pada: "பாதம்",
        btn_download_pdf: "PDF பதிவிறக்கம்",
        btn_view_porutham: "பொருத்த முடிவுகளைக் காண்க",
        btn_generate_another: "புதியது உருவாக்கு",

        // Porutham Page
        porutham_label: "திருமணப் பொருத்தம்",
        porutham_title: "பொருத்த பகுப்பாய்வு",
        porutham_score_label: "பொருத்தம்",
        porutham_detail_title: "விரிவான பொருத்த முடிவுகள்",
        th_hash: "#",
        th_porutham: "பொருத்தம்",
        th_status: "நிலை",
        th_description: "விளக்கம்",
        btn_download_results: "முடிவுகள் PDF பதிவிறக்கம்",
        btn_view_charts: "ஜாதகங்களைக் காண்க",
        btn_new_matching: "புதிய பொருத்தம்",

        // Porutham verdicts
        verdict_excellent: "சிறப்பான பொருத்தம்",
        verdict_good: "நல்ல பொருத்தம்",
        verdict_average: "சராசரி பொருத்தம்",
        verdict_poor: "குறைவான பொருத்தம்",
        verdict_excellent_desc: "இந்த ஜோடிக்கு சிறப்பான பொருத்தம் உள்ளது. இந்த இணைவு மிகவும் சுபமான திருமண வாழ்க்கைக்கு ஏற்றது.",
        verdict_good_desc: "இந்த ஜோடிக்கு நல்ல பொருத்தம் உள்ளது. இந்த இணைவு சுபமான திருமண வாழ்க்கைக்கு ஏற்றது.",
        verdict_average_desc: "இந்த ஜோடிக்கு சராசரி பொருத்தம் உள்ளது. ஜோதிடரிடம் ஆலோசிக்க பரிந்துரைக்கப்படுகிறது.",
        verdict_poor_desc: "இந்த ஜோடிக்கு குறைவான பொருத்தம் உள்ளது. பரிகாரங்களுக்கு தகுதியான ஜோதிடரிடம் ஆலோசிக்கவும்.",
        badge_recommended: "திருமணத்திற்கு பரிந்துரைக்கப்படுகிறது",
        badge_consult: "ஜோதிடரை அணுகவும்",
        match_yes: "✔ பொருந்தும்",
        match_no: "✖ பொருந்தாது",

        // History Page
        history_label: "வாடிக்கையாளர் பதிவுகள்",
        history_title: "பொருத்த வரலாறு",
        history_subtitle: "முந்தைய பொருத்த பகுப்பாய்வுகளை உலாவுக",
        th_id: "எண்",
        th_bride: "மணமகள்",
        th_groom: "மணமகன்",
        th_date: "தேதி",
        th_score: "மதிப்பெண்",
        th_actions: "செயல்கள்",
        btn_view: "காண்க",
        no_records: "பதிவுகள் இல்லை. உங்கள் முதல் பதிவை உருவாக்க ஜாதகம் உருவாக்கவும்.",
        history_loading: "பதிவுகள் ஏற்றப்படுகின்றன..."
    }
};

// ─── Language Engine ────────────────────────────────────────────────────────

let currentLang = localStorage.getItem('thirukanidham_lang') || 'en';

function t(key) {
    return TRANSLATIONS[currentLang]?.[key] || TRANSLATIONS['en']?.[key] || key;
}

function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('thirukanidham_lang', lang);
    applyTranslations();
}

function toggleLanguage() {
    setLanguage(currentLang === 'en' ? 'ta' : 'en');
}

function applyTranslations() {
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (key) el.textContent = t(key);
    });

    // Update all elements with data-i18n-placeholder
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (key) el.placeholder = t(key);
    });

    // Update lang toggle button text
    const toggleBtn = document.getElementById('langToggle');
    if (toggleBtn) toggleBtn.textContent = t('lang_toggle');

    // Update html lang attribute
    document.documentElement.lang = currentLang === 'ta' ? 'ta' : 'en';
}

function initLanguage() {
    applyTranslations();
}

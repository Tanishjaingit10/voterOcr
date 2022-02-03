cities = [
    'अजमेर',
    'अलवर',
    'उदयपुर',
    'करौली',
    'कोटा',
    'गंगानगर',
    'चुरु',
    'चित्तौड़गढ़',
    'जयपुर',
    'जैसलमेर',
    'जालौर',
    'जोधपुर',
    'झुँझुनू',
    'झालावाड़',
    'टौंक',
    'डूंगरपूर',
    'दौसा',
    'धौलपुर',
    'नागोर',
    'प्रतापगढ़',
    'पाली',
    'बूँदी',
    'बाड़मेर',
    'बाराँ',
    'बांसवाड़ा',
    'बीकानेर',
    'भरतपुर',
    'भीलवाड़ा',
    'राजसमंद',
    'सवाईमाधोपुर',
    'सिरोही',
    'सीकर',
    'हनुमानगढ़'
]

# a = {"ajamer": ["kishanagadh", "pushkar", "ajamer uttar", "ajamer dakshin", "naseeraabaad", "byaavar", "masooda", "kekadee"], "alavar": ["tijaara", "kishanagadhabaas", "mundaavar", "baharod", "baanasoor", "thaanaagaajee", "alavar graameen", "alavar shaharee", "raamagadh", "raajagadh-lakshmanagadh", "kathoomar"], "udayapur": ["gogunda", "jhaadol", "kheravaada", "udayapur graameen", "udayapur", "maavalee", "vallabhanagar", "salumbar"], "karaulee": ["todaabheem", "hindaun", "karaulee", "sapotara"], "kota": ["peepalada", "saagaud", "kota uttar", "kota dakshin", "laadapura", "raamaganjamandee"], "gangaanagar": ["saadulashahar", "gangaanagar", "karanapur", "sooratagadh", "raayasinhanagar", "anoopagadh"], "churu": ["saadulapur", "taaraanagar", "saradaarashahar", "chooru", "ratanagadh", "sujaanagadh"], "chittaudagadh": ["kapaasan", "begoon", "chittodagadh", "nimbaaheda", "badee saadadee"], "jayapur": ["kotapootalee", null, "shaahapura", "chaumoo", "phulera", "doodoo", "jhotavaada", "aamer", "jamavaaraamagadh", "havaamahal", "vidyaadharanagar", "sivil laeen", "kishanapol", "aadarsh nagar", "maalaveey nagar", "saangaaner", null, "bassee", "chaakasoo"], "jaisalamer": ["jaisalamer", "pokaran"], "jaalaur": [null, "jaalaur", "bheenamaal", "saanchor", "raaneevaada"], "jodhapur": ["phalaudee", null, "sheragadh", "osiyaan", "bhopaalagadh", "saradaarapura", "jodhapur", "soorasaagar", "loonee", "bilaada"], "null": ["pilaanee", "soorajagadh", "jhunjhunoo", "mandaava", "navalagadh", "udayapuravaatee", "khetadee"], "jhaalaavaad": ["dag", "jhaalaraapaatan", "khaanapur", "manoharathaana"], "taunk": ["maalapura", "nivaee", "tonk", "devalee-uniyaara"], "doongarapur": ["doongarapur", "aasapur", "saagavaada", "chauraasee"], "dausa": [null, "mahua", "sikaraay", "dausa", "laalasot"], "dhaulapur": ["basedee", "baadee", "dhaulapur", "raajaakheda"], "naagor": ["laadanoon", "deedavaana", "jaayal", "naagaur", "kheenvasar", "medata", "degaana", "makaraana", "parabatasar", "naavaan"], "prataapagadh": ["dhariyaavaad", "prataapagadh"], "paalee": ["jaitaaran", "saujat", "paalee", "maaravaad jakshan", "baalee", "sumerapur"], "boondee": [null, "keshoraayapaatan", "boondee"], "baadamer": ["shiv", "baadamer", "baayatoo", "pachapadara", "sivaana", "gudhaamalaanee", "chauhatan"], "baaraan": ["anta", "kishanaganj", "baaraan-ataru", "chhabada"], "baansavaada": ["ghaatol", "gadhee", "baansavaada", "baageedaura", "kushalagadh"], "beekaaner": ["khaajoovaala", "beekaaner pashchim", "beekaaner poorv", "kolaayat", "loonakaranasar", "doongaragadh", "nokha"], "bharatapur": ["kaamaan", "nagar", "deeg-kumher", "bharatapur", "nadabee", "bair", "bayaana"], "bheelavaada": ["aaseend", "maandal", "sahaada", "bheelavaada", "shaahapura", "jahaajapur", "maandalagadh"], "raajasamand": ["bheem", "kumbhalagadh", "raajasamand", "naathadvaara"], "savaeemaadhopur": ["gangaapur", "baamanavaas", "savaeemaadhopur", "khandaar"], "sirohee": ["sirohee", "pindavaada aaboo", "revadar"], "seekar": ["phatehapur", "lakshmanagadh", "dhod (a.ja.)", "seekar", "daantaaraamagadh", "khandela", "neem ka thaana", "shreemaadhopur"], "hanumaanagadh": ["sangariya", "hanumaanagadh", "peeleebanga", "nohar", "bhaadara"]}
list = {'अजमेर': ['किशनगढ़', 'पुष्कर', 'अजमेर उत्तर', 'अजमेर दक्षिण', 'नसीराबाद', 'ब्यावर', 'मसूदा', 'केकडी'], 'अलवर': ['तिजारा', 'किशनगढ़बास', 'मुण्डावर', 'बहरोड़', 'बानसूर', 'थानागाजी', 'अलवर ग्रामीण', 'अलवर शहरी', 'रामगढ़', 'राजगढ़-लक्ष्मणगढ़', 'कठूमर'], 'उदयपुर': ['गोगुन्दा', 'झाडोल', 'खेरवाड़ा', 'उदयपुर ग्रामीण', 'उदयपुर', 'मावली', 'वल्लभनगर', 'सलुम्बर'], 'करौली': ['टोडाभीम', 'हिण्डौन', 'करौली', 'सपोटरा'], 'कोटा': ['पीपलदा', 'सागौद', 'कोटा उत्तर', 'कोटा दक्षिण', 'लाडपुरा', 'रामगंजमण्डी'], 'गंगानगर': ['सादुलशहर', 'गंगानगर', 'करनपुर', 'सूरतगढ़', 'रायसिंहनगर', 'अनूपगढ़'], 'चुरु': ['सादुलपुर', 'तारानगर', 'सरदारशहर', 'चूरु', 'रतनगढ़', 'सुजानगढ़'], 'चित्तौड़गढ़': ['कपासन', 'बेगूं', 'चित्तोड़गढ़', 'निम्बाहेड़ा', 'बड़ी सादड़ी'], 'जयपुर': ['कोटपूतली', 'विराटनगर', 'शाहपुरा', 'चौमू', 'फुलेरा', 'दूदू', 'झोटवाड़ा', 'आमेर', 'जमवारामगढ़', 'हवामहल', 'विद्याधरनगर', 'सिविल लाईन', 'किशनपोल', 'आदर्श नगर', 'मालवीय नगर', 'सांगानेर', 'बगरु', 'बस्सी', 'चाकसू'], 'जैसलमेर': ['जैसलमेर', 'पोकरण'], 'जालौर': ['आहौर', 'जालौर', 'भीनमाल', 'सांचोर', 'रानीवाड़ा'], 'जोधपुर': ['फलौदी', 'लोहावत', 'शेरगढ़', 'ओसियां', 'भोपालगढ़', 'सरदारपुरा', 'जोधपुर', 'सूरसागर', 'लूनी', 'बिलाड़ा'], 'झुँझुनू': ['पिलानी', 'सूरजगढ़', 'झुन्झुनू', 'मण्डावा', 'नवलगढ़', 'उदयपुरवाटी', 'खेतड़ी'], 'झालावाड़': ['डग', 'झालरापाटन', 'खानपुर', 'मनोहरथाना'], 'टौंक': ['मालपुरा', 'निवाई', 'टोंक', 'देवली-उनियारा'], 'डूंगरपूर': ['डूंगरपुर', 'आसपुर', 'सागवाड़ा', 'चौरासी'], 'दौसा': ['बाँदीकुई', 'महुआ', 'सिकराय', 'दौसा', 'लालसोट'], 'धौलपुर': ['बसेडी', 'बाड़ी', 'धौलपुर', 'राजाखेड़ा'], 'नागोर': ['लाडनूं', 'डीडवाना', 'जायल', 'नागौर', 'खींवसर', 'मेड़ता', 'डेगाना', 'मकराना', 'परबतसर', 'नावां'], 'प्रतापगढ़': ['धरियावाद', 'प्रतापगढ़'], 'पाली': ['जैतारण', 'सौजत', 'पाली', 'मारवाड़ जक्शन', 'बाली', 'सुमेरपुर'], 'बूँदी': ['हिन्डौली', 'केशोरायपाटन', 'बून्दी'], 'बाड़मेर': ['शिव', 'बाड़मेर', 'बायतू', 'पचपदरा', 'सिवाना', 'गुढ़ामलानी', 'चौहटन'], 'बाराँ': ['अन्ता', 'किशनगंज', 'बारां-अटरु', 'छबड़ा'], 'बांसवाड़ा': ['घाटोल', 'गढ़ी', 'बांसवाड़ा', 'बागीदौरा', 'कुशलगढ़'], 'बीकानेर': ['खाजूवाला', 'बीकानेर पश्चिम', 'बीकानेर पूर्व', 'कोलायत', 'लूणकरणसर', 'डूँगरगढ़', 'नोखा'], 'भरतपुर': ['कामां', 'नगर', 'डीग-कुम्हेर', 'भरतपुर', 'नदबई', 'बैर', 'बयाना'], 'भीलवाड़ा': ['आसीन्द', 'माण्डल', 'सहाडा', 'भीलवाड़ा', 'शाहपुरा', 'जहाजपुर', 'माण्डलगढ़'], 'राजसमंद': ['भीम', 'कुम्भलगढ़', 'राजसमन्द', 'नाथद्वारा'], 'सवाईमाधोपुर': ['गंगापुर', 'बामनवास', 'सवाईमाधोपुर', 'खण्डार'], 'सिरोही': ['सिरोही', 'पिंडवाड़ा आबू', 'रेवदर'], 'सीकर': ['फतेहपुर', 'लक्ष्मणगढ़', 'धोद (अ.जा.)', 'सीकर', 'दांतारामगढ़', 'खण्डेला', 'नीम का थाना', 'श्रीमाधोपुर'], 'हनुमानगढ़': ['संगरिया', 'हनुमानगढ़', 'पीलीबंगा', 'नोहर', 'भादरा']}

"""
from google_trans_new import google_translator
translator = google_translator()
translator.translate("अजमेर", lang_tgt="en", lang_src="hi", pronounce=True)[1]


from electoralroll.static__.city_and_assembly_data import a
from electoralroll.models import *
for k, v in a.items():
    c = City.objects.create(name=k)
    for o in v:
        LegislativeAssembly.objects.create(city=c, assembly_name=o)


"""
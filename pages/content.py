"""What the Menu, FAQ and Gallery pages show.

Dish names stay in Italian; everything wrapped in _() is translated (locale/es).
"""
from django.utils.translation import gettext_lazy as _

IMG = "https://res.cloudinary.com/diktmeiui/image/upload/"

MENU = [
    {"id": "entrees", "name": _("Entrées"), "dishes": [
        ("Bruschetta Classica", _("Toasted rustic bread with marinated tomatoes, basil, and a drizzle of extra virgin olive oil."), IMG + "v1759422796/Bruschetta_Classica_ta4dr1.png"),
        ("Carpaccio di Manzo", _("Thinly sliced beef tenderloin with arugula, parmesan shavings, and truffle oil."), IMG + "v1759422887/Carpaccio_di_Manzo_s0rcwz.png"),
        ("Arancini Siciliani", _("Golden risotto croquettes filled with mozzarella and herbs."), IMG + "v1759423160/Arancini_Siciliani_mau34k.png"),
        ("Caprese Elegante", _("Fresh buffalo mozzarella layered with heirloom tomatoes and basil, finished with balsamic pearls."), IMG + "v1759423190/Caprese_Elegante_jthe6u.png"),
        ("Antipasto Aurea", _("A curated selection of Italian cured meats, artisanal cheeses, and olives."), IMG + "v1759422977/Antipasto_Aurea_ra5isn.png"),
        ("Frittura di Calamari", _("Lightly fried calamari with lemon aioli and fresh herbs."), IMG + "v1759422941/Frittura_di_Calamari_s3ly8j.png"),
    ]},
    {"id": "mains", "name": _("Mains"), "dishes": [
        ("Tagliatelle Bolognese", _("Fresh ribbon pasta with a slow-cooked beef ragù."), IMG + "v1759425649/Tagliatelle_Bolognese_yyf6fr.png"),
        ("Risotto al Tartufo", _("Creamy arborio rice infused with black truffle and parmesan."), IMG + "v1759425551/Risotto_al_Tartufo_byixjj.png"),
        ("Sea Bass alla Griglia", _("Grilled Mediterranean sea bass with lemon butter and roasted fennel."), IMG + "v1759425607/SeaBassallaGriglia_d5f81x.png"),
        ("Pollo alla Parmigiana", _("Breaded chicken breast with mozzarella, parmesan, and a light tomato sauce."), IMG + "v1759425475/Pollo_alla_Parmigiana_u1s6mc.png"),
        ("Osso Buco Milanese", _("Braised veal shank with saffron risotto and gremolata."), IMG + "v1759425439/OssoBucoMilanese_retdqq.png"),
        ("Linguine ai Frutti di Mare", _("Pasta with clams, mussels, shrimp, and calamari in a white wine sauce."), IMG + "v1759425400/LinguineaiFruttidiMare_u7blwx.png"),
    ]},
    {"id": "desserts", "name": _("Desserts"), "dishes": [
        ("Tiramisu Classico", _("Layers of espresso-soaked ladyfingers with mascarpone cream and cocoa."), IMG + "v1759426231/Tiramisu_Classico_fgmfy5.png"),
        ("Panna Cotta alla Vaniglia", _("Silky vanilla cream topped with a wild berry coulis."), IMG + "v1759426192/PannaCottaallaVaniglia_epxxqd.png"),
        ("Cannoli Siciliani", _("Crisp pastry shells filled with ricotta cream and candied orange."), IMG + "v1759426080/CannoliSiciliani_n7d9fk.png"),
        ("Affogato al Caffè", _("Vanilla gelato drowned in hot espresso."), IMG + "v1759426041/AffogatoalCaff%C3%A8_zkmf0r.png"),
        ("Torta Caprese", _("Flourless chocolate and almond cake with powdered sugar."), IMG + "v1759426272/TortaCaprese_p0lltz.png"),
        ("Gelato Artigianale", _("Chef’s selection of artisanal Italian gelato flavors."), IMG + "v1759426153/GelatoArtigianale_zmmweh.png"),
    ]},
    {"id": "extras", "name": _("Extras"), "dishes": [
        ("Focaccia al Rosmarino", _("Warm rosemary focaccia with olive oil."), IMG + "v1759427474/FocacciaalRosmarino_udanyy.png"),
        ("Patate al Tartufo", _("Truffle-dusted potato wedges."), IMG + "v1759427889/PatatealTartufo_ypk6oj.png"),
        ("Verdure Grigliate", _("Grilled seasonal vegetables."), IMG + "v1759427808/VerdureGrigliate_ryr30x.png"),
        ("Polenta Cremosa", _("Creamy parmesan polenta."), IMG + "v1759427608/PolentaCremosa_hac3wz.png"),
        ("Funghi Trifolati", _("Sautéed mushrooms with garlic, parsley, and olive oil."), IMG + "v1759427748/FunghiTrifolati_qbrwak.png"),
        ("Pane della Casa", _("Assorted house bread with dipping oils."), IMG + "v1759427522/PanedellaCasa_cbzajc.png"),
    ]},
    {"id": "drinks", "name": _("Drinks"), "dishes": [
        ("Prosecco di Valdobbiadene", _("Sparkling, crisp, refreshing."), IMG + "v1759428874/Prosecco_di_Valdobbiadene_amtugp.png"),
        ("Pinot Grigio delle Venezie", _("Classic light Italian white."), IMG + "v1759428831/Pinot_Grigio_delle_Venezie_u4obbs.png"),
        ("Chianti Classico Riserva", _("Robust Tuscan red."), IMG + "v1759428746/Chianti_Classico_Riserva_sdfqij.png"),
        ("Barolo DOCG", _("The “King of Wines” from Piedmont."), IMG + "v1759428704/Barolo_DOCG_vont2k.png"),
        ("Amaro Averna", _("Traditional Sicilian digestif."), IMG + "v1759428644/Amaro_Averna_uhgmwr.png"),
        ("Limoncello di Sorrento", _("Iconic lemon liqueur from the Amalfi coast."), IMG + "v1759428789/Limoncello_di_Sorrento_cice3s.png"),
    ]},
]

FAQ = [
    (_("What type of cuisine do you serve?"),
     _("We specialise in authentic Italian cuisine — handmade pastas, wood-fired pizzas, and fresh Mediterranean-inspired dishes.")),
    (_("Do you have vegetarian or vegan options?"),
     _("Yes! We offer a variety of vegetarian and vegan dishes prepared with fresh seasonal ingredients.")),
    (_("How can I book a table?"),
     _("You can book online through our website or call us directly. Walk-ins are welcome too!")),
    (_("Do you offer delivery or takeaway?"),
     _("Yes! We offer both delivery and takeaway options. You can order online or by phone.")),
    (_("Do you accommodate food allergies?"),
     _("Absolutely! Please inform our staff about any allergies, and we’ll do our best to provide safe and delicious options.")),
    (_("What are your opening hours?"),
     _("We are open Monday to Sunday, from 12:00 to 22:00.")),
    (_("Do you cater for events?"),
     _("Yes! We provide catering services for private parties, weddings, and corporate events. Contact us for more details.")),
    (_("Do you have parking available?"),
     _("Yes, we have free parking available for all our guests.")),
]

GALLERY = [
    IMG + "v1759277224/restaurant_inside3_xlelue.jpg",
    IMG + "v1759277223/restaurant_inside2_ncelao.jpg",
    IMG + "v1759277224/restaurant_inside4_n07bsn.jpg",
    IMG + "v1759277224/restaurant_inside6_qgpggz.jpg",
    IMG + "v1759277224/restaurant_inside5_xfeef1.jpg",
    IMG + "v1759339315/restaurant_inside8_agldst.jpg",
]

# Shown on the home page
SIGNATURE = ["Risotto al Tartufo", "Tagliatelle Bolognese", "Tiramisu Classico"]

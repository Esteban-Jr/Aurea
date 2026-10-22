"""What the Menu, FAQ and Gallery pages show.

Dish names stay in Italian; everything wrapped in _() is translated (locale/es).
"""
import re

from django.utils.translation import gettext_lazy as _

IMG = "https://res.cloudinary.com/diktmeiui/image/upload/"


# Dietary tags and the 14 UK allergens. Allergen info is a guide; guests are told to check with staff.
TAGS = {"v": _("Vegetarian"), "vg": _("Vegan"), "gf": _("Gluten-free")}
ALLERGENS = {
    "gluten": _("Gluten"), "crustaceans": _("Crustaceans"), "eggs": _("Eggs"), "fish": _("Fish"),
    "peanuts": _("Peanuts"), "soya": _("Soya"), "milk": _("Milk"), "nuts": _("Nuts"),
    "celery": _("Celery"), "mustard": _("Mustard"), "sesame": _("Sesame"), "sulphites": _("Sulphites"),
    "lupin": _("Lupin"), "molluscs": _("Molluscs"),
}


def dish(name, description, image, story, tags="", allergens=""):
    return {
        "slug": re.sub(r"[^a-z]+", "-", name.lower().replace("è", "e")).strip("-"),
        "name": name,
        "description": description,
        "image": IMG + image,
        "story": story,
        "tags": [TAGS[t] for t in tags.split()],
        "allergens": [ALLERGENS[a] for a in allergens.split()],
    }

MENU = [
    {"id": "entrees", "name": _("Entrées"), "dishes": [
        dish("Bruschetta Classica", _("Toasted rustic bread with marinated tomatoes, basil, and a drizzle of extra virgin olive oil."), "v1759422796/Bruschetta_Classica_ta4dr1.png",
             _("Our bread is baked every morning, grilled over the flame and rubbed with garlic, then topped with ripe tomatoes marinated in olive oil and torn basil. A Tuscan farmhouse classic."),
             tags="v vg", allergens="gluten"),
        dish("Carpaccio di Manzo", _("Thinly sliced beef tenderloin with arugula, parmesan shavings, and truffle oil."), "v1759422887/Carpaccio_di_Manzo_s0rcwz.png",
             _("Prime beef tenderloin, chilled and sliced paper-thin, dressed with lemon, peppery rocket, aged Parmigiano Reggiano and a few drops of black truffle oil. The dish was created in Venice in 1950."),
             tags="gf", allergens="milk"),
        dish("Arancini Siciliani", _("Golden risotto croquettes filled with mozzarella and herbs."), "v1759423160/Arancini_Siciliani_mau34k.png",
             _("Sicily’s favourite street food: saffron risotto shaped by hand around a heart of melting mozzarella, rolled in breadcrumbs and fried until golden."),
             tags="v", allergens="gluten eggs milk"),
        dish("Caprese Elegante", _("Fresh buffalo mozzarella layered with heirloom tomatoes and basil, finished with balsamic pearls."), "v1759423190/Caprese_Elegante_jthe6u.png",
             _("A tribute to the island of Capri in the colours of the Italian flag: creamy buffalo mozzarella from Campania, heirloom tomatoes and basil, finished with pearls of aged balsamic from Modena."),
             tags="v gf", allergens="milk sulphites"),
        dish("Antipasto Aurea", _("A curated selection of Italian cured meats, artisanal cheeses, and olives."), "v1759422977/Antipasto_Aurea_ra5isn.png",
             _("A sharing board for the table: prosciutto di Parma, salame and mortadella, aged pecorino and gorgonzola, marinated olives and crisp grissini."),
             tags="", allergens="gluten milk sulphites"),
        dish("Frittura di Calamari", _("Lightly fried calamari with lemon aioli and fresh herbs."), "v1759422941/Frittura_di_Calamari_s3ly8j.png",
             _("Tender squid dusted in seasoned flour and fried in seconds so it stays light and crisp, served the Neapolitan way with lemon and a garlicky lemon aioli."),
             tags="", allergens="gluten eggs molluscs"),
    ]},
    {"id": "mains", "name": _("Mains"), "dishes": [
        dish("Tagliatelle Bolognese", _("Fresh ribbon pasta with a slow-cooked beef ragù."), "v1759425649/Tagliatelle_Bolognese_yyf6fr.png",
             _("Our ragù simmers for four hours with beef, pork, vegetables, red wine and a splash of milk, just like in Bologna. Tossed with egg tagliatelle rolled by hand every morning."),
             tags="", allergens="gluten eggs milk celery sulphites"),
        dish("Risotto al Tartufo", _("Creamy arborio rice infused with black truffle and parmesan."), "v1759425551/Risotto_al_Tartufo_byixjj.png",
             _("Arborio rice stirred slowly with white wine and vegetable stock, finished with butter, Parmigiano and shavings of black truffle. Patience in a bowl."),
             tags="v gf", allergens="milk celery sulphites"),
        dish("Sea Bass alla Griglia", _("Grilled Mediterranean sea bass with lemon butter and roasted fennel."), "v1759425607/SeaBassallaGriglia_d5f81x.png",
             _("Mediterranean sea bass grilled skin-side down until crisp, with lemon butter and fennel roasted until sweet and caramelised."),
             tags="gf", allergens="fish milk"),
        dish("Pollo alla Parmigiana", _("Breaded chicken breast with mozzarella, parmesan, and a light tomato sauce."), "v1759425475/Pollo_alla_Parmigiana_u1s6mc.png",
             _("Chicken breast pounded thin, breaded and pan-fried, then baked under tomato sauce, mozzarella and Parmigiano until bubbling. Comfort food from southern Italy."),
             tags="", allergens="gluten eggs milk"),
        dish("Osso Buco Milanese", _("Braised veal shank with saffron risotto and gremolata."), "v1759425439/OssoBucoMilanese_retdqq.png",
             _("Veal shank braised slowly in white wine and vegetables until it falls from the bone, served with saffron risotto and a fresh gremolata of lemon zest, parsley and garlic."),
             tags="", allergens="gluten milk celery sulphites"),
        dish("Linguine ai Frutti di Mare", _("Pasta with clams, mussels, shrimp, and calamari in a white wine sauce."), "v1759425400/LinguineaiFruttidiMare_u7blwx.png",
             _("Linguine tossed with clams, mussels, prawns and squid in white wine, garlic, chilli and parsley: the taste of a summer evening on the Amalfi coast."),
             tags="", allergens="gluten crustaceans molluscs sulphites"),
    ]},
    {"id": "desserts", "name": _("Desserts"), "dishes": [
        dish("Tiramisu Classico", _("Layers of espresso-soaked ladyfingers with mascarpone cream and cocoa."), "v1759426231/Tiramisu_Classico_fgmfy5.png",
             _("Savoiardi biscuits dipped in fresh espresso, layered with whipped mascarpone, rested overnight and dusted with cocoa. Its name means “pick me up”."),
             tags="v", allergens="gluten eggs milk"),
        dish("Panna Cotta alla Vaniglia", _("Silky vanilla cream topped with a wild berry coulis."), "v1759426192/PannaCottaallaVaniglia_epxxqd.png",
             _("“Cooked cream” from Piedmont: cream gently set with real vanilla, with a sharp coulis of wild berries."),
             tags="gf", allergens="milk"),
        dish("Cannoli Siciliani", _("Crisp pastry shells filled with ricotta cream and candied orange."), "v1759426080/CannoliSiciliani_n7d9fk.png",
             _("Crisp pastry tubes filled to order, so they never go soft, with sweet ricotta, candied orange and a sprinkle of pistachio."),
             tags="v", allergens="gluten eggs milk nuts"),
        dish("Affogato al Caffè", _("Vanilla gelato drowned in hot espresso."), "v1759426041/AffogatoalCaff%C3%A8_zkmf0r.png",
             _("Simple and perfect: a scoop of vanilla gelato “drowned” at the table in a shot of hot espresso."),
             tags="v gf", allergens="milk"),
        dish("Torta Caprese", _("Flourless chocolate and almond cake with powdered sugar."), "v1759426272/TortaCaprese_p0lltz.png",
             _("Born by happy accident in Capri when a baker forgot the flour: a rich, fudgy cake of dark chocolate and ground almonds."),
             tags="v gf", allergens="eggs milk nuts"),
        dish("Gelato Artigianale", _("Chef’s selection of artisanal Italian gelato flavors."), "v1759426153/GelatoArtigianale_zmmweh.png",
             _("Three scoops from our daily selection, churned in small batches. Ask for today’s flavours; pistachio and stracciatella are guest favourites."),
             tags="v gf", allergens="milk nuts"),
    ]},
    {"id": "extras", "name": _("Extras"), "dishes": [
        dish("Focaccia al Rosmarino", _("Warm rosemary focaccia with olive oil."), "v1759427474/FocacciaalRosmarino_udanyy.png",
             _("Light, airy Ligurian focaccia, dimpled by hand, soaked with olive oil and baked with rosemary and sea salt."),
             tags="v vg", allergens="gluten"),
        dish("Patate al Tartufo", _("Truffle-dusted potato wedges."), "v1759427889/PatatealTartufo_ypk6oj.png",
             _("Potato wedges roasted until crisp, then tossed with truffle salt and fresh herbs."),
             tags="v vg gf", allergens=""),
        dish("Verdure Grigliate", _("Grilled seasonal vegetables."), "v1759427808/VerdureGrigliate_ryr30x.png",
             _("Courgette, aubergine, peppers and red onion, chargrilled and dressed with olive oil, garlic and fresh herbs."),
             tags="v vg gf", allergens=""),
        dish("Polenta Cremosa", _("Creamy parmesan polenta."), "v1759427608/PolentaCremosa_hac3wz.png",
             _("Golden cornmeal cooked slowly and finished with butter and Parmigiano, a northern Italian classic."),
             tags="v gf", allergens="milk"),
        dish("Funghi Trifolati", _("Sautéed mushrooms with garlic, parsley, and olive oil."), "v1759427748/FunghiTrifolati_qbrwak.png",
             _("Mushrooms sautéed in olive oil with garlic and parsley. “Trifolati” means cooked the way you would cook truffles."),
             tags="v vg gf", allergens=""),
        dish("Pane della Casa", _("Assorted house bread with dipping oils."), "v1759427522/PanedellaCasa_cbzajc.png",
             _("A basket of our breads baked that morning, with extra virgin olive oil and aged balsamic for dipping."),
             tags="v vg", allergens="gluten sulphites"),
    ]},
    {"id": "drinks", "name": _("Drinks"), "dishes": [
        dish("Prosecco di Valdobbiadene", _("Sparkling, crisp, refreshing."), "v1759428874/Prosecco_di_Valdobbiadene_amtugp.png",
             _("From the hills of Valdobbiadene in the Veneto: fine bubbles with notes of green apple and white flowers. The perfect start to a meal."),
             tags="", allergens="sulphites"),
        dish("Pinot Grigio delle Venezie", _("Classic light Italian white."), "v1759428831/Pinot_Grigio_delle_Venezie_u4obbs.png",
             _("Fresh and dry, with hints of pear and citrus. A lovely match for seafood and light pasta."),
             tags="", allergens="sulphites"),
        dish("Chianti Classico Riserva", _("Robust Tuscan red."), "v1759428746/Chianti_Classico_Riserva_sdfqij.png",
             _("Sangiovese from the heart of Tuscany, aged at least two years: cherry, leather and spice. Made for our ragù and grilled meats."),
             tags="", allergens="sulphites"),
        dish("Barolo DOCG", _("The “King of Wines” from Piedmont."), "v1759428704/Barolo_DOCG_vont2k.png",
             _("Nebbiolo from Piedmont, aged at least three years. Powerful and elegant, with notes of roses and dark cherry."),
             tags="", allergens="sulphites"),
        dish("Amaro Averna", _("Traditional Sicilian digestif."), "v1759428644/Amaro_Averna_uhgmwr.png",
             _("A Sicilian herbal liqueur made since 1868, bittersweet with orange, liquorice and herbs. Served after dinner."),
             tags="", allergens=""),
        dish("Limoncello di Sorrento", _("Iconic lemon liqueur from the Amalfi coast."), "v1759428789/Limoncello_di_Sorrento_cice3s.png",
             _("Made by steeping Sorrento lemon peel in alcohol and sugar. Served ice-cold to finish the meal."),
             tags="", allergens=""),
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

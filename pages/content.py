"""What the FAQ and Gallery pages show (the menu lives in the database: pages.models).

Everything wrapped in _() is translated (locale/es).
"""
from django.utils.translation import gettext_lazy as _

IMG = "https://res.cloudinary.com/diktmeiui/image/upload/"


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

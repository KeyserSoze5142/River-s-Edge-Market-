# Site-wide configuration for the River's Edge Market build.

# Where the live site will be hosted (canonical URLs, sitemap, JSON-LD)
SITE_BASE = "https://www.theriversedgemarket.com"

# Where product "shop" links point. Products check out through the existing
# Square Online store. If the new site takes over the main domain, switch this
# to the free Square-provided domain for the store (Square Dashboard ->
# Website -> Domains, e.g. "https://rivers-edge-market.square.site").
PRODUCT_BASE = "https://www.theriversedgemarket.com"

GIFT_CARD_URL = "https://squareup.com/gift/QF29BQ0P00BMZ/order"

BUSINESS = {
    "name": "River's Edge Market",
    "legal": "River's Edge Market, LLC",
    "street": "1340 The Townes",
    "city": "Tuscaloosa",
    "region": "AL",
    "zip": "35406",
    "phone": "(659) 210-6590",
    "phone_e164": "+16592106590",
    "email": "katielemerson@theriversedgemarket.com",
    "founded": "2019",
    "maps": "https://www.google.com/maps/search/?api=1&query=River%27s+Edge+Market%2C+1340+The+Townes%2C+Tuscaloosa%2C+AL+35406",
}

HOURS = [
    ("Monday", None),
    ("Tuesday", ("10:00", "17:00")),
    ("Wednesday", ("10:00", "17:00")),
    ("Thursday", ("10:00", "17:00")),
    ("Friday", ("10:00", "17:00")),
    ("Saturday", ("10:00", "14:00")),
    ("Sunday", None),
]

SOCIALS = {
    "Facebook": "https://www.facebook.com/riversedgemarket",
    "Instagram": "https://www.instagram.com/theriversedgemarket/",
    "TikTok": "https://www.tiktok.com/@riversedgemarket",
}

PLACEHOLDER_IMG = "assets/placeholder.svg"

# Collections: slug -> (display name, department, blurb)
COLLECTIONS = {
    "circle-e-candles": ("Circle E Candles", "Home Fragrance",
        "Hand-poured Texas candles with legendary burn times and rich, room-filling scent."),
    "nest": ("NEST New York", "Home Fragrance",
        "Luxury candles, diffusers and home fragrance from NEST New York."),
    "capri-blue": ("Capri Blue", "Home Fragrance",
        "The iconic Volcano scent and more — candles, diffusers, body and home care."),
    "gifts": ("Gifts & Home Fragrance", "Home Fragrance",
        "Signature scents, candles and giftable finds for every occasion."),
    "1818-farms": ("1818 Farms", "Bath & Body",
        "Small-batch shea crèmes, balms and botanical bath goods from 1818 Farms."),
    "riman": ("Riman Skincare", "Bath & Body",
        "K-beauty skincare essentials for a radiant, healthy glow."),
    "lemon-lavender": ("Lemon Lavender", "Bath & Body",
        "Playful self-care and beauty essentials to brighten your routine."),
    "plated-jewelry": ("Plated Jewelry", "Jewelry",
        "Elevated gold- and silver-plated earrings and necklaces for every day and evening."),
    "pura-vida": ("Pura Vida", "Jewelry",
        "Beachy, stackable rings and earrings, made to layer and love."),
    "able": ("ABLE Leather", "Bags & Leather",
        "Ethically crafted leather totes, crossbodies and wallets that only get better with age."),
    "bogg": ("Bogg Bag", "Bags & Leather",
        "The cult-favorite tote that goes everywhere — washable, durable, iconic."),
    "swig": ("Swig Life", "Drinkware & Entertaining",
        "Insulated tumblers, mugs and party cups — including Tuscaloosa exclusives."),
    "pirani": ("Pirani", "Drinkware & Entertaining",
        "Stainless party tumblers built for a lifetime of celebrations."),
    "kanga": ("Kanga Coolers", "Drinkware & Entertaining",
        "Iceless coolers and kase mates that keep the party cold."),
    "mydrinkbomb": ("My Drink Bomb", "Drinkware & Entertaining",
        "Craft cocktail bombs — drop, fizz, sip. Entertaining made effortless."),
    "tops": ("Tops & Sweaters", "Apparel",
        "Refined blouses, knits and statement sweaters."),
    "bottoms": ("Bottoms", "Apparel",
        "Tailored pants, skorts and easy shorts."),
    "rompers-and-dresses": ("Dresses & Rompers", "Apparel",
        "Occasion-ready dresses, satin maxis and effortless rompers."),
    "sets": ("Matching Sets", "Apparel",
        "Polished two-piece sets, styled in seconds."),
    "nydj-denim": ("NYDJ Denim", "Apparel",
        "Premium denim with a flawless, flattering fit."),
    "hello-mello": ("Hello Mello Loungewear", "Loungewear",
        "Buttery-soft lounge sets, PJs and slippers for slow mornings."),
    "kids": ("Baby & Kids", "Baby & Kids",
        "Heirloom-soft swaddles, gowns and plush friends for the littlest ones."),
}

DEPARTMENTS = ["Home Fragrance", "Bath & Body", "Jewelry", "Bags & Leather",
               "Drinkware & Entertaining", "Apparel", "Loungewear", "Baby & Kids"]

BRANDS = ["Capri Blue", "NEST New York", "Circle E Candles", "ABLE", "Bogg Bag",
          "Swig Life", "Pura Vida", "NYDJ", "1818 Farms", "Hello Mello",
          "Pirani", "Kanga", "My Drink Bomb", "Riman"]

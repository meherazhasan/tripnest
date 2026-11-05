def img(photo_id):
    return f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=800&q=80"


COX = img("1590523277543-a94d2e4eb00b")
STM = img("1520250497591-112f2f40a3f4")
HILLS = img("1519681393784-d120267933ba")
LAKE = img("1506905925346-21bda4d32df4")
SAJEK = img("1464822759023-fed622ff2c3b")
BEACH = img("1507525428034-b723cf961d3e")
RIVER = img("1500534623283-312aade485b7")
FOREST = img("1441974231531-c6227db76b6e")
OLD = img("1548013146-72479768bada")
SYLHET = img("1600100397608-59c0c8d5f0f5")
TEA = img("1563911302283-d2bc129e7570")
MANGROVE = img("1544197150-b99a580bb7a8")

destinations = [
    # Chattogram Division
    {"name": "Cox's Bazar", "division": "Chattogram", "desc": "World's longest natural sea beach.", "img": COX},
    {"name": "Saint Martin's Island", "division": "Chattogram", "desc": "A small coral island in the Bay of Bengal.", "img": STM},
    {"name": "Bandarban", "division": "Chattogram", "desc": "Hill district with waterfalls and tribal culture.", "img": HILLS},
    {"name": "Rangamati", "division": "Chattogram", "desc": "Famous for the Kaptai Lake and hanging bridge.", "img": LAKE},
    {"name": "Khagrachari", "division": "Chattogram", "desc": "Hill district known as the Alutila Cave and Sajek gateway.", "img": SAJEK},
    {"name": "Sajek Valley", "division": "Chattogram", "desc": "Known as the 'Queen of Hills'.", "img": SAJEK},
    {"name": "Nijhum Dwip", "division": "Chattogram", "desc": "Island famous for deer and migratory birds.", "img": BEACH},
    {"name": "Foy's Lake", "division": "Chattogram", "desc": "Popular amusement and lake park in Chattogram.", "img": RIVER},
    {"name": "Patenga Beach", "division": "Chattogram", "desc": "Beach near the port city of Chattogram.", "img": BEACH},
    {"name": "Cox's Bazar Marine Drive", "division": "Chattogram", "desc": "Longest marine drive road in the country.", "img": COX},
    {"name": "Mirsorai", "division": "Chattogram", "desc": "Home to numerous waterfalls and eco-parks near Chattogram.", "img": FOREST},
    {"name": "Mainamati", "division": "Chattogram", "desc": "Ancient Buddhist archaeological site.", "img": OLD},
    {"name": "Kaptai Lake", "division": "Chattogram", "desc": "Largest man-made lake in Bangladesh.", "img": LAKE},
    {"name": "Alutila Cave", "division": "Chattogram", "desc": "Natural cave in Khagrachari with underground stream.", "img": SAJEK},
    {"name": "Chimbuk Hill", "division": "Chattogram", "desc": "One of the highest points in Bandarban.", "img": HILLS},
    {"name": "Nafakhum Waterfall", "division": "Chattogram", "desc": "Largest waterfall in the Bandarban hill tracts.", "img": FOREST},
    {"name": "Boga Lake", "division": "Chattogram", "desc": "Crater lake located in the hills of Bandarban.", "img": LAKE},
    {"name": "Chittagong Hill Tracts", "division": "Chattogram", "desc": "Home to indigenous communities and hills.", "img": HILLS},

    # Sylhet Division
    {"name": "Sylhet City", "division": "Sylhet", "desc": "Land of tea gardens and hills.", "img": SYLHET},
    {"name": "Srimangal", "division": "Sylhet", "desc": "Tea capital of Bangladesh.", "img": TEA},
    {"name": "Jaflong", "division": "Sylhet", "desc": "Scenic hills, rivers, and stone collection area.", "img": RIVER},
    {"name": "Ratargul Swamp Forest", "division": "Sylhet", "desc": "The only swamp forest in Bangladesh.", "img": FOREST},
    {"name": "Madhabkunda Waterfall", "division": "Sylhet", "desc": "The largest waterfall in Bangladesh.", "img": FOREST},
    {"name": "Lawachara National Park", "division": "Sylhet", "desc": "Rainforest home to rare wildlife.", "img": FOREST},
    {"name": "Bisnakandi", "division": "Sylhet", "desc": "Crystal clear water with hills and stones.", "img": RIVER},
    {"name": "Lalakhal", "division": "Sylhet", "desc": "River famous for its clear turquoise water.", "img": RIVER},
    {"name": "Tanguar Haor", "division": "Sylhet", "desc": "Vast wetland ecosystem with rich biodiversity.", "img": RIVER},
    {"name": "Hakaluki Haor", "division": "Sylhet", "desc": "One of the largest wetlands in Asia.", "img": RIVER},

    # Barishal Division
    {"name": "Kuakata", "division": "Barishal", "desc": "The only beach in Bangladesh to see both sunrise and sunset.", "img": BEACH},
    {"name": "Barisal City", "division": "Barishal", "desc": "Known as the 'Venice of Bengal'.", "img": RIVER},
    {"name": "Durga Sagar", "division": "Barishal", "desc": "One of the largest ponds in Bangladesh.", "img": RIVER},
    {"name": "Guthia Mosque", "division": "Barishal", "desc": "Historic mosque in Barguna district.", "img": OLD},

    # Khulna Division
    {"name": "Sundarbans", "division": "Khulna", "desc": "The largest mangrove forest in the world.", "img": MANGROVE},
    {"name": "Shat Gombuj Mosque", "division": "Khulna", "desc": "Historic 15th-century mosque in Bagerhat.", "img": OLD},
    {"name": "Jessore", "division": "Khulna", "desc": "Historic city known for its flower industry.", "img": RIVER},

    # Rajshahi Division
    {"name": "Paharpur", "division": "Rajshahi", "desc": "UNESCO World Heritage archaeological site.", "img": OLD},
    {"name": "Kantajew Temple", "division": "Rajshahi", "desc": "Terracotta Hindu temple in Dinajpur.", "img": OLD},
    {"name": "Somapura Mahavihara", "division": "Rajshahi", "desc": "Ancient Buddhist monastery ruins.", "img": OLD},
    {"name": "Chalan Beel", "division": "Rajshahi", "desc": "One of the largest wetlands in Bangladesh.", "img": RIVER},
    {"name": "Puthia Temple Complex", "division": "Rajshahi", "desc": "Largest collection of Hindu temples in Bangladesh.", "img": OLD},
    {"name": "Varendra Research Museum", "division": "Rajshahi", "desc": "Oldest museum in Bangladesh, located in Rajshahi.", "img": OLD},

    # Rangpur Division
    {"name": "Tajhat Palace", "division": "Rangpur", "desc": "Zamindar palace in Rangpur with Mughal architecture.", "img": OLD},
    {"name": "Bhinna Jagat Park", "division": "Rangpur", "desc": "Amusement and cultural park in Rangpur.", "img": RIVER},
    {"name": "Kantaji Temple", "division": "Rangpur", "desc": "Famous terracotta temple in Dinajpur.", "img": OLD},

    # Mymensingh Division
    {"name": "Shashi Lodge", "division": "Mymensingh", "desc": "Historic zamindar mansion in Mymensingh.", "img": OLD},
    {"name": "Muktagacha Rajbari", "division": "Mymensingh", "desc": "Old palace of the Muktagacha zamindars.", "img": OLD},
    {"name": "Garo Hills", "division": "Mymensingh", "desc": "Hilly border area with scenic tribal villages.", "img": HILLS},

    # Dhaka Division
    {"name": "Lalbagh Fort", "division": "Dhaka", "desc": "17th-century Mughal fort in Dhaka.", "img": OLD},
    {"name": "Ahsan Manzil", "division": "Dhaka", "desc": "The Pink Palace, former residence of Dhaka's Nawabs.", "img": OLD},
    {"name": "Sonargaon", "division": "Dhaka", "desc": "Ancient capital of Bengal.", "img": OLD},
    {"name": "Panam City", "division": "Dhaka", "desc": "Historic abandoned merchant city.", "img": OLD},
    {"name": "National Parliament House", "division": "Dhaka", "desc": "Iconic modern architecture designed by Louis Kahn.", "img": OLD},
    {"name": "Star Mosque", "division": "Dhaka", "desc": "Beautifully decorated mosque in Old Dhaka.", "img": OLD},
    {"name": "Curzon Hall", "division": "Dhaka", "desc": "Historic building of Dhaka University.", "img": OLD},
    {"name": "Dhakeshwari Temple", "division": "Dhaka", "desc": "The national temple of Bangladesh.", "img": OLD},
]
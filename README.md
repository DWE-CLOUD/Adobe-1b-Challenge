# 1B ADOBE CHALLENGE
-----

# Fast Document Analyst

I built this tool, the Fast Document Analyst, to help me quickly get to the heart of large sets of documents. It's designed to scan through multiple PDFs and pull out the most relevant information based on a specific role and task I define.

-----

## What It Does

The script processes a directory of PDF files. I give it a "persona" (my role) and a "job to be done" (my task), and it returns a JSON object containing the most relevant takeaways and supporting evidence from the documents.

  * **Reads PDFs**: It extracts text from every page of the PDFs provided.
  * **Chunks and Indexes**: The text is broken down into manageable pieces and indexed for fast searching using Faiss.
  * **Caches for Speed**: If I analyze the same set of documents again, it loads from a cache, which saves a lot of time.
  * **Finds Relevant Info**: It uses a sentence-transformer model to find the text chunks most relevant to my persona and job description.
  * **Synthesizes Key Points**: It then pulls out the most important sentences from those chunks to create a list of actionable takeaways.
  * **Outputs Structured Data**: The final result is a clean JSON file with the analysis metadata, key takeaways, and the original text excerpts as supporting evidence.

-----

## How to Use It

I've set this up to run with Docker to keep things simple and self-contained.

### 1\. Build the Docker Image

From the root directory of the project, run the build command:

```bash
docker build -t fast-document-analyst .
```

### 2\. Run the Analysis

To run the analysis, I use the `docker run` command. This command needs to map a local directory containing my PDFs to the `/app/reports` directory inside the container, and a local output directory to `/app/output`.

**Command Template:**

```bash
docker run --rm -v "{path_to_your_pdfs}:/app/reports" -v "{path_to_your_output_directory}:/app/output" fast-document-analyst /app/reports -o /app/output/analysis_result.json --persona "{your_persona}" --job "{your_job}"
```

**Example:**

If my PDFs are in `C:\Users\Ao Developer\Music\adobe-hack\pdf` and I want the output in `C:\Users\Ao Developer\Music\adobe-hack\outputs`, the command looks like this:

```bash
docker run --rm -v "C:\Users\Ao Developer\Music\adobe-hack\pdf:/app/reports" -v "C:\Users\Ao Developer\Music\adobe-hack\outputs:/app/output" fast-document-analyst /app/reports -o /app/output/analysis_result.json --persona "travel planner" --job "plan a trip of 4 days for a group of 10 college friends"
```

-----

## Full Output Example

The command will generate a JSON file (`analysis_result.json` in the example) in the specified output folder. Here is a complete example of what the output looks like.

```json
{
    "metadata": {
        "analysis_type": "Fast Extractive Summary",
        "input_documents": [
            "South of France - Cities.pdf",
            "South of France - Cuisine.pdf",
            "South of France - History.pdf",
            "South of France - Restaurants and Hotels.pdf",
            "South of France - Things to Do.pdf",
            "South of France - Tips and Tricks.pdf",
            "South of France - Traditions and Culture.pdf"
        ],
        "persona": "travel planner",
        "job_to_be_done": "plan a trip of 4 days for a group of 10 college friends",
        "processing_timestamp_utc": "2025-07-28T18:09:17Z",
        "processing_time_seconds": 4.46
    },
    "actionable_synthesis": [
        {
            "text": "Whether you're traveling solo, with kids, or in a group, this guide will help you make the most of your trip.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 1)"
        },
        {
            "text": "By following this comprehensive guide and incorporating the tips and tricks provided, you'll be well-prepared for a comfortable and enjoyable trip.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 9)"
        },
        {
            "text": "Remember to pack light, versatile clothing, and essential items to make the most of your travel experience.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 9)"
        },
        {
            "text": "• Pack a Day Bag: Bring a small day bag for daily excursions.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 8)"
        },
        {
            "text": "• Snacks: Bring a variety of snacks for travel and outings.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 6)"
        },
        {
            "text": "This guide covers everything from packing essentials to travel tips, catering to all seasons and various activities.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 1)"
        },
        {
            "text": "• Additional Tips: Download maps and travel guides to your devices for oﬄine use.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 5)"
        },
        {
            "text": "City Exploration • Day Bag: A small, secure day bag for carrying essentials like water, snacks, and a camera.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 7)"
        },
        {
            "text": "The friendly staﬀ and aﬀordable rates make it a good option for travelers on a budget.",
            "source": "(Source: South of France - Restaurants and Hotels.pdf, Page: 8)"
        },
        {
            "text": "Conclusion Packing for a trip to the South of France involves considering the season, planned activities, and the needs of both adults and children.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 9)"
        },
        {
            "text": "• Camargue: Enjoy a retreat focused on mindfulness and nature immersion.",
            "source": "(Source: South of France - Things to Do.pdf, Page: 7)"
        },
        {
            "text": "Bon voyage!",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 9)"
        },
        {
            "text": "• Books and Entertainment: A book, e-reader, or tablet for entertainment during travel.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 4)"
        },
        {
            "text": "Consider packing a travel potty for young children.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 7)"
        },
        {
            "text": "• Additional Tips: Pack a small backpack for each child with their essentials to keep them engaged.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 6)"
        },
        {
            "text": "Wine Tours • Comfortable Clothing: Wear comfortable, casual clothing suitable for walking and wine tasting.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 7)"
        },
        {
            "text": "luxurious hotel oﬀering elegant rooms, a spa, and breathtaking views of the Mediterranean.",
            "source": "(Source: South of France - Restaurants and Hotels.pdf, Page: 12)"
        },
        {
            "text": "The beautiful setting and all-inclusive amenities make it a hassle-free vacation spot.",
            "source": "(Source: South of France - Restaurants and Hotels.pdf, Page: 9)"
        },
        {
            "text": "The modern amenities and convenient location make it a great choice for budget-conscious travelers.",
            "source": "(Source: South of France - Restaurants and Hotels.pdf, Page: 8)"
        },
        {
            "text": "• Guidebook: A guidebook or map to help navigate and find points of interest.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 7)"
        },
        {
            "text": "The refined decor and serene atmosphere make it a perfect retreat.",
            "source": "(Source: South of France - Restaurants and Hotels.pdf, Page: 11)"
        },
        {
            "text": "• Travel Pillow and Blanket: A compact travel pillow and blanket can make long flights or train rides more comfortable.",
            "source": "(Source: South of France - Tips and Tricks.pdf, Page: 2)"
        },
        {
            "text": "variety of activities for children.",
            "source": "(Source: South of France - Restaurants and Hotels.pdf, Page: 9)"
        },
        {
            "text": "friendly staﬀ and aﬀordable rates make it a good option for travelers on a budget.",
            "source": "(Source: South of France - Restaurants and Hotels.pdf, Page: 8)"
        },
        {
            "text": "pilgrimage sites.",
            "source": "(Source: South of France - Traditions and Culture.pdf, Page: 4)"
        }
    ],
    "supporting_evidence": [
        {
            "rank": 1,
            "document": "South of France - Tips and Tricks.pdf",
            "page": 2,
            "relevance_score": "0.3511",
            "text_excerpt": "General Packing Tips and Tricks • Layering: The weather can vary, so pack layers to stay comfortable in diﬀerent temperatures. • Versatile Clothing: Choose items that can be mixed and matched to create multiple outfits, helping you pack lighter. • Packing Cubes: Use packing cubes to organize your clothes and maximize suitcase space. • Roll Your Clothes: Rolling clothes saves space and reduces wrinkles. • Travel-Sized Toiletries: Bring travel-sized toiletries to save space and comply with airline regulations. • Reusable Bags: Pack a few reusable bags for laundry, shoes, or shopping. • First Aid Kit: Include a small first aid kit with band-aids, antiseptic wipes, and any necessary medications. • Copies of Important Documents: Make copies of your passport, travel insurance, and other important documents. Keep them separate from the originals. • Portable Laundry Kit: A small laundry kit with detergent and a travel clothesline can be handy for longer trips. • Multi-Purpose Shoes: Choose shoes that are comfortable for walking but can also be worn to a nice dinner. • Travel Pillow and Blanket: A compact travel pillow and blanket can make long flights or train rides more comfortable. • Ziplock Bags: Use ziplock bags for liquids, snacks, or to keep items organized and protected from spills. • Emergency Contact List: Have a list of emergency contacts, including local embassy or consulate information."
        },
        {
            "rank": 2,
            "document": "South of France - Tips and Tricks.pdf",
            "page": 8,
            "relevance_score": "0.3491",
            "text_excerpt": "• Notebook: Bring a notebook to jot down notes about the wines you taste. • Water Bottle: Stay hydrated by drinking water between tastings. • Additional Tips: Plan your wine tour route in advance and consider hiring a driver or joining a guided tour to avoid drinking and driving. Tips and Tricks for Packing • Check the Weather: Check the forecast before packing to ensure appropriate clothing. • Make a Packing List: Create a list to ensure nothing is forgotten. Cross oﬀ items as you pack. • Use Packing Cubes: Organize clothes and maximize space. • Roll Your Clothes: Save space and reduce wrinkles. • Pack Dual-Purpose Items: Choose items that serve multiple purposes. • Wear Bulky Items: Wear bulky items like coats or boots during travel to save suitcase space. • Pack a Day Bag: Bring a small day bag for daily excursions. • Leave Room for Souvenirs: Leave extra space or bring a foldable bag for souvenirs. • Additional Tips: Pack a small travel umbrella, a reusable shopping bag, and a portable phone charger. Consider using a luggage scale to avoid overweight baggage fees."
        },
        {
            "rank": 3,
            "document": "South of France - Tips and Tricks.pdf",
            "page": 4,
            "relevance_score": "0.3000",
            "text_excerpt": "• Additional Tips: Winter is mild compared to other regions, but it's still important to pack warm clothing for cooler evenings. Consider packing thermal underwear for extra warmth. Packing for Adults Clothing • Casual Wear: Comfortable clothes for sightseeing and casual dining, like jeans, t- shirts, and casual dresses. • Evening Wear: Dressier outfits for dining out or events. Pack a nice dress or dress pants and a blouse/shirt. • Active Wear: If you plan on hiking or outdoor activities, pack activewear like leggings, shorts, and moisture-wicking tops. • Swimwear: Don't forget your swimsuit for beach or pool visits. • Accessories: A stylish yet functional bag, a lightweight scarf, and a versatile jacket. • Additional Tips: Pack a few statement pieces that can be dressed up or down, such as a versatile dress or a pair of stylish shoes. Toiletries • Basic Toiletries: Toothbrush, toothpaste, shampoo, conditioner, body wash, deodorant, and personal hygiene items. • Skincare: Sunscreen, moisturizer, and daily skincare products. • Makeup: Pack essentials in a travel-sized makeup bag. • Additional Items: A small sewing kit, nail clippers, and a razor. • Additional Tips: Consider packing a travel-sized perfume or cologne to freshen up on the go. Gadgets and Accessories • Electronics: Smartphone, charger, power bank, and other devices. Bring a travel adapter if needed. • Camera: Capture memories with a camera, extra batteries, and memory cards. • Books and Entertainment: A book, e-reader, or tablet for entertainment during travel."
        },
        {
            "rank": 4,
            "document": "South of France - Tips and Tricks.pdf",
            "page": 7,
            "relevance_score": "0.2875",
            "text_excerpt": "• Additional Tips: Bring a favorite stuﬀed animal or comfort item to help kids feel at home. Consider packing a travel potty for young children. Special Considerations Beach Trips • Beach Bag: A large, waterproof bag for essentials. • Towels: Lightweight, quick-drying beach towels. • Beach Toys: Buckets, shovels, and toys for kids. • Snorkeling Gear: Bring your own gear for a better fit and comfort. • Additional Tips: Pack a beach umbrella or tent for shade and a cooler for drinks and snacks. Consider bringing a waterproof phone case to protect your device. Hiking and Outdoor Activities • Backpack: A sturdy, comfortable backpack for essentials. • Water Bottle: A reusable water bottle. • First Aid Kit: A small kit with band-aids, antiseptic wipes, and medications. • Insect Repellent: Protect against bugs and mosquitoes. • Additional Tips: Wear moisture-wicking clothing and sturdy hiking boots. Bring a map and compass or GPS device. Pack energy bars or snacks for long hikes. City Exploration • Day Bag: A small, secure day bag for carrying essentials like water, snacks, and a camera. • Comfortable Shoes: Wear comfortable walking shoes for exploring cities. • Guidebook: A guidebook or map to help navigate and find points of interest. • Additional Tips: Use a money belt or hidden pouch to keep valuables safe. Consider using public transportation to explore cities eﬃciently. Wine Tours • Comfortable Clothing: Wear comfortable, casual clothing suitable for walking and wine tasting."
        },
        {
            "rank": 5,
            "document": "South of France - Tips and Tricks.pdf",
            "page": 1,
            "relevance_score": "0.2801",
            "text_excerpt": "The Ultimate South of France Travel Companion: Your Comprehensive Guide to Packing, Planning, and Exploring Introduction Planning a trip to the South of France requires thoughtful preparation to ensure a comfortable and enjoyable experience. This guide covers everything from packing essentials to travel tips, catering to all seasons and various activities. Whether you're traveling solo, with kids, or in a group, this guide will help you make the most of your trip."
        },
        {
            "rank": 6,
            "document": "South of France - Tips and Tricks.pdf",
            "page": 5,
            "relevance_score": "0.2723",
            "text_excerpt": "• Additional Tips: Download maps and travel guides to your devices for oﬄine use. Consider bringing a portable Wi-Fi hotspot for reliable internet access."
        },
        {
            "rank": 7,
            "document": "South of France - Tips and Tricks.pdf",
            "page": 9,
            "relevance_score": "0.2718",
            "text_excerpt": "Conclusion Packing for a trip to the South of France involves considering the season, planned activities, and the needs of both adults and children. By following this comprehensive guide and incorporating the tips and tricks provided, you'll be well-prepared for a comfortable and enjoyable trip. Remember to pack light, versatile clothing, and essential items to make the most of your travel experience. Bon voyage!"
        },
        {
            "rank": 8,
            "document": "South of France - Restaurants and Hotels.pdf",
            "page": 8,
            "relevance_score": "0.2270",
            "text_excerpt": "Hotels Budget-Friendly Hotels • Ibis Budget Nice Californie Lenval (Nice): A budget-friendly hotel oﬀering comfortable rooms and easy access to the beach and city center. The modern amenities and convenient location make it a great choice for budget-conscious travelers. • Hotel Le Saint Paul (Nice): A charming hotel located in a historic building, oﬀering aﬀordable rates and beautiful views of the Mediterranean. The cozy rooms and friendly service make it a pleasant stay. • Hotel des Arts (Montpellier): A budget-friendly hotel located in the heart of Montpellier, oﬀering comfortable rooms and easy access to the city's attractions. The artistic decor and central location make it a popular choice. • Hotel Le Mistral (Marseille): A budget-friendly hotel oﬀering simple, clean rooms and a convenient location near the Old Port. The friendly staﬀ and aﬀordable rates make it a good option for travelers on a budget. • Hotel Azur (Nice): A budget-friendly hotel oﬀering comfortable rooms and easy access to the beach and city center. The modern amenities and convenient location make it a great choice for budget-conscious travelers. • Hotel de la Paix (Marseille): A budget-friendly hotel oﬀering simple, clean rooms and a convenient location near the Old Port. The friendly staﬀ and aﬀordable rates make it a good option for travelers on a budget. • Hotel du Palais (Montpellier): A budget-friendly hotel located in the heart of Montpellier, oﬀering comfortable rooms and easy access to the city's attractions. The artistic decor and central location make it a popular choice."
        },
        {
            "rank": 9,
            "document": "South of France - Restaurants and Hotels.pdf",
            "page": 9,
            "relevance_score": "0.2231",
            "text_excerpt": "variety of activities for children. The elegant decor and attentive service ensure a comfortable stay for families. • Hôtel Royal Riviera (Saint-Jean-Cap-Ferrat): A luxurious family-friendly hotel oﬀering spacious rooms, beautiful gardens, and a variety of activities for children. The elegant decor and attentive service ensure a comfortable stay for families. • Hôtel Le Negresco (Nice): A luxurious family-friendly hotel oﬀering spacious rooms, beautiful gardens, and a variety of activities for children. The elegant decor and attentive service ensure a comfortable stay for families. • Hôtel Martinez (Cannes): A luxurious family-friendly hotel oﬀering spacious rooms, beautiful gardens, and a variety of activities for children. The elegant decor and attentive service ensure a comfortable stay for families. • Hôtel de Paris (Monaco): A luxurious family-friendly hotel oﬀering spacious rooms, beautiful gardens, and a variety of activities for children. The elegant decor and attentive service ensure a comfortable stay for families."
        },
        {
            "rank": 10,
            "document": "South of France - Restaurants and Hotels.pdf",
            "page": 12,
            "relevance_score": "0.2185",
            "text_excerpt": "Luxurious Hotels • Grand-Hôtel du Cap-Ferrat, A Four Seasons Hotel (Saint-Jean-Cap-Ferrat): A luxurious hotel set on 7 hectares of Mediterranean gardens, oﬀering elegant rooms, a spa, and a private beach. The exclusive setting and world-class amenities make it a top choice for luxury travelers. • Hôtel de Paris Monte-Carlo (Monaco): A luxurious hotel located in the heart of Monaco, oﬀering opulent rooms, a world-class spa, and several Michelin-starred restaurants. The historic grandeur and exceptional service make it a premier destination. • Château Saint-Martin & Spa (Vence): A luxurious hotel set in a historic château, oﬀering elegant rooms, a Michelin-starred restaurant, and a world-class spa. The tranquil setting and luxurious amenities make it a perfect getaway. • Airelles Château de la Messardière (Saint-Tropez): A luxurious hotel set in a historic château, oﬀering elegant rooms, beautiful gardens, and stunning views of the Mediterranean. The refined ambiance and top-tier services make it a standout choice for luxury accommodations. • Hôtel du Cap-Eden-Roc (Antibes): A legendary hotel oﬀering luxurious rooms, a private beach, and a world-class spa. The stunning location and impeccable service make it a favorite among celebrities and discerning travelers. • La Réserve Ramatuelle (Ramatuelle): A luxurious hotel oﬀering elegant rooms, a spa, and breathtaking views of the Mediterranean. The serene setting and exceptional service make it a top choice for a relaxing retreat. • Villa La Coste (Le Puy-Sainte-Réparade): A luxurious hotel set in a vineyard, oﬀering elegant rooms, a spa, and a Michelin-starred restaurant."
        },
        {
            "rank": 11,
            "document": "South of France - Restaurants and Hotels.pdf",
            "page": 12,
            "relevance_score": "0.2159",
            "text_excerpt": "luxurious hotel oﬀering elegant rooms, a spa, and breathtaking views of the Mediterranean. The serene setting and exceptional service make it a top choice for a relaxing retreat. • Villa La Coste (Le Puy-Sainte-Réparade): A luxurious hotel set in a vineyard, oﬀering elegant rooms, a spa, and a Michelin-starred restaurant. The artistic ambiance and world-class amenities make it a unique and memorable stay. • Hôtel Hermitage Monte-Carlo (Monaco): A luxurious hotel oﬀering opulent rooms, a world-class spa, and several fine dining options. The historic charm and exceptional service make it a premier destination in Monaco. • Le Byblos (Saint-Tropez): A luxurious hotel oﬀering elegant rooms, a spa, and a vibrant nightlife scene. The glamorous setting and top-notch amenities make it a favorite among the jet set."
        },
        {
            "rank": 12,
            "document": "South of France - Restaurants and Hotels.pdf",
            "page": 13,
            "relevance_score": "0.2148",
            "text_excerpt": "• Hôtel Métropole Monte-Carlo (Monaco): A luxurious hotel oﬀering opulent rooms, a world-class spa, and several Michelin-starred restaurants. The refined elegance and exceptional service make it a top choice for luxury travelers."
        },
        {
            "rank": 13,
            "document": "South of France - Restaurants and Hotels.pdf",
            "page": 8,
            "relevance_score": "0.2135",
            "text_excerpt": "friendly staﬀ and aﬀordable rates make it a good option for travelers on a budget. • Hotel du Palais (Montpellier): A budget-friendly hotel located in the heart of Montpellier, oﬀering comfortable rooms and easy access to the city's attractions. The artistic decor and central location make it a popular choice. • Hotel de la Mer (Nice): A budget-friendly hotel oﬀering comfortable rooms and easy access to the beach and city center. The modern amenities and convenient location make it a great choice for budget-conscious travelers. • Hotel de la Plage (Marseille): A budget-friendly hotel oﬀering simple, clean rooms and a convenient location near the Old Port. The friendly staﬀ and aﬀordable rates make it a good option for travelers on a budget. • Hotel de la Gare (Montpellier): A budget-friendly hotel located in the heart of Montpellier, oﬀering comfortable rooms and easy access to the city's attractions. The artistic decor and central location make it a popular choice."
        },
        {
            "rank": 14,
            "document": "South of France - Tips and Tricks.pdf",
            "page": 6,
            "relevance_score": "0.1960",
            "text_excerpt": "Packing for Kids Clothing • Comfortable Wear: T-shirts, shorts, pants, dresses, pajamas, and underwear. • Layering: Depending on the season, pack sweaters, jackets, and hats. • Swimwear: Swimsuits and cover-ups for beach or pool days. • Accessories: A sun hat, sunglasses, and a lightweight jacket. • Additional Tips: Pack extra clothing for kids, as they may need more changes of clothes than adults. Essentials • Diapers and Wipes: For babies or toddlers, pack enough diapers and wipes. • Snacks: Bring a variety of snacks for travel and outings. • Toys and Entertainment: Favorite toys, books, or games. Consider a tablet with pre- downloaded content. • Additional Tips: Pack a small backpack for each child with their essentials to keep them engaged. Include comfort items like a favorite blanket or stuﬀed animal. Toiletries • Basic Toiletries: Toothbrush, toothpaste, shampoo, body wash, and personal hygiene items. • Sunscreen: Kid-friendly sunscreen. • Additional Items: A small first aid kit with child-specific medications. • Additional Tips: Pack extra toiletries for kids, as they may need more frequent use of items like wipes and hand sanitizer. Safety and Comfort • Car Seat: Check if a car seat is provided if renting a car. If not, bring your own. • Stroller: A lightweight, foldable stroller for younger children. • Blanket and Pillow: A small blanket and travel pillow for comfort during flights or long car rides."
        },
        {
            "rank": 15,
            "document": "South of France - Restaurants and Hotels.pdf",
            "page": 9,
            "relevance_score": "0.1927",
            "text_excerpt": "Family-Friendly Hotels • Club Med Opio en Provence (Opio): A family-friendly resort oﬀering a wide range of activities for children and adults, including sports, entertainment, and kids' clubs. The beautiful setting and all-inclusive amenities make it a hassle-free vacation spot. • Le Mas de Pierre (Saint-Paul-de-Vence): A luxurious family-friendly hotel oﬀering spacious rooms, beautiful gardens, and a variety of activities for children. The elegant decor and attentive service ensure a comfortable stay for families. • Hôtel Les Roches Rouges (Saint-Raphaël): A family-friendly hotel located on the beach, oﬀering comfortable rooms, a kids' club, and a variety of water sports. The beachfront location and family-oriented amenities make it a great choice for a seaside vacation. • Château de Berne (Lorgues): A family-friendly hotel located on a vineyard, oﬀering spacious rooms, a kids' club, and a variety of outdoor activities. The picturesque setting and family-friendly facilities make it a unique and enjoyable stay. • Hôtel Barrière Le Majestic (Cannes): A luxurious family-friendly hotel oﬀering spacious rooms, beautiful gardens, and a variety of activities for children. The elegant decor and attentive service ensure a comfortable stay for families. • Hôtel du Cap-Eden-Roc (Antibes): A luxurious family-friendly hotel oﬀering spacious rooms, beautiful gardens, and a variety of activities for children. The elegant decor and attentive service ensure a comfortable stay for families. • Hôtel Royal Riviera (Saint-Jean-Cap-Ferrat): A luxurious family-friendly hotel oﬀering spacious rooms, beautiful gardens, and a variety of activities for children. The elegant decor and attentive service ensure a comfortable stay for families."
        },
        {
            "rank": 16,
            "document": "South of France - Traditions and Culture.pdf",
            "page": 4,
            "relevance_score": "0.1796",
            "text_excerpt": "pilgrimage sites. The town of Lourdes, located in the Pyrenees, is one of the most famous, attracting millions of visitors each year. Pilgrims come to Lourdes to visit the Sanctuary of Our Lady of Lourdes, where the Virgin Mary is said to have appeared to a young girl in 1858. The town of Saintes-Maries-de-la-Mer is another significant pilgrimage site, particularly for the Romani community, who venerate Saint Sara. Christmas Traditions Christmas in Provence is marked by unique traditions that reflect the region's cultural heritage. One of the most distinctive customs is the \"13 Desserts,\" a feast of thirteen diﬀerent sweets served after Midnight Mass on Christmas Eve. The number represents Jesus and the twelve apostles. Another tradition is the \"santon\" figurines, which are handcrafted clay figures"
        },
        {
            "rank": 17,
            "document": "South of France - Restaurants and Hotels.pdf",
            "page": 3,
            "relevance_score": "0.1755",
            "text_excerpt": "Family-Friendly Restaurants • Club 55 (Saint-Tropez): This iconic beach club oﬀers a relaxed, family-friendly atmosphere with a menu featuring fresh seafood and Mediterranean dishes. The beachside location and casual vibe make it perfect for families. • Le Safari (Nice): Located in the heart of the old town, this restaurant oﬀers a diverse menu with options for both adults and children. The lively setting and outdoor seating make it a great spot for a family meal. • La Table du Marché (Saint-Rémy-de-Provence): A welcoming restaurant with a varied menu that includes kid-friendly options and fresh, local ingredients. The charming setting and friendly staﬀ ensure a pleasant dining experience for families. • Le Grill (Decize): A family-friendly restaurant oﬀering a variety of grilled meats and classic French dishes in a casual setting. The relaxed atmosphere and extensive menu cater to all ages. • Le Jardin de Benjamin (Lorgues): This restaurant oﬀers a variety of dishes made with fresh, local ingredients. The outdoor seating and kid-friendly menu make it a great spot for families. • Le Petit Jardin (Montpellier): A family-friendly restaurant oﬀering a variety of Mediterranean dishes. The outdoor seating and relaxed atmosphere make it a great spot for a family meal. • Le Café de la Plage (Arcachon): This beachfront café oﬀers a variety of seafood dishes and kid-friendly options. The relaxed setting and beautiful views make it a great spot for families. • Le Petit Nice (Marseille): A family-friendly restaurant oﬀering a variety of seafood dishes."
        },
        {
            "rank": 18,
            "document": "South of France - Things to Do.pdf",
            "page": 7,
            "relevance_score": "0.1727",
            "text_excerpt": "Relaxation and Wellness For those seeking relaxation and rejuvenation, the South of France oﬀers plenty of options: Spa and Wellness Retreats • Aix-en-Provence: Visit Thermes Sextius for thermal baths and massages. • Bordeaux: Enjoy vinotherapy treatments at Les Sources de Caudalie. • Vichy: Experience hydrotherapy and mud baths at Spa Vichy Célestins. • Evian-les-Bains: Relax at the Evian Resort, known for its mineral-rich waters. • Saint-Raphaël: Visit the Thalasso Spa for seawater treatments and relaxation. • Biarritz: Enjoy the luxurious spas and wellness centers in this coastal town. • Cannes: Indulge in a pampering session at one of the many high-end spas. Yoga and Meditation Retreats • Provence: Join a yoga retreat in the serene countryside. • Pyrenees: Escape to the mountains for a meditation retreat. • Côte d'Azur: Combine relaxation with luxury at a wellness retreat. • Luberon: Participate in a holistic retreat with yoga, meditation, and organic meals. • Camargue: Enjoy a retreat focused on mindfulness and nature immersion. • Saint-Tropez: Find tranquility at a yoga retreat overlooking the Mediterranean. • Corsica: Experience a yoga and wellness retreat on this beautiful island."
        },
        {
            "rank": 19,
            "document": "South of France - Tips and Tricks.pdf",
            "page": 3,
            "relevance_score": "0.1721",
            "text_excerpt": "Packing for All Seasons Spring (March to May) • Clothing: Light sweaters, long-sleeve shirts, t-shirts, and a light jacket or raincoat. • Footwear: Comfortable walking shoes and sandals. • Accessories: Sunglasses, a hat, and a small umbrella. • Additional Tips: Spring can be unpredictable, so be prepared for both sunny and rainy days. Consider packing a lightweight scarf for cooler evenings. Summer (June to August) • Clothing: Lightweight, breathable fabrics like cotton and linen. Pack t-shirts, shorts, sundresses, and swimwear. • Footwear: Sandals, flip-flops, and comfortable walking shoes. • Accessories: Sunglasses, a wide-brimmed hat, sunscreen, and a reusable water bottle. • Additional Tips: The South of France can get very hot in the summer, so stay hydrated and seek shade during peak sun hours. Pack a cooling towel to help manage the heat. Autumn (September to November) • Clothing: Light sweaters, long-sleeve shirts, t-shirts, and a medium-weight jacket. • Footwear: Comfortable walking shoes and boots. • Accessories: Sunglasses, a scarf, and a small umbrella. • Additional Tips: Autumn is a great time to visit vineyards and enjoy the harvest season. Pack layers to adjust to varying temperatures throughout the day. Winter (December to February) • Clothing: Warm layers such as sweaters, long-sleeve shirts, and thermal tops. A heavy coat, gloves, and a hat. • Footwear: Waterproof boots and comfortable walking shoes. • Accessories: A scarf, sunglasses for sunny winter days, and a travel-sized hand warmer."
        },
        {
            "rank": 20,
            "document": "South of France - Restaurants and Hotels.pdf",
            "page": 11,
            "relevance_score": "0.1684",
            "text_excerpt": "Upscale Hotels • Hotel Negresco (Nice): A historic five-star hotel located on the Promenade des Anglais, oﬀering luxurious rooms and exceptional service. The opulent decor and prime location make it a landmark in Nice. • InterContinental Marseille - Hotel Dieu (Marseille): A luxurious hotel located in a beautifully restored 18th-century building, oﬀering stunning views of the Old Port and the city. The elegant rooms and top-notch amenities make it a standout choice. • Hotel Martinez (Cannes): A luxurious hotel located on the Boulevard de la Croisette, oﬀering elegant rooms, a private beach, and a Michelin-starred restaurant. The glamorous setting and high-end services make it a favorite among celebrities. • La Bastide de Gordes (Gordes): A luxurious hotel located in a historic building, oﬀering elegant rooms, beautiful gardens, and stunning views of the Luberon Valley. The refined decor and serene atmosphere make it a perfect retreat. • Hôtel Barrière Le Majestic (Cannes): A luxurious hotel located on the Boulevard de la Croisette, oﬀering elegant rooms, a private beach, and a Michelin-starred restaurant. The glamorous setting and high-end services make it a favorite among celebrities. • Hôtel du Cap-Eden-Roc (Antibes): A luxurious hotel located on the Boulevard de la Croisette, oﬀering elegant rooms, a private beach, and a Michelin-starred restaurant. The glamorous setting and high-end services make it a favorite among celebrities. • Hôtel Royal Riviera (Saint-Jean-Cap-Ferrat): A luxurious hotel located on the Boulevard de la Croisette, oﬀering elegant rooms, a private beach, and a Michelin- starred restaurant."
        },
        {
            "rank": 21,
            "document": "South of France - Restaurants and Hotels.pdf",
            "page": 11,
            "relevance_score": "0.1561",
            "text_excerpt": "la Croisette, oﬀering elegant rooms, a private beach, and a Michelin-starred restaurant. The glamorous setting and high-end services make it a favorite among celebrities. • Hôtel Royal Riviera (Saint-Jean-Cap-Ferrat): A luxurious hotel located on the Boulevard de la Croisette, oﬀering elegant rooms, a private beach, and a Michelin- starred restaurant. The glamorous setting and high-end services make it a favorite among celebrities. • Hôtel Le Negresco (Nice): A luxurious hotel located on the Boulevard de la Croisette, oﬀering elegant rooms, a private beach, and a Michelin-starred restaurant. The glamorous setting and high-end services make it a favorite among celebrities. • Hôtel Martinez (Cannes): A luxurious hotel located on the Boulevard de la Croisette, oﬀering elegant rooms, a private beach, and a Michelin-starred restaurant. The glamorous setting and high-end services make it a favorite among celebrities. • Hôtel de Paris (Monaco): A luxurious hotel located on the Boulevard de la Croisette, oﬀering elegant rooms, a private beach, and a Michelin-starred restaurant. The glamorous setting and high-end services make it a favorite among celebrities."
        },
        {
            "rank": 22,
            "document": "South of France - Cities.pdf",
            "page": 10,
            "relevance_score": "0.1549",
            "text_excerpt": "Montpellier: A University City with Medieval Charm History Montpellier, founded in the 10th century, is known for its prestigious university and vibrant cultural scene. The city has a rich history, with a blend of medieval, Renaissance, and modern architecture. Montpellier has been a center of learning and innovation for centuries, attracting scholars and students from around the world. Key Attractions • Place de la Comédie: The central square of Montpellier, this bustling area is surrounded by cafes, shops, and the impressive Opéra Comédie. It is a great place to start exploring the city. • Saint-Pierre Cathedral: This Gothic cathedral, built in the 14th century, is known for its imposing facade and twin towers. It is the seat of the Archdiocese of Montpellier. • Promenade du Peyrou: This 17th-century promenade oﬀers stunning views of the city and features the Arc de Triomphe and the Château d'Eau, a beautiful water tower. • Musée Fabre: One of the most important art museums in France, the Musée Fabre houses an extensive collection of European paintings, sculptures, and decorative arts. Student Life • University Influence: Highlight the vibrant student life and the influence of the university on the city's culture. • Modern Architecture: Mention modern architectural landmarks like the Antigone district or the Pierresvives building. Cultural Highlights Montpellier is renowned for its vibrant cultural scene, with numerous theaters, music venues, and festivals. The city hosts the Montpellier Dance Festival, which attracts contemporary dance companies from around the world."
        },
        {
            "rank": 23,
            "document": "South of France - Cities.pdf",
            "page": 5,
            "relevance_score": "0.1526",
            "text_excerpt": "Nice: The Jewel of the French Riviera History Nice, located on the French Riviera, has been a popular destination for centuries. Its history dates back to the ancient Greeks, who founded the city around 350 BC. Nice later became a Roman colony and has since evolved into a glamorous resort town. In the 19th century, Nice became a favorite winter retreat for European aristocrats, which contributed to its development as a luxurious destination. Key Attractions • Promenade des Anglais: This famous seaside promenade, built in the 19th century, is perfect for a leisurely stroll along the coast. It oﬀers stunning views of the Mediterranean and is lined with cafes and hotels. • Castle Hill (Colline du Château): This hilltop park oﬀers panoramic views of Nice and the Mediterranean. It was once the site of a medieval castle, which was destroyed in the 18th century. • Old Town (Vieux Nice): The historic center of Nice is a labyrinth of narrow streets, baroque churches, and bustling markets. Don't miss the Cours Saleya market, where you can find fresh produce, flowers, and local delicacies. • Matisse Museum: Dedicated to the works of Henri Matisse, who spent much of his life in Nice, this museum features a comprehensive collection of his paintings, sculptures, and drawings. Hidden Gems • Russian Orthodox Cathedral: Visit the stunning Russian Orthodox Cathedral, a unique architectural gem in Nice. • Marc Chagall National Museum: Explore the works of Marc Chagall at this dedicated museum."
        },
        {
            "rank": 24,
            "document": "South of France - Things to Do.pdf",
            "page": 9,
            "relevance_score": "0.1521",
            "text_excerpt": "Family-Friendly Activities The South of France oﬀers a variety of activities that are perfect for families with children: Theme Parks and Attractions • Antibes: Visit Marineland for marine shows and an aquarium. • Fréjus: Cool oﬀ at Aqualand water park. • Villeneuve-Loubet: Enjoy quirky attractions at Le Village des Fous. • Monteux: Spend a day at Parc Spirou, a theme park based on the famous comic book character. • La Palmyre: Explore the La Palmyre Zoo, home to a wide variety of animals. • Cap d'Agde: Have fun at Luna Park, an amusement park with rides and games. • Toulouse: Visit the Cité de l'Espace, a space-themed science museum with interactive exhibits. Outdoor Adventures • Verdon Gorge: Take a family hike or rent paddle boats to explore the stunning Verdon Gorge. • Camargue Natural Park: Explore wetlands with wild horses and flamingos, and enjoy horseback riding, bird watching, and boat tours. • Various Locations: Try tree-top adventure parks with zip lines, rope bridges, and climbing challenges. • Gorges du Tarn: Go on a family-friendly hike and enjoy the scenic views. • Lake Annecy: Rent bikes and ride along the lake's picturesque bike paths. • Pyrenees: Take a cable car ride for stunning mountain views and easy hiking trails. • Dordogne: Explore the region's caves and prehistoric sites with guided tours suitable for children. Educational Experiences • Toulouse: Visit Cité de l'Espace for a space-themed science museum with interactive exhibits, a planetarium, and a replica of the Mir space station."
        },
        {
            "rank": 25,
            "document": "South of France - Things to Do.pdf",
            "page": 10,
            "relevance_score": "0.1517",
            "text_excerpt": "• Monaco: Explore the Musée Océanographique and its marine exhibits, including a shark lagoon and touch tanks. • Dordogne: See ancient cave paintings at prehistoric sites like Lascaux and Rouﬃgnac, and visit museums dedicated to prehistoric life. • Montpellier: Discover the Planet Ocean World, an aquarium and planetarium with interactive exhibits. • Carcassonne: Take a guided tour of the medieval citadel and learn about its history and architecture. • Nîmes: Visit the Roman amphitheater and learn about ancient Roman history. • Arles: Explore the Roman ruins and the Musée de l'Arles Antique, which showcases artifacts from the city's past."
        },
        {
            "rank": 26,
            "document": "South of France - History.pdf",
            "page": 10,
            "relevance_score": "0.1416",
            "text_excerpt": "Montpellier: A University City with Medieval Charm Montpellier, founded in the 10th century, is known for its prestigious university and vibrant cultural scene. The city has a rich history, with a blend of medieval, Renaissance, and modern architecture. Key Historical Sites in Montpellier • Place de la Comédie: The central square of Montpellier, this bustling area is surrounded by cafes, shops, and the impressive Opéra Comédie. It is a great place to start exploring the city. • Saint-Pierre Cathedral: This Gothic cathedral, built in the 14th century, is known for its imposing facade and twin towers. It is the seat of the Archdiocese of Montpellier. • Promenade du Peyrou: This 17th-century promenade oﬀers stunning views of the city and features the Arc de Triomphe and the Château d'Eau, a beautiful water tower. • Musée Fabre: One of the most important art museums in France, the Musée Fabre houses an extensive collection of European paintings, sculptures, and decorative arts. • University of Montpellier: Founded in 1289, it is one of the oldest universities in the world and has been a center of learning and culture for centuries. • Jardin des Plantes: Established in 1593, it is the oldest botanical garden in France and was created for the study of medicinal plants."
        },
        {
            "rank": 27,
            "document": "South of France - Cuisine.pdf",
            "page": 4,
            "relevance_score": "0.1393",
            "text_excerpt": "experience. • Chez Pipo (Nice): A local favorite for Socca, this casual eatery is perfect for a quick and delicious snack. Chez Pipo has been serving Socca since 1923 and is a beloved institution in Nice. The restaurant's simple, no-frills approach allows the quality of the Socca to shine through. • L'Atelier de Jean-Luc Rabanel (Arles): A Michelin-starred restaurant known for its creative and contemporary take on Provençal cuisine. Chef Jean-Luc Rabanel's dishes are a feast for the senses, combining bold flavors with artistic presentation. The restaurant's tasting menu oﬀers a journey through the flavors of Provence, with each course showcasing the region's finest ingredients. • La Table de Plaisance (Saint-Émilion): A two-Michelin-starred restaurant oﬀering a sophisticated menu that highlights the flavors of the region. The restaurant is located in a historic building in the heart of Saint-Émilion, a town known for its world-class wines. The menu features dishes that pair beautifully with the local wines, creating a truly memorable dining experience."
        },
        {
            "rank": 28,
            "document": "South of France - Cities.pdf",
            "page": 8,
            "relevance_score": "0.1352",
            "text_excerpt": "Aix-en-Provence: A City of Art and Culture History Aix-en-Provence, founded by the Romans in 123 BC, is known for its elegant architecture, vibrant cultural scene, and association with the painter Paul Cézanne. The city's rich history is reflected in its beautiful buildings and lively atmosphere. Aix-en-Provence has been a center of art and learning for centuries, attracting artists, writers, and scholars. Key Attractions • Cours Mirabeau: This grand boulevard, lined with plane trees, cafes, and fountains, is the heart of Aix-en-Provence. It is a great place to soak up the city's atmosphere. • Saint-Sauveur Cathedral: This cathedral, built between the 5th and 17th centuries, features a mix of architectural styles, including Romanesque, Gothic, and Baroque. It is known for its beautiful cloister and triptych by Nicolas Froment. • Hôtel de Ville: The town hall of Aix-en-Provence, built in the 17th century, is an elegant building with a beautiful clock tower and an ornate facade. The square in front of the Hôtel de Ville is a lively spot, often hosting markets and events. • Atelier Cézanne: The studio of Paul Cézanne, one of the most famous painters associated with Aix-en-Provence, is preserved as a museum. Visitors can see where Cézanne created many of his masterpieces and gain insight into his artistic process. Artistic Heritage • Walking Tour: Take a walking tour of sites related to Paul Cézanne, such as the Terrain des Peintres and the Bibémus Quarry."
        },
        {
            "rank": 29,
            "document": "South of France - Things to Do.pdf",
            "page": 2,
            "relevance_score": "0.1340",
            "text_excerpt": "Coastal Adventures The South of France is renowned for its beautiful coastline along the Mediterranean Sea. Here are some activities to enjoy by the sea: Beach Hopping • Nice: Visit the sandy shores and enjoy the vibrant Promenade des Anglais. • Antibes: Relax on the pebbled beaches and explore the charming old town. • Saint-Tropez: Experience the exclusive beach clubs and glamorous atmosphere. • Marseille to Cassis: Explore the stunning limestone cliﬀs and hidden coves of Calanques National Park. • Îles d'Hyères: Discover pristine beaches and excellent snorkeling opportunities on islands like Porquerolles and Port-Cros. • Cannes: Enjoy the sandy beaches and luxury beach clubs along the Boulevard de la Croisette. • Menton: Visit the serene beaches and beautiful gardens in this charming town near the Italian border. Water Sports • Cannes, Nice, and Saint-Tropez: Try jet skiing or parasailing for a thrill. • Toulon: Dive into the underwater world with scuba diving excursions to explore wrecks. • Cerbère-Banyuls: Visit the marine reserve for an unforgettable diving experience. • Mediterranean Coast: Charter a yacht or join a sailing tour to explore the coastline and nearby islands. • Marseille: Go windsurfing or kitesurfing in the windy bays. • Port Grimaud: Rent a paddleboard and explore the canals of this picturesque village. • La Ciotat: Try snorkeling in the clear waters around the Île Verte."
        },
        {
            "rank": 30,
            "document": "South of France - Restaurants and Hotels.pdf",
            "page": 3,
            "relevance_score": "0.1325",
            "text_excerpt": "for a family meal. • Le Café de la Plage (Arcachon): This beachfront café oﬀers a variety of seafood dishes and kid-friendly options. The relaxed setting and beautiful views make it a great spot for families. • Le Petit Nice (Marseille): A family-friendly restaurant oﬀering a variety of seafood dishes. The relaxed setting and fresh ingredients make it a popular choice. • Le Jardin des Sens (Montpellier): This restaurant oﬀers a variety of dishes made with fresh, local ingredients. The outdoor seating and kid-friendly menu make it a great spot for families. • Le Café des Arts (Nice): A family-friendly café oﬀering a variety of dishes and kid- friendly options. The relaxed setting and friendly service make it a great spot for a family meal."
        }
    ]
}
```

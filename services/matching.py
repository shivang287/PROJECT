from math import radians, sin, cos, sqrt, atan2


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two geographical coordinates.
    Returns distance in kilometers.
    """

    earth_radius = 6371

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(earth_radius * c, 2)


def calculate_match_score(farmer, demand):
    """
    Calculate buyer-farmer compatibility score.

    Weight:
    Quantity  : 30%
    Distance  : 25%
    Quality   : 20%
    Price     : 15%
    Delivery  : 10%
    """

    # -----------------------------
    # 1. QUANTITY SCORE
    # -----------------------------

    quantity_ratio = min(
        farmer["quantity"] / demand["quantity"],
        1
    )

    quantity_score = quantity_ratio * 100


    # -----------------------------
    # 2. DISTANCE SCORE
    # -----------------------------

    distance = calculate_distance(
        farmer["latitude"],
        farmer["longitude"],
        demand["latitude"],
        demand["longitude"]
    )

    if distance <= 50:
        distance_score = 100

    elif distance <= 100:
        distance_score = 80

    elif distance <= 150:
        distance_score = 60

    elif distance <= 250:
        distance_score = 40

    else:
        distance_score = 20


    # -----------------------------
    # 3. QUALITY SCORE
    # -----------------------------

    if farmer["quality"] == demand["quality"]:
        quality_score = 100

    elif farmer["quality"] == "B" and demand["quality"] == "A":
        quality_score = 50

    else:
        quality_score = 30


    # -----------------------------
    # 4. PRICE SCORE
    # -----------------------------

    if (
        demand["min_price"]
        <= farmer["price"]
        <= demand["max_price"]
    ):
        price_score = 100

    elif farmer["price"] < demand["min_price"]:
        difference = demand["min_price"] - farmer["price"]
        price_score = max(60, 100 - difference * 10)

    else:
        difference = farmer["price"] - demand["max_price"]
        price_score = max(40, 100 - difference * 10)


    # -----------------------------
    # 5. DELIVERY SCORE
    # -----------------------------

    if farmer["delivery_days"] <= 2:
        delivery_score = 100

    elif farmer["delivery_days"] == 3:
        delivery_score = 80

    elif farmer["delivery_days"] == 4:
        delivery_score = 60

    else:
        delivery_score = 40


    # -----------------------------
    # FINAL SCORE
    # -----------------------------

    final_score = (
        quantity_score * 0.30
        + distance_score * 0.25
        + quality_score * 0.20
        + price_score * 0.15
        + delivery_score * 0.10
    )

    return {
        "score": round(final_score),
        "distance": distance,
        "quantity_score": round(quantity_score),
        "distance_score": distance_score,
        "quality_score": quality_score,
        "price_score": price_score,
        "delivery_score": delivery_score
    }


def rank_farmers(farmers, demand):
    """
    Rank all compatible farmers/FPOs.
    """

    results = []

    for farmer in farmers:

        # Ignore different products
        if farmer["product"].lower() != demand["product"].lower():
            continue

        result = calculate_match_score(
            farmer,
            demand
        )

        results.append({
            **farmer,
            **result
        })

    # Highest score first
    results.sort(
        key=lambda farmer: farmer["score"],
        reverse=True
    )

    return results


def create_smart_pool(farmers, demand):
    """
    Create an optimal farmer pool to satisfy buyer demand.

    Farmers are considered in matching-score order.
    """

    ranked_farmers = rank_farmers(
        farmers,
        demand
    )

    selected = []

    total_quantity = 0

    for farmer in ranked_farmers:

        if total_quantity >= demand["quantity"]:
            break

        selected.append(farmer)

        total_quantity += farmer["quantity"]


    fulfilled = total_quantity >= demand["quantity"]

    shortage = max(
        0,
        demand["quantity"] - total_quantity
    )

    return {
        "farmers": selected,
        "total_quantity": total_quantity,
        "required_quantity": demand["quantity"],
        "fulfilled": fulfilled,
        "shortage": shortage
    }
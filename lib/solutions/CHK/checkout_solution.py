

# noinspection PyUnusedLocal
# skus = unicode string

"""
Our price table and offers:
+------+-------+------------------------+
| Item | Price | Special offers         |
+------+-------+------------------------+
| A    | 50    | 3A for 130, 5A for 200 |
| B    | 30    | 2B for 45              |
| C    | 20    |                        |
| D    | 15    |                        |
| E    | 40    | 2E get one B free      |
+------+-------+------------------------+
"""

prices = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
    "E": 40,
}

# Item code: [(required amount, deal type, return)]
specials = {
    "A": [((3, "A"), "NORMAL", 130), ((5, "A"), "NORMAL", 200)],
    "B": [((2, "B"), "NORMAL", 45)],
    "E": [((2, "E"), "FREE", (1, "B"))],
}


def calculate_discount_savings(offer):
    offer_required = offer[0]
    offer_type = offer[1]
    offer_return = offer[2]
    savings = 0
    if offer_type == "NORMAL":
        expected_to_pay = prices[offer_required[1]]*offer_required[0]
        savings = expected_to_pay - offer_return
    if offer_type == "FREE":
        expected_to_pay = prices[offer_return[1]]
        savings = expected_to_pay
    return savings


def get_applicable_discounts(basket):
    applicable_offers = []
    for code, count in basket.items():
        if code not in specials:
            continue

        offers_for_code = specials[code]
        for offer in offers_for_code:
            required_items = offer[0][0]
            if count >= required_items:
                applicable_offers.append(offer)

    return applicable_offers


def prioritised_applicable_offers(basket):
    offers = get_applicable_discounts(basket)

    for offer in offers:
        print("OFFER: %s, SAVINGS: %d" % (offer, calculate_discount_savings(offer)))

    offers.sort(key=lambda x: -calculate_discount_savings(x))
    return offers


def apply_to_basket(offer, basket):
    return basket


def apply_discounts(basket):
    """
    Return a reduced count of items in the basket, and the cost of what offers were applied
    :param basket:
    :return:
    """
    prioritised_offers = prioritised_applicable_offers(basket)
    print([calculate_discount_savings(x) for x in prioritised_offers])
    cost_of_discounted = []
    for offer in prioritised_offers:
        basket = apply_to_basket(offer, basket)
    # for code, count in basket.items():
    #     if code not in specials:
    #         continue
    #     required_items = specials[code][0]
    #     if count >= required_items:
    #         fits = count // required_items
    #         basket[code] = basket[code] - fits*required_items
    #         cost_of_discounted.append(fits*specials[code][1])
    return basket, cost_of_discounted


def checkout(skus):
    if not isinstance(skus, str):
        return -1
    skus = [x for x in skus]
    basket = {}
    # Remap to count
    for item in skus:
        if item not in prices:
            return -1
        basket[item] = basket.get(item, 0) + 1

    no_discount_basket, discount_costs = apply_discounts(basket)

    total = 0
    for code, quant in no_discount_basket.items():
        total += prices[code]*quant
    total += sum(discount_costs)
    return total


checkout("AAABDB")  # 190)
checkout("AAAAAAABDCC")  # 385)
checkout("BBBEE")  # 95  # 2B, 2E.
checkout("BBBBEE")  # 155  # 2B+1B+2E = 45+30+80 = 75+80
checkout(""),  # 0
checkout("A"),  # 50
checkout("B"),  # 30
checkout("C"),  # 20
checkout("D"),  # 15
checkout("a"),  # -1






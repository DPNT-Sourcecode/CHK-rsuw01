

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
| F    | 10    | 2F get one F free      |
+------+-------+------------------------+
"""

prices = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
    "E": 40,
    "F": 10,
}

# Item code: [(required amount, deal type, return)]
specials = {
    "A": [((3, "A"), "NORMAL", 130), ((5, "A"), "NORMAL", 200)],
    "B": [((2, "B"), "NORMAL", 45)],
    "E": [((2, "E"), "FREE", (1, "B"))],
    "F": [((2, "F"), "FREE", (1, "F"))],
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

    # for offer in offers:
    #     print("OFFER: %s, SAVINGS: %d" % (offer, calculate_discount_savings(offer)))

    offers.sort(key=lambda x: -calculate_discount_savings(x))
    return offers


def reduce_free_excess(in_basket, required_for_deal, to_remove):
    """
    Given FFFFF return FFFF (i.e. given an amount of 5, the amount of free ones we can get is 1 without ruining the deal
    :param amount:
    :param returned:
    :return:

    2, 2, 1 > 2 payable, 0 free
    3, 2, 1 > 2 payable, 1 free
    4, 2, 1 > 3 payable, 1 free
    5, 2, 1 > 4 payable, 1 free
    6, 2, 1 > 4 payable, 2 free
    7, 2, 1 > 5 payable, 2 free
    8, 2, 1 > 6 payable, 2 free

    """
    used = 0
    saved = 0
    while in_basket > 0:
        in_basket = in_basket - required_for_deal
        used += required_for_deal
        saved += to_remove
        print("U:%d, S:%d, B:%s" % (used, saved, in_basket))
    return 1



def apply_to_basket(offer, basket):
    """
    Apply to basket as many times as possible before returning the basket
    :param offer:
    :param basket:
    :return:
    """
    requirements = offer[0]
    offer_type = offer[1]
    offer_return = offer[2]
    saved = 0
    if offer_type == "FREE":
        offer_key = offer_return[1]
        # Remove only B from the basket, original item not removed
        amount_in_basket = basket[requirements[1]]
        if offer_key == requirements[1]:
            basket[offer_key] = basket[offer_key] - reduce_free_excess(amount_in_basket, requirements[0], offer_return[0])
        else:
            fits = amount_in_basket // requirements[0]
            # Reduce basket by amount
            if offer_key in basket:
                basket[offer_key] = basket[offer_key] - (fits*offer_return[0])
    if offer_type == "NORMAL":
        amount_in_basket = basket[requirements[1]]
        fits = amount_in_basket // requirements[0]
        # Reduce basket by amount
        basket[requirements[1]] = basket[requirements[1]] - (fits*requirements[0])
        # TODO: instead of returning saved here, we should be returning the full price or something?
        saved = offer[2]*fits

    return basket, saved


def apply_discounts(basket):
    """
    Return a reduced count of items in the basket, and the cost of what offers were applied
    :param basket:
    :return:
    """
    prioritised_offers = prioritised_applicable_offers(basket)
    savings = 0
    for offer in prioritised_offers:
        basket, saved = apply_to_basket(offer, basket)
        savings += saved
    return basket, savings


def checkout(skus):
    if not isinstance(skus, str):
        print("-1")
        return -1
    skus = [x for x in skus]
    basket = {}
    # Remap to count
    for item in skus:
        if item not in prices:
            print("-1")
            return -1
        basket[item] = basket.get(item, 0) + 1

    no_discount_basket, saved = apply_discounts(basket)

    total = 0
    for code, quant in no_discount_basket.items():
        total += prices[code]*quant
    total += saved
    print(total)
    return total


print(checkout("FF") == 20)   # 20
print(checkout("FFF") == 20)  # 20
print(checkout("FFFF") == 30)  # 30
print(checkout("FFFFF") == 40)  # 40


# checkout("EE")  # 80
# checkout("EEB")  # 80
# checkout("EEEB")  # 120
#
# checkout("AAABDB")  # 190)
# checkout("AAAAAAABDCC")  # 385)
# checkout("BBBEE")  # 125  # 2B deal + 2E = 45+80.
# checkout("BBBBEE")  # 155  # 2B+1B+2E = 45+30+80 = 75+80
# checkout(""),  # 0
# checkout("A"),  # 50
# checkout("B"),  # 30
# checkout("C"),  # 20
# checkout("D"),  # 15
# checkout("a"),  # -1


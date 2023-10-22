

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

specials = {
    "A": [(3, "NORMAL", 130), (5, "NORMAL", 200)],
    "B": [(2, "NORMAL", 45)],
    "E": [(2, "FREE", (1, "B"))],
}

def get_applicable_discounts(basket):
    for code, count in basket.items():
        if code not in specials:
            continue

        offers_for_code = specials[code]
        applicable_offers = []
        for offer in offers_for_code:
            if count >= offer[0]:
                applicable_offers.append(offer)

    return applicable_offers

def apply_discounts(basket):
    """
    Return a reduced count of items in the basket, and the cost of what offers were applied
    :param basket:
    :return:
    """
    print(get_applicable_discounts(basket))
    cost_of_discounted = []
    for code, count in basket.items():
        if code not in specials:
            continue
        required_items = specials[code][0]
        if count >= required_items:
            fits = count // required_items
            basket[code] = basket[code] - fits*required_items
            cost_of_discounted.append(fits*specials[code][1])
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

# # print(checkout("AAABDB"))
# # print(checkout("AAAAAAABDCC"))
# print(checkout(""))
# print(checkout("A"))
# print(checkout("B"))
# print(checkout("C"))
# print(checkout("D"))
# print(checkout("a"))


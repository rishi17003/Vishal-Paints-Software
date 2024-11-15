def calculate_rate(materials):
    """A utility function to calculate the total rate based on materials and their quantities"""
    total_rate = 0
    for material_id, quantity in materials:
        # Assuming a function `get_material_price()` that returns price of material by ID
        price = get_material_price(material_id)
        total_rate += price * float(quantity)
    return total_rate

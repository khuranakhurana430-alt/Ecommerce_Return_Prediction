from faker import Faker
import random
import pandas as pd

fake = Faker('en_IN')

# ---------------- STATE / CITY ---------------- #

INDIA_STATES_CITIES = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur"],
    "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat"],
    "Himachal Pradesh": ["Shimla", "Solan", "Dharamshala"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode"],
    "Madhya Pradesh": ["Indore", "Bhopal", "Jabalpur"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
    "Manipur": ["Imphal", "Thoubal", "Bishnupur"],
    "Meghalaya": ["Shillong", "Tura", "Jowai"],
    "Mizoram": ["Aizawl", "Lunglei", "Saiha"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur"],
    "Sikkim": ["Gangtok", "Namchi", "Gyalshing"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad"],
    "Tripura": ["Agartala", "Udaipur", "Dharmanagar"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Noida"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Haldwani"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur"]
}

# ---------------- CUSTOMERS ---------------- #

customers = []

for i in range(5000):
    state = random.choice(list(INDIA_STATES_CITIES.keys()))
    city = random.choice(INDIA_STATES_CITIES[state])

    customers.append({
        "customer_id": i + 1,
        "name": fake.name(),
        "email": fake.email(),
        "signup_date": fake.past_date(),
        "city": city,
        "state": state
    })

customer_table = pd.DataFrame(customers)

# ---------------- CATEGORIES ---------------- #

CATEGORIES = [
    "Apparel/Fashion",
    "Electronics",
    "Beauty/Cosmetics",
    "Home & Kitchen Furniture",
    "Food & Beverages",
    "Toys"
]

categories = []
for i, name in enumerate(CATEGORIES):
    categories.append({
        "category_id": i + 1,
        "category_name": name
    })

category_table = pd.DataFrame(categories)

# ---------------- PRODUCTS ---------------- #

products = []

ecommerce_products = [
    "Smartphone","Laptop","Wireless earbuds","Bluetooth speaker","Smartwatch",
    "Running shoes","T-shirt","Backpack","Perfume","Coffee maker",
    "Office chair","Bedsheets","Gaming mouse","Printer","Water bottle"
]

for i in range(300):

    cost = round(random.uniform(100, 40000), 2)
    price = round(cost * random.uniform(1.1, 1.6), 2)

    products.append({
        "product_id": i + 1,
        "product_name": random.choice(ecommerce_products),
        "category_id": random.choice(category_table["category_id"].tolist()),
        "price": price,
        "cost_price": cost
    })

product_table = pd.DataFrame(products)

# ---------------- ORDERS ---------------- #

orders = []

for i in range(9000):

    orders.append({
        "order_id": i + 1,
        "customer_id": random.choice(customer_table["customer_id"].tolist()),
        "order_status": random.choice(["Delivered", "In Transit", "Canceled"]),
        "payment_method": random.choice(
            ["Cash on Delivery", "Net Banking", "UPI", "Loyalty Points"]
        )
    })

order_table = pd.DataFrame(orders)

# ---------------- ORDER ITEMS ---------------- #

order_items = []

for i in range(15000):

    selected_order = random.choice(order_table["order_id"].tolist())
    selected_product = random.choice(product_table["product_id"].tolist())

    product_row = product_table.loc[
        product_table["product_id"] == selected_product
    ].iloc[0]

    quantity = random.randint(1, 5)
    unit_price = product_row["price"]

    order_items.append({
        "order_item_id": i + 1,
        "order_id": selected_order,
        "product_id": selected_product,
        "quantity": quantity,
        "unit_price": unit_price
    })

order_item_table = pd.DataFrame(order_items)

# ---------------- RETURNS ---------------- #

returns = []

delivered_items = order_item_table.merge(
    order_table[order_table["order_status"] == "Delivered"],
    on="order_id"
)

returned_sample = delivered_items.sample(n=1500, random_state=42)

for i, row in returned_sample.iterrows():

    refund_amount = row["unit_price"] * row["quantity"]

    returns.append({
        "return_id": len(returns) + 1,
        "order_item_id": row["order_item_id"],
        "return_date": fake.date_between(start_date="-2m", end_date="today"),
        "refund_amount": round(refund_amount, 2)
    })

return_table = pd.DataFrame(returns)

# ---------------- EXPORT ---------------- #

# customer_table.to_csv("customers.csv", index=False)
# category_table.to_csv("categories.csv", index=False)
# product_table.to_csv("products.csv", index=False)
# order_table.to_csv("orders.csv", index=False)
# order_item_table.to_csv("order_items.csv", index=False)
# return_table.to_csv("returns.csv", index=False)

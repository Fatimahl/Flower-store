import streamlit as st
import pandas as pd
import base64
import os
from PIL import Image
from datetime import datetime
import ast

st.set_page_config(page_title="Flower Store", page_icon="🌸", layout="wide")

orders_file = "orders.csv"
products_file = "products.csv"
ADMIN_PASSWORD = "4444"

# ======================
# Style + Background
# ======================
try:
    with open("FA.jpeg", "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{b64_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        section[data-testid="stSidebar"] {{
            background-color: rgba(255,255,255,0.95) !important;
        }}

        section[data-testid="stSidebar"] * {{
            color: #3f2a2a !important;
        }}

        .stTextInput input,
        .stNumberInput input {{
            background-color: rgba(255,255,255,0.95) !important;
            color: #3f2a2a !important;
            border: 2px solid #b56b78 !important;
            border-radius: 14px !important;
            height: 52px !important;
        }}

        .stButton>button {{
            background-color: rgba(255,255,255,0.95) !important;
            color: #3f2a2a !important;
            border-radius: 16px !important;
            border: 2px solid #b56b78 !important;
            padding: 10px 22px;
            font-weight: bold;
        }}

        .stButton>button:hover {{
            background-color: #f8dfe4 !important;
            color: #3f2a2a !important;
        }}

        .box {{
            background-color: rgba(255,255,255,0.80);
            padding: 18px;
            border-radius: 22px;
            margin-bottom: 18px;
        }}

        h1, h2, h3, label, div, p {{
            color: #3f2a2a;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
except:
    pass


# ======================
# Products
# image = اسم الصورة
# cost = بكم انتي شريتيه
# price = بكم بتبيعينه
# ======================
default_products = [
    {"name": "روز أحمر", "cost": 3, "price": 5, "image": "A.jpeg", "available": True},
    {"name": "روز خربزي", "cost": 3, "price": 5, "image": "B.jpeg", "available": True},
    {"name": "بيبي روز فوشي", "cost": 4, "price": 7, "image": "C.jpeg", "available": True},
    {"name": "بيبي روز أورنج", "cost": 4, "price": 7, "image": "D.jpeg", "available": True},
    {"name": "بيبي روز موف فاتح", "cost": 4, "price": 7, "image": "E.jpeg", "available": True},
    {"name": "توليب موف", "cost": 8, "price": 12, "image": "F.jpeg", "available": True},
    {"name": "توليب بينك فاتح", "cost": 8, "price": 12, "image": "G.jpeg", "available": True},
    {"name": "هايبركم أحمر", "cost": 5, "price": 9, "image": "H.jpeg", "available": True},
    {"name": "هايبركم أبيض", "cost": 5, "price": 9, "image": "I.jpeg", "available": True},
    {"name": "ستاتس موف فاتح", "cost": 4, "price": 8, "image": "J.jpeg", "available": True},
    {"name": "دوار الشمس", "cost": 7, "price": 12, "image": "K.jpeg", "available": True},
    {"name": "ستاتس موف", "cost": 4, "price": 8, "image": "L.jpeg", "available": True},
    {"name": "رسكوس سفندر", "cost": 5, "price": 9, "image": "M.jpeg", "available": True},
    {"name": "ليليوم ستارجيزر هولندي", "cost": 10, "price": 15, "image": "N.jpeg", "available": True},
    {"name": "ليليوم أصفر", "cost": 9, "price": 14, "image": "O.jpeg", "available": True},
    {"name": "ليليوم وردي", "cost": 9, "price": 14, "image": "P.jpeg", "available": True},
    {"name": "ليليوم أحمر", "cost": 9, "price": 14, "image": "Q.jpeg", "available": True},
    {"name": "ليليوم أبيض", "cost": 9, "price": 14, "image": "R.jpeg", "available": True},
    {"name": "توليب وردي", "cost": 8, "price": 12, "image": "S.jpeg", "available": True},
    {"name": "توليب أحمر", "cost": 8, "price": 12, "image": "T.jpeg", "available": True},
    {"name": "استرومريا بينك", "cost": 6, "price": 10, "image": "U.jpeg", "available": True},
    {"name": "كريز أخوان دبل بينك", "cost": 6, "price": 10, "image": "V.jpeg", "available": True},
    {"name": "كريز أخوان أبيض", "cost": 6, "price": 10, "image": "W.jpeg", "available": True},
    {"name": "بيبي روز بينك", "cost": 4, "price": 7, "image": "X.jpeg", "available": True},
]

if not os.path.exists(products_file):
    pd.DataFrame(default_products).to_csv(products_file, index=False)

if not os.path.exists(orders_file):
    pd.DataFrame(columns=[
        "time", "name", "role", "budget", "items",
        "total", "cost_total", "profit", "status"
    ]).to_csv(orders_file, index=False)


def load_products():
    return pd.read_csv(products_file)


def save_products(df):
    df.to_csv(products_file, index=False)


def load_orders():
    df = pd.read_csv(orders_file)

    needed_columns = ["time", "name", "role", "budget", "items", "total", "cost_total", "profit", "status"]
    for col in needed_columns:
        if col not in df.columns:
            df[col] = 0 if col in ["budget", "total", "cost_total", "profit"] else ""

    return df


def save_order(order):
    df = load_orders()
    df = pd.concat([df, pd.DataFrame([order])], ignore_index=True)
    df.to_csv(orders_file, index=False)


def go(page_name):
    st.session_state.page = page_name
    st.rerun()


def check_password():
    password = st.text_input("Enter password:", type="password")
    if password == ADMIN_PASSWORD:
        return True
    elif password:
        st.error("Wrong password.")
    return False


if "page" not in st.session_state:
    st.session_state.page = "start"

if "cart" not in st.session_state:
    st.session_state.cart = []

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

if "role" not in st.session_state:
    st.session_state.role = "Student"


side = st.sidebar.radio(
    "Navigation",
    ["Customer", "Admin Dashboard", "Statistics"]
)

if side == "Customer":
    if st.session_state.page in ["admin", "stats"]:
        st.session_state.page = "start"

elif side == "Admin Dashboard":
    st.session_state.page = "admin"

elif side == "Statistics":
    st.session_state.page = "stats"


st.markdown("<h1 style='text-align:center;'>🌸 FLOWER STORE 🌸</h1>", unsafe_allow_html=True)


# ======================
# Customer Start Page
# ======================
if st.session_state.page == "start":

    st.markdown("## Welcome to our flower store 💐")

    st.session_state.customer_name = st.text_input(
        "Enter your name:",
        value=st.session_state.customer_name
    )

    st.write("Choose your category:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Student"):
            st.session_state.role = "Student"

    with col2:
        if st.button("Teacher"):
            st.session_state.role = "Teacher"

    budget = 25 if st.session_state.role == "Student" else 50

    st.info(f"Selected: {st.session_state.role}")
    st.info(f"Your available points: {budget} SAR")

    old_orders = load_orders()

    if st.session_state.customer_name:
        previous = old_orders[
            old_orders["name"].astype(str).str.lower()
            == st.session_state.customer_name.lower()
        ]

        if not previous.empty:
            st.error("You already ordered before. Your points were used.")
        else:
            if st.button("Next: Start Shopping"):
                go("shop")


# ======================
# Shop Page
# ======================
elif st.session_state.page == "shop":

    st.markdown("## Available Flowers")

    products_df = load_products()
    available_products = products_df[products_df["available"] == True]

    if available_products.empty:
        st.warning("No flowers available right now.")
    else:
        cols = st.columns(2)

        for i, product in available_products.iterrows():
            with cols[i % 2]:
                st.markdown("<div class='box'>", unsafe_allow_html=True)
                try:
                    files = [
                        f for f in os.listdir()
                        if os.path.splitext(f)[0] in list("ABCDEFGHIJKLMNOPQRSTUVWX")
                        and f.lower().endswith(("jpg", "jpeg", "png"))
                    ]

                    files.sort()

                    if i < len(files):
                        st.image(files[i], width=220)
                    else:
                        st.warning("مافي صورة لهذا المنتج")

                except:
                    st.warning("ما انعرضت الصورة")
                                
                st.subheader(product["name"])
                st.write(f"Price: {product['price']} SAR")

                quantity = st.number_input(
                    "Quantity:",
                    min_value=0,
                    max_value=10,
                    step=1,
                    key=f"qty_{product['name']}"
                )

                if st.button("Add to Cart", key=f"add_{product['name']}"):
                    if quantity > 0:
                        st.session_state.cart.append({
                            "name": product["name"],
                            "price": int(product["price"]),
                            "cost": int(product["cost"]),
                            "quantity": int(quantity)
                        })
                        st.success("Added to cart ✅")
                    else:
                        st.warning("Choose quantity first.")

                st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            go("start")

    with col2:
        if st.button("Next: Cart"):
            go("cart")


# ======================
# Cart Page
# ======================
elif st.session_state.page == "cart":

    st.markdown("## 🛒 Cart & Checkout")

    budget = 25 if st.session_state.role == "Student" else 50
    total = 0
    cost_total = 0

    if st.session_state.cart:
        for item in st.session_state.cart:
            item_total = item["price"] * item["quantity"]
            item_cost = item["cost"] * item["quantity"]

            total += item_total
            cost_total += item_cost

            st.write(f"{item['name']} × {item['quantity']} = {item_total} SAR")

        profit = total - cost_total

        st.write(f"### Total: {total} SAR")
        st.info(f"Your budget: {budget} SAR")

        if total > budget:
            st.error("You do not have enough points.")
        else:
            if st.button("Submit Order"):
                order = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "name": st.session_state.customer_name,
                    "role": st.session_state.role,
                    "budget": budget,
                    "items": str(st.session_state.cart),
                    "total": total,
                    "cost_total": cost_total,
                    "profit": profit,
                    "status": "Waiting"
                }

                save_order(order)
                st.session_state.cart = []
                st.success("Your order has been sent successfully 🌸")
                st.balloons()

    else:
        st.info("Your cart is empty.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back to Shop"):
            go("shop")

    with col2:
        if st.button("Back to Start"):
            go("start")


# ======================
# Admin Dashboard
# ======================
elif st.session_state.page == "admin":

    st.markdown("## 🔒 Admin Dashboard")

    if check_password():

        st.markdown("### Orders")

        df = load_orders()

        if df.empty:
            st.info("No orders yet.")
        else:
            edited_df = st.data_editor(
                df,
                column_config={
                    "status": st.column_config.SelectboxColumn(
                        "status",
                        options=["Waiting", "Ready for pickup", "Received"]
                    )
                },
                hide_index=True,
                use_container_width=True
            )

            if st.button("Save Order Changes"):
                edited_df.to_csv(orders_file, index=False)
                st.success("Order status updated ✅")

        st.markdown("---")
        st.markdown("### Product Settings")

        products_df = load_products()

        edited_products = st.data_editor(
            products_df,
            column_config={
                "available": st.column_config.CheckboxColumn(
                    "Available",
                    help="Uncheck if the product is sold out"
                )
            },
            hide_index=True,
            use_container_width=True,
            num_rows="dynamic"
        )

        if st.button("Save Product Changes"):
            save_products(edited_products)
            st.success("Products updated ✅")


# ======================
# Statistics Page
# ======================
elif st.session_state.page == "stats":

    st.markdown("## 🔒 Sales Statistics")

    if check_password():

        df = load_orders()

        if df.empty:
            st.info("No sales yet.")
        else:
            total_sales = df["total"].sum()
            total_cost = df["cost_total"].sum()
            total_profit = df["profit"].sum()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Sales", f"{total_sales} SAR")

            with col2:
                st.metric("Total Cost", f"{total_cost} SAR")

            with col3:
                st.metric("Total Profit", f"{total_profit} SAR")

            st.metric("Number of Orders", len(df))

            flower_count = {}

            for items in df["items"]:
                try:
                    items_list = ast.literal_eval(items)
                    for item in items_list:
                        flower_count[item["name"]] = flower_count.get(item["name"], 0) + item["quantity"]
                except:
                    pass

            if flower_count:
                stats_df = pd.DataFrame({
                    "Flower Type": list(flower_count.keys()),
                    "Sold Count": list(flower_count.values())
                })

                st.bar_chart(stats_df.set_index("Flower Type"))

                best = max(flower_count, key=flower_count.get)
                st.success(f"Most sold flower: {best} 🌸")
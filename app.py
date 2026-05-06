import streamlit as st
import pandas as pd
import base64
import os
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
        .stNumberInput input,
        textarea {{
            background-color: rgba(255,255,255,0.95) !important;
            color: #3f2a2a !important;
            border: 2px solid #b56b78 !important;
            border-radius: 14px !important;
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
# cost = بكم انتي شريتيه
# price = بكم بتبيعينه
# الأسعار تتعدل من الأدمن
# ======================
default_products = [
    {"name": "ماتشا | Flower Matcha", "cost": 5, "price": 10, "image": "A.jpeg", "available": True},
    {"name": "روز احمر", "cost": 3, "price": 5, "image": "B.jpeg", "available": True},
    {"name": "روز بنفسجي ", "cost": 3, "price": 5, "image": "C.jpeg", "available": True},
    {"name": " ستاتس بنفسجي", "cost": 4, "price": 7, "image": "D.jpeg", "available": True},
    {"name": " سDDتاتس اصفر", "cost": 4, "price": 7, "image": "E.jpeg", "available": True},
    {"name": "ستاتس وردي ", "cost": 4, "price": 7, "image": "F.jpeg", "available": True},
    {"name": " بيبي روز اصفر", "cost": 8, "price": 12, "image": "G.jpeg", "available": True},
    {"name": "بيبي روز ابيض ", "cost": 8, "price": 12, "image": "H.jpeg", "available": True},
    {"name": "بيبي روز وردي ", "cost": 5, "price": 9, "image": "I.jpeg", "available": True},
    {"name": "استر", "cost": 5, "price": 9, "image": "J.jpeg", "available": True},
    {"name": "كريز ازرق ", "cost": 4, "price": 8, "image": "K.jpeg", "available": True},
    {"name": "كريزاصفر ", "cost": 7, "price": 12, "image": "L.jpeg", "available": True},
    {"name": "كريز احمر ", "cost": 4, "price": 8, "image": "M.jpeg", "available": True},
    {"name": "ماتيولا بنفسجي ", "cost": 5, "price": 9, "image": "N.jpeg", "available": True},
    {"name": "جراس ", "cost": 10, "price": 15, "image": "O.jpeg", "available": True},
    {"name": "سفندر ", "cost": 9, "price": 14, "image": "P.jpeg", "available": True},
]

if not os.path.exists(products_file):
    pd.DataFrame(default_products).to_csv(products_file, index=False)

if not os.path.exists(orders_file):
    pd.DataFrame(columns=[
        "time", "name", "role", "items",
        "total", "cost_total", "profit",
        "payment_method", "matcha_notes", "rating",
        "status"
    ]).to_csv(orders_file, index=False)


def load_products():
    return pd.read_csv(products_file)


def save_products(df):
    df.to_csv(products_file, index=False)


def load_orders():
    df = pd.read_csv(orders_file)

    needed_columns = [
        "time", "name", "role", "items",
        "total", "cost_total", "profit",
        "payment_method", "matcha_notes", "rating",
        "status"
    ]

    for col in needed_columns:
        if col not in df.columns:
            df[col] = 0 if col in ["total", "cost_total", "profit", "rating"] else ""

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

if "payment_method" not in st.session_state:
    st.session_state.payment_method = ""

if "last_order_status" not in st.session_state:
    st.session_state.last_order_status = ""


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

    st.info(f"Selected: {st.session_state.role}")

    if st.session_state.customer_name:
        orders_df = load_orders()
        customer_orders = orders_df[
            orders_df["name"].astype(str).str.lower()
            == st.session_state.customer_name.lower()
        ]

        if not customer_orders.empty:
            latest_status = customer_orders.iloc[-1]["status"]
            st.info(f"آخر حالة طلب لك: {latest_status}")

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
                        if os.path.splitext(f)[0] in list("ABCDEFGHIJKLMNOP")
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

                matcha_notes = ""
                if "ماتشا" in str(product["name"]) or "Matcha" in str(product["name"]):
                    matcha_notes = st.text_area(
                        "كيف تحبي الماتشا؟",
                        key="matcha_notes"
                    )

                if st.button("Add to Cart", key=f"add_{product['name']}"):
                    if quantity > 0:
                        st.session_state.cart.append({
                            "name": product["name"],
                            "price": int(product["price"]),
                            "cost": int(product["cost"]),
                            "quantity": int(quantity),
                            "notes": matcha_notes
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

    total = 0
    cost_total = 0
    all_matcha_notes = []

    if st.session_state.cart:
        for item in st.session_state.cart:
            item_total = item["price"] * item["quantity"]
            item_cost = item["cost"] * item["quantity"]

            total += item_total
            cost_total += item_cost

            st.write(f"{item['name']} × {item['quantity']} = {item_total} SAR")

            if item.get("notes"):
                st.write(f"ملاحظات الماتشا: {item['notes']}")
                all_matcha_notes.append(item["notes"])

        profit = total - cost_total

        st.write(f"### Total: {total} SAR")

        st.markdown("### اختاري طريقة الدفع")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("تحويل"):
                st.session_state.payment_method = "تحويل"

        with col2:
            if st.button("كاش"):
                st.session_state.payment_method = "كاش"

        if st.session_state.payment_method:
            st.success(f"طريقة الدفع: {st.session_state.payment_method}")

        rating = st.slider("قيّمي خدمتنا من خمس نجوم ⭐", 1, 5, 5)

        if st.button("Submit Order"):
            if not st.session_state.payment_method:
                st.warning("اختاري طريقة الدفع قبل إرسال الطلب.")
            else:
                order = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "name": st.session_state.customer_name,
                    "role": st.session_state.role,
                    "items": str(st.session_state.cart),
                    "total": total,
                    "cost_total": cost_total,
                    "profit": profit,
                    "payment_method": st.session_state.payment_method,
                    "matcha_notes": " | ".join(all_matcha_notes),
                    "rating": rating,
                    "status": "قيد الانتظار"
                }

                save_order(order)
                st.session_state.cart = []
                st.session_state.last_order_status = "قيد الانتظار"
                st.success("تم إرسال طلبك 🌸 حالة الطلب: قيد الانتظار")
                st.toast("تم إرسال الطلب بنجاح 🌸")
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
            df["delete"] = False

            edited_df = st.data_editor(
                df,
                column_config={
                    "status": st.column_config.SelectboxColumn(
                        "status",
                        options=["قيد الانتظار", "قيد التجهيز", "تم التجهيز", "تم الاستلام"]
                    ),
                    "delete": st.column_config.CheckboxColumn(
                        "Delete",
                        help="اختاري هذا المربع لحذف الطلب"
                    )
                },
                hide_index=True,
                use_container_width=True
            )

            if st.button("Save Order Changes"):
                edited_df = edited_df[edited_df["delete"] == False]
                edited_df = edited_df.drop(columns=["delete"])
                edited_df.to_csv(orders_file, index=False)
                st.success("Order changes saved ✅")

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
            matcha_sales = 0
            matcha_cost = 0
            matcha_profit = 0
            matcha_count = 0

            flower_sales = 0
            flower_cost = 0
            flower_profit = 0
            flower_count = 0

            flower_items_count = {}

            for items in df["items"]:
                try:
                    items_list = ast.literal_eval(items)

                    for item in items_list:
                        item_name = str(item["name"])
                        quantity = int(item["quantity"])
                        item_sales = int(item["price"]) * quantity
                        item_cost = int(item["cost"]) * quantity
                        item_profit = item_sales - item_cost

                        if "ماتشا" in item_name or "Matcha" in item_name:
                            matcha_sales += item_sales
                            matcha_cost += item_cost
                            matcha_profit += item_profit
                            matcha_count += quantity
                        else:
                            flower_sales += item_sales
                            flower_cost += item_cost
                            flower_profit += item_profit
                            flower_count += quantity
                            flower_items_count[item_name] = flower_items_count.get(item_name, 0) + quantity

                except:
                    pass

            st.markdown("## 🍵 Matcha Statistics")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Matcha Sales", f"{matcha_sales} SAR")

            with col2:
                st.metric("Matcha Cost", f"{matcha_cost} SAR")

            with col3:
                st.metric("Matcha Profit", f"{matcha_profit} SAR")

            with col4:
                st.metric("Matcha Sold Count", matcha_count)

            st.markdown("---")

            st.markdown("## 🌸 Flower Statistics")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Flower Sales", f"{flower_sales} SAR")

            with col2:
                st.metric("Flower Cost", f"{flower_cost} SAR")

            with col3:
                st.metric("Flower Profit", f"{flower_profit} SAR")

            with col4:
                st.metric("Flower Sold Count", flower_count)

            if "rating" in df.columns:
                st.metric("Average Rating", f"{df['rating'].mean():.1f} ⭐")

            if flower_items_count:
                stats_df = pd.DataFrame({
                    "Flower Type": list(flower_items_count.keys()),
                    "Sold Count": list(flower_items_count.values())
                })

                st.bar_chart(stats_df.set_index("Flower Type"))

                best = max(flower_items_count, key=flower_items_count.get)
                st.success(f"Most sold flower: {best} 🌸")

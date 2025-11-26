import requests, os, streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Used car price prediction (Streamlit Demo)")

# POLA:
car_name = st.slider("car_name", 0, 83, 39)
yr_mfr = st.slider("yr_mfr", 0, 15, 11)
fuel_type = st.radio("fuel_type", [0,1,2,3], 1, horizontal=True)
kms_run = st.number_input("kms_run", min_value=0, value=28652)
city = st.slider("city", 0, 13, 1)
times_viewed = st.number_input("times_viewed", value=483)
body_type = st.radio("body_type", [0,1,2,3,4,5], 0, horizontal=True)
transmission = st.radio("transmission", [0,1,2], 0, horizontal=True)
variant = st.slider("car_name", 0, 208, 171)
assured_buy = st.checkbox("assured_buy", 1)
registered_city = st.slider("registered_city", 0, 75, 15)
registered_state = st.slider("registered_state", 0, 11, 5)
is_hot = st.checkbox("is_hot", 1)
rto = st.slider("rto", 0, 92, 43)
source = st.radio("source", [0,1], 0, horizontal=True)
make = st.slider("make", 0, 16, 9)
model = st.slider("model", 0, 83, 6)
car_availability = st.radio("car_availability", [0,1,2,3,4], 1, horizontal=True)
total_owners = st.slider("total_owners", 1, 3, 2)
broker_quote = st.number_input("broker_quote", min_value=0, value=386415)
original_price = st.number_input("original_price", min_value=0.0, value=395599.0)
car_rating = st.radio("car_rating", [0,1,2,3], 2, horizontal=True)
fitness_certificate = st.checkbox("fitness_certificate", 1)
emi_starts_from = st.number_input("emi_starts_from", min_value=0, value=9189)
booking_down_pymnt = st.number_input("booking_down_pymnt", min_value=0, value=59340)
reserved = st.checkbox("reserved", 0)
warranty_avail = st.checkbox("warranty_avail", 0)

# Przycisk wysłania payloada
if st.button("Predict"):

    payload = {
        "car_name": car_name,
        "yr_mfr": yr_mfr,
        "fuel_type": fuel_type,
        "kms_run": kms_run,
        "city": city,
        "times_viewed": times_viewed,
        "body_type": body_type,
        "transmission": transmission,
        "variant": variant,
        "assured_buy": assured_buy,
        "registered_city": registered_city,
        "registered_state": registered_state,
        "is_hot": is_hot,
        "rto": rto,
        "source": source,
        "make": make,
        "model": model,
        "car_availability": car_availability,
        "total_owners": total_owners,
        "broker_quote": broker_quote,
        "original_price": original_price,
        "car_rating": car_rating,
        "fitness_certificate": fitness_certificate,
        "emi_starts_from": emi_starts_from,
        "booking_down_pymnt": booking_down_pymnt,
        "reserved": reserved,
        "warranty_avail": warranty_avail
        }

    r = requests.post(f"{API_URL}/predict", json=payload, timeout=10)

    st.write("Status:", r.status_code)
    st.write("Response:", r.json())

import streamlit as st

# Set up page configuration
st.set_page_config(page_title="Legal Services Portal", page_icon="⚖️", layout="centered")

# App Header
st.title("⚖️ Legal Services Pre-Payment Portal")
st.write("Select your required legal services and complete your transfer securely.")
st.write("---")

# Service Pricing (in ETB / Birr)
PRICES = {
    "Consultation Fee": 1000,
    "Drafting Charges (Statement of Claim/Application)": 4000,
    "Drafting Defence": 4000
}

# Target Payment Details
MERCHANT_PHONE = "+251914539226"

st.subheader("📁 1. Select Required Services")

selected_services = []
total_amount = 0

# Checkboxes for services
for service, price in PRICES.items():
    if st.checkbox(f"{service} — {price:,} ETB"):
        selected_services.append(service)
        total_amount += price

st.write("---")

# Summary Section
st.subheader("📊 2. Invoice Summary")

if total_amount > 0:
    for service in selected_services:
        st.write(f"🔹 {service}")
    
    # Large Display of Total Due
    st.metric(label="Total Amount to Send", value=f"{total_amount:,} ETB")
    
    st.write("---")
    
    # Payment Method Choice
    st.subheader("💳 3. Choose Payment Method")
    payment_method = st.radio(
        "Select your preferred mobile wallet:",
        ["telebirr", "CBE Birr"],
        horizontal=True
    )
    
    # Instructions Container
    with st.container(border=True):
        st.markdown(f"### 📲 Instructions for **{payment_method}**")
        st.write("Please manually transfer the total amount using your phone:")
        
        # Display the phone number prominently with a copy field
        st.text_input("Copy Recipient Phone Number:", value=MERCHANT_PHONE, disabled=True)
        st.text_input("Copy Amount to Send:", value=f"{total_amount}", disabled=True)
        
        if payment_method == "telebirr":
            st.markdown(f"""
            1. Open the **telebirr** App or dial `*127#`.
            2. Choose **Send Money** (or *Pay Merchant* if using a merchant account).
            3. Enter the phone number: **`{MERCHANT_PHONE}`**
            4. Enter the exact amount: **`{total_amount} Birr`**
            5. Confirm the recipient name matches the owner of this number.
            6. Enter your PIN to complete the transfer.
            """)
        else: # CBE Birr
            st.markdown(f"""
            1. Open the **CBEBirr** App or dial `*847#`.
            2. Choose **Send Money** (or *Pay Bill/Merchant*).
            3. Enter the phone number: **`{MERCHANT_PHONE}`**
            4. Enter the exact amount: **`{total_amount} Birr`**
            5. Verify the account name matches the owner of this number.
            6. Enter your PIN to complete the transaction.
            """)
            
    # Confirmation Section
    st.write("---")
    st.subheader("✅ 4. Confirm Payment Submission")
    st.info("After completing the transfer on your phone, click the button below to notify us.")
    
    if st.button("I Have Sent the Payment", type="primary"):
        st.success(f"🎉 Thank you! Your request for {total_amount:,} ETB via {payment_method} has been submitted.")
        st.balloons()
        st.warning("📥 *Note: Please keep a screenshot of your transaction SMS/Receipt for confirmation upon consultation.*")

else:
    st.info("Please check at least one legal service checkbox above to generate payment instructions.")

# Footer
st.write("---")
st.caption("Secure Client Pre-payment Interface • Phone: +251914539226")
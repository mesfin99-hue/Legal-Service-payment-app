import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- Page Configurations ---
st.set_page_config(page_title="Legal Services Intake", page_icon="⚖️", layout="centered")

# --- Custom Styling (Blue Background, Bright Pink Fonts) ---
custom_css = """
<style>
    /* Entire application background */
    .stApp {
        background-color: #0047AB !important; /* Blue background */
    }
    
    /* Override font colors to Bright Pink */
    html, body, p, h1, h2, h3, h4, h5, h6, span, label, li, div {
        color: #FF1493 !important; /* Bright Pink */
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Style input boxes and text areas for visibility */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        color: #FF1493 !important;
        border: 2px solid #FF1493 !important;
        background-color: #FFFFFF !important; /* White background inside input boxes for text contrast */
        font-weight: bold;
    }

    /* Checkbox text label override */
    .stCheckbox label p {
        color: #FF1493 !important;
        font-weight: bold;
    }

    /* Form Container Border */
    div[data-testid="stForm"] {
        border: 3px solid #FF1493 !important;
        background-color: rgba(0, 0, 0, 0.2);
        border-radius: 12px;
        padding: 25px;
    }

    /* Submit Button styling */
    div.stButton > button:first-child {
        background-color: #FF1493 !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 30px !important;
        cursor: pointer;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #FF69B4 !important; /* Lighter bright pink on hover */
        color: white !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Email Notification Function ---
def send_email_notification(client_name, client_phone, selected_service, case_details, attached_file):
    # Configurations for sending notifications
    sender_email = "shewet2015@gmail.com"  # Replace with your system email address
    sender_password = "cckj ayyn xvia djpm"         # Replace with your Gmail App Password
    receiver_email = "shewet2015@gmail.com"
    
    # Setup the multi-part email structure
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"⚖️ NEW PRE-PAID CASE: {client_name}"
    
    body = f"""
    You have received a new pre-paid legal case submission.
    
    CLIENT DETAILS:
    -------------------------------------------
    Full Name: {client_name}
    Phone Number: {client_phone}
    
    SERVICE & PAYMENT REQUESTED:
    -------------------------------------------
    Selected Service: {selected_service}
    
    CASE DETAILS:
    -------------------------------------------
    {case_details}
    
    *The client's payment invoice receipt is attached to this email.*
    """
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # Process the file attachment if present
    if attached_file is not None:
        payload = MIMEBase('application', 'octet-stream')
        payload.set_payload(attached_file.getvalue())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', f'attachment; filename={attached_file.name}')
        msg.attach(payload)
        
    try:
        # Connecting to SMTP Server (port 587 with TLS)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False

# --- App Structure & UI ---
st.title("⚖️ Legal Services Pre-Payment Portal")
st.write("በይዘኦም ዝደልይዎ ዓይነት ኣገልግሎት መሪፆም ክፍሊት ዝፈፀሙሉ ደረሰይ የተሓሕዙ። ካብኡ ናይ ጉዳዮም ዝርዝር ሓበሬታ የቐምጡ።")

# Price breakdown table
st.subheader("ናይ ኣገልግሎት ዋጋ ዝርዝር (Pricing Structure)")
pricing_data = {
    "ናይ ኣገልግሎት ዓይነት (Service Type)": [
        "ንምምኻር (Consultation)",
        "ክሲ ንምፅሓፍ (Statement of Claim)",
        "መልሲ ንምፅሓፍ (Statement of Defense)",
        "መመልከቲታት (ውርሲ፣ ሽም ምቕያር፣ ሞግዚት ንምሻም)",
        "ንኻልኦት (Other Applications)"
    ],
    "ዋጋ (Price)": ["2000 ብር", "4000 ብር", "3000 ብር", "1000 ብር", "2500 ብር"]
}
st.table(pricing_data)

st.write("---")

# Main Client Form
with st.form("legal_intake_form"):
    st.subheader("ናይ ዓሚል መመልከቲ ፎርሚ (Client Intake Form)")
    
    # Personal Details
    name = st.text_input("ሙሉእ ሽም (Full Name)")
    phone = st.text_input("ስልኪ ቁፅሪ (Phone Number)")
    
    # Service drop-down
    service = st.selectbox(
        "ዝደልይዎ ኣገልግሎት (Choose Service):",
        [
            "ንምምኻር — 1000 ብር",
            "ክሲ ንምፅሓፍ — 3000 ብር",
            "መልሲ ንምፅሓፍ — 2000 ብር",
            "መመልከቲታት (ውርሲ፣ ሽም ምቕያር፣ ሞግዚት ንምሻም) — 1000 ብር",
            "ንኻልኦት — 1500 ብር"
        ]
    )
    
    # Payment Upload and Confirmation
    invoice = st.file_uploader("ዝኸፈልሉ ደረሰይ ኣብዚ የተሓሕዙ (Attach Paid Invoice / Receipt)", type=["pdf", "png", "jpg", "jpeg"])
    confirmed = st.checkbox("ትኽክለኛ ክፍሊት ምኽፋለይ የረጋግፅ (I confirm that I have paid the required amount)")
    
    # Detailed case information field
    st.write("#### ናይ ጉዳዮም ዝርዝር መግለፂ (Case Details)")
    details = st.text_area("ናይ ጉዳዮም ዝርዝር መግለፂ ኣብዚ ይፅሓፉ (Write every detail about your case here):", height=250)
    
    # Submit button
    submit_btn = st.form_submit_button("እዚ መረዳእታ ለኣኽ (Submit Details)")

# --- Submission Logic Handler ---
if submit_btn:
    if not name or not phone:
        st.error("በይዘኦም ሽሞምን ስልኪ ቁፅሮምን ይምልኡ (Please fill out Name and Phone Number).")
    elif not invoice:
        st.error("በይዘኦም ናይ ክፍሊት መረጋገፂ ደረሰይ የተሓሕዙ (Please attach your payment invoice).")
    elif not confirmed:
        st.error("በይዘኦም ክፍሊት ምፍፃሞም ዘረጋግፅ ሳንዱቕ ይፅቀጡ (Please check the payment confirmation checkbox).")
    elif not details:
        st.error("በይዘኦም ናይ ጉዳዮም ዝርዝር መብርሂ ይፅሓፉ (Please write your case details).")
    else:
        with st.spinner("ኣብ ምምሕልላፍ ይርከብ... በይዘኦም ይፀበዩ (Sending notification...)"):
            # Send the data over email via SMTP
            success = send_email_notification(name, phone, service, details, invoice)
            
            st.success("እቲ ዝመልኡዎ ፎርሚ ብዝተሳኸዐ ተላኢኹ ኣሎ! ነመስግን:: መፍለጢ ናብቲ መማኸሪ ተላኢኹ ኣሎ ኢንተርኔት ኣብሪሆም ኣብ ዋትስኣብ ይፀበዩ።")
            st.balloons()
            
            st.info(f"**መጠቓለሊ (Notification Sent):**\n\n"
                    f"👤 ዓሚል (Client): {name}\n"
                    f"📞 ስልኪ ቁፅሪ (Phone): {phone}\n"
                    f"💼 ግልጋሎት (Service): {service}\n"
                    f"📧 Email Sent To: shewet2015@gmail.com")




      
           
            
   

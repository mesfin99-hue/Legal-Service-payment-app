import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import io
import openai  # Optional: Used for transcribing audio via Whisper API

# --- Page Configurations ---
st.set_page_config(page_title="Legal Services Intake", page_icon="⚖️", layout="centered")

# --- Custom Styling (Cyan Background, Blue Fonts) ---
custom_css = """
<style>
    .stApp { background-color: #00FFFF !important; }
    html, body, p, h1, h2, h3, h4, h5, h6, span, label, li, div {
        color: #0000FF !important;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        color: #0000FF !important;
        border: 2px solid #0000FF !important;
        background-color: #FFFFFF !important;
        font-weight: bold;
    }
    .stCheckbox label p {
        color: #0000FF !important;
        font-weight: bold;
    }
    div[data-testid="stForm"] {
        border: 3px solid #0000FF !important;
        background-color: rgba(0, 0, 0, 0.2);
        border-radius: 12px;
        padding: 25px;
    }
    div.stButton > button:first-child {
        background-color: #0000FF !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 30px !important;
        cursor: pointer;
    }
    div.stButton > button:first-child:hover {
        background-color: #87CEEB !important;
        color: white !important;
    }
    .payment-box {
        border: 2px dashed #0000FF;
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Helper Function to Transcribe Audio (Optional OpenAI Whisper Integration) ---
def transcribe_audio(audio_bytes):
    try:
        # Requires: pip install openai and st.secrets["OPENAI_API_KEY"]
        client = openai.OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        return transcript.text
    except Exception as e:
        return f"[Audio transcription unavailable or failed: {str(e)}]"

# --- Email Notification Function ---
def send_email_notification(client_name, client_phone, selected_service, payment_method, case_details, attached_file, audio_bytes=None):
    sender_email = "maregawi99@gmail.com"
    sender_password = "idxd yaqi nydu kjec"  # Note: Use st.secrets in production
    receiver_email = "maregawi99@gmail.com"
    
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
    Payment Method Selected: {payment_method}
    Payment Number: +251914539226
    
    CASE DETAILS:
    -------------------------------------------
    {case_details}
    
    *Attached: Payment Receipt/Invoice and (if recorded) Client Audio Message.*
    """
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # Attach Invoice
    if attached_file is not None:
        payload = MIMEBase('application', 'octet-stream')
        payload.set_payload(attached_file.getvalue())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', f'attachment; filename={attached_file.name}')
        msg.attach(payload)
        
    # Attach Audio File (if present)
    if audio_bytes is not None:
        audio_payload = MIMEBase('audio', 'wav')
        audio_payload.set_payload(audio_bytes)
        encoders.encode_base64(audio_payload)
        audio_payload.add_header('Content-Disposition', 'attachment; filename=client_case_audio.wav')
        msg.attach(audio_payload)
        
    try:
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
st.title("ናይ ሕጊ ኣገልግሎት ንምርካብ ቅድመ ክፍሊት መፍለጢ ⚖️") 
st.write("እዚ ግልጋሎት ኩሉ ግዜ ንጉሆ ካብ ሰዓት 1:00 ክሳብ ሰዓት 6:00፣ ድሕሪ ሰዓት ካብ ሰዓት 9:00 ክሳብ ሰዓት 2:00 ምሸት እዩ። በይዘኦም ዝደልይዎ ዓይነት ኣገልግሎት መሪፆም ክፍሊት ዝፈፀሙሉ ደረሰይ የተሓሕዙ። ካብኡ ናይ ጉዳዮም ዝርዝር ሓበሬታ የቐምጡ።")

# Price breakdown table
st.subheader("ናይ ኣገልግሎት ዋጋ ዝርዝር (Pricing Structure)")
pricing_data = {
    "ናይ ኣገልግሎት ዓይነት (Service Type)": [
        "ንምምኻር (Consultation)",
        "ክሲ ንምፅሓፍ (Statement of Claim)",
        "መልሲ ንምፅሓፍ (Statement of Defense)",
        "ውዕሊ ንምፅሓፍ (Drafting Contract)",
        "መመልከቲታት (ውርሲ፣ ሽም ምቕያር፣ ሞግዚት ንምሻም)",
        "ኣብ ቤት ፍርዲ ጥብቅና ንምቛም (Represention in Court)",
        "ንኻልኦት (Other Applications)"
    ],
    "ዋጋ (Price)": ["1000 ብር", "3000 ብር", "2000 ብር", "5000 ብር", "1000 ብር", "10%", "3000 ብር"]
}
st.table(pricing_data)

st.write("---")

# Audio input placed outside st.form for live updates/transcription
st.subheader("🎙️ ናይ ድምፂ መመልከቲ (Voice Case Input)")
st.write("ናይ ጉዳዮም ዝርዝር ብድምፂ ንምልኣኽ ኣብ ታሕቲ ዘሎ መቐረቢ ድምፂ ይተቀምጡ (Record your case details via voice below):")
recorded_audio = st.audio_input("ተዛረቡ (Record Audio)")

transcribed_text = ""
audio_bytes = None

if recorded_audio:
    audio_bytes = recorded_audio.read()
    st.audio(audio_bytes, format="audio/wav")
    with st.spinner("ድምፅኹም ናብ ፅሑፍ ኣብ ምቕያር ይርከብ... (Transcribing audio...)"):
        transcribed_text = transcribe_audio(audio_bytes)

# Main Client Form
with st.form("legal_intake_form"):
    st.subheader("ናይ ዓሚል ድሌት መግለፂ ፎርሚ (Client Intake Form)")
    
    name = st.text_input("ሙሉእ ሽም (Full Name)")
    phone = st.text_input("ስልኪ ቁፅሪ (Phone Number)")
    
    service = st.selectbox(
        "ዝደልይዎ ኣገልግሎት (Choose Service):",
        [
            "ንምምኻር — 1000 ብር",
            "ክሲ ንምፅሓፍ — 3000 ብር",
            "መልሲ ንምፅሓፍ — 2000 ብር",
            "ውዕሊ ንምፅሓፍ — 5000 ብር",
            "መመልከቲታት (ውርሲ፣ ሽም ምቕያር፣ ሞግዚት ንምሻም) — 1000 ብር",
            "ኣብ ቤት ፍርዲ ጥብቅና ንምቛም — 10%",
            "ንኻልኦት — 3000 ብር"
        ]
    )
    
    st.write("#### ናይ ክፍሊት መማረፂታት (Payment Options)")
    st.markdown("""
    <div class="payment-box">
        <p style="margin-bottom: 5px;"><strong>ከፍሊት ዝፍፅምሉ ቁፅሪ (Payment Account / Number):</strong></p>
        <p style="font-size: 20px; font-weight: bold; margin-bottom: 5px;">📱 +251914539226</p>
        <p style="margin-bottom: 0px;">በዚ ቁፅሪ ብ <strong>Telebirr</strong> ወይ ብ <strong>CBE Birr</strong> ክፍሊት ይፈፅሙ።</p>
    </div>
    """, unsafe_allow_html=True)
    
    payment_method = st.radio(
        "ዝኸፍልሉ መንገዲ ይምረፁ (Select Your Payment Method):",
        ["Telebirr", "CBE Birr"]
    )
    
    invoice = st.file_uploader("ዝኸፈልሉ ደረሰይ ይኹን ካልእ መረዳእታ ኣብዚ የተሓሕዙ (Attach Paid Invoice / Receipt)", type=["pdf", "png", "jpg", "jpeg"])
    confirmed = st.checkbox("ትኽክለኛ ክፍሊት ምኽፋለይ የረጋግፅ (I confirm that I have paid the required amount)")
    
    st.write("#### ናይ ጉዳዮም ዝርዝር መግለፂ (Case Details)")
    
    # Autofills text area if voice was recorded, but allows client to manually type/edit
    initial_text = transcribed_text if transcribed_text else ""
    details = st.text_area(
        "ናይ ጉዳዮም ዝርዝር መግለፂ ኣብዚ ይፅሓፉ ወይ ብድምፂ ዘእተውዎ ኣብዚ ይርኣዩ (Write or edit your case details here):",
        value=initial_text,
        height=250
    )
    
    submit_btn = st.form_submit_button("ለኣኽ (Submit)")

# --- Submission Logic Handler ---
if submit_btn:
    if not name or not phone:
        st.error("በይዘኦም ሽሞም፣ ኢመይሎምን ስልኪ ቁፅሮምን ይምልኡ (Please fill out Name and Phone Number).")
    elif not invoice:
        st.error("በይዘኦም ናይ ክፍሊት መረጋገፂ ደረሰይ የተሓሕዙ (Please attach your payment invoice).")
    elif not confirmed:
        st.error("በይዘኦም ክፍሊት ምፍፃሞም ዘረጋግፅ ሳንዱቕ ይፅቀጡ (Please check the payment confirmation checkbox).")
    elif not details and not audio_bytes:
        st.error("በይዘኦም ናይ ጉዳዮም ዝርዝር መብርሂ ይፅሓፉ ወይ ብድምፂ ይልኣኹ (Please write case details or record audio).")
    else:
        with st.spinner("ኣብ ምምሕልላፍ ይርከብ... በይዘኦም ይፀበዩ (Sending notification...)"):
            success = send_email_notification(
                name, phone, service, payment_method, details, invoice, audio_bytes=audio_bytes
            )
            
            if success:
                st.success("እቲ ዝመልኡዎ ፎርሚ ብዝተሳኸዐ ተላኢኹ ኣሎ! ነመስግን:: መፍለጢ ናብቲ ጠበቓ ተላኢኹ ኣሎ ኢንተርኔት ኣብሪሆም ኣብ ዋትስኣብ ይፀበዩ። ኣብ ውሽጢ 1:00 ሰዓት ዝደለይዎ እንተዘይመፅዩዎም ገንዘቦም ክምለሰሎም እዩ።")
                st.balloons()
            else:
                st.error("መፍለጢ ኣብ ምልኣኽ ፀገም ኣጋጢሙ። በይዘኦም ደጊሞም ይሞክሩ። (Failed to send email. Please try again.)")

import streamlit as st
import pandas as pd
import pyodbc
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import streamlit.components.v1 as components

# --- Load login password from secrets ---
APP_PASSWORD = st.secrets["APP_PASSWORD"]

# --- Check login ---
def check_login():
    st.title("🔒 لاگ ان درکار ہے")
    password = st.text_input("پاس ورڈ درج کریں:", type="password")
    if password == APP_PASSWORD:
        st.success("✅ درست پاس ورڈ")
        return True
    elif password != "":
        st.error("❌ غلط پاس ورڈ")
        return False
    else:
        st.warning("براہ کرم پاس ورڈ درج کریں")
        return False

# --- Streamlit Page Setup ---
st.set_page_config(page_title="📋 Crop Info App", layout="wide")
st.title("🌾 فصل کی معلومات کا سسٹم")
if not check_login():
    st.stop()

# --- Database connection using pymssql ---
def get_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={st.secrets['DB_SERVER']};"
            f"DATABASE={st.secrets['DB_NAME']};"
            f"UID={st.secrets['DB_USER']};"
            f"PWD={st.secrets['DB_PASSWORD']}",
            timeout=5
        )
        return conn
    except Exception as e:
        st.error("❌ ڈیٹا بیس کنکشن میں مسئلہ ہے۔")
        st.exception(e)
        st.stop()

# --- Load crop info view ---
@st.cache_data
def load_main_data():
    conn = get_connection()
    query = """
        SELECT 
            CropinfodetailID AS CinfoID,
            ud,
            other AS description,
            Square AS Murabba,
            AcreNo,
            CropID,
            Crop_Name,
            YouTubeLink,
            Remarks
        FROM View_CropInfoDetail
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- Load related images ---
def load_images(cinfoid):
    conn = get_connection()
    query = "SELECT CropInfoImage FROM tbl_CropInfoImage WHERE CropinfodetaillD = ?"
    df = pd.read_sql(query, conn, params=[cinfoid])
    conn.close()
    return df

# --- Embed YouTube video ---
def embed_youtube(url, width=720, height=400):
    if not url:
        st.info("ویڈیو دستیاب نہیں ہے۔")
        return

    video_id = None
    if "watch?v=" in url:
        video_id = url.split("watch?v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1].split("?")[0]
    elif "shorts/" in url:
        video_id = url.split("shorts/")[-1].split("?")[0]

    if video_id:
        embed_url = f"https://www.youtube.com/embed/{video_id}"
        iframe_html = f"""
            <iframe width="{width}" height="{height}" src="{embed_url}" 
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen></iframe>
        """
        components.html(iframe_html, height=height + 50)
    else:
        st.warning("❌ درست YouTube ویڈیو ID حاصل نہیں ہو سکی۔")

# --- Load and display grid data ---
data = load_main_data()
data_grid = data.head(6)

st.subheader("📊 تمام فصلوں کی تفصیل (Grid View)")

gb = GridOptionsBuilder.from_dataframe(data_grid)
gb.configure_selection(selection_mode="single", use_checkbox=False)
grid_options = gb.build()

grid_response = AgGrid(
    data,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    fit_columns_on_grid_load=True
)

selected_row_df = grid_response["selected_rows"]

if selected_row_df is None or selected_row_df.empty:
    st.warning("⚠️ براہ کرم کوئی قطار منتخب کریں۔")
    st.stop()
else:
    selected_data = selected_row_df.iloc[0].to_dict()

# --- Get selected data ---
#selected_data = selected_row_df[0]
selected_cinfoid = selected_data.get("CinfoID")

if not selected_cinfoid:
    st.error("🔴 منتخب قطار میں 'CinfoID' موجود نہیں ہے۔")
    st.stop()

st.success(f"✅ منتخب فصل ID: {selected_cinfoid}")

# --- Get full row by ID ---
row_data = data[data["CinfoID"] == selected_cinfoid]
if row_data.empty:
    st.error("🔴 مکمل ڈیٹا حاصل نہیں ہو سکا۔")
    st.stop()
row_data = row_data.iloc[0]

# --- Show crop details ---
st.markdown("---")
st.subheader(f"🔎 تفصیل: {row_data['Crop_Name']}  👤 **اپ ڈیٹ بائے**: {row_data['ud']}")
st.write(
    f"🧾 **تفصیل**: {row_data['description']}      "
    f"📍 **مربعہ**: {row_data['Murabba']}    "
    f"🌾 **ایکر نمبر**: {row_data['AcreNo']}  "
    f"🆔 **کروپ آئی ڈی**: {row_data['CropID']}"
)
st.write(f"🗒️ **ریمارکس**: {row_data['Remarks']}")

# --- Show related images ---
image_df = load_images(selected_cinfoid)
if not image_df.empty:
    st.markdown("### 🖼️ متعلقہ تصاویر")
    cols = st.columns(3)
    for i, row in image_df.iterrows():
        img = row["CropInfoImage"]
        if isinstance(img, (str, bytes)):
            with cols[i % 3]:
                st.image(img, use_container_width=True)
else:
    st.info("اس فصل کی کوئی تصویر موجود نہیں ہے۔")

# --- Show YouTube video ---
yt_link = row_data["YouTubeLink"]
if yt_link:
    st.markdown("---")
    st.subheader("🎬 متعلقہ ویڈیو")
    embed_youtube(yt_link)
else:
    st.info("ویڈیو دستیاب نہیں ہے۔")

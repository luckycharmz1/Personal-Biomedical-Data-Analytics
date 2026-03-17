# =========================
# Imports
# =========================
from pathlib import Path
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Biomedical Dashboard",
    layout="wide"
)

# =========================
# Sidebar Navigation
# =========================
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Data Viewer", "Graphs", "Contact"],
        icons=["house", "file-earmark-text", "bar-chart", "envelope"],
        menu_icon="cast",
        default_index=0
    )

# =========================
# Data Folder
# =========================
data_folder = Path("Samsung Health") / "my_data.csv"  # folder containing CSVs

# =========================
# HOME PAGE
# =========================
if selected == "Home":
    st.title("Charmaine's Biomedical Data Dashboard")

    st.markdown(
        """
        Welcome to my biomedical data exploration dashboard.

        This project bridges science and technology, combining my love
        for data with my lived experience with sickle cell anemia.

        From September 2025 to December 2025, I worked with a Stanford
        mentor to develop hypotheses about physiological patterns that may
        precede sickle cell crises.

        I have then to go on to conduct my own independent research on wearable 
        technology and sickle cell anemia. I greatly appreciate my mentor Dr. Nowah Afangbedii
        for giving me the knowleedge to conduct this independent research. 

        This dashboard explores trends in wearable data to identify
        meaningful patterns over time.

        ⚠️ This tool is exploratory and not intended for medical diagnosis.
        """
    )

    st.markdown("---")
    st.info("This is an evolving research and portfolio project.")
    st.markdown(
        """
        Here is the unofficial scientific research paper. 
        Currently, its only contents consists of the Obersavation and Hypothesis as of now. As it
        is not a completed experiment.
        
        Click here to read: "[Charmaine's Unofficial Scientific Research Paper](https://docs.google.com/document/d/1v469ivc47A7XoQT55V1xtfQh5k40MWHi3-0tb7b99n0/edit?usp=sharing)"
        """
    )

# =========================
# DATA VIEWER PAGE
# =========================
elif selected == "Data Viewer":
    st.header("Samsung Health Data Viewer")

    if not data_folder.exists() or not data_folder.is_dir():
        st.error(f"Folder '{data_folder}' does not exist.")
    else:
        all_files = [f for f in data_folder.glob("*.csv") if f.is_file()]

        if not all_files:
            st.warning("No CSV files found in the folder.")
        else:
            selected_file = st.selectbox(
                "Select dataset to view",
                all_files,
                format_func=lambda x: x.name
            )

            try:
                # Read CSV without headers
                df = pd.read_csv(selected_file, header=None, engine="python", on_bad_lines="skip")

                # Clean strings
                df = df.applymap(lambda x: str(x).replace('"', '').strip() if isinstance(x, str) else x)

                st.subheader("Preview")
                st.dataframe(df.head(), use_container_width=True)

                st.subheader("Basic Info")
                st.write(f"Rows: {df.shape[0]}")
                st.write(f"Columns: {df.shape[1]}")

            except pd.errors.EmptyDataError:
                st.warning(f"{selected_file.name} is empty and could not be loaded.")
            except Exception as e:
                st.error(f"Error reading file: {e}")

# =========================
# GRAPHS PAGE
# =========================
elif selected == "Graphs":
    st.header("Interactive Biomedical Graphs")

    if not data_folder.exists() or not data_folder.is_dir():
        st.error(f"Folder '{data_folder}' does not exist.")
    else:
        all_files = [f for f in data_folder.glob("*.csv") if f.is_file()]

        if not all_files:
            st.warning("No CSV files found in the folder.")
        else:
            # Let the user select which CSV to plot
            selected_file = st.selectbox(
                "Select dataset to visualize",
                all_files,
                format_func=lambda x: x.name
            )

            try:
                # Read CSV with headers if present, else fallback to no headers
                try:
                    df = pd.read_csv(selected_file, engine="python", on_bad_lines="skip")
                except pd.errors.ParserError:
                    df = pd.read_csv(selected_file, header=None, engine="python", on_bad_lines="skip")

                if df.empty:
                    st.warning("CSV file is empty.")
                else:
                    # Clean numeric columns
                    df_numeric = pd.DataFrame()
                    for col in df.columns:
                        temp_col = df[col].astype(str).str.replace(r"[^0-9.-]", "", regex=True)
                        df_numeric[col] = pd.to_numeric(temp_col, errors="coerce")

                    numeric_cols = [c for c in df_numeric.columns if df_numeric[c].count() > 0]

                    if not numeric_cols:
                        st.warning("No numeric columns found to plot.")
                    else:
                        metric = st.selectbox("Select metric to analyze", numeric_cols)

                        st.subheader(f"{metric} from {selected_file.name}")
                        st.line_chart(df_numeric[metric])

            except Exception as e:
                st.error(f"Error processing {selected_file.name}: {e}")

# =========================
# CONTACT PAGE
# =========================
elif selected == "Contact":
    st.header("Contact")

    st.markdown(
        "🌐 Connect with me here: "
        "[Charmaine's Linktree](https://linktr.ee/the.real.charmainee)"
    )

    st.write("Thank you for supporting biomedical data exploration.")
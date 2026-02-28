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
# Data Folder (FIXED)
# =========================
data_folder = Path("Samsung Health")


# =========================
# HOME PAGE
# =========================
if selected == "Home":
    st.title("Charmaine's Biomedical Data Dashboard")

    st.markdown(
        """
        Welcome to my biomedical data exploration dashboard.

        This project bridges *science and technology*, combining my love
        for data with my lived experience with *sickle cell anemia*.

        From September 2025 to December 2025, I worked with a Stanford
        mentor to develop hypotheses about physiological patterns that may
        precede sickle cell crises.

        This dashboard explores trends in wearable data to identify
        meaningful patterns over time.

        ⚠️ This tool is exploratory and not intended for medical diagnosis.
        """
    )

    st.markdown("---")
    st.info("This is an evolving research and portfolio project.")


# =========================
# DATA VIEWER PAGE
# =========================
elif selected == "Data Viewer":
    st.header("Samsung Health Data Viewer")

    if not data_folder.exists() or not data_folder.is_dir():
        st.error(f"Folder '{data_folder}' does not exist.")
    else:
        all_files = list(data_folder.glob("*.csv"))

        if not all_files:
            st.warning("No CSV files found in the folder.")
        else:
            selected_file = st.selectbox(
                "Select dataset to view",
                all_files,
                format_func=lambda x: x.name
            )

            try:
                df = pd.read_csv(selected_file, engine="python", on_bad_lines="skip")

                # Clean strings
                df = df.applymap(
                    lambda x: str(x).replace('"', '').strip()
                    if isinstance(x, str) else x
                )

                st.subheader("Preview")
                st.dataframe(df.head(), use_container_width=True)

                st.subheader("Basic Info")
                st.write(f"Rows: {df.shape[0]}")
                st.write(f"Columns: {df.shape[1]}")

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
        all_files = list(data_folder.glob("*.csv"))

        if not all_files:
            st.warning("No CSV files found in the folder.")
        else:
            selected_file = st.selectbox(
                "Select dataset",
                all_files,
                format_func=lambda x: x.name
            )

            try:
                df = pd.read_csv(selected_file, engine="python", on_bad_lines="skip")

                # Clean strings
                df = df.applymap(
                    lambda x: str(x).replace('"', '').strip()
                    if isinstance(x, str) else x
                )

                # Detect time columns
                time_cols = [
                    c for c in df.columns
                    if "time" in c.lower() or "date" in c.lower()
                ]

                for col in time_cols:
                    df[col] = pd.to_datetime(df[col], errors="coerce")

                # Detect numeric columns
                df_numeric = df.apply(pd.to_numeric, errors="coerce")
                numeric_cols = [
                    c for c in df_numeric.columns
                    if df_numeric[c].count() > 0
                ]

                if not numeric_cols:
                    st.warning("No numeric columns found.")
                else:
                    metric = st.selectbox(
                        "Select metric to analyze",
                        numeric_cols
                    )

                    # If time column exists → time-series analysis
                    if time_cols:
                        x_col = time_cols[0]

                        min_date = df[x_col].min()
                        max_date = df[x_col].max()

                        start_date, end_date = st.date_input(
                            "Select date range",
                            [min_date, max_date]
                        )

                        filtered_df = df[
                            (df[x_col] >= pd.to_datetime(start_date)) &
                            (df[x_col] <= pd.to_datetime(end_date))
                        ].copy()

                        # Rolling average
                        window = st.slider(
                            "Rolling Average Window (days)",
                            1, 30, 7
                        )

                        filtered_df["Rolling Avg"] = (
                            pd.to_numeric(filtered_df[metric], errors="coerce")
                            .rolling(window)
                            .mean()
                        )

                        st.subheader(f"{metric} Over Time")
                        st.line_chart(
                            filtered_df,
                            x=x_col,
                            y=[metric, "Rolling Avg"]
                        )

                        # Correlation Explorer
                        st.subheader("Correlation Explorer")

                        x_axis = st.selectbox(
                            "X-axis",
                            numeric_cols,
                            key="x_axis"
                        )

                        y_axis = st.selectbox(
                            "Y-axis",
                            numeric_cols,
                            index=1 if len(numeric_cols) > 1 else 0,
                            key="y_axis"
                        )

                        st.scatter_chart(
                            df_numeric,
                            x=x_axis,
                            y=y_axis
                        )

                    else:
                        st.line_chart(df_numeric[metric])

            except Exception as e:
                st.error(f"Error processing file: {e}")


# =========================
# CONTACT PAGE
# =========================
elif selected == "Contact":
    st.header("Contact")

    st.markdown(
        "🌐 Connect with me here: "
        "[Charmainee's Linktree](https://linktr.ee/the.real.charmainee)"
    )

    st.write("Thank you for supporting biomedical data exploration.")
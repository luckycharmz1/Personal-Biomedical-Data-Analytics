from pathlib import Path
import pandas as pd
import streamlit as st

# -------------------------
# Streamlit App Title
# -------------------------
st.title("Charmaine's Biomedical Data Dashboard")

# -------------------------
# Path to your Samsung Health folder
# -------------------------
data_folder = Path("Samsung Health") / "my_data.csv"

# -------------------------
# Check folder exists
# -------------------------
if not data_folder.exists() or not data_folder.is_dir():
    st.error(f"Folder {data_folder} does not exist or is not a folder.")
else:
    # -------------------------
    # List all files in the folder
    # -------------------------
    all_files = list(data_folder.iterdir())
    if not all_files:
        st.error("No files found in the folder.")
    else:
        # -------------------------
        # Let user select a file
        # -------------------------
        selected_file = st.selectbox(
            "Select dataset to view",
            all_files,
            format_func=lambda x: x.name
        )

        # -------------------------
        # Try to read the selected file
        # -------------------------
        try:
            # Read CSV safely, skipping bad lines
            df = pd.read_csv(selected_file, engine='python', on_bad_lines='skip')

            # -------------------------
            # Clean the data: remove quotes and extra spaces
            # -------------------------
            df_clean = df.applymap(lambda x: str(x).replace('"','').strip() if isinstance(x, str) else x)

            # -------------------------
            # Convert numeric-like columns
            # -------------------------
            df_numeric = df_clean.apply(pd.to_numeric, errors='coerce')
            numeric_cols = [c for c in df_numeric.columns if df_numeric[c].count() > 0]

            # -------------------------
            # Detect time columns
            # -------------------------
            time_cols = [c for c in df_clean.columns if "time" in c.lower() or "date" in c.lower()]
            for c in time_cols:
                df_clean[c] = pd.to_datetime(df_clean[c], errors='coerce')

            # -------------------------
            # Display Data Table
            # -------------------------
            st.subheader("Data Preview")
            st.dataframe(df_clean.head())

            # -------------------------
            # Plotting
            # -------------------------
            if numeric_cols:
                st.subheader("Line Chart of Numeric Data")
                if time_cols:
                    x_col = time_cols[0]  # Use first time column as x-axis
                    for col in numeric_cols:
                        st.line_chart(data=df_clean, x=x_col, y=col)
                else:
                    # No time column, just plot numeric columns
                    st.line_chart(df_numeric[numeric_cols])
            else:
                st.warning("No numeric columns found to plot.")

        except Exception as e:
            st.error(f"Could not read {selected_file.name}. Error: {e}")
            st.info("Some Samsung Health files may not be CSV-compatible. Try another file.")

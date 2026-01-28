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
            # Use python engine and skip bad lines for messy CSVs
            df = pd.read_csv(selected_file, engine='python', on_bad_lines='skip')
            st.success(f"Loaded {selected_file.name} successfully!")

            # -------------------------
            # Display first few rows
            # -------------------------
            st.subheader("Data Preview")
            st.dataframe(df.head())

            # -------------------------
            # Convert potential numeric columns
            # -------------------------
            df_numeric = df.apply(pd.to_numeric, errors='coerce')
            numeric_cols = df_numeric.columns[df_numeric.notna().any()]

            # -------------------------
            # Detect time columns
            # -------------------------
            time_cols = [c for c in df.columns if "time" in c.lower() or "date" in c.lower()]
            for c in time_cols:
                df[c] = pd.to_datetime(df[c], errors='coerce')

            # -------------------------
            # Plotting
            # -------------------------
            if len(numeric_cols) > 0:
                st.subheader("Numeric Data Plot")
                if time_cols:
                    # If time column exists, plot numeric columns against the first time column
                    x_col = time_cols[0]
                    for col in numeric_cols:
                        st.line_chart(data=df, x=x_col, y=col)
                else:
                    # No time column, just plot numeric columns
                    st.line_chart(df_numeric[numeric_cols])
            else:
                st.warning("No numeric columns found to plot.")

        except Exception as e:
            st.error(f"Could not read {selected_file.name}. Error: {e}")
            st.info("Some Samsung Health files may not be CSV-compatible. Try another file.")

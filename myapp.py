from pathlib import Path
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu


# -------------------------
# Sidebar Menu
# -------------------------
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Data Viewer", "Graphs", "Contact"],
        icons=["house", "file-earmark-text", "bar-chart", "envelope"],
        menu_icon="cast",
        default_index=0
    )

# -------------------------
# Path to your Samsung Health folder
# -------------------------
data_folder = Path("Samsung Health") / "my_data.csv"

# -------------------------
# Home Page
# -------------------------
if selected == "Home":
    st.header("Charmaine's Biomedical Dashboard")
    
    # Personal introduction paragraph
    st.markdown(
        """
        Welcome to my first biomedical data dashboard!  

        I'm still actively working on improving this app, so please be patient with me.  
        My goal is to **bridge science and technology**—combining my love for technology with my experience living with **sickle cell anemia**.  

        My love for science grew even deeper from **September 2025 to December 2025**, when my Stanford University mentor helped me form hypotheses to explore my curiosity about sickle cell anemia.  
        What started as a single question is now **becoming an app**.  

        Through this dashboard, I hope to create something **useful for sickle cell patients**—helping predict oncoming crises and potentially preventing them.  

        Thank you for visiting, and I hope you find the data here interesting!
        """
    )
    st.markdown("💡 This is a work in progress. Thank you for your patience!")
    st.markdown("---")  # horizontal line

# -------------------------
# Data Viewer Page
# -------------------------
elif selected == "Data Viewer":
    st.header("View Samsung Health Data")

    if not data_folder.exists() or not data_folder.is_dir():
        st.error(f"Folder {data_folder} does not exist or is not a folder.")
    else:
        all_files = list(data_folder.iterdir())
        if not all_files:
            st.warning("No files found in the folder.")
        else:
            selected_file = st.selectbox(
                "Select dataset to view",
                all_files,
                format_func=lambda x: x.name
            )

            try:
                # Read CSV safely, skipping bad lines
                df = pd.read_csv(selected_file, engine='python', on_bad_lines='skip')

                # Clean the data: remove quotes and extra spaces
                df_clean = df.applymap(lambda x: str(x).replace('"','').strip() if isinstance(x, str) else x)

                st.subheader("Data Preview")
                st.dataframe(df_clean.head())

            except Exception as e:
                st.error(f"Could not read {selected_file.name}. Error: {e}")

# -------------------------
# Graphs Page
# -------------------------
elif selected == "Graphs":
    st.header("Interactive Biomedical Graphs")

    if not data_folder.exists() or not data_folder.is_dir():
        st.error(f"Folder {data_folder} does not exist or is not a folder.")
    else:
        all_files = list(data_folder.glob("*.csv"))

        if not all_files:
            st.warning("No CSV files found in the folder.")
        else:
            selected_file = st.selectbox(
                "Select dataset to plot",
                all_files,
                format_func=lambda x: x.name
            )

            try:
                df = pd.read_csv(selected_file, engine='python', on_bad_lines='skip')
                df = df.applymap(lambda x: str(x).replace('"','').strip() if isinstance(x, str) else x)

                # Convert date/time columns
                time_cols = [c for c in df.columns if "time" in c.lower() or "date" in c.lower()]
                for c in time_cols:
                    df[c] = pd.to_datetime(df[c], errors='coerce')

                # Convert numeric columns
                df_numeric = df.apply(pd.to_numeric, errors='coerce')
                numeric_cols = [c for c in df_numeric.columns if df_numeric[c].count() > 0]

                if not numeric_cols:
                    st.warning("No numeric columns found to plot.")
                else:
                    metric = st.selectbox("Select metric to analyze", numeric_cols)

                    if time_cols:
                        x_col = time_cols[0]

                        # Date filter
                        min_date = df[x_col].min()
                        max_date = df[x_col].max()

                        start_date, end_date = st.date_input(
                            "Select date range",
                            [min_date, max_date]
                        )

                        filtered_df = df[
                            (df[x_col] >= pd.to_datetime(start_date)) &
                            (df[x_col] <= pd.to_datetime(end_date))
                        ]

                        # Rolling average slider
                        window = st.slider("Rolling average window (days)", 1, 30, 7)

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

                    else:
                        st.line_chart(df_numeric[metric])

            except Exception as e:
                st.error(f"Could not read {selected_file.name}. Error: {e}")
# -------------------------
# Contact Page
# -------------------------
elif selected == "Contact":
    st.header("Contact")
    st.write("You can reach out for questions or support.")
    
    # Add Linktree
    st.markdown(
        "🌐 Check out my links here: [Charmainee's Linktree](https://linktr.ee/the.real.charmainee)"
    )

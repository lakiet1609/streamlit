import streamlit as st
import pandas as pd
import io


def process_data(df):
    df = pd.read_excel('data.xlsx')
    grouped = df.groupby('ID')['URL'].apply(list)
    df_expanded = pd.DataFrame(grouped.tolist(), index=grouped.index)
    df_expanded.columns = [f'URL_{i+1}' for i in range(df_expanded.shape[1])]
    df_expanded.reset_index(inplace=True)
    df_expanded['ID'] = df_expanded['ID'].astype(str)
    return df_expanded

# File uploader that accepts Excel files.
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    processed_df = process_data(df)
    st.write(processed_df)
    
    # Save processed data to a BytesIO buffer
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        processed_df.to_excel(writer)
    output.seek(0)  # rewind the buffer to the beginning after writing

    # Download link
    st.download_button(
        label="Download processed Excel file",
        data=output,
        file_name='processed_urls.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
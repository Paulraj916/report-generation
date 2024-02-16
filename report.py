import streamlit as st
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import mm, inch
import os
import shutil
from zipfile import ZipFile
from io import BytesIO

def main():
    st.title("Student Data Filter")

    # File upload for input data
    uploaded_file = st.file_uploader("Upload input Excel file", type=["xlsx"])
    if uploaded_file is not None:
        input_file_path = "input.xlsx"
        with open(input_file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success("File uploaded successfully.")

        # Input fields
        marks_10th = st.number_input("Enter % Marks - 10th")
        marks_10th_radio = st.radio("Marks - 10th Comparison", ("Less Than", "Greater Than or Equal To"))

        marks_12th = st.number_input("Enter % Marks - 12th")
        marks_12th_radio = st.radio("Marks - 12th Comparison", ("Less Than", "Greater Than or Equal To"))

        graduation_agg = st.number_input("Enter CGPA")
        graduation_agg_radio = st.radio("Graduation Aggregate Comparison", ("Less Than", "Greater Than or Equal To"))

        current_backlogs_radio = st.radio("CB", ("No current backlogs", "Number of backlogs"))
        num_backlogs = 0
        num_backlogs_radio = 0
        if current_backlogs_radio == "Number of backlogs":
            num_backlogs = st.number_input("Enter the number of backlogs")
            num_backlogs_radio = st.radio("Backlogs Comparison", ("Less Than", "Greater Than or Equal To"))

        history_of_arrears_radio = st.radio("HOA", ("No HOA", "Number of HOA"))
        num_arrears = 0
        num_arrears_radio = 0
        if history_of_arrears_radio == "Number of HOA":
            num_arrears = st.number_input("Enter the number of HOA")
            num_arrears_radio = st.radio("Arrears Comparison", ("Less Than", "Greater Than or Equal To"))

        # Button to trigger filtering
        if st.button("Filter Data"):
            # Perform filtering based on user input
            filtered_data = filter_data(marks_10th, marks_10th_radio, marks_12th, marks_12th_radio,
                                        graduation_agg, graduation_agg_radio, current_backlogs_radio,
                                        num_backlogs, num_backlogs_radio, history_of_arrears_radio,
                                        num_arrears, num_arrears_radio, input_file_path)
            # Save filtered data to Excel
            output_folder = "output"
            os.makedirs(output_folder, exist_ok=True)
            output_file_path = os.path.join(output_folder, "demo1.pdf")
            save_to_pdf(filtered_data, output_file_path)

            # Create a zip file containing the output folder and its contents in memory
            buffer = BytesIO()
            with ZipFile(buffer, 'w') as zipf:
                for root, _, files in os.walk(output_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, output_folder)
                        zipf.write(file_path, arcname=arcname)

            # Provide a download link for the zip file with the correct file name and type
            st.download_button("Download Output Folder", buffer.getvalue(), file_name="output.zip", mime="application/zip")

            # Remove the temporary output folder
            shutil.rmtree(output_folder)

            # Cleanup files
            os.remove(input_file_path)


def filter_data(marks_10th, marks_10th_radio, marks_12th, marks_12th_radio,
                graduation_agg, graduation_agg_radio, current_backlogs_radio,
                num_backlogs, num_backlogs_radio, history_of_arrears_radio,
                num_arrears, num_arrears_radio, input_file_path):
    # Load sample data
    data = pd.read_excel(input_file_path, engine="openpyxl")  # Specify engine="openpyxl"

    # Filtering logic
    if marks_10th_radio == "Less Than":
        data = data.loc[data['10th'] < marks_10th]
    else:
        data = data.loc[data['10th'] >= marks_10th]

    if marks_12th_radio == "Less Than":
        data = data.loc[data['12th'] < marks_12th]
    else:
        data = data.loc[data['12th'] >= marks_12th]

    if graduation_agg_radio == "Less Than":
        data = data.loc[data['CGPA'] < graduation_agg]
    else:
        data = data.loc[data['CGPA'] >= graduation_agg]

    if current_backlogs_radio == "Number of backlogs":
        if num_backlogs_radio == "Less Than":
            data = data.loc[data['CB'] < num_backlogs]
        else:
            data = data.loc[data['CB'] >= num_backlogs]
    else:
        data = data.loc[data['CB'] == 0]

    if history_of_arrears_radio == "Number of HOA":
        if num_arrears_radio == "Less Than":
            data = data.loc[data['HOA'] < num_arrears]
        else:
            data = data.loc[data['HOA'] >= num_arrears]
    else:
        data = data.loc[data['HOA'] == 0]

    selected_columns = ['Student Name', '10th', '12th', 'CGPA',
                        'CB', 'HOA', 'Email ID', 'Mobile Number']
    data = data[selected_columns]

    return data


def save_to_pdf(df, output_file_path):
    pdf = SimpleDocTemplate(output_file_path, pagesize=(11 * inch, 20 * inch))

    data = [df.columns.tolist()] + df.values.tolist()

    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)

    pdf.build([table])


if __name__ == "__main__":
    main()

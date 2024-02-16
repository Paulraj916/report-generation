import streamlit as st
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import mm, inch


def main():
    st.title("Student Data Filter")

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
                                    num_arrears, num_arrears_radio)
        # Save filtered data to Excel
        save_to_excel(filtered_data)

def filter_data(marks_10th, marks_10th_radio, marks_12th, marks_12th_radio,
                graduation_agg, graduation_agg_radio, current_backlogs_radio,
                num_backlogs, num_backlogs_radio, history_of_arrears_radio,
                num_arrears, num_arrears_radio):
    # Load sample data
    data = pd.read_excel("tvk.csv", engine="openpyxl")  # Specify engine="openpyxl"
    
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

    if current_backlogs_radio == "Number of backlogs" :
        if num_backlogs_radio == "Less Than":
            data = data.loc[data['CB'] < num_backlogs]
        else:
            data = data.loc[data['CB'] >= num_backlogs]
    else:
        data = data.loc[data['CB'] == 0]

    if history_of_arrears_radio == "Number of HOA" :
        if num_arrears_radio == "Less Than":
            data = data.loc[data['HOA'] < num_arrears]
        else:
            data = data.loc[data['HOA'] >= num_arrears]
    else:
        data = data.loc[data['HOA'] == 0]

    selected_columns = ['Reg', 'Student Name','10th','12th', 'CGPA',
                       'CB', 'HOA','Email ID','Mobile Number']
    data = data[selected_columns]
    data

    return data

def save_to_excel(df):
    # df.to_excel("demo.xlsx", index=False)
     # Create a PDF document
    pdf = SimpleDocTemplate("demo1.pdf", pagesize=(11*inch, 20*inch))
    
    # Convert DataFrame to a list of lists for table creation
    data = [df.columns.tolist()] + df.values.tolist()
    
    # # Calculate column widths to fit within the page width
    # col_widths = [pdf.width / len(data[0]) for _ in range(len(data[0]))]
    
    # Create a table
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0,0), (-1,0), 12),
                        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                        ('GRID', (0,0), (-1,-1), 1, colors.black)])
    table.setStyle(style)
    
    # Add table to PDF
    pdf.build([table])

if __name__ == "__main__":
    main()

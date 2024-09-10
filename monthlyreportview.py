import streamlit as st
import pandas as pd

def emp_page():
    st.set_page_config(
        page_title="FlairMinds Software - Employee Details",
        page_icon=":bar_chart:",
        layout="wide"
    )    
    # Logo and company name
    col1, col2 = st.columns([1, 20])
    with col1:
        st.image("FlairMinds_logo.jfif")
    with col2:
        st.title("FlairMinds Software - **Employee Details**")

    uploaded_monthly_file ="processed_report_file.xlsx"

    if uploaded_monthly_file:
        pf = pd.read_excel(uploaded_monthly_file,sheet_name='Processed_Report')
        list_of_columns = ['Date', 'EntryExempt','Dayslogs','Dayslogs_OutTime','In_Out_Difference', 'ZymmrLoggedTime', 
                           'Typeofleaveapproved','EntryinTime', 'DateofLeaveApplication', 'Leavestatus','WorkingDay',
                           'ApprovalDate', 'Approvedonsamedate', 'Status', 'Unpaidstatus',
                           'Swappedholidaydate']

        emp_id = st.text_input('Enter Employee ID:',placeholder="Like EMP1...")
        filtered_data = pf[pf['Employee_Id'] == emp_id]
        selected_date = st.date_input('Select Date:')
        date1 = pf['Date1'].iloc[0]
        date1 = pd.to_datetime(date1,format="%d-%m-%Y")
        if selected_date.month == date1.month:
            day = selected_date.day     
            d = {}
            if not filtered_data.empty:
                for index,row in filtered_data.iterrows():
                    dates_unpaid=[]
                    dates_paid=[]
                    dates_half=[]
                    for day_value in range(1,32):
                        if f"Status{day_value}" in pf.columns:
                            value = row[f"Unpaidstatus{day_value}"]
                            value2=row[f'Status{day_value}']
                            if value2=="Half Day":
                                dates_half.append(row[f'Date{day_value}'])
                            if value=="Paid":
                                dates_paid.append(row[f'Date{day_value}'])
                            if value=="Unpaid":
                                dates_unpaid.append(row[f'Date{day_value}'])
                            elif value2=="Unpaid":
                                dates_unpaid.append(row[f'Date{day_value}'])

                data = {'Status': ["Paid"] * len(dates_paid) + ["Unpaid"] * len(dates_unpaid)+["Half Day"]*len(dates_half),
                        'Date': dates_paid + dates_unpaid+dates_half}
                df = pd.DataFrame(data)
                st.header(f"Employee Name: {filtered_data['Employee_Name'].iloc[0]}")
                st.table(df)
                st.header(f"**Basic Information for Employee Name {filtered_data['Employee_Name'].iloc[0]} on Day {day}:**")
                d["Employee ID"] = filtered_data['Employee_Id'].iloc[0]
                d["Employee Name"] = filtered_data['Employee_Name'].iloc[0]
                d["Team Lead Coordinator"] = filtered_data['TeamLeadCoordinator'].iloc[0]
                d["Paid Count On This Month"] = filtered_data['Paid_count'].iloc[0]
                d["UnPaid Count On This Month"] = filtered_data['Absence without approved leave(Full day unpaid)'].iloc[0]
                d["Half Day Off Count On This Month"] = filtered_data['Late entry without exemptions(Half day unpaid)'].iloc[0]            
                for column in list_of_columns:
                    col_data = filtered_data[f'{column}{day}']
                    d[f"{column}"] = col_data.iloc[0]
                df = pd.DataFrame.from_dict(d, orient='Index', columns=['Value'])
                st.table(df)
        else:
            st.write("Please Enter the Right EMP ID or Month...!!!")
    else:
        st.write("No data available. Please process the files on the main page first.")

if __name__ == "__main__":
    emp_page()
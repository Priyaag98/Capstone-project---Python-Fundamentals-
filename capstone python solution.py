# Import required libraries
import pandas as pd
import numpy as np

# -----------------------------
# Task 1: Create three dataframes and save as CSV
# -----------------------------

employee_data = {
    'ID': ['A001', 'A002', 'A003', 'A004', 'A005'],
    'Name': ['John Alter', 'Alice Luxumberg', 'Tom Sabestine', 'Nina Adgra', 'Amy Johny'],
    'Gender': ['M', 'F', 'M', 'F', 'F'],
    'City': ['Paris', 'London', 'Berlin', 'Newyork', 'Madrid'],
    'Age': [25, 27, 29, 31, 30]
}

df_employee = pd.DataFrame(employee_data)
df_employee.to_csv('Employee.csv', index=False)
print("Employee DataFrame:")
print(df_employee)

seniority_data = {
    'ID': ['A001', 'A002', 'A003', 'A004', 'A005'],
    'Designation Level': [2, 2, 3, 2, 3]
}

df_seniority = pd.DataFrame(seniority_data)
df_seniority.to_csv('Seniority.csv', index=False)
print("\nSeniority DataFrame:")
print(df_seniority)

project_data = {
    'ID': ['A001','A002','A003','A004','A005','A002','A005','A003','A001','A003','A001','A004','A004','A005'],
    'Project': ['Project 1','Project 2','Project 3','Project 4','Project 5','Project 6','Project 7','Project 8','Project 9','Project 10','Project 11','Project 12','Project 13','Project 14'],
    'Cost': [1002000, 2000000, 4500000, 5500000, np.nan, 680000, 400000, 350000, np.nan, 300000, 2000000, 1000000, 3000000, 200000],
    'Status': ['Finished','Ongoing','Finished','Ongoing','Finished','Failed','Finished','Failed','Ongoing','Finished','Failed','Ongoing','Finished','Finished']
}

df_project = pd.DataFrame(project_data)
df_project.to_csv('Project.csv', index=False)
print("\nProject DataFrame:")
print(df_project)

# -----------------------------
# Task 2: Fill missing Cost values using running average with for loop
# -----------------------------
cost_list = df_project['Cost'].tolist()
for i in range(len(cost_list)):
    if pd.isna(cost_list[i]):
        running_sum = sum([x for x in cost_list[:i] if not pd.isna(x)])
        running_count = len([x for x in cost_list[:i] if not pd.isna(x)])
        cost_list[i] = running_sum / running_count if running_count > 0 else 0

df_project['Cost'] = cost_list
print("\nTask 2 Output: Project DataFrame with missing costs replaced")
print(df_project)

# -----------------------------
# Task 3: Split Name into First Name and Last Name
# -----------------------------
df_employee[['First Name', 'Last Name']] = df_employee['Name'].str.split(' ', 1, expand=True)
df_employee.drop('Name', axis=1, inplace=True)
print("\nTask 3 Output: Employee DataFrame after splitting names")
print(df_employee)

# -----------------------------
# Task 4: Join all three dataframes into one "Final"
# -----------------------------
df_final = df_project.merge(df_employee, on='ID', how='left').merge(df_seniority, on='ID', how='left')
print("\nTask 4 Output: Combined Final DataFrame")
print(df_final)

# -----------------------------
# Task 5: Add Bonus column (5% for Finished projects)
# -----------------------------
df_final['Bonus'] = np.where(df_final['Status'] == 'Finished', df_final['Cost']*0.05, 0)
print("\nTask 5 Output: Final DataFrame with Bonus column")
print(df_final[['ID','Project','Cost','Status','Bonus']])

# -----------------------------
# Task 6: Demote designation for Failed projects and delete >4
# -----------------------------
df_final['Designation Level'] = np.where(df_final['Status'] == 'Failed', df_final['Designation Level'] + 1, df_final['Designation Level'])
df_final = df_final[df_final['Designation Level'] <= 4]
print("\nTask 6 Output: After demotion and removal of >4 designation level")
print(df_final[['ID','Project','Status','Designation Level']])

# -----------------------------
# Task 7: Add Mr./Mrs. prefix based on gender, drop gender
# -----------------------------
df_final['First Name'] = np.where(df_final['Gender']=='M', 'Mr. ' + df_final['First Name'], 'Mrs. ' + df_final['First Name'])
df_final.drop('Gender', axis=1, inplace=True)
print("\nTask 7 Output: Gender dropped and prefix added")
print(df_final[['ID','First Name','Last Name','City']])

# -----------------------------
# Task 8: Promote designation by 1 if Age > 29
# -----------------------------
df_final['Designation Level'] = np.where(df_final['Age'] > 29, df_final['Designation Level'] - 1, df_final['Designation Level'])
df_final['Designation Level'] = df_final['Designation Level'].clip(lower=1)
print("\nTask 8 Output: Designation promoted for Age > 29")
print(df_final[['ID','Age','Designation Level']])

# -----------------------------
# Task 9: Total project cost per employee
# -----------------------------
total_proj_cost = df_final.groupby(['ID', 'First Name'])['Cost'].sum().reset_index()
total_proj_cost.rename(columns={'Cost':'Total Cost'}, inplace=True)
print("\nTask 9 Output: Total Project Cost per Employee")
print(total_proj_cost)

# -----------------------------
# Task 10: Employees whose city contains letter 'o'
# -----------------------------
employees_with_o = df_final[df_final['City'].str.contains('o', case=False)]
print("\nTask 10 Output: Employees from cities containing 'o'")
print(employees_with_o[['ID','First Name','City']])

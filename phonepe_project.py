# -*- coding: utf-8 -*-
import pandas as pd

#1.1

df_state=pd.read_excel(r"C:\Users\mail4\OneDrive\Documents\Python Projects\phonepe-raw-data.xlsx",sheet_name=0)
df_state.head()

df_split=pd.read_excel(r"C:\Users\mail4\OneDrive\Documents\Python Projects\phonepe-raw-data.xlsx",sheet_name=1)
df_split.tail(10)

df_device=pd.read_excel(r"C:\Users\mail4\OneDrive\Documents\Python Projects\phonepe-raw-data.xlsx",sheet_name=2)
mid_idx=len(df_device)//2 
df_device.iloc[mid_idx-5:mid_idx+5]

df_district=pd.read_excel(r"C:\Users\mail4\OneDrive\Documents\Python Projects\phonepe-raw-data.xlsx",sheet_name=3)
df_district.head(10)
df_district.tail(10)

df_demo=pd.read_excel(r"C:\Users\mail4\OneDrive\Documents\Python Projects\phonepe-raw-data.xlsx",sheet_name=4)
df_demo.iloc[::10]

#1.2

file_name = r"C:\Users\mail4\OneDrive\Documents\Python Projects\phonepe-raw-data.xlsx"
sheets = ['State_Txn and Users','State_TxnSplit','State_DeviceData','District_Txn and Users','District Demographics']

for sheet in sheets:
  df = pd.read_excel(file_name, sheet_name=sheet)
  print(f'=== Summary Statistics for: {sheet} ===')
  print(df.describe())
  print('\n' + '=' * 50 + '\n')

for sheet in sheets:
  df = pd.read_excel(file_name, sheet_name=sheet)
  print(f'=== Data Types for: {sheet} ===')
  print(df.dtypes)
  print('\n' + '=' * 50 + '\n')
  
#1.3

for sheet in sheets:
  df = pd.read_excel(file_name, sheet_name=sheet)
  print(f'=== Missing Values Count for: {sheet} ===')
  print(df.isnull().sum())
  print('\n' + '=' * 50 + '\n')
  
for sheet in sheets:
  df = pd.read_excel(file_name, sheet_name=sheet)
  missing_pct = (df.isnull().sum() / len(df)) * 100
  print(f'=== Missing Percentage for: {sheet} ===')
  print(missing_pct[missing_pct > 0])
  print('\n' + '=' * 50 + '\n')
  
for sheet in sheets:
  df = pd.read_excel(file_name, sheet_name=sheet)
  missing_pct = (df.isnull().sum() / len(df)) * 100
  if missing_pct.max() > 0:
    max_col = missing_pct.idxmax()
    max_val = missing_pct.max()
    print(
        f'Dataset "{sheet}" -> Highest missing column: **{max_col}** with'
        f' **{max_val:.4f}%** missing values.'
    )
  else:
    print(f'Dataset "{sheet}" -> No missing values.')
  
#1.4

total_states = df_district['State'].nunique()
total_districts = df_district['District'].nunique()

print(f'Total Number of States: {total_states}')
print(f'Total Number of Districts: {total_districts}')

# Using the District Demographics sheet or District_Txn and Users sheet
# Count districts per state and find the maximum using idxmax()
state_district_counts = df_demo['State'].value_counts()
highest_state = state_district_counts.idxmax()
max_count = state_district_counts.max()

print(f'State with the highest number of districts: {highest_state} ({max_count} districts)')

#2.1

# Group by State and sum transactions and amount
state_summary = (df_state.groupby('State')[['Transactions', 'Amount (INR)']].sum().reset_index())

# Display in tabular format
print(state_summary.to_string(index=False))

# Sort by Transactions descending
sorted_states = state_summary.sort_values(by='Transactions', ascending=False)

print('=== Top 5 States by Transaction Volume ===')
print(sorted_states.head(5).to_string(index=False))

#2.2

# Group by State, Year, Quarter, and Transaction Type to sum total transactions
split_grouped = (df_split.groupby(['State', 'Year', 'Quarter', 'Transaction Type'])['Transactions'].sum().reset_index())
print(split_grouped)
# Find the row with the maximum transactions for each state, year, and quarter group
idx_max = split_grouped.groupby(['State', 'Year', 'Quarter'])['Transactions'].idxmax()
most_common_type = split_grouped.loc[idx_max]

# Display results
print(most_common_type.to_string(index=False))

#2.3

# Group by State and Brand, then sum registered users
device_grouped = (df_device.groupby(['State', 'Brand'])['Registered Users'].sum().reset_index())

# Find the brand with the max registered users for each state
idx_max_device = device_grouped.groupby('State')['Registered Users'].idxmax()
top_brand_per_state = device_grouped.loc[idx_max_device]

# Display results
print(top_brand_per_state.to_string(index=False))

#2.4

# Find the row index with max population for each state
idx_max_pop = df_demo.groupby('State')['Population'].idxmax()
top_district_pop = df_demo.loc[idx_max_pop, ['State', 'District', 'Population']]

# Display in tabular format
print(top_district_pop.to_string(index=False))

import matplotlib.pyplot as plt

# Sort for better plotting visualization
plot_data = top_district_pop.sort_values(by='Population', ascending=False)

plt.figure(figsize=(14, 8))
plt.barh(plot_data['State'], plot_data['Population'],color='skyblue')
plt.title('District with the Highest Population for Each State')
plt.xlabel('Population')
plt.ylabel('State')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='District')
plt.tight_layout()
plt.show()

#2.5

# Calculate overall ATV as total amount divided by total transactions
state_atv = (df_state.groupby('State').apply(lambda x: x['Amount (INR)'].sum() / x['Transactions'].sum()).reset_index(name='Overall ATV'))

print(state_atv.to_string(index=False))

sorted_atv = state_atv.sort_values(by='Overall ATV', ascending=False)

print('=== Top 5 States by ATV ===')
print(sorted_atv.head(5).to_string(index=False))

print('\n=== Bottom 5 States by ATV ===')
print(sorted_atv.tail(5).to_string(index=False))

#2.6

app_opens_summary = (df_state.groupby(['State', 'Year', 'Quarter'])['App Opens'].sum().reset_index())
print(app_opens_summary.to_string(index=False))

# Choose a state (e.g., 'Maharashtra')
selected_state = 'Maharashtra'
state_data = df_state[df_state['State'] == selected_state].copy()

# Combine Year and Quarter into a timeline column
state_data['TimePeriod'] = (state_data['Year'].astype(str) + '-Q' + state_data['Quarter'].astype(str))
trend_data = (state_data.groupby('TimePeriod')['App Opens'].sum().reset_index())

# Line plot
plt.figure(figsize=(10, 5))
plt.plot(trend_data['TimePeriod'],trend_data['App Opens'],marker='o',color='purple',linewidth=2)
plt.title(f'App Opens Trend Over Time in {selected_state}')
plt.xlabel('Year & Quarter')
plt.ylabel('Total App Opens')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

#2.7

# Find the most recent quarter in the dataset
max_year = df_split['Year'].max()
max_qtr = df_split[df_split['Year'] == max_year]['Quarter'].max()

recent_split = df_split[(df_split['Year'] == max_year) & (df_split['Quarter'] == max_qtr)]

# Pivot data for stacked/grouped bar chart (states on X-axis, transaction types as bars)
pivot_split = recent_split.pivot(index='State', columns='Transaction Type', values='Transactions').fillna(0)

# Plot bar chart
pivot_split.plot(kind='bar', figsize=(16, 7), width=0.8)
plt.title(f'Distribution of Transaction Types by State (Q{max_qtr} {max_year})')
plt.xlabel('State')
plt.ylabel('Total Transactions')
plt.xticks(rotation=90)
plt.legend(title='Transaction Type', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.show()

#2.8

# Extract unique district name and code mappings using drop_duplicates()
district_mapping = df_district[['State', 'District', 'Code']].drop_duplicates()

# Display first few rows of the mapping
print(district_mapping.head().to_string(index=False))

# Export to a CSV file
output_file = 'district_code_mapping.csv'
district_mapping.to_csv(output_file, index=False)

print(f'\nSuccessfully exported unique mappings to {output_file}')

#3.0

# 1. Aggregate district-level data to the state level by State, Year, and Quarter
district_agg = (df_district.groupby(['State', 'Year', 'Quarter'])[['Transactions', 'Amount (INR)', 'Registered Users']].sum().reset_index())

# 2. Merge aggregated district data with the state-level dataset for comparison
merged_df = pd.merge(df_state,district_agg,on=['State', 'Year', 'Quarter'],suffixes=('_state', '_district_sum'),)

# 3. Identify and display any discrepancies
discrepancies = merged_df[(merged_df['Transactions_state'] != merged_df['Transactions_district_sum'])| (merged_df['Amount (INR)_state'] != merged_df['Amount (INR)_district_sum'])| (merged_df['Registered Users_state']!= merged_df['Registered Users_district_sum'])]

print(f'Total comparison records: {len(merged_df)}')
print(f'Total discrepancies found: {len(discrepancies)}')

if len(discrepancies) > 0:
    print('\n=== Sample Discrepancies Found ===')
    print(discrepancies[['State','Year','Quarter','Transactions_state','Transactions_district_sum','Registered Users_state','Registered Users_district_sum',]].head(10).to_string(index=False))
else:
    print('No discrepancies found! State and district totals match perfectly.')
    
    
#4.1 
import seaborn as sns

# Assuming df_txn_users and df_demographics are loaded dataframes
# Group demographics by state if necessary
state_demographics =(df_demo.groupby("State")["Population"].sum().reset_index())
state_users = (df_state.groupby("State")["Registered Users"].sum().reset_index())

# Merge datasets
df_ratio = pd.merge(state_users, state_demographics, on="State")
df_ratio["User_to_Population_Ratio"] = (df_ratio["Registered Users"] / df_ratio["Population"])

# Display tabular result
print(df_ratio[["State", "Registered Users", "Population", "User_to_Population_Ratio"]])

# 2. Create a column chart
plt.figure(figsize=(12, 6))
sns.barplot(data=df_ratio, x="State", y="User_to_Population_Ratio", palette="viridis")
plt.xticks(rotation=90)
plt.title("Ratio of Users to Population by State")
plt.xlabel("State")
plt.ylabel("User-to-Population Ratio")
plt.tight_layout()
plt.show()


#4.2

# 1. Merge the df_district dataset with the df_demo dataset
merged_42 = pd.merge(df_district, df_demo, on=['State', 'District'], how='inner')

# 2. Calculate the correlation between population density and transaction volume
correlation = merged_42['Density'].corr(merged_42['Transactions'])
print(f"Correlation between Population Density and Transaction Volume: {correlation:.4f}")

# 3. Create a scatter plot to visualize the correlation
plt.figure(figsize=(10, 6))
sns.scatterplot(data=merged_42, x='Density', y='Transactions', alpha=0.5, color='b')
plt.title('Population Density vs Transaction Volume by District', fontsize=14)
plt.xlabel('Population Density (sq km)', fontsize=12)
plt.ylabel('Transactions', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

#4.3

# 1. Group by state using df_state to calculate total amount and registered users
state_agg = df_state.groupby('State')[['Amount (INR)', 'Registered Users']].sum()
state_agg['Avg Transaction Amount per User'] = state_agg['Amount (INR)'] / state_agg['Registered Users']

# Display results in a tabular format
print("=== Average Transaction Amount Per User by State ===")
print(state_agg[['Avg Transaction Amount per User']])

# 2. Identify top 5 and bottom 5 states
sorted_states = state_agg.sort_values(by='Avg Transaction Amount per User', ascending=False)

print("\n--- Top 5 States with Highest Average Transaction Amount per User ---")
print(sorted_states[['Avg Transaction Amount per User']].head(5))

print("\n--- Top 5 States with Lowest Average Transaction Amount per User ---")
print(sorted_states[['Avg Transaction Amount per User']].tail(5))

#4.4

# 1. Merge the df_device dataset with the df_state dataset on State, Year, and Quarter
merged_44 = pd.merge(df_device,df_state,on=['State', 'Year', 'Quarter'],suffixes=('_device', '_state'),)

# 2. Calculate the ratio of users using each device brand to the total registered users in each state
# (Note: df_device['Registered Users'] is users per brand, df_state['Registered Users'] is total registered users per state/quarter)
merged_44['Brand_User_Ratio'] = (merged_44['Registered Users_device'] / merged_44['Registered Users_state'])

# Display results in a tabular format
print('=== Device Brand Usage Ratio by State, Year, Quarter ===')
print(merged_44[['State', 'Year', 'Quarter', 'Brand', 'Brand_User_Ratio']].head(10))

# 3. Create a bar chart depicting the device brand usage ratio (e.g., averaged across all periods for each state/brand)
brand_summary = (merged_44.groupby(['State', 'Brand'])['Brand_User_Ratio'].mean().reset_index())

# Example visualization for a specific state (e.g., 'Andaman & Nicobar Islands')
sample_state = 'Andaman & Nicobar Islands'
state_data = brand_summary[brand_summary['State'] == sample_state]

plt.figure(figsize=(12, 6))
sns.barplot(data=state_data, x='Brand', y='Brand_User_Ratio', palette='viridis')
plt.title(f'Device Brand Usage Ratio in {sample_state}', fontsize=14)
plt.xlabel('Device Brand', fontsize=12)
plt.ylabel('Usage Ratio', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#5.1

# 1. Create a line plot showing total transactions and total transaction amount over time (Years and Quarters) for a selected state
selected_state = ('Karnataka')  # You can change this to your home state or any other state


# Filter data for the selected state and sort chronologically by Year and Quarter
state_time_df = df_state[df_state['State'] == selected_state].sort_values(by=['Year', 'Quarter'])
# Create a combined time period label (e.g., "2018-Q1")
state_time_df['Time_Period'] = (state_time_df['Year'].astype(str)+ '-Q'+ state_time_df['Quarter'].astype(str))

# Set up dual-axis or subplots to display both Transactions and Amount
fig, ax1 = plt.subplots(figsize=(14, 6))

# Plot Total Transactions on Primary Y-axis
color = 'tab:blue'
ax1.set_xlabel('Time Period (Year & Quarter)', fontsize=12)
ax1.set_ylabel('Total Transactions', color=color, fontsize=12)
ax1.plot(state_time_df['Time_Period'],state_time_df['Transactions'],color=color,marker='o',linewidth=2,label='Transactions',)
ax1.tick_params(axis='y', labelcolor=color)
plt.xticks(rotation=45)

# Create Secondary Y-axis for Total Amount (INR)
ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Total Amount (INR)', color=color, fontsize=12)
ax2.plot(state_time_df['Time_Period'],state_time_df['Amount (INR)'],color=color,marker='s',linewidth=2,linestyle='--',label='Amount (INR)',)
ax2.tick_params(axis='y', labelcolor=color)

plt.title(f'Total Transactions and Amount Over Time for {selected_state}',fontsize=14,)
fig.tight_layout()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()


#5.2

# 1. Filter df_split for a selected state, year, and quarter
selected_state = 'Karnataka'  # You can change this to any state
selected_year = 2020
selected_quarter = 1

subset_df = df_split[(df_split['State'] == selected_state) & (df_split['Year'] == selected_year) & (df_split['Quarter'] == selected_quarter)]

# 2. Create a pie chart showing the distribution of different transaction types
plt.figure(figsize=(9, 9))
plt.pie(subset_df['Transactions'],labels=subset_df['Transaction Type'],autopct='%1.1f%%',startangle=140,colors=plt.cm.Paired.colors,)
plt.title(f'Transaction Types Distribution in {selected_state} ({selected_year} Q{selected_quarter})',fontsize=14,)
plt.tight_layout()
plt.show()


#5.3

# 1. Filter df_demo (District Demographics) for a selected state
selected_state = 'Karnataka'  # You can change this to any state
state_demographics = df_demo[df_demo['State'] == selected_state]

# Sort districts by population density for better readability
state_demographics = state_demographics.sort_values( by='Density', ascending=False)

# 2. Create a bar plot showing the population density of districts
plt.figure(figsize=(14, 6))
sns.barplot( data=state_demographics, x='District', y='Density',palette='Blues_r',hue='District',legend=False,)
plt.title(f'Population Density of Districts in {selected_state}', fontsize=14)
plt.xlabel('District', fontsize=12)
plt.ylabel('Population Density (sq km)', fontsize=12)
plt.xticks(rotation=90)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
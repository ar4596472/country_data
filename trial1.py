# Importing required libraries
import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns

# Load your clustered dataset
clustered_dataset = pd.read_csv("Country_data.csv")

# Streamlit UI
st.title("Fund Allocation Based on Clustering")

# Input Section
st.sidebar.title("Input Section")

# Country Selection Dropdown
country_options = ['All Countries'] + clustered_dataset['country'].tolist()
selected_country = st.sidebar.selectbox("Select a Country:", country_options)

# Data Input Fields
gdpp = st.sidebar.number_input("Enter GDP per capita (gdpp):", min_value=0)
income = st.sidebar.number_input("Enter Net Income per person (Income):", min_value=0)
child_mort = st.sidebar.number_input("Enter Child Mortality (child_mort):", min_value=0)

submit_button = st.sidebar.button("Submit")

# Function to classify country
def classify_country(gdpp, income, child_mort):
    if gdpp > 50000 or income > 40000:
        return "Developed"
    elif gdpp < 10000 or income < 1000 or child_mort > 50:
        return "Underdeveloped"
    else:
        return "Developing"

# Function to plot graphs
def plot_graphs(filtered_data):
    fig = plt.figure(figsize=(18, 12))
    
    # Check if clustering columns exist in the filtered_data DataFrame
    if 'cluster_id_hc' in filtered_data.columns:
        
        # Scatterplots
        ax1 = fig.add_subplot(2, 3, 1, title="gdpp vs child_mort")
        ax2 = fig.add_subplot(2, 3, 2, title="gdpp vs income")
        ax3 = fig.add_subplot(2, 3, 3, title="income vs child_mort")
        
        sns.scatterplot(x='gdpp', y='child_mort', hue='cluster_id_hc', palette=['red', 'blue', 'green'], data=filtered_data, ax=ax1)
        sns.scatterplot(x='gdpp', y='income', hue='cluster_id_hc', palette=['red', 'blue', 'green'], data=filtered_data, ax=ax2)
        sns.scatterplot(x='income', y='child_mort', hue='cluster_id_hc', palette=['red', 'blue', 'green'], data=filtered_data, ax=ax3)
        
        # Rotate x-axis labels for better readability
        for ax in [ax1, ax2, ax3]:
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        
        plt.tight_layout()
        st.pyplot(fig)
        
    else:
        st.write("Cluster ID (Hierarchical) not available in the dataset for visualization.")
    
    # Close the figure to free up memory
    plt.close(fig)

# Output Section
if submit_button:
    st.header(f"Selected Country: {selected_country}")
    
    # Filter dataset based on country selection
    if selected_country == 'All Countries':
        filtered_data = clustered_dataset
    else:
        filtered_data = clustered_dataset[clustered_dataset['country'] == selected_country]
    
    # Display Cluster Information
    cluster_info_columns = ['country']
    if 'cluster_id_hc' in filtered_data.columns:
        cluster_info_columns.append('cluster_id_hc')
    if 'cluster_id_km' in filtered_data.columns:
        cluster_info_columns.append('cluster_id_km')
    
    cluster_info = filtered_data[cluster_info_columns]
    st.subheader("Cluster Information")
    st.write(cluster_info)
    
    # Display Country Classification
    st.subheader("Country Classification")
    if selected_country != 'All Countries':
        classification = classify_country(gdpp, income, child_mort)
        st.write(f"Country Classification: {classification}")
    
    # Visualization
    st.subheader("Visualization")
    plot_graphs(filtered_data)

# my_streamlit_app.py
import streamlit as st



import streamlit as st
import os
import sys
import numpy as np
import json
import MDAnalysis
import urllib.request
import yaml
import random

import pandas as pd
import math

def ShowTableGui(SortedQualities, quality):
    """
    Shows a table of simulation qualities against experimental data in a Streamlit app.

    :param SortedQualities: list of dictionaries to be shown, available in folder ``Data/Ranking/``
    :param quality: should be either ``TotalQuality`` or universal lipid name. First one shows the system total quality. Latter shows the individual lipid quality.
    """
    rounding = ['headgroup', 'sn-1', 'sn-2', 'total', 'tails', 'FFQuality']
    QualityTable = []
    
    for i in SortedQualities:
        StoredToTable = {}
        
        for k, v in i[quality].items():
            if k in rounding:
                if v and v != float("inf") and not math.isnan(v):
                    StoredToTable[k] = round(float(v), 2)
        
        StoredToTable['Forcefield'] = i['system']['FF']
        molecules = ''
        MolNumbers = ''
        for lipid in i['system']['COMPOSITION']:
            molecules += lipid + ':'
            MolNumbers += str(np.sum(i['system']['COMPOSITION'][lipid]['COUNT']))  + ':'
        StoredToTable['Molecules'] = molecules[:-1]
        StoredToTable['Number of molecules'] = ' (' + MolNumbers[:-1] + ')'
        StoredToTable['Temperature'] = i['system']['TEMPERATURE']
        StoredToTable['ID'] = i['system']['ID']
        
        QualityTable.append(StoredToTable)
    
    df = pd.json_normalize(QualityTable)
    st.table(df)




# Set page configuration to wide layout
st.set_page_config(layout="wide")


# This defines the path for the NMRlipids databank on your computer.
# Default is that this repository and the NMRlipids databank repository are cloned to the same folder.
# If this is not the case, change this to the folder where the NMRlipids databank repository is located.
databankPath = './Databank/'

# Path for the NMRlipids databank
databankPath = './Databank/'

# Access to functions defined in the NMRlipids databank
sys.path.insert(1, databankPath + '/Scripts/BuildDatabank/')
from databankLibrary import *

# Initialize the databank
systems = initialize_databank(databankPath)


# Sidebar title
st.sidebar.title("NMRlipids")

# Sidebar for page selection
page = st.sidebar.selectbox("Choose a page", ["Simulation Ranking", "Lipid Ranking", "POPC-CHOL Ranking"])


# Content for Ranking Tables page
if page == "Simulation Ranking":
    st.title("Ranking tables of simulations against experimental data")


    # Selectbox for choosing sorting criteria
    Fragments = ['total', 'tails', 'headgroup', 'FormFactor']
    SortBasedOn = st.selectbox('Select Sorting Criteria', Fragments)

    # Button to show sorted table
    if st.button('Show Sorted Table'):
        st.write(f'Sorted based on {SortBasedOn} quality')

        # Path to the ranking file
        FFrankingPath = databankPath + '/Data/Ranking/SYSTEM_' + SortBasedOn + '_Ranking.json'
        
        # Load ranking data
        with open(FFrankingPath) as json_file:
            FFranking = json.load(json_file)

        # Display the table
        ShowTableGui(FFranking, 'TotalQuality')

# Content for other pages...
elif page == "Lipid Ranking":
    st.title("Show ranking separately for each lipid")


    # Selectbox for choosing sorting criteria
    Fragments = ['total','sn-1','sn-2','headgroup']
    SortBasedOn = st.selectbox('Select Sorting Criteria', Fragments)

    # Button to show sorted table
    if st.button('Show Sorted Table'):
        st.write(f'Sorted based on {SortBasedOn} quality')

        # Path to the ranking file
        for lipid in lipids_dict:
            FFrankingPath = databankPath +  '/Data/Ranking/' + lipid + '_' + SortBasedOn + '_Ranking.json'
        
            # Load ranking data
            with open(FFrankingPath) as json_file:
                FFranking = json.load(json_file)

            # Display the table
            ShowTableGui(FFranking, lipid)


# Content for other pages...
elif page == "POPC-CHOL Ranking":
    st.title("Show sn-1 ranking only for systems with POPC and CHOLESTEROL")

        
    ### This is showing the ranking only for systems containing POPC and cholesterol
    
    FFrankingPath = databankPath + '/Data/Ranking/POPC_sn-1_Ranking.json'
    lipid = 'CHOL'
    
    
    with open(FFrankingPath) as json_file:
        FFranking = json.load(json_file)
    json_file.close()
    
    NewRank = []
    for i in FFranking:
        #print(i)
        #for tst in i:
        #    print(tst)
        if lipid in i['system']['COMPOSITION']:
            NewRank.append(i)
       
    ShowTableGui(NewRank,'POPC')










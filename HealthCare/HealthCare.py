#Change Working Directory
import os
os.chdir('/Users/mutturaj.baradol/Desktop/Health')

# import the dataset
import pandas as pd
donor = pd.read_csv('DonorDetails.csv',)
recipient = pd.read_csv('RecipientDetails.csv',)

#Copy Donor important columns to the recipient
recipient["DHLA_A"] = donor["HLA-A"]
recipient["DHLA_B"] = donor["HLA-B"]
recipient["DHLA_C"] = donor["HLA-C"]
recipient["DHLA_DR"] = donor["HLA-DR"]
recipient["DHLA_DQ"] = donor["HLA-DQ"]

#Create new columns based on score
recipient["Score_TOD"] = recipient["Time on dialysis (months)"]
recipient["Score_PIGF"] = recipient["Previous immunological graft failure, withing 3 months of transplantation"]
recipient["Score_AOR"] = recipient["Age"]
recipient["Score_AVF"] = recipient["Vascular access: Failed all AV Fistula sites (Y or N)"]
recipient["Score_AVFG"] = recipient["Vascular access: Failed AV Graft after failed all AV Fistula sites"]
recipient["Score_PRA"] = recipient["PRA%"]
recipient["Score_PLDT"] = recipient["Previous living donor transplantation (now needs transplantation again)"]
recipient["Score_NROPDD"] = recipient["Near relative of previous deceased donor, now requiring transplantation"]
recipient["Score_BLOOD_GROUP"] = recipient["Blood group"]

#Print and check the output
recipient

#Assigning weights based on the scoring rules defined
recipient.loc[ recipient['Score_PIGF'] == "Y", 'Score_PIGF'] = 3
recipient.loc[ recipient['Score_PIGF'] == "N", 'Score_PIGF'] = 0

recipient.loc[ recipient['Score_AOR'] == "<1 year", 'Score_AOR'] = 1
recipient.loc[ recipient['Score_AOR'] == "65+", 'Score_AOR'] = 0

recipient.loc[ recipient['Score_AVF'] == "Y", 'Score_AVF'] = 2
recipient.loc[ recipient['Score_AVF'] == "N", 'Score_AVF'] = 0

recipient.loc[ recipient['Score_AVFG'] == "Y", 'Score_AVFG'] = 4
recipient.loc[ recipient['Score_AVFG'] == "N", 'Score_AVFG'] = 0

recipient.loc[ recipient['Score_PLDT'] == "Y", 'Score_PLDT'] = 5
recipient.loc[ recipient['Score_PLDT'] == "N", 'Score_PLDT'] = 0

recipient.loc[ recipient['Score_NROPDD'] == "Y", 'Score_NROPDD'] = 5
recipient.loc[ recipient['Score_NROPDD'] == "N", 'Score_NROPDD'] = 0

recipient.loc[ recipient['Score_BLOOD_GROUP'] != 'O', 'Score_BLOOD_GROUP'] = 1
recipient.loc[ recipient['Score_BLOOD_GROUP'] == 'O', 'Score_BLOOD_GROUP'] = 4

#Print and check the output
recipient

#Replace 'NA' or 'NaN' with Zero's
recipient["Score_TOD"].fillna(0, inplace=True)
recipient["Score_PIGF"].fillna(0, inplace=True)
recipient["Score_AOR"].fillna(0, inplace=True)
recipient["Score_AVF"].fillna(0, inplace=True)
recipient["Score_AVFG"].fillna(0, inplace=True)
recipient["Score_PRA"].fillna(0, inplace=True)
recipient["Score_PLDT"].fillna(0, inplace=True)
recipient["Score_NROPDD"].fillna(0, inplace=True)
recipient["Score_BLOOD_GROUP"].fillna(0, inplace=True)


#Type cast to Int
recipient["Score_TOD"] = recipient["Score_TOD"].astype(int)
recipient["Score_PIGF"] = recipient["Score_PIGF"].astype(int)
recipient["Score_AOR"] = recipient["Score_AOR"].astype(int)
recipient["Score_AVF"] = recipient["Score_AVF"].astype(int)
recipient["Score_AVFG"] = recipient["Score_AVFG"].astype(int)
recipient["Score_PRA"] = recipient["Score_PRA"].astype(int)
recipient["Score_PLDT"] = recipient["Score_PLDT"].astype(int)
recipient["Score_NROPDD"] = recipient["Score_NROPDD"].astype(int)
recipient["Score_BLOOD_GROUP"] = recipient["Score_BLOOD_GROUP"].astype(int)

#Print the check the output
recipient

#Check Object Type
recipient["Score_TOD"].dtypes
recipient["Score_PIGF"].dtypes
recipient["Score_AOR"].dtypes
recipient["Score_AVF"].dtypes
recipient["Score_AVFG"].dtypes
recipient["Score_PRA"].dtypes
recipient["Score_PLDT"].dtypes
recipient["Score_NROPDD"].dtypes


#Type case Serial Number to float
recipient["S.No"] = recipient["S.No"].astype(float)

#Weight Score of Age of recipient and replace age 
import math
for recipient in [recipient]:
    recipient.loc[ recipient['Age'] == '<1 year', 'Age'] = 1
    recipient.loc[ recipient['Age'] == '65+', 'Age'] = 66
    recipient.loc[ recipient['Score_AOR'] <= 6, 'Score_AOR'] = 3
    recipient.loc[(recipient['Score_AOR'] > 6) & (recipient['Score_AOR'] <= 12), 'Score_AOR'] = 2
    recipient.loc[(recipient['Score_AOR'] > 12) & (recipient['Score_AOR'] <= 18), 'Score_AOR'] = 1
    recipient.loc[(recipient['Score_AOR'] > 18), 'Score_AOR'] = 0
    
#Create Column 'HLA_MATCH' fillNa's and type cast to int
recipient['HLA_MATCH'] = recipient['Age']
recipient["HLA_MATCH"].fillna(0, inplace=True)
recipient["HLA_MATCH"] = recipient["HLA_MATCH"].astype(int)

# Weight HLA_MATCH based on the rules defined
HLA_Match = 0;
for x in recipient.index : #: range(0,5)
    HLA_Match = 0;
    if recipient['Unacceptable HLA-A'][x] != recipient['DHLA_A'][x] and recipient['HLA-A'][x] == recipient['DHLA_A'][x] :
        HLA_Match += 2
    else :
        HLA_Match = -1
    if recipient['Unacceptable HLA-B'][x] != recipient['DHLA_B'][x] and recipient['HLA-B'][x] == recipient['DHLA_B'][x] :
        HLA_Match += 2
    else :
        HLA_Match = -1
    if recipient['Unacceptable HLA-C'][x] != recipient['DHLA_C'][x] and recipient['HLA-C'][x] == recipient['DHLA_C'][x] :
        HLA_Match += 1
    else :
        HLA_Match = -1
    if recipient['Unacceptable HLA-DR'][x] != recipient['DHLA_DR'][x] and recipient['HLA-DR'][x] == recipient['DHLA_DR'][x] :
        HLA_Match += 3
    else :
        HLA_Match = -1
    if recipient['Unacceptable HLA-DQB1'][x] != recipient['DHLA_DQ'][x] and recipient['HLA-DQB1'][x] == recipient['DHLA_DQ'][x] :
        HLA_Match += 1
    else :
        HLA_Match = -1
    print x, recipient['Blood group'][x], HLA_Match
    recipient['HLA_MATCH'][x] = HLA_Match

#Print and check the output
recipient

#Find priority by adding the scores
recipient['priority'] = recipient["Score_TOD"] + recipient['Score_PIGF'] + recipient['Score_AOR'] + recipient['Score_AVF'] + recipient['Score_AVFG'] + recipient['Score_PRA']+ recipient['Score_PLDT']+ recipient['Score_NROPDD']+ recipient['Score_BLOOD_GROUP']+ recipient['HLA_MATCH']

#Remove recipients with un acceptable HLA's
recipient = recipient[recipient.HLA_MATCH != -1]
recipient = recipient[recipient.HLA_MATCH != 0]

# Find how many recipients with age < 18
recipient_TEEN = recipient[recipient.Age <= 18]

# print and check the output
recipient_TEEN

#Find how many recipients with age > 18
recipient_ADULT = recipient[recipient.Age > 18]

#Print and check the output
recipient_ADULT

#Sort the recipient based on the priority, higher the better
recipient_ADULT = recipient_ADULT.sort_values(['priority'], ascending=[0])

#Print and check the output
recipient_ADULT

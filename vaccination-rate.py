# In[1]
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# In[2]
vaccine_data = pd.read_excel(
    r'E:\GIS\VaccinationRate\vaccine.xlsx', skiprows=[0])

# In[3]

vaccine_data = vaccine_data[['Tỉnh/Thành phố',
                             'Dân số (người)', 'Số liều vaccine']]
vaccine_data.rename(columns={'Tỉnh/Thành phố': 'District',
                    'Dân số (người)': 'Population', 'Số liều vaccine': 'Vaccine'}, inplace=True)


# In[4]
count = len(vaccine_data['Population'])
for i in range(0, count):
    pop = vaccine_data['Population'][i]
    new_pop = float(pop.replace(".", ""))
    vaccine_data.replace(pop, new_pop, inplace=True)


# In[5]

nep_districts = gpd.read_file(
    r'E:\GIS\VaccinationRate\VNM_adm\VNM_adm1.shp')

nep_districts = nep_districts[['NAME_1', 'geometry']]
nep_districts.rename(columns={'NAME_1': 'District'}, inplace=True)

nep_districts.to_crs(epsg=32645, inplace=True)

# In[6]
vaccine_data.replace('Đắk Nông', 'Đăk Nông', inplace=True)
vaccine_data.replace('Thành phố Hồ Chí Minh',
                     'Hồ Chí Minh city', inplace=True)
vaccine_data.replace('Thừa Thiên Huế', 'Thừa Thiên - Huế', inplace=True)

for index, row in nep_districts['District'].iteritems():
    if row in vaccine_data['District'].tolist():
        pass
    else:
        print('The district ', row, ' is NOT in the vaccine_data list')

# In[7]
nep_districts = nep_districts.merge(vaccine_data, on='District')
# In[8]
nep_districts['Vaccination Rate (%)'] = (nep_districts['Vaccine'] /
                                         nep_districts['Population']) * 100
# In[9]
nep_districts.plot(column='Vaccination Rate (%)',
                   cmap='Spectral', legend=True, figsize=(6, 12))

# %%

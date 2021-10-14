# In[1]
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


# In[2]
# data = pd.read_html(
#     'https://meta.vn/hotro/dien-tich-va-dan-so-cac-tinh-viet-nam-10058')

# for population_data in data:
#     print(population_data)

# population_data.to_excel(r'E:\GIS\PopulationVietNam\pop.xlsx')

# In[3]
vaccine_data = pd.read_excel(
    r'D:\DataBackupStudy\GIS\VaccinationRate\vaccine.xlsx', skiprows=[0])

# In[4]

vaccine_data = vaccine_data[['Tỉnh/Thành phố',
                             'Dân số (người)', 'Số liều vaccine']]
vaccine_data.rename(columns={'Tỉnh/Thành phố': 'District',
                    'Dân số (người)': 'Population', 'Số liều vaccine': 'Vaccine'}, inplace=True)


# In[5]
count = len(vaccine_data['Population'])
for i in range(0, count):
    pop = vaccine_data['Population'][i]
    new_pop = float(pop.replace(".", ""))
    vaccine_data.replace(pop, new_pop, inplace=True)


# In[6]

nep_districts = gpd.read_file(
    r'D:\DataBackupStudy\GIS\VaccinationRate\VNM_adm\VNM_adm1.shp')

nep_districts = nep_districts[['NAME_1', 'geometry']]
nep_districts.rename(columns={'NAME_1': 'District'}, inplace=True)

nep_districts.to_crs(epsg=32645, inplace=True)

# In[7]
vaccine_data.replace('Đắk Nông', 'Đăk Nông', inplace=True)
vaccine_data.replace('Thành phố Hồ Chí Minh',
                     'Hồ Chí Minh city', inplace=True)
vaccine_data.replace('Thừa Thiên Huế', 'Thừa Thiên - Huế', inplace=True)

for index, row in nep_districts['District'].iteritems():
    if row in vaccine_data['District'].tolist():
        pass
    else:
        print('The district ', row, ' is NOT in the vaccine_data list')

# In[8]
nep_districts = nep_districts.merge(vaccine_data, on='District')
# In[9]
nep_districts['Vaccination Rate (%)'] = (nep_districts['Vaccine'] /
                                         nep_districts['Population']) * 100
# In[10]
# nep_districts.plot(column='Vaccination Rate (%)',
#                    cmap='Spectral', legend=True, figsize=(6, 12))

# In[11]

nep_districts['coords'] = nep_districts['geometry'].apply(lambda x: x.representative_point().coords[:])
nep_districts['coords'] = [coords[0] for coords in nep_districts['coords']]

# In[12]
nep_districts.plot(column='Vaccination Rate (%)',
                   cmap='Spectral', legend=True, figsize=(20, 28))
for idx, row in nep_districts.iterrows():
    plt.annotate(s=row['District'], xy=row['coords'],
                 horizontalalignment='center')

# %%

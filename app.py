# importing  libraries 

import pandas as pd
import numpy as np #untuk menyebut angka random
import plotly.express as px
import streamlit as st

########################################################################################

#data_loc berfungsi sebagai pencari dimana lokasi file csv yang ingin kita import
data_loc = "vgsales.csv"


# Fungsi ini memuat data dan melakukan pembersihan data yang sangat mendasar.
def load_data():
	data = pd.read_csv(data_loc,na_values = ["N/A",""," "])
	data.dropna(inplace = True)
	data["Year"] = data["Year"].astype("int")
	data.set_index("Rank")
	temp = data["Year"]
	temp = temp[temp <= 2016]
	return data , temp

# Di sini data dikelompokkan berdasarkan atribut Tahun.
def groupingdata(data):
	x = data.groupby("Year")
	
	return x

#function calling

data , data_year = load_data()	

grouped_data = groupingdata(data)


########################################################################################
# Judul dan Subjudul untuk aplikasi web.

st.title("「 🎮 」 Video Game Sales「 🎮 」 ")
st.subheader("Kelompok 8 - Visualisasi Data")
st.markdown("Project ini dibuat untuk memenuhi tugas mata kuliah visualisasi data, yang dikerjakan oleh Saddam dan Kikik")

########################################################################################


st.header("Jajaran 10 Game Terlaris di Dunia : ")
other_sales = data[["Name","Global_Sales"]].head(20)

st.write(px.bar( other_sales,x = "Name" , y = "Global_Sales" , hover_data = ["Name" , "Global_Sales"] , color = "Global_Sales" ))
if st.checkbox("Show Raw Data",False):
	st.write(other_sales)
st.markdown("---")
########################################################################################

st.header("Jajaran Game Terlaris di berbagai belahan dunia : ")
check = st.selectbox("Pilih Negara" , ["Amerika Utara","Eropa","Jepang","Berbagai Negara"])

if check == "Amerika Utara":

	st.subheader("Game dengan Pendapatan Tertinggi di Amerika Utara.")
	other_sales = data[["Name","Year","NA_Sales"]].sort_values(by = "NA_Sales",ascending = False).head(20)
	st.write(px.bar(other_sales, x = "Name" , y = "NA_Sales" , hover_data = ["Name" , "NA_Sales"] , color = "NA_Sales"))
	st.markdown("Menurut data diatas, Game dengan pendapatan tertinggi di negara Amerika Utara adalah Wiisports dengan index 41.49 penjualan. Sedangkan untuk pendapatan terendah dinegara Amerika Utara dipegang oleh game dari Jepang yaitu Super Mario World dengan index 12.78.")

if check == "Eropa":

	st.subheader("Game dengan Pendapatan Tertinggi di Eropa.")
	other_sales = data[["Name","Year","EU_Sales"]].sort_values(by = "EU_Sales",ascending = False).head(20)
	st.write(px.bar(other_sales, x = "Name" , y = "EU_Sales" , hover_data = ["Name" , "EU_Sales"] , color = "EU_Sales"))
	st.markdown("Menurut data diatas, Game dengan pendapatan tertinggi di negara Eropa adalah Wiisports dengan index 29.02 penjualan. Sedangkan untuk pendapatan terendah dinegara Eropa dipegang oleh game Wii Fit Plus dengan index 8.59.")


if check == "Jepang":

	st.subheader("Game dengan Pendapatan Tertinggi di Jepang.")
	other_sales = data[["Name","Year","JP_Sales "]].sort_values(by = "JP_Sales ",ascending = False).head(10)
	st.write(px.bar(other_sales, x = "Name" , y = "JP_Sales " , hover_data = ["Name" , "JP_Sales "] , color = "JP_Sales "))
	st.markdown("Menurut data diatas, Game dengan pendapatan tertinggi di negara Jepang adalah Pokemon Red / Pokemon Blue dengan index 10.22 penjualan. Sedangkan untuk pendapatan terendah dinegara Jepang dipegang oleh game Monster Hunter Freedom 3 dengan index 4.87.")


elif check == "Berbagai Negara": 
	st.subheader("Game dengan Pendapatan Tertinggi di Berbagai Negara.")
	other_sales = data[["Name","Year","Other_Sales"]].sort_values(by = "Other_Sales",ascending = False).head(10)
	st.write(px.bar(other_sales, x = "Name" , y = "Other_Sales" , hover_data = ["Name" , "Other_Sales"] , color = "Other_Sales"))
	st.markdown("Menurut data diatas, Game dengan pendapatan tertinggi diberbagai negara adalah Grand Theft Auto: San Andreas (GTA) dengan index 10.57 penjualan. Sedangkan untuk pendapatan terendah diberbagai negara dipegang oleh game Nintendogs dengan index 2.75.")

if st.checkbox("Show Raw data",False):
	st.write(other_sales)

st.markdown("---")
########################################################################################

st.subheader("Genre dengan Pendapatan Tertinggi : ")
other_sales = data[["Genre","Global_Sales"]].groupby("Genre").agg("sum").sort_values(by = "Global_Sales",ascending = False)
other_sales["Genre"] = other_sales.index
st.write(px.bar(other_sales, x = "Genre" , y = "Global_Sales" , hover_data = ["Genre" , "Global_Sales"] , color = "Global_Sales"))
if st.checkbox("show Raw Data",False):
	st.write(other_sales)
st.markdown("Menurut data diatas, Genre Action menjadi salah satu genre yang paling banyak diminati dan mendapatkan pendapatan tertinggi dengan index 1735.55. Sedangkan untuk genre yang paling sepi peminat adalah genre strategy dengan index 173.27.")

st.markdown("---")	

########################################################################################

st.subheader("Publishers dengan Pendapatan Tertinggi : ")
other_sales = data[["Publisher","Global_Sales"]].groupby("Publisher").agg("sum").sort_values(by = "Global_Sales",ascending = False).head(20)
other_sales["Publisher"] = other_sales.index
st.write(px.bar(other_sales, x = "Publisher" , y = "Global_Sales" , hover_data = ["Publisher" , "Global_Sales"] , color = "Global_Sales"))
if st.checkbox("Show raw Data",False):
	st.write(other_sales)
st.markdown("Menurut data diatas, Publisher Nintendo menjadi salah satu publisher yang paling banyak diminati dan mendapatkan pendapatan tertinggi dengan index 1785.46. Sedangkan untuk publisher yang paling sepi peminat adalah midway games dengan index 69.29.")

st.markdown("---")	

########################################################################################

st.subheader("Publishers/Genre/Game dengan Pendapatan Tertinggi pada Tahun Tertentu : ")

user_input_year = st.text_input("Hanya Tersedia ditahun 1970 sampai 2016" , 2000)
user_input_field = st.selectbox("Pilih Jenis" , ["Publisher" , "Genre" , "Name"])
try:
	x1 = np.int32(user_input_year)
	if np.int32(user_input_year) not in list(data_year):
		st.write("Data Tidak Ditemukan")
	else:	
		specific_df= grouped_data.get_group(np.int32(user_input_year))[["Name" ,"Genre" , "Publisher", "Global_Sales"]]
		if len(list(specific_df["Name"])) <= 15:
			st.write(px.pie(specific_df, values = "Global_Sales" , names = user_input_field , width = 900))            
		else:                                                                         				
		
			st.write(px.pie(specific_df[specific_df["Global_Sales"] > 2], values = "Global_Sales" , names = user_input_field , width = 900))

		if st.checkbox("Show data" , False):
			st.write(specific_df)
except ValueError:
	st.write("Tulis yang benar")



st.markdown("---")

########################################################################################

st.subheader("Trends Berbagai Macam Video Games Di Setiap Negara Per Tahunnya")

# Select Box Untuk Pilihan Negara dan Tahun
selected_country = st.selectbox("Negara", ["Amerika Utara", "Eropa", "Jepang", "Berbagai Negara"])
selected_year = st.selectbox("Tahun", sorted(list(data["Year"].unique())))

# Source Code Untuk Filter Trends Negara dan Tahun
if selected_country == "Amerika Utara":
    filtered_data = data[data["Year"] == selected_year][["Name", "NA_Sales"]]
    title = "Trends Video Game Di Amerika Utara"
elif selected_country == "Eropa":
    filtered_data = data[data["Year"] == selected_year][["Name", "EU_Sales"]]
    title = "Trends Video Game Di Eropa"
elif selected_country == "Jepang":
    filtered_data = data[data["Year"] == selected_year][["Name", "JP_Sales "]]
    title = "Trends Video Game Di Jepang"
else:
    filtered_data = data[data["Year"] == selected_year][["Name", "Other_Sales"]]
    title = "Trends Video Game Di Berbagai Negara"

# Mengurutkan data berdasarkan kolom Sales secara menurun
filtered_data_sorted = filtered_data.sort_values(by=filtered_data.columns[1], ascending=False)

# Mengambil 10 data teratas
filtered_data_top_10 = filtered_data_sorted.head(10)

# Membuat Bar Chart
fig = px.bar(filtered_data_top_10, x=filtered_data.columns[1], y="Name", orientation="h", title=title)

# Set chart untuk axis label
fig.update_layout(xaxis_title="Sales", yaxis_title="Name")

# Menampilkan Grafik Bar Chart
st.plotly_chart(fig)

# st.subheader("Trends Berbagai Macam Video Games Di Setiap Negara Per Tahunnya")


# # Select Box Untuk Pilihan Negara dan Tahun
# selected_country = st.selectbox("Negara", ["Amerika Utara", "Eropa", "Jepang", "Berbagai Negara"])
# selected_year = st.selectbox("Tahun", sorted(list(data["Year"].unique())))

# # Source Code Untuk Filter Trends Negara dan Tahun
# if selected_country == "Amerika Utara":
#     filtered_data = data[data["Year"] == selected_year][["Name", "NA_Sales"]]
#     title = "Trends Video Game Di Amerika Utara"
# elif selected_country == "Eropa":
#     filtered_data = data[data["Year"] == selected_year][["Name", "EU_Sales"]]
#     title = "Trends Video Game Di Eropa"
# elif selected_country == "Jepang":
#     filtered_data = data[data["Year"] == selected_year][["Name", "JP_Sales "]]
#     title = "Trends Video Game Di Jepang"
# else:
#     filtered_data = data[data["Year"] == selected_year][["Name", "Other_Sales"]]
#     title = "Trends Video Game Di Berbagai Negara"

# # Membuat Line Chart
# fig = px.bar(filtered_data, x=filtered_data.columns[1], y="Name")

# # Set chart untuk judul dan axis label
# fig.update_layout(title=title, xaxis_title="Name", yaxis_title="Sales")

# # Memutar label sumbu-x sebesar -45 derajat. untuk meningkatkan view label sumbu-x ketika labelnya miring.
# fig.update_layout(xaxis_tickangle=-45)

# # DMenampilkan Grafik Line Chart
# st.plotly_chart(fig)

########################################################################################

# Membaca dataset
data = pd.read_csv("vgsales.csv")

# Judul
st.subheader("Statistik Penjualan Game Dari Tahun ke tahun")
st.markdown("Disarankan Untuk Mencoba Menggunakan Dataset Grand Theft Auto atau GTA")

# Select Box untuk Pilihan Nama Game
names = data['Name'].unique()  # Mendapatkan nama-nama game dari dataset
selected_name = st.selectbox("Pilih Nama Game", names)

# Filter dataset berdasarkan nama game yang dipilih
filtered_data = data[data['Name'] == selected_name][['Year', 'Global_Sales']]

# Membuat Line Chart
fig = px.line(filtered_data, x='Year', y='Global_Sales', title=f"Trends Penjualan {selected_name}")

# Set chart untuk axis label
fig.update_layout(xaxis_title="Tahun", yaxis_title="Penjualan Global")

# Menampilkan Grafik Line Chart
st.plotly_chart(fig)

########################################################################################

st.subheader("Progress Penjualan Berdasarkan Genre Setiap 5 Tahun")

# Filter data berdasarkan range tahun
start_year = min(data["Year"])
end_year = max(data["Year"])
selected_years = st.slider("Pilih Range Tahun", start_year, end_year, (start_year, end_year), format="%d")

# Select Box Untuk Pilihan Genre
selected_genre = st.selectbox("Genre", sorted(list(data["Genre"].unique())))

# Filter data berdasarkan genre dan range tahun yang dipilih
filtered_data = data[(data["Genre"] == selected_genre) & (data["Year"].between(selected_years[0], selected_years[1]))]

# Menghitung total penjualan per tahun
sales_per_year = filtered_data.groupby("Year")["Global_Sales"].sum().reset_index()

# Membuat Line Chart
fig = px.line(sales_per_year, x="Year", y="Global_Sales", title=f"Progress Penjualan Genre {selected_genre} Setiap 5 Tahun")

# Set chart untuk axis label
fig.update_layout(
    title_automargin=False,
    xaxis_title="Tahun",
    yaxis_title="Total Penjualan",
    xaxis=dict(
        tickformat="d"
    )
)

# Memutar label sumbu-x sebesar -45 derajat untuk meningkatkan tampilan label sumbu-x yang miring
fig.update_layout(xaxis_tickangle=-45)

# Menampilkan Grafik Line Chart
st.plotly_chart(fig)

########################################################################################

st.subheader("Progress Penjualan Berdasarkan Publisher Setiap 5 Tahun")

# Filter data berdasarkan range tahun
start_year = min(data["Year"])
end_year = max(data["Year"])
selected_years = st.slider("Pilih Range Tahun", start_year, end_year, (start_year, end_year), key="range_tahun")

# Select Box Untuk Pilihan Publisher
selected_publisher = st.selectbox("Publisher", data["Publisher"].unique(), key="pilihan_publisher")

# Filter data berdasarkan publisher dan range tahun yang dipilih
filtered_data = data[(data["Publisher"] == selected_publisher) & (data["Year"].between(selected_years[0], selected_years[1]))]

# Menghitung total penjualan per tahun
sales_per_year = filtered_data.groupby("Year")["Global_Sales"].sum().reset_index()

# Membuat Line Chart
fig = px.line(sales_per_year, x="Year", y="Global_Sales", title=f"Progress Penjualan Publisher {selected_publisher} Setiap Tahun")

# Set chart untuk axis label
fig.update_layout(xaxis_title="Tahun", yaxis_title="Total Penjualan")

# Memutar label sumbu-x sebesar -45 derajat untuk meningkatkan tampilan label sumbu-x yang miring
fig.update_layout(xaxis_tickangle=-45)

# Menampilkan Grafik Line Chart
st.plotly_chart(fig)

########################################################################################

st.subheader("Perbandingan Penjualan Tertinggi Antar 2 Genre Game Setiap Tahunnya")

# Select Box Untuk Pilihan Genre
selected_genre1 = st.selectbox("Genre 1", sorted(list(data["Genre"].unique())))
selected_genre2 = st.selectbox("Genre 2", sorted(list(data["Genre"].unique())))

# Filter data berdasarkan genre yang dipilih
filtered_data1 = data[data["Genre"] == selected_genre1]
filtered_data2 = data[data["Genre"] == selected_genre2]

# Menghitung penjualan tertinggi antara dua genre game pada setiap tahunnya
sales_comparison = pd.concat([filtered_data1.groupby("Year")["Global_Sales"].max(),
                              filtered_data2.groupby("Year")["Global_Sales"].max()], axis=1)
sales_comparison.columns = [selected_genre1, selected_genre2]
sales_comparison.reset_index(inplace=True)

# Mengubah struktur data menggunakan metode melt
sales_comparison_melted = pd.melt(sales_comparison, id_vars="Year", var_name="Genre", value_name="Penjualan Tertinggi")

# Membuat Bar Chart
fig = px.bar(sales_comparison_melted, x="Year", y="Penjualan Tertinggi", color="Genre",
             title="Perbandingan Penjualan Tertinggi Antar 2 Genre Game Setiap Tahunnya")

# Set chart untuk axis label
fig.update_layout(xaxis_title="Tahun", yaxis_title="Penjualan Tertinggi")

# Menampilkan Grafik Bar Chart
st.plotly_chart(fig)

########################################################################################

st.subheader("Perbandingan Penjualan Tertinggi Antar 2 Publisher Game Setiap Tahunnya")

# Select Box Untuk Pilihan Publisher
selected_publisher1 = st.selectbox("Publisher 1", data["Publisher"].unique())
selected_publisher2 = st.selectbox("Publisher 2", data["Publisher"].unique())

# Filter data berdasarkan publisher yang dipilih
filtered_data1 = data[data["Publisher"] == selected_publisher1]
filtered_data2 = data[data["Publisher"] == selected_publisher2]

# Menghitung penjualan tertinggi antara dua publisher game pada setiap tahunnya
sales_comparison = pd.concat([filtered_data1.groupby("Year")["Global_Sales"].max(),
                              filtered_data2.groupby("Year")["Global_Sales"].max()], axis=1)
sales_comparison.columns = [selected_publisher1, selected_publisher2]
sales_comparison.reset_index(inplace=True)

# Mengubah struktur data menggunakan metode melt
sales_comparison_melted = pd.melt(sales_comparison, id_vars="Year", var_name="Publisher", value_name="Penjualan Tertinggi")

# Membuat Bar Chart
fig = px.bar(sales_comparison_melted, x="Year", y="Penjualan Tertinggi", color="Publisher",
             title="Perbandingan Penjualan Tertinggi Antar 2 Publisher Game Setiap Tahunnya")

# Set chart untuk axis label
fig.update_layout(xaxis_title="Tahun", yaxis_title="Penjualan Tertinggi")

# Menampilkan Grafik Bar Chart
st.plotly_chart(fig)

########################################################################################

st.write('Deskripsi Datasets (EDA):')
kolom_deskripsi = ['NA_Sales', 'EU_Sales', 'JP_Sales ', 'Other_Sales', 'Global_Sales']
deskripsi_statistik = data[kolom_deskripsi].describe()
modus = data[kolom_deskripsi].mode().iloc[0]
deskripsi_statistik.loc['modus'] = modus
st.write(deskripsi_statistik)
        

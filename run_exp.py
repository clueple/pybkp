import streamlit as st 
import pandas as pd 
import datetime as dt 

# """ Setting1 """
url = r'https://github.com/clueple/pybkp'
version ='20220426'
ext = 'csv'
#template language source url
lang_url = 'https://github.com/clueple/pybkp/blob/main/lang20220426.csv'
#template expense.xlsx source url
exp_url = 'https://github.com/clueple/pybkp/blob/main/expense20220426.csv'

# """Setting2"""
# use the data structure to reverse lookup row/col index, and lookup row value
class data:
	def __init__(self):
		self.data_name = data_name

	@classmethod
	def get_url(cls, data_name:'str'):
		cls.url = f"{url}/blob/main/{data_name}{version}.{ext}"
		return cls.url

	@classmethod
	def get_table(cls,data_name:'str'):
		cls.table = pd.read_html(data.get_url(data_name))[0].drop('Unnamed: 0', axis=1)
		return cls.table

class ilookup: #index, either column or row index lookup, given a unique value in a predefined table
	def __init__(self, table_name:'str'):
		self.table_name = table_name

	def lookup_col(self, target_text:'str'): #look up for the column index given a value in a predefined table
		self.col = self.table_name.eq(target_text).any()
		self.col = self.col[self.col].index[0]
		return self.col
	def lookup_row(self, target_text:'str'): #look up for the row index given a value in a predefined table
		self.row = self.table_name.eq(target_text).any(axis=1)
		self.row = self.row[self.row].index[0]
		return self.row

#use  this function when the nav bar button is clicked for specific table
@st.cache
def retrieve_item(table_name, item_name, target_text): 
	retrieve = table_name.loc[ilookup(table_name).lookup_row(target_text),item_name] #retrieve the row value given the column name (item_name) and search text (target_text)
	return retrieve


#this is the blank expense.xlsx available for download
# temp_exp = get_template_data(exp_url).to_csv(index=False).encode('utf-8')
# exp_field = get_template_data(exp_url).columns

temp_exp = data.get_table(data_name='expense').to_csv().encode('utf-8')

#"""Setting 3 """
#define language table
lang = data.get_table(data_name='lang')
#language options available for selectbox, 'lang_choice'
lang_select = lang.apply(lambda x: x[x['code']], axis=1) #language choices availale for lang_choice dropbox

#"""Setting 4"""
field = data.get_table(data_name ='field')


#"""App Interface"""
def main():
	
	st.download_button(
		label='Download Template',
		data = temp_exp,
		file_name = 'expense.csv',
		mime ='text/csv'
		)

	upload_exp = st.file_uploader(
		label = 'Upload your expens file',
		type = ['csv'],
		key = 'upload_exp',
		)

	lang_choice = st.selectbox(f"Select language", lang_select) #language choice dropbox 
	lang_code = lang.loc[ilookup(lang).lookup_row(target_text=lang_choice), 'code'] # language code
	st.info(lang_code)

	with st.sidebar:
		st.write(
			st.write(retrieve_item(field, item_name=lang_code, target_text='inv_num'))
			)
	
if __name__== '__main__':
	main()




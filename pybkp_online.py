""" Python packages needed """
import streamlit as st 
import pandas as pd 
from streamlit_option_menu import option_menu as om 

# url for all the source tables (csv format)
url = r'https://github.com/clueple/pybkp'
version = r'20220426'
ext = 'csv'

#example source data of 'bank':  "  https://github.com/clueple/pybkp/blob/main/bank20220426.csv  " -> f"{url}/blob/main/{bank}20220426.csv"

data_name = [
'bank', #inter bank transactions
'bank_acct', #list of bank accounts and their associated GL account
'chartOfAcct', #list of GL accounts
'customer', #list of customers
'expense', #list of vendor invoices
'field', #list of items in different languages
'income', #list of sales invoices
'lang',#list of interface languages 
'payment',#list of payments to settle vendor invoices
'receipt', #list of payments to settle sales invoices
'table', #list of interface in different languages
'vendor' #list of vendors
]

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

@st.cache
def retrieve_item(table_name, item_name, target_text): #use  this function when the nav bar button is clicked for specific table
	retrieve = table_name.loc[ilookup(table_name).lookup_row(target_text),item_name] #retrieve the row value given the column name (item_name) and search text (target_text)
	return retrieve

#register settings

lang = data.get_table('lang')
field = data.get_table('field')
bank_acct = data.get_table('bank_acct')
chartOfAcct = data.get_table('chartOfAcct')
table = data.get_table('table')
vendor = data.get_table('vendor')


lang_select = lang.apply(lambda x: x[x['code']], axis=1) #language choices availale for lang_choice dropbox
lang_choice = st.selectbox(f"Select language", lang_select) #language choice dropbox 
lang_code = lang.loc[ilookup(lang).lookup_row(target_text=lang_choice), 'code'] # language code



with st.expander(f"Preview your language code:"):
	st.info(f"{lang_code}")
with st.expander('Preview Table Summary'):
	st.table(table)

#table displayed name based on reporting language 
table['display'] = table[lang_code]

# """ Table types """
backend = ['master'] #the master table that contains the pre-processed journal entry data should be hidden from the bookkeepers
setting = ['table', 'field', 'vendor', 'lang', 'chartOfAcct', 'bank_acct', 'customer'] #these tables are viewable but not editable by bookkeepers
bookkeep = ['expense','income','bank','payment','receipt']
report = ['journal', 'tb', 'pnl'] #these reports should only be accessed by the client management/owners and/or the accountant


def main():
	#the sidebar contains the buttons to link up with different interfaces specified in data table, 'table'
	with st.sidebar:
		selected = om('-',table['display'].to_list(), icons=['house','cloud-upload','list-task','gear'], menu_icon='cast', default_index=1,orientation='vertical')
		selected

	# if you click the button in the 'backend' catetory, it'll show the message to hide the backend
	if retrieve_item(table_name=table, item_name='table_name', target_text=selected) in backend:
		st.write('The backend is hidden from the bookkeepers')
	# if you click the button in the 'setting' category, you'll be able to view the respective data, but not able to edit 
	elif retrieve_item(table_name=table, item_name='table_name', target_text=selected) in setting:
		st.write(retrieve_item(table, 'table_name', selected))
		st.write(type(retrieve_item(table, 'table_name', selected)))
		st.write(f"url: {data.get_url(retrieve_item(table, 'table_name', selected))}")
		st.table(data.get_table(retrieve_item(table, 'table_name', selected)))
	# if you click the button in the 'bookkeep' category, you'll be prompted to enter data
	# elif retrieve_item(table_name=table, item_name='table_name', target_text=selected) in bookkeep:
	# 	st.write(f"You're working on {selected}")
	# 	st.write('create a form here')
	elif retrieve_item(table_name=table,item_name='table_name',target_text=selected) == 'expense':
		with st.form(key='expense', clear_on_submit=True):
			st.title(f"{retrieve_item(table, lang_code, selected)}")
			submit_exp = st.form_submit_button("submit")
	# if you click the button in the 'report' category, you can view the respective report
	elif retrieve_item(table_name=table, item_name='table_name', target_text=selected) in report:
		st.write('The reports are viewable by the client management/owner and/or the accountant only')
	else:
		st.write(f"Anything else?")


if __name__ == '__main__':
	main()


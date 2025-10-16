# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """
  Choose the fruits you want in your smoothie! 
  """
)

name_on_order = st.text_input("Name on smoothie:")
st.write("The name on your smoothie will be:", name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

available_fruits = st.multiselect(
                    'Choose up to 5 ingredients: ', my_dataframe, max_selections= 5 
)

if available_fruits:

    available_fruits_string = ''

    for fruit in available_fruits:
        available_fruits_string += fruit + ' '

    # st.write(available_fruits_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + available_fruits_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit Order')

    

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Hi {name_on_order}, Your Smoothie is ordered!", icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/orange")
sf_df = st.dataframe( data = smoothiefroot_response.json(), use_container_width = True)

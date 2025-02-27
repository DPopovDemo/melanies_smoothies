# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your order :cup_with_straw:")
st.write(
    """Welcome!
    """
)

order_name = st.text_input('Order Name:')
st.write('The name on your smoothie will be:', order_name)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    
    ingredients_string = ''

    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
        st.subheader(fruit + ' nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + order_name + """')"""

    #st.write(my_insert_stmt)
    #st.stop();
    time_to_insert = st.button('Submit Order')


    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,' + ' ' + order_name + '!', icon="✅")





    
    

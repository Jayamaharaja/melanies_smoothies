# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Form to customise your smoothie :)")
st.write(
    """Your smoothie can be customized with your fav fruits
    """
)

name_on_order= st.text_input('Name on smoothie')
st.write("Name on smoothie will be"+name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()
ingredients_list = st.multiselect(
    'choose upto 5 ingredients:',
    my_dataframe,
    max_selections = 5,
    placeholder = 'you can choose upto max of 5 fruits'
)

if ingredients_list:
    st.write(ingredients_list)
    ingredients_string = '';
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
        st.subheader(fruit + ' Nutritional Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit)
        fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width = True)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:

        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string +"""','"""+name_on_order+ """')"""
    
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")





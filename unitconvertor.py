import streamlit as st
from num2words import num2words

# Set up the app
st.set_page_config(page_title="Unit Converter", page_icon="🔄")
st.title("🔄 Unit Converter App")

# Sidebar with name and roll number
st.sidebar.header("User Information")
name = st.sidebar.text_input("Name:", "Your Name")
roll_number = st.sidebar.text_input("Roll Number:", "Your Roll Number")
st.sidebar.write(f"**Name:** {name}")
st.sidebar.write(f"**Roll Number:** {roll_number}")

# Conversion type selection in the sidebar
conversion_type = st.sidebar.selectbox("Select conversion type:", ['Length', 'Weight', 'Temperature', 'Area'])

# Conversion functions
def length_converter(value, from_unit, to_unit):
    length_units = {
        'Meters': 1,
        'Kilometers': 0.001,
        'Centimeters': 100,
        'Millimeters': 1000,
        'Miles': 0.000621371,
        'Yards': 1.09361,
        'Feet': 3.28084,
        'Inches': 39.3701
    }
    return value * (length_units[to_unit] / length_units[from_unit])


def weight_converter(value, from_unit, to_unit):
    weight_units = {
        'Kilograms': 1,
        'Grams': 1000,
        'Pounds': 2.20462,
        'Ounces': 35.274
    }
    return value * (weight_units[to_unit] / weight_units[from_unit])


def temperature_converter(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    elif from_unit == 'Celsius' and to_unit == 'Fahrenheit':
        return (value * 9/5) + 32
    elif from_unit == 'Fahrenheit' and to_unit == 'Celsius':
        return (value - 32) * 5/9
    elif from_unit == 'Celsius' and to_unit == 'Kelvin':
        return value + 273.15
    elif from_unit == 'Kelvin' and to_unit == 'Celsius':
        return value - 273.15
    elif from_unit == 'Fahrenheit' and to_unit == 'Kelvin':
        return (value - 32) * 5/9 + 273.15
    elif from_unit == 'Kelvin' and to_unit == 'Fahrenheit':
        return (value - 273.15) * 9/5 + 32


def area_converter(value, from_unit, to_unit):
    area_units = {
        'Square Meters': 1,
        'Square Kilometers': 0.000001,
        'Square Centimeters': 10000,
        'Square Millimeters': 1000000,
        'Square Miles': 3.861e-7,
        'Square Yards': 1.19599,
        'Square Feet': 10.7639,
        'Square Inches': 1550,
        'Acres': 0.000247105,
        'Hectares': 0.0001
    }
    return value * (area_units[to_unit] / area_units[from_unit])

# Enable input only for specific roll number
if roll_number == '289407':
    value = st.number_input("Enter value:", value=0.0)
else:
    st.warning("You are not authorized to enter a value. Roll Number must be 289407.")
    value = 0.0

if conversion_type == 'Length':
    from_unit = st.selectbox("From:", ['Meters', 'Kilometers', 'Centimeters', 'Millimeters', 'Miles', 'Yards', 'Feet', 'Inches'])
    to_unit = st.selectbox("To:", ['Meters', 'Kilometers', 'Centimeters', 'Millimeters', 'Miles', 'Yards', 'Feet', 'Inches'])
    result = length_converter(value, from_unit, to_unit)
elif conversion_type == 'Weight':
    from_unit = st.selectbox("From:", ['Kilograms', 'Grams', 'Pounds', 'Ounces'])
    to_unit = st.selectbox("To:", ['Kilograms', 'Grams', 'Pounds', 'Ounces'])
    result = weight_converter(value, from_unit, to_unit)
elif conversion_type == 'Temperature':
    from_unit = st.selectbox("From:", ['Celsius', 'Fahrenheit', 'Kelvin'])
    to_unit = st.selectbox("To:", ['Celsius', 'Fahrenheit', 'Kelvin'])
    result = temperature_converter(value, from_unit, to_unit)
elif conversion_type == 'Area':
    from_unit = st.selectbox("From:", ['Square Meters', 'Square Kilometers', 'Square Centimeters', 'Square Millimeters', 'Square Miles', 'Square Yards', 'Square Feet', 'Square Inches', 'Acres', 'Hectares'])
    to_unit = st.selectbox("To:", ['Square Meters', 'Square Kilometers', 'Square Centimeters', 'Square Millimeters', 'Square Miles', 'Square Yards', 'Square Feet', 'Square Inches', 'Acres', 'Hectares'])
    result = area_converter(value, from_unit, to_unit)

# Display result with words in styled format
st.write(f"### Result: {result} {to_unit}")
st.markdown(f'<p style="color:green; font-size:20px; font-weight:bold;">{num2words(result)} {to_unit}</p>', unsafe_allow_html=True)







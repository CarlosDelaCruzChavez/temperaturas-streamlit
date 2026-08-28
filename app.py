import streamlit as st

# =========================
# Configuración de la página
# =========================
st.set_page_config(
    page_title="Conversor de Temperaturas",
    page_icon="🌡️",
    layout="centered"
)

# =========================
# Funciones de conversión
# =========================
def celsius_a_fahrenheit(c):
    return (c * 9/5) + 32

def celsius_a_kelvin(c):
    return c + 273.15

def fahrenheit_a_celsius(f):
    return (f - 32) * 5/9

def fahrenheit_a_kelvin(f):
    return fahrenheit_a_celsius(f) + 273.15

def kelvin_a_celsius(k):
    return k - 273.15

def kelvin_a_fahrenheit(k):
    return celsius_a_fahrenheit(kelvin_a_celsius(k))


def convertir_temperatura(valor, unidad_origen, unidad_destino):
    """Convierte 'valor' desde 'unidad_origen' hacia 'unidad_destino'."""
    if unidad_origen == unidad_destino:
        return valor

    # Primero convertimos todo a Celsius como paso intermedio
    if unidad_origen == "Celsius (°C)":
        celsius = valor
    elif unidad_origen == "Fahrenheit (°F)":
        celsius = fahrenheit_a_celsius(valor)
    elif unidad_origen == "Kelvin (K)":
        celsius = kelvin_a_celsius(valor)

    # Luego convertimos desde Celsius a la unidad destino
    if unidad_destino == "Celsius (°C)":
        return celsius
    elif unidad_destino == "Fahrenheit (°F)":
        return celsius_a_fahrenheit(celsius)
    elif unidad_destino == "Kelvin (K)":
        return celsius_a_kelvin(celsius)


# =========================
# Interfaz de usuario
# =========================
st.title("🌡️ Conversor de Temperaturas")
st.markdown(
    "Convierte valores entre **Celsius (°C)**, **Fahrenheit (°F)** y **Kelvin (K)** "
    "de forma rápida y sencilla."
)

st.divider()

unidades = ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"]

col1, col2 = st.columns(2)

with col1:
    unidad_origen = st.selectbox("Unidad de origen", unidades, index=0)

with col2:
    # Por defecto selecciona una unidad destino distinta a la de origen
    opciones_destino = [u for u in unidades if u != unidad_origen]
    unidad_destino = st.selectbox("Unidad de destino", unidades, index=unidades.index(opciones_destino[0]))

valor = st.number_input(
    f"Ingresa el valor en {unidad_origen}",
    value=0.0,
    step=0.1,
    format="%.2f"
)

# Validación básica: Kelvin no puede ser negativo (0 K es el cero absoluto)
error = False
if unidad_origen == "Kelvin (K)" and valor < 0:
    st.error("⚠️ La temperatura en Kelvin no puede ser negativa (0 K es el cero absoluto).")
    error = True

st.divider()

if st.button("Convertir 🔄", use_container_width=True) and not error:
    resultado = convertir_temperatura(valor, unidad_origen, unidad_destino)

    # Alerta si el resultado en Kelvin resulta negativo (no debería pasar, pero por seguridad)
    if unidad_destino == "Kelvin (K)" and resultado < 0:
        st.warning("El resultado obtenido no es físicamente posible (Kelvin negativo).")
    else:
        st.success(f"**{valor:.2f} {unidad_origen}** equivale a **{resultado:.2f} {unidad_destino}**")

    # Mostrar también la conversión a las otras dos unidades como referencia
    with st.expander("Ver conversión en todas las unidades"):
        for unidad in unidades:
            valor_conv = convertir_temperatura(valor, unidad_origen, unidad)
            st.write(f"- **{unidad}:** {valor_conv:.2f}")

st.divider()
st.caption("Desarrollado con ❤️ usando Python y Streamlit.")

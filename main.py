import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def calcular_hipoteca(monto, tasa_anual, años, cargo_adicional=0):
    tasa_mensual = (tasa_anual / 100) / 12
    meses = años * 12
    cuota_base = monto * (tasa_mensual * (1 + tasa_mensual) ** meses) / ((1 + tasa_mensual) ** meses - 1)

    # La cuota total incluye la cuota base más el cargo adicional
    cuota_total = cuota_base + cargo_adicional

    saldo = monto
    tabla = []

    for mes in range(1, meses + 1):
        interes = round(saldo * tasa_mensual, 2)
        amortizacion = round(cuota_base - interes, 2)
        saldo = round(saldo - amortizacion, 2)
        tabla.append(
            [
                mes,
                round(cuota_base, 2),
                round(cargo_adicional, 2),
                round(cuota_total, 2),
                interes,
                amortizacion,
                saldo if saldo > 0 else 0,
            ]
        )

    df = pd.DataFrame(
        tabla, columns=["Mes", "Cuota Base", "Cargo Adicional", "Cuota Total", "Interés", "Amortización", "Saldo"]
    )
    return df


def proxima_cuota(fecha_inicio):
    hoy = datetime.today()
    diferencia_meses = (hoy.year - fecha_inicio.year) * 12 + (hoy.month - fecha_inicio.month)
    cuota_actual = diferencia_meses + 1 if hoy.day <= fecha_inicio.day else diferencia_meses + 2

    año = fecha_inicio.year + (cuota_actual - 1) // 12
    mes = (fecha_inicio.month + (cuota_actual - 1) % 12 - 1) % 12 + 1
    dia_vencimiento = fecha_inicio.day

    return cuota_actual, datetime(año, mes, dia_vencimiento).strftime("%d-%m-%Y")


def calcular_precancelacion(fecha_inicio, tabla_amortizacion, cuota_actual):
    saldo_pendiente = tabla_amortizacion.iloc[cuota_actual - 1 :]["Amortización"].sum()
    return round(saldo_pendiente, 2)

# Parámetros del crédito


monto_prestamo = 1_000_000
tasa_interes = 15
años_credito = 10  # Crédito a 10 años
cargo_adicional = 469.37  # Cargo adicional mensual (puede ser un seguro u otros costos)
fecha_primera_cuota = datetime(2017, 11, 6)

# Calcular tabla de amortización
tabla_amortizacion = calcular_hipoteca(monto_prestamo, tasa_interes, años_credito, cargo_adicional)

# Mostrar tabla completa
print(tabla_amortizacion.to_string(index=False))

# Calcular y mostrar la próxima cuota a vencer
nro_cuota, fecha_vencimiento = proxima_cuota(fecha_primera_cuota)
print(f"Próxima cuota a vencer: Cuota {nro_cuota} - Fecha {fecha_vencimiento}")

# Calcular y mostrar el saldo pendiente para precancelación
capital_adeudado = calcular_precancelacion(fecha_primera_cuota, tabla_amortizacion, nro_cuota)
print(f"Capital adeudado para precancelación: {capital_adeudado}")

# Graficar la evolución del saldo pendiente
plt.figure(figsize=(10, 6))
plt.plot(tabla_amortizacion["Mes"], tabla_amortizacion["Saldo"], label="Saldo Pendiente", color="blue")
plt.title("Evolución del saldo pendiente del crédito")
plt.xlabel("Meses")
plt.ylabel("Saldo Pendiente (en $)")
plt.grid(True)
plt.legend()
plt.show()

# Graficar la distribución entre interés y amortización
plt.figure(figsize=(10, 6))
plt.plot(tabla_amortizacion["Mes"], tabla_amortizacion["Interés"], label="Interés", color="red")
plt.plot(tabla_amortizacion["Mes"], tabla_amortizacion["Amortización"], label="Amortización", color="green")
plt.title("Distribución entre interés y amortización")
plt.xlabel("Meses")
plt.ylabel("Monto (en $)")
plt.grid(True)
plt.legend()
plt.show()

# Graficar la evolución del saldo pendiente, interés y amortización con escala logarítmica

plt.figure(figsize=(12, 7))

# Curva de saldo pendiente
plt.plot(tabla_amortizacion["Mes"], tabla_amortizacion["Saldo"], label="Saldo Pendiente", color="blue", linestyle="--")

# Curva de interés y amortización
plt.plot(tabla_amortizacion["Mes"], tabla_amortizacion["Interés"], label="Interés", color="red")
plt.plot(tabla_amortizacion["Mes"], tabla_amortizacion["Amortización"], label="Amortización", color="green")

# Resaltar la parte en la que el saldo comienza a disminuir significativamente en relación con los intereses
plt.axvline(x=nro_cuota, color="orange", linestyle=":", label=f"Cancelación recomendada: Cuota {nro_cuota}")

# Ajustar el gráfico a una escala logarítmica en el eje Y
plt.yscale("log")

# Títulos y etiquetas
plt.title("Análisis de cancelación de crédito con escala logarítmica")
plt.xlabel("Meses")
plt.ylabel("Monto (en $)")

# Leyenda y cuadrícula
plt.legend()
plt.grid(True)

# Mostrar gráfico
plt.show()

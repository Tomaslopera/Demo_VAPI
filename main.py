from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from zoneinfo import ZoneInfo 
from datetime import datetime, date

app = FastAPI()

# Cargar CSV al iniciar
df = pd.read_csv("creditos_dummy.csv", dtype=str)
df["nombre_norm"] = df["nombre persona"].str.strip().str.lower()
df["id_norm"] = df["id"].astype(str).str.strip()

def hoy_bogota_iso():
    return datetime.now(ZoneInfo("America/Bogota")).date().isoformat()  # 'YYYY-MM-DD'


def calcular_dias_mora(fecha_credito: str) -> int:
    """
    Calcula los días de mora desde la fecha del crédito hasta hoy.
    
    Args:
        fecha_credito: Fecha en formato 'M/D/YYYY' (ej: '9/20/2024')
    
    Returns:
        int: Días de mora (0 si no está vencido)
    """
    try:
        # Convertir fecha del crédito de M/D/YYYY a objeto date
        fecha_parts = fecha_credito.split('/')
        mes, dia, año = int(fecha_parts[0]), int(fecha_parts[1]), int(fecha_parts[2])
        fecha_vencimiento = date(año, mes, dia)
        
        # Obtener fecha actual en zona horaria de Bogotá
        fecha_actual = datetime.now(ZoneInfo("America/Bogota")).date()
        
        # Calcular diferencia en días
        diferencia = (fecha_actual - fecha_vencimiento).days
        
        # Si la diferencia es positiva, el crédito está vencido
        return max(0, diferencia)
    except (ValueError, IndexError):
        return 0


def calcular_monto_a_pagar(capital: float, interes_anual: float, dias_mora: int, 
                          interes_moratorio_diario: float = 0.1) -> dict:
    """
    Calcula el monto total a pagar considerando capital, interés y mora.
    
    Args:
        capital: Monto original del crédito
        interes_anual: Tasa de interés anual del crédito (%)
        dias_mora: Número de días de mora
        interes_moratorio_diario: Tasa de interés moratorio diario (% por día)
    
    Returns:
        dict: Desglose del monto a pagar
    """
    # Calcular interés sobre el capital
    interes_capital = capital * (interes_anual / 100)
    
    # Calcular interés moratorio (sobre capital + interés)
    base_mora = capital + interes_capital
    interes_mora = base_mora * (interes_moratorio_diario / 100) * dias_mora
    
    # Monto total
    monto_total = capital + interes_capital + interes_mora
    
    return {
        "capital": round(capital, 2),
        "interes_capital": round(interes_capital, 2),
        "interes_mora": round(interes_mora, 2),
        "monto_total": round(monto_total, 2),
        "dias_mora": dias_mora
    }


class ClienteRequest(BaseModel):
    nombre: str
    identificacion: str


class ClienteResponse(BaseModel):
    found: bool
    cliente: dict = None
    

class ClienteDetalleResponse(BaseModel):
    nombre: str
    id: str
    credit_amount: float
    credit_date: str
    credit_interest: float
    dias_mora: int
    monto_total: float

@app.get("/")
def root():
    return {"status": "ok", "message": "DummyClient API está corriendo"}

@app.get("/now")
def now_endpoint():
    return {"today": hoy_bogota_iso(), "tz": "America/Bogota"}


@app.post("/buscar_cliente")
def buscar_cliente(req: ClienteRequest):
    nombre = req.nombre.strip().lower()
    identificacion = str(req.identificacion).strip()
    
    monto = calcular_monto_a_pagar(
                capital=float(row["credit amount"]),
                interes_anual=float(row["credit interest"]),
                dias_mora=calcular_dias_mora(row["credit date"])
            )

    cliente = df[(df["nombre_norm"] == nombre) & (df["id_norm"] == identificacion)]

    if cliente.empty:
        return {"found": False, "cliente": None}

    row = cliente.iloc[0]
    return {
        "found": True,
        "cliente": {
            "nombre": row["nombre persona"],
            "id": str(row["id"]),
            "credit_amount": float(row["credit amount"]),
            "credit_date": row["credit date"],  # string YYYY-MM-DD
            "credit_interest": float(row["credit interest"]),
            "dias_mora": calcular_dias_mora(row["credit date"]),
            "monto_total": monto["monto_total"]
        }
    }


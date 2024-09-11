import pandas as pd
import mysql.connector
from config import DB_CONFIG #diccionario DB_CONFIG de modulo config para incrementar seguridad
from queries import Queries
from datetime import datetime, timedelta


class Database(Queries):
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            user = DB_CONFIG['username'],
            password = DB_CONFIG['password'],
            host = DB_CONFIG['host'],
            database = DB_CONFIG['database'],
            port = DB_CONFIG['port']
        )
        self.cursor = self.connection.cursor()

    def clientes(self) -> pd.DataFrame:
        self.cursor.execute("SELECT b.id, b.zone_id, b.name, b.short_name, b.email, b.address, b.is_active, b.created_at, b.updated_at, b.deleted_at, b.alto_riesgo, f.family_name, b.mcc_description_id FROM businesses b JOIN mcc_families f ON b.mcc_family_id = f.id WHERE b.deleted_at IS NULL AND b.name NOT LIKE 'CONTROLADORA' AND b.description NOT LIKE 'onboarding business' AND f.deleted_at IS NULL;")
        clientes = pd.DataFrame(self.cursor.fetchall())
        clientes.rename(columns={0:'ID',1:'ID Zona',2:'Nombre de comercio',3:'Nombre Corto',4:'Correo',5:'Dirección',6:'Activo',7:'Creado',8:'Actualizado',9:'Eliminado',10:'Alto Riesgo',11:'Familia MCC',12:'Descripción MCC'}, inplace=True) 
        return clientes
    
    def active_clients(self) -> int:
        self.cursor.execute("SELECT COUNT(*) FROM businesses WHERE deleted_at IS NULL AND name NOT LIKE 'CONTROLADORA ELVA ELF SAPI DE CV' AND description NOT LIKE 'onboarding business'")
        active_clients = pd.DataFrame(self.cursor.fetchall())
        return active_clients.iloc[0,0]
    
    def aquierers_activos(self) -> int:
        self.cursor.execute("SELECT COUNT(*) FROM adquirers")
        adquirers = pd.DataFrame(self.cursor.fetchall())
        return adquirers.iloc[0,0]
    
    def volumen_transaccional(self) -> float:
        self.cursor.execute(Queries.volumen_transaccional_q)
        vol_transaccional = self.cursor.fetchall()
        return vol_transaccional[0]
    
    def transacciones_merchant_id(self) -> pd.DataFrame:
        self.cursor.execute(Queries.transacciones_merchant_id_q)
        transacciones = pd.DataFrame(self.cursor.fetchall())
        transacciones = transacciones.rename(columns={0:'ID',1:'Nombre de Comercio',2:'Monto Transaccionado',3:'Creado'})
        return transacciones
    
    def card_brands(self) -> pd.DataFrame:
        self.cursor.execute(Queries.card_brand_q)
        card_brand = pd.DataFrame(self.cursor.fetchall())
        return card_brand
    
    def card_issuers(self) -> pd.DataFrame:
        self.cursor.execute(Queries.card_issuers_q)
        card_issuer = pd.DataFrame(self.cursor.fetchall())
        card_issuer = card_issuer.rename(columns={0:'Banco',1:"Numero de Transacciones"})
        return card_issuer
    
    def zone(self) -> pd.DataFrame:
        self.cursor.execute(Queries.zone_q)
        zona = pd.DataFrame(self.cursor.fetchall())
        zona = zona.rename(columns={0:'id_zona',1:'nombre_zona',2:'num_comercios'})
        return zona
    
    def debito_credito(self) -> pd.DataFrame:
        self.cursor.execute(Queries.debito_credito_q)
        debito_credito = pd.DataFrame(self.cursor.fetchall())
        debito_credito = debito_credito.rename(columns={0:'Tipo de Tarjeta',1:'Cantidad'})
        debito_credito['Tipo de Tarjeta'] = debito_credito['Tipo de Tarjeta'].replace({0: 'Credito', 1: 'Debito', 2: '1', 3: '2'})
        return debito_credito
    
    def transacciones_en_tiempo(self) -> pd.DataFrame:
        self.cursor.execute(Queries.transacciones_tiempo_q)
        transacciones_tiempo = pd.DataFrame(self.cursor.fetchall())
        transacciones_tiempo = transacciones_tiempo.rename(columns={0:'Inicio de Semana',1:'Total'})
        return transacciones_tiempo
    
    def vol_transaccional_MCC(self) -> pd.DataFrame:
        self.cursor.execute(Queries.vol_transaccional_MCC_q)
        vol_transaccional_mcc = pd.DataFrame(self.cursor.fetchall())
        vol_transaccional_mcc = vol_transaccional_mcc.rename(columns={0:'MCC ID',1:'Descripción MCC',2:"MCC",3:'Monto Transaccionado'})
        return vol_transaccional_mcc
    
    def cliente_churn(self) -> pd.DataFrame:
        self.cursor.execute(Queries.clientes_churn_q)
        churn = pd.DataFrame(self.cursor.fetchall())
        churn = churn.rename(columns={0:'merchant_id',1:'Nombre de Comercio',2:'Fecha de última transacción',3:'Dias desde última transacción'})
        return churn
    
    def churn_rate(self) -> pd.DataFrame:
        fecha_inicio = (datetime.now() - timedelta(days=182)).strftime('%Y-%m-%d') #fecha de inicio del periodo a considerar siempre serán seis meses desde hoy
        fecha_fin = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') #fecha del fin del periodo (siempre es ayer, hace que churn rate sea dinámico)
        churn_threshold = 90 #número de días sin transaccionar que cuando pasen el cliente se considera churn.
        query = f"""
        WITH customer_activity AS (SELECT merchant_id, MAX(transaction_date) AS last_transaction_date FROM card_transactions WHERE transaction_date BETWEEN '{fecha_inicio}' AND '{fecha_fin}' GROUP BY merchant_id) SELECT COUNT(DISTINCT merchant_id) AS total_customers, SUM(CASE WHEN DATEDIFF('{fecha_fin}', last_transaction_date) > {churn_threshold} THEN 1 ELSE 0 END) AS churned_customers, COALESCE(ROUND((SUM(CASE WHEN DATEDIFF('{fecha_fin}', last_transaction_date) > {churn_threshold} THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(DISTINCT merchant_id), 0)), 2), 0) AS churn_rate_percentage FROM customer_activity;
        """
        self.cursor.execute(query)
        churn_rate = pd.DataFrame(self.cursor.fetchall())
        return churn_rate
    
    def close_connection(self) -> None:
        self.cursor.close()
        self.connection.close()
        print("Connection closed")

if __name__ == '__main__':
    instance = Database()
    instance.close_connection()

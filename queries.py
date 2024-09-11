# clase que define todas las SQL Queries que se implementan en data_analysis.py
class Queries():
    def __init__(self) -> None:
        pass

    clientes_churn_q = 'WITH latest_transactions AS (SELECT ct.merchant_id, b.name AS business_name, MAX(ct.transaction_date) AS last_transaction_date FROM card_transactions ct JOIN businesses b ON ct.merchant_id = b.merchant_id GROUP BY ct.merchant_id, b.name) SELECT lt.merchant_id, lt.business_name, lt.last_transaction_date, DATEDIFF(CURRENT_DATE, lt.last_transaction_date) AS days_since_last_transaction FROM latest_transactions lt WHERE DATEDIFF(CURRENT_DATE, lt.last_transaction_date) > 30 ORDER BY days_since_last_transaction DESC'
    vol_transaccional_MCC_q = 'WITH transaction_totals AS (SELECT b.mcc_description_id, SUM(ct.amount) AS Transacted_Amount FROM businesses b JOIN card_transactions ct ON ct.merchant_id = b.merchant_id WHERE b.merchant_id IS NOT NULL GROUP BY b.mcc_description_id) SELECT mcc.id AS mcc_id, mcc.description AS mcc_description, f.family_name AS mcc_family, COALESCE(tt.Transacted_Amount, 0) AS Total_Transacted_Amount FROM mcc_descriptions mcc LEFT JOIN mcc_families f ON mcc.mcc_family_id = f.id LEFT JOIN transaction_totals tt ON mcc.id = tt.mcc_description_id WHERE mcc.deleted_at IS NULL AND f.deleted_at IS NULL ORDER BY Total_Transacted_Amount DESC;'
    transacciones_tiempo_q = 'SELECT DATE(transaction_date - INTERVAL WEEKDAY(transaction_date) DAY) AS inicio_semana, SUM(amount) AS total_amount FROM card_transactions WHERE approved = 1 GROUP BY inicio_semana ORDER BY inicio_semana;'
    debito_credito_q = 'SELECT card_type, COUNT(card_type) AS tipo_tarjeta FROM card_transactions WHERE card_type IS NOT NULL GROUP BY card_type;'
    zone_q = 'SELECT z.id as id_zona, z.name as nombre_zona, COUNT(b.id) as num_comercios FROM zones z LEFT JOIN businesses b ON z.id = b.zone_id WHERE b.deleted_at IS NULL GROUP BY z.id, z.name ORDER BY num_comercios DESC;'
    card_issuers_q = "SELECT issuer, COUNT(*) AS issuer_count FROM card_transactions WHERE issuer NOT LIKE '' GROUP BY issuer ORDER BY issuer_count DESC;"
    card_brand_q = 'SELECT card_brand COUNT(card_brand) FROM card_transactions GROUP BY card_brand'
    transacciones_merchant_id_q = 'SELECT b.merchant_id, b.name, SUM(ct.amount) AS Transacted_Amount, b.created_at FROM businesses b LEFT JOIN card_transactions ct ON ct.merchant_id = b.merchant_id WHERE b.merchant_id IS NOT NULL GROUP BY b.merchant_id, b.name HAVING SUM(ct.amount) IS NOT NULL;'
    volumen_transaccional_q = 'SELECT SUM(amount) FROM card_transactions WHERE approved = 1;'
from db_connection import connect_db

def store_tax_record(person_id, tfn, income, tax_withheld, has_phic, tax, ml, mls, refund):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_tax_records (
            person_id, tfn, income, tax_withheld, has_phic, tax,
            medicare_levy, medicare_levy_surcharge, refund_or_payable
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (person_id, tfn if tfn != "No TFN" else None, income, tax_withheld, has_phic, tax, ml, mls, refund))
    conn.commit()
    cur.close()
    conn.close()
    print("Tax record saved to database.")
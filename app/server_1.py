import Pyro5.api
from tax_calculate import calculate_tax, calculate_medicare_levy, calculate_medicare_levy_surcharge
from tax_database import store_tax_record

@Pyro5.api.expose
class TaxServer:
    def __init__(self):
        self.pitd = None

    def set_db_uri(self, uri):
        self.pitd = Pyro5.api.Proxy(uri)

    def estimate_with_tfn(self, person_id, tfn, has_phic):
        records = self.pitd.get_tax_records(tfn)
        if not records:
            return {"error": "No records found for this TFN."}
        return self.calculate_estimate(person_id, records, has_phic, tfn)

    def add_tfn_records(self, tfn, records):
        for income, withheld in records:
            self.pitd.add_tax_record(tfn, income, withheld)

    def estimate_no_tfn(self, person_id, records, has_phic):
        return self.calculate_estimate(person_id, records, has_phic, "No TFN")

    def calculate_estimate(self, person_id, records, has_phic, tfn):
        income_total = sum([r[0] for r in records])
        withheld_total = sum([r[1] for r in records])
        net_income = income_total - withheld_total

        tax = calculate_tax(income_total)
        ml = calculate_medicare_levy(income_total)
        mls = calculate_medicare_levy_surcharge(income_total, has_phic)
        refund = withheld_total - tax - ml - mls

        store_tax_record(person_id, tfn, income_total, withheld_total, has_phic, tax, ml, mls, refund)

        return {
            "Person ID": person_id,
            "TFN": tfn,
            "Annual Taxable Income": round(income_total, 2),
            "Total Tax Withheld": round(withheld_total, 2),
            "Total Net Income": round(net_income, 2),
            "Estimated Refund or Payable": round(refund, 2)
        }

def main():
    daemon = Pyro5.api.Daemon()
    uri = daemon.register(TaxServer)
    print("Server 1 running. URI:", uri)
    daemon.requestLoop()

if __name__ == "__main__":
    main()

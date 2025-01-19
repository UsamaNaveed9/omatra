import frappe
from frappe.utils import add_days

def update_payment_schedule(doc,method=None):
	for ref in doc.get("references"):
		if ref.payment_term == "5% Advance Payment":
			#update due date with posting date of payment entry
			query_for_update(doc.get("posting_date"), ref.reference_name, ref.payment_term)
		if ref.payment_term == "15% Payment Before Shipping":
			#update due date with posting date of payment entry and update due date for other terms
			query_for_update(doc.get("posting_date"), ref.reference_name, ref.payment_term)

			ref_doc = frappe.get_doc(ref.reference_doctype, ref.reference_name)
			for py_sch in ref_doc.payment_schedule:
				if py_sch.payment_term == "20% After 3 Months":
					credit_days = frappe.db.get_value("Payment Term", py_sch.payment_term, "credit_days")
					due_date = add_days(doc.get("posting_date"), credit_days)
					query_for_update(due_date, ref.reference_name, py_sch.payment_term)
				if py_sch.payment_term == "20% After 6 Months":
					credit_days = frappe.db.get_value("Payment Term", py_sch.payment_term, "credit_days")
					due_date = add_days(doc.get("posting_date"), credit_days)
					query_for_update(due_date, ref.reference_name, py_sch.payment_term)
				if py_sch.payment_term == "20% After 9 Months":
					credit_days = frappe.db.get_value("Payment Term", py_sch.payment_term, "credit_days")
					due_date = add_days(doc.get("posting_date"), credit_days)
					query_for_update(due_date, ref.reference_name, py_sch.payment_term)
				if py_sch.payment_term == "20% After 12 Months":
					credit_days = frappe.db.get_value("Payment Term", py_sch.payment_term, "credit_days")
					due_date = add_days(doc.get("posting_date"), credit_days)
					query_for_update(due_date, ref.reference_name, py_sch.payment_term)

def query_for_update(date,parent,payment_term):
	frappe.db.sql(
		"""
		UPDATE `tabPayment Schedule`
		SET
			due_date = %s
		WHERE parent = %s and payment_term = %s""",
		(date, parent, payment_term),
	)
	frappe.db.commit()
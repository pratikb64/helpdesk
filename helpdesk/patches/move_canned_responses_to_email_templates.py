import frappe


def execute():
    canned_responses = frappe.get_all("HD Canned Response")
    for cr in canned_responses:
        canned_response = frappe.get_doc("HD Canned Response", cr.name)
        frappe.get_doc(
            {
                "doctype": "Email Template",
                "__newname": canned_response.title,
                "subject": canned_response.title,
                "response": canned_response.message,
                "reference_doctype": "HD Ticket",
            }
        ).insert()

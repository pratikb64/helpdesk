# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class HDDashboard(Document):
    pass


@frappe.whitelist()
def get_default_agent_dashboard():
    return '[{"chart":"agent_tickets","type":"card","data":{},"layout":{"x":0,"y":0,"w":17,"h":9,"i":0,"moved":false}},{"chart":"avg_first_response_time","type":"card","data":{},"layout":{"x":0,"y":0,"w":17,"h":9,"i":1,"moved":false}},{"chart":"avg_resolution_time","type":"card","data":{},"layout":{"x":0,"y":0,"w":17,"h":9,"i":2,"moved":false}},{"chart":"upcoming_sla_violations","data":{},"layout":{"x":0,"y":9,"w":50,"h":24,"i":3,"moved":false}},{"chart":"recently_assigned_tickets","data":{},"layout":{"x":0,"y":33,"w":27,"h":24,"i":4,"moved":false}},{"chart":"recent_feedback","data":{},"layout":{"x":0,"y":57,"w":27,"h":10,"i":5,"moved":false}}]'

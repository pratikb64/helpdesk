# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class HDDashboard(Document):
    pass


@frappe.whitelist()
def get_default_agent_dashboard():
    return '[{"chart":"avg_resolution_time","layout":{"x":0,"y":44,"w":18,"h":9,"i":"0.18689323820150838","moved":false}},{"chart":"avg_time_metrics","layout":{"x":0,"y":0,"w":50,"h":26,"i":"0.10672051701644925","moved":false}},{"chart":"recent_feedback","layout":{"x":34,"y":26,"w":16,"h":27,"i":"0.22123736497986313","moved":false}},{"chart":"avg_first_response_time","layout":{"x":0,"y":35,"w":18,"h":9,"i":"0.20643198647210093","moved":false}},{"chart":"agent_tickets","layout":{"x":0,"y":26,"w":18,"h":9,"i":"0.6902620583501805","moved":false}},{"chart":"recently_assigned_tickets","layout":{"x":18,"y":26,"w":16,"h":27,"i":"0.19181602705060297","moved":false}},{"chart":"pending_tickets","layout":{"x":0,"y":78,"w":50,"h":25,"i":"0.8041359513172142","moved":false}},{"chart":"upcoming_sla_violations","layout":{"x":0,"y":53,"w":50,"h":25,"i":"0.0323143803760213","moved":false}}]'

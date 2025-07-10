import ast
import frappe
import json
import re

from frappe.model.rename_doc import update_document_title


@frappe.whitelist()
def duplicate_assignment_rule(docname, new_name):
    doc = frappe.get_doc("Assignment Rule", docname)
    doc.name = new_name
    doc.document_type = "HD Ticket"
    doc.insert(ignore_permissions=True)
    return "success"


@frappe.whitelist()
def get_assignment_rule(docname):
    doc = frappe.get_doc("Assignment Rule", docname)
    if doc.assign_condition:
        doc.assign_condition = json.dumps(convert_to_object(doc.assign_condition))
    if doc.unassign_condition:
        doc.unassign_condition = json.dumps(convert_to_object(doc.unassign_condition))
    ticket_counts = [
        dict(
            user=d.user,
            count=frappe.db.count(
                "ToDo",
                dict(
                    reference_type="HD Ticket",
                    allocated_to=d.user,
                    status="Open",
                ),
            ),
        )
        for d in doc.users
    ]

    return {**doc.as_dict(), "ticket_counts": ticket_counts}


@frappe.whitelist()
def save_assignment_rule(doc, is_new):
    assignment_rule = None
    if is_new:
        assignment_rule = frappe.client.insert(
            {
                **doc,
                "name": doc["assignment_rule_name"],
                "doctype": "Assignment Rule",
                "assign_condition": convert_to_conditions(doc["assign_condition"]),
                "unassign_condition": convert_to_conditions(doc["unassign_condition"]),
            }
        )
    else:
        assignment_rule = frappe.get_doc("Assignment Rule", doc["name"])
        assignment_rule.update(
            {
                **doc,
                "assign_condition": convert_to_conditions(doc["assign_condition"]),
                "unassign_condition": convert_to_conditions(doc["unassign_condition"]),
            }
        )
        assignment_rule.save()

        if assignment_rule.name != doc["assignment_rule_name"]:
            update_document_title(
                **{
                    "doctype": "Assignment Rule",
                    "docname": doc["name"],
                    "enqueue": False,
                    "merge": 0,
                    "freeze": True,
                    "name": doc["assignment_rule_name"],
                    "freeze_message": "Updating assignment rule name",
                }
            )
        assignment_rule = frappe.get_doc("Assignment Rule", doc["assignment_rule_name"])

    return assignment_rule


def convert_to_conditions(conditions, is_nested=False):
    condition_str = ""
    for i, condition in enumerate(conditions):
        if i > 0:
            condition_str += f" {condition.get('conjunction', 'and')} "

        if condition.get("field") == "group":
            condition_str += f"({convert_to_conditions(condition.get('value', []), is_nested=True)})"
            continue

        field = condition.get("field", {})
        fieldname = field.get("fieldname")
        operator = condition.get("operator")
        value = condition.get("value")

        if not fieldname or not operator:
            continue

        # Get fieldtype to handle value quoting
        meta = frappe.get_meta("HD Ticket")
        field_meta = meta.get_field(fieldname)
        fieldtype = field_meta.fieldtype if field_meta else "Data"

        # Handle different operators
        if operator == "equals":
            op_str = "=="
        elif operator == "not equals":
            op_str = "!="
        elif operator == "like":
            op_str = "in"
        elif operator == "not like":
            op_str = "not in"
        else:
            op_str = operator

        # Handle value formatting
        if operator in ["in", "not in"] and isinstance(value, str):
            value_str = f"[{', '.join([f'{repr(v.strip())}' for v in value.split(',')])}]"
        elif operator in ["is", "is not"] and value in ["set", "not set"]:
            value_str = "None" if value == "not set" else "not None"
        elif fieldtype in ["Select", "Link", "Data", "Text Editor", "Small Text", "Text"]:
            value_str = repr(value)
        else:
            value_str = value

        if operator in ["like", "not like"]:
            condition_str += f"{value_str} {op_str} {fieldname}"
        else:
            condition_str += f"{fieldname} {op_str} {value_str}"

    return condition_str

def convert_to_object(condition_str):
    if not condition_str:
        return []

    # This is a simplified parser. For complex scenarios, a proper parsing library would be more robust.
    groups = {}
    processed_str = list(condition_str)
    i = 0
    while i < len(processed_str):
        if processed_str[i] == '(':
            start = i
            balance = 1
            i += 1
            while i < len(processed_str) and balance > 0:
                if processed_str[i] == '(':
                    balance += 1
                elif processed_str[i] == ')':
                    balance -= 1
                i += 1
            
            if balance == 0:
                group_content = "".join(processed_str[start+1:i-1])
                group_id = f"__group_{len(groups)}__"
                groups[group_id] = group_content
                # Replace the group with its ID
                processed_str = processed_str[:start] + list(group_id) + processed_str[i:]
                # Reset index to re-scan from the beginning of the modified string
                i = -1 
        i += 1
    
    processed_str = "".join(processed_str)

    # Split by conjunctions
    conditions = re.split(r'\s+(and|or)\s+', processed_str)
    
    result = []
    i = 0
    while i < len(conditions):
        part = conditions[i].strip()
        if not part:
            i += 1
            continue

        conjunction = conditions[i-1].strip() if i > 0 else None

        if part in groups:
            # This is a nested group
            nested_conditions = convert_to_object(groups[part])
            group_obj = {
                "field": "group",
                "operator": "equals", # This seems to be the default for groups in the example
                "value": nested_conditions,
            }
            if conjunction:
                group_obj["conjunction"] = conjunction
            result.append(group_obj)
        else:
            # This is a simple condition
            obj = _parse_simple_condition(part)
            if obj:
                if conjunction:
                    obj["conjunction"] = conjunction
                result.append(obj)
        i += 1

    return result

def _parse_simple_condition(condition_part):
    # This helper function will parse a single condition like 'status == "Open"'
    # It's a simplified implementation.
    match = re.match(r"'([^']*)'\s+(in|not in)\s+([a-zA-Z0-9_]+)", condition_part)  # like, not like
    if not match:
        match = re.match(r"([a-zA-Z0-9_]+)\s+(==|!=|in|not in|is|is not|<|>|<=|>=)\s+(.*)", condition_part)

    if not match:
        return None

    meta = frappe.get_meta("HD Ticket")

    if "'" in condition_part and (' in ' in condition_part or ' not in ' in condition_part) and condition_part.startswith("'"):
        # like / not like
        value, py_operator, fieldname = match.groups()
        operator = 'like' if py_operator == 'in' else 'not like'
    else:
        fieldname, py_operator, value_str = match.groups()
        value_str = value_str.strip()

        operator_map = {
            "==": "equals",
            "!=": "not equals",
            "in": "in",
            "not in": "not in",
            "is": "is",
            "is not": "is",  # 'is not' also maps to 'is', but value becomes 'not set'
            "<": "<",
            ">": ">",
            "<=": "<=",
            ">=": ">=",
        }
        operator = operator_map.get(py_operator, py_operator)

        # Convert value from string back to original type
        if value_str.startswith('[') and value_str.endswith(']'):
            # List value for 'in' or 'not in'
            value = [v.strip().strip("'") for v in value_str[1:-1].split(',')]
            value = ", ".join(value)
        elif value_str == 'None':
            value = 'not set' if py_operator == 'is not' else 'set'
        elif value_str.startswith("'") and value_str.endswith("'"):
            value = value_str[1:-1]
        else:
            try:
                value = int(value_str)
            except ValueError:
                try:
                    value = float(value_str)
                except ValueError:
                    value = value_str # Keep as string if not a number

    field_meta = meta.get_field(fieldname)
    
    return {
        "field": {
            "value": fieldname,
            "fieldname": fieldname,
            "fieldtype": field_meta.fieldtype if field_meta else "Data",
            "label": field_meta.label if field_meta else fieldname,
            "options": field_meta.options if field_meta else None
        },
        "operator": operator,
        "value": value
    }

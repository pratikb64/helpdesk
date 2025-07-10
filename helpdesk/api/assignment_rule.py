import ast
import frappe
import json

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
    """
    Convert conditions array to Python string

    Args:
        conditions (list/dict): List of conditions or a single condition dict
        is_nested (bool): Whether this is a nested condition (for internal use)

    Returns:
        str: Python condition string
    """
    if not conditions:
        return ""

    if isinstance(conditions, dict):
        conditions = [conditions]

    conditions_str = []

    for condition in conditions:
        field = condition.get("field")
        operator = condition.get("operator", "==").lower()
        value = condition.get("value")
        conjunction = condition.get("conjunction", "and").lower()

        # Handle nested conditions
        if field == "group" and isinstance(value, list):
            nested_condition = convert_to_conditions(value, is_nested=True)
            conditions_str.append(f"({nested_condition})")
            continue

        # Skip if field is not properly defined
        if not isinstance(field, dict) or "fieldname" not in field:
            continue

        fieldname = field["fieldname"]
        fieldtype = field.get("fieldtype", "")

        # Format field access
        field_access = fieldname

        # Format operator
        operator_map = {
            # Basic comparisons
            "equals": "==",
            "=": "==",
            "!=": "!=",
            "not equals": "!=",
            "<": "<",
            "<=": "<=",
            ">": ">",
            ">=": ">=",
            # Membership
            "in": "in",
            "not in": "not in",
            # String matching
            "like": "like",
            "not like": "not like",
            # Identity
            "is": "is",
            "is not": "is not",
            # Date specific
            "between": "between",
            "timespan": "timespan",
        }

        op = operator_map.get(operator, operator)

        if isinstance(value, str):
            if fieldname == "_assign":
                if op == "like":
                    op = "like"
                    value_str = f"'%{value}%'"
                elif op == "not like":
                    op = "not like"
                    value_str = f"'%{value}%'"
                elif op == "is":
                    value_str = "None"
            elif fieldtype == "Check":
                if value.lower() in ("yes", "true", "1"):
                    value_str = "1"
                else:
                    value_str = "0"
                if op == "==" and value_str == "1":
                    conditions_str.append(field_access)
                    continue
                elif op == "==" and value_str == "0":
                    conditions_str.append(f"not {field_access}")
                    continue
            elif op == "timespan":
                conditions_str.append(f"# Timespan: {value} not implemented")
                continue
            elif op == "between" and "," in value:
                start, end = [v.strip() for v in value.split(",")]
                conditions_str.append(
                    f"({field_access} >= '{start}' and {field_access} <= '{end}')"
                )
                continue
            elif op in ("in", "not in") and "," in value:
                items = [f"'{v.strip()}'" for v in value.split(",")]
                value_str = f"[{', '.join(items)}]"
            elif op in ("like", "not like"):
                value_str = f"'%{value}%'"
            else:
                value_str = f"'{value}'"
        elif isinstance(value, (int, float, bool)):
            value_str = str(value).lower() if isinstance(value, bool) else str(value)
        elif value is None:
            value_str = "None"
        else:
            value_str = str(value)

        condition_str = f"{field_access} {op} {value_str}"

        if fieldtype == "Check" and op == "==" and value_str in ("0", "1"):
            if value_str == "1":
                condition_str = field_access
            else:
                condition_str = f"not {field_access}"

        conditions_str.append(condition_str)

    if not conditions_str:
        return ""

    result = f" {conjunction} ".join(conditions_str)

    if (
        not is_nested
        and len(conditions) == 1
        and not any(c in result for c in ["(", ")"])
    ):
        return result

    result = result.replace("  ", " ").replace("  ", " ").strip()

    if is_nested and len(conditions) > 1:
        result = f"({result})"

    # Remove any double parentheses that might have been added
    while "((" in result and "))" in result:
        result = result.replace("((", "(").replace("))", ")")

    return result


def convert_to_object(condition_str):
    if not condition_str or not isinstance(condition_str, str):
        return []

    fields_meta = {f.fieldname: f for f in frappe.get_meta("HD Ticket").fields}

    def get_field_info(fieldname):
        meta = fields_meta.get(fieldname)
        if not meta:
            return {
                "value": fieldname,
                "fieldname": fieldname,
                "fieldtype": "Data",
                "label": fieldname.replace("_", " ").title(),
            }
        return {
            "value": fieldname,
            "fieldname": meta.fieldname,
            "fieldtype": meta.fieldtype,
            "label": meta.label,
            "options": meta.options,
        }

    def get_operator_str(op):
        return {
            ast.Eq: "equals",
            ast.NotEq: "not equals",
            ast.Lt: "<",
            ast.LtE: "<=",
            ast.Gt: ">",
            ast.GtE: ">=",
            ast.In: "in",
            ast.NotIn: "not in",
        }.get(type(op), "")

    def parse_node(node, is_top_level=False):
        if isinstance(node, ast.BoolOp):
            conjunction = "and" if isinstance(node.op, ast.And) else "or"

            child_results = [parse_node(v) for v in node.values]

            for i in range(1, len(child_results)):
                child = child_results[i]
                if child and child[0]:
                    child[0]["conjunction"] = conjunction

            flat_conditions = []
            for child in child_results:
                if child:
                    flat_conditions.extend(child)

            if len(node.values) > 1 and not is_top_level:
                return [
                    {
                        "field": "group",
                        "operator": "equals",
                        "value": flat_conditions,
                    }
                ]

            return flat_conditions

        elif isinstance(node, ast.Compare):
            # Handle both Attribute (doc.field) and Name (field) nodes
            if isinstance(node.left, ast.Attribute):
                fieldname = node.left.attr
            elif isinstance(node.left, ast.Name):
                fieldname = node.left.id
            else:
                return None

            op = get_operator_str(node.ops[0])
            val = ast.literal_eval(node.comparators[0])

            if fields_meta.get(fieldname, {}).get("fieldtype") == "Check":
                value = "Yes" if val else "No"
            elif isinstance(val, list):
                value = ", ".join(map(str, val))
            else:
                value = str(val)

            return [
                {
                    "field": get_field_info(fieldname),
                    "operator": op,
                    "value": value,
                }
            ]

        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            condition = parse_node(node.operand)
            if condition and condition[0]:
                condition[0]["value"] = "No"
                return condition
            return None

        elif isinstance(node, ast.Attribute):
            fieldname = node.attr
            if fields_meta.get(fieldname, {}).get("fieldtype") == "Check":
                return [
                    {
                        "field": get_field_info(fieldname),
                        "operator": "equals",
                        "value": "Yes",
                    }
                ]
            return None

        elif isinstance(node, ast.Expr):
            return parse_node(node.value, is_top_level)

        return None

    try:
        parsed_ast = ast.parse(condition_str.strip(), mode="eval")
        conditions = parse_node(parsed_ast.body, is_top_level=True)
        return conditions or []

    except (SyntaxError, ValueError) as e:
        frappe.log_error(f"Error parsing condition string: {e}", "SLA API Error")
        return []

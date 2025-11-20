import json
from datetime import date, timedelta

import frappe

from helpdesk.helpdesk.doctype.hd_dashboard.hd_dashboard import (
    get_default_agent_dashboard,
)
from helpdesk.utils import agent_only


@frappe.whitelist()
@agent_only
def get_dashboard():
    dashboard = frappe.db.exists("HD Dashboard", frappe.session.user)

    if not dashboard:
        dashboard = frappe.get_doc(
            {
                "doctype": "HD Dashboard",
                "name": frappe.session.user,
                "user": frappe.session.user,
                "layout": get_default_agent_dashboard(),
            },
        ).insert(ignore_permissions=True)
        frappe.db.commit()
        layout = json.loads(get_default_agent_dashboard())
    else:
        layout = json.loads(
            frappe.get_value(
                "HD Dashboard",
                frappe.session.user,
                "layout",
            )
        )

    for chart in layout:
        method_name = f"get_{chart['chart']}"
        if hasattr(frappe.get_attr("helpdesk.api.agent_dashboard"), method_name):
            method = getattr(
                frappe.get_attr("helpdesk.api.agent_dashboard"), method_name
            )
            chart["data"] = method()
        else:
            chart["data"] = None

    return layout


@frappe.whitelist()
@agent_only
def get_agent_tickets(period="last month"):
    periods = {"last week": 7, "last month": 30, "last 3 months": 90}
    days = periods.get(period, 7)

    current_from = frappe.utils.add_days(frappe.utils.nowdate(), -days)
    current_to = frappe.utils.nowdate()
    previous_from = frappe.utils.add_days(frappe.utils.nowdate(), -2 * days)
    previous_to = frappe.utils.add_days(frappe.utils.nowdate(), -days)

    def get_ticket_data(from_date, to_date):
        result = frappe.db.sql(
            """
            SELECT
                DATE(creation) as date,
                COUNT(name) as count
            FROM `tabHD Ticket`
            WHERE creation >= %(from_date)s AND creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY)
            AND JSON_SEARCH(_assign, 'one', %(agent)s) IS NOT NULL
            GROUP BY DATE(creation)
            ORDER BY DATE(creation)
            """,
            {
                "from_date": from_date,
                "to_date": to_date,
                "agent": frappe.session.user,
            },
            as_dict=1,
        )
        return result

    current_result = get_ticket_data(current_from, current_to)
    previous_result = get_ticket_data(previous_from, previous_to)

    current_total = sum(row["count"] for row in current_result)
    previous_total = sum(row["count"] for row in previous_result)

    if previous_total > 0:
        percentage_change = round(
            ((current_total - previous_total) / previous_total) * 100, 2
        )
    elif current_total > 0:
        percentage_change = 999
    else:
        percentage_change = 0

    # Fill missing days with 0
    from_date_obj = date.fromisoformat(current_from)
    to_date_obj = date.fromisoformat(current_to)
    date_dict = {}
    current_date = from_date_obj
    while current_date <= to_date_obj:
        date_str = current_date.isoformat()
        date_dict[date_str] = 0
        current_date += timedelta(days=1)

    for row in current_result:
        date_dict[str(row["date"])] = row["count"]

    data = [{"date": date, "count": count} for date, count in sorted(date_dict.items())]

    return {
        "data": data,
        "total": current_total,
        "percentage_change": percentage_change,
    }


@frappe.whitelist()
@agent_only
def get_avg_first_response_time(period="last month"):
    periods = {"last week": 7, "last month": 30, "last 3 months": 90}
    days = periods.get(period, 7)

    current_from = frappe.utils.add_days(frappe.utils.nowdate(), -days)
    current_to = frappe.utils.nowdate()
    previous_from = frappe.utils.add_days(frappe.utils.nowdate(), -2 * days)
    previous_to = frappe.utils.add_days(frappe.utils.nowdate(), -days)

    def get_avg_time(from_date, to_date, time_field):
        result = frappe.db.sql(
            f"""
            SELECT AVG({time_field}) as avg_time
            FROM `tabHD Ticket`
            WHERE creation >= %(from_date)s AND creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY)
            AND JSON_SEARCH(_assign, 'one', %(agent)s) IS NOT NULL
            AND {time_field} IS NOT NULL
            """,
            {
                "from_date": from_date,
                "to_date": to_date,
                "agent": frappe.session.user,
            },
            as_dict=1,
        )
        return (
            result[0]["avg_time"] if result and result[0]["avg_time"] is not None else 0
        )

    current_avg = get_avg_time(current_from, current_to, "first_response_time")
    previous_avg = get_avg_time(previous_from, previous_to, "first_response_time")

    if previous_avg > 0:
        percentage_change = round(
            ((current_avg - previous_avg) / previous_avg) * 100, 2
        )
    elif current_avg > 0:
        percentage_change = 999
    else:
        percentage_change = 0

    return {
        "average": current_avg,
        "percentage_change": percentage_change,
    }


@frappe.whitelist()
@agent_only
def get_avg_resolution_time(period="last month"):
    periods = {"last week": 7, "last month": 30, "last 3 months": 90}
    days = periods.get(period, 7)

    current_from = frappe.utils.add_days(frappe.utils.nowdate(), -days)
    current_to = frappe.utils.nowdate()
    previous_from = frappe.utils.add_days(frappe.utils.nowdate(), -2 * days)
    previous_to = frappe.utils.add_days(frappe.utils.nowdate(), -days)

    def get_avg_time(from_date, to_date, time_field):
        result = frappe.db.sql(
            f"""
            SELECT AVG({time_field}) as avg_time
            FROM `tabHD Ticket`
            WHERE creation >= %(from_date)s AND creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY)
            AND JSON_SEARCH(_assign, 'one', %(agent)s) IS NOT NULL
            AND {time_field} IS NOT NULL
            """,
            {
                "from_date": from_date,
                "to_date": to_date,
                "agent": frappe.session.user,
            },
            as_dict=1,
        )
        return (
            result[0]["avg_time"] if result and result[0]["avg_time"] is not None else 0
        )

    current_avg = get_avg_time(current_from, current_to, "resolution_time")
    previous_avg = get_avg_time(previous_from, previous_to, "resolution_time")

    if previous_avg > 0:
        percentage_change = round(
            ((current_avg - previous_avg) / previous_avg) * 100, 2
        )
    elif current_avg > 0:
        percentage_change = 999
    else:
        percentage_change = 0

    return {
        "average": current_avg,
        "percentage_change": percentage_change,
    }


@frappe.whitelist()
@agent_only
def get_sla_fulfilled_count(period="last month"):
    periods = {"last week": 7, "last month": 30, "last 3 months": 90}
    days = periods.get(period, 7)

    current_from = frappe.utils.add_days(frappe.utils.nowdate(), -days)
    current_to = frappe.utils.nowdate()
    previous_from = frappe.utils.add_days(frappe.utils.nowdate(), -2 * days)
    previous_to = frappe.utils.add_days(frappe.utils.nowdate(), -days)

    resolved_statuses = tuple(
        frappe.get_all(
            "HD Ticket Status",
            filters={"category": "Resolved"},
            pluck="name",
        )
    )

    def get_sla_data(from_date, to_date):
        fulfilled_result = frappe.db.sql(
            """
            SELECT COUNT(name) as fulfilled_count
            FROM `tabHD Ticket`
            WHERE creation >= %(from_date)s AND creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY)
            AND agreement_status = 'Fulfilled'
            AND status in %(resolved_statuses)s
            AND JSON_SEARCH(_assign, 'one', %(agent)s) IS NOT NULL
            """,
            {
                "from_date": from_date,
                "to_date": to_date,
                "resolved_statuses": resolved_statuses,
                "agent": frappe.session.user,
            },
            as_dict=1,
        )

        total_result = frappe.db.sql(
            """
            SELECT COUNT(name) as total_count
            FROM `tabHD Ticket`
            WHERE creation >= %(from_date)s AND creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY)
            AND status in %(resolved_statuses)s
            AND JSON_SEARCH(_assign, 'one', %(agent)s) IS NOT NULL
            """,
            {
                "from_date": from_date,
                "to_date": to_date,
                "resolved_statuses": resolved_statuses,
                "agent": frappe.session.user,
            },
            as_dict=1,
        )

        fulfilled_count = fulfilled_result[0].fulfilled_count or 0
        total_count = total_result[0].total_count or 0
        percentage = (fulfilled_count / total_count * 100) if total_count > 0 else 0

        return percentage

    current_percentage = get_sla_data(current_from, current_to)
    previous_percentage = get_sla_data(previous_from, previous_to)

    if previous_percentage > 0:
        percentage_change = round(
            ((current_percentage - previous_percentage) / previous_percentage) * 100, 2
        )
    elif current_percentage > 0:
        percentage_change = 999
    else:
        percentage_change = 0

    return {
        "percentage": current_percentage,
        "percentage_change": percentage_change,
    }


@frappe.whitelist()
@agent_only
def get_unresolved_tickets():
    allowed_statuses = frappe.get_all(
        "HD Ticket Status", filters={"category": ["!=", "Resolved"]}, pluck="name"
    )
    count = frappe.db.count(
        "HD Ticket",
        filters=[
            ["_assign", "like", f"%{frappe.session.user}%"],
            ["status", "in", allowed_statuses],
        ],
    )
    return {"total": count}


@frappe.whitelist()
@agent_only
def get_recently_assigned_tickets():
    allowed_statuses = frappe.get_all(
        "HD Ticket Status", filters={"category": ["!=", "Resolved"]}, pluck="name"
    )
    tickets = frappe.get_list(
        "HD Ticket",
        fields=[
            "name",
            "subject",
            "status",
            "priority",
            "modified",
            "creation",
        ],
        filters=[
            ["_assign", "like", f"%{frappe.session.user}%"],
            ["status", "in", allowed_statuses],
        ],
        order_by="modified desc",
        limit=10,
    )
    return tickets


@frappe.whitelist()
@agent_only
def get_recent_feedback():
    agent = frappe.session.user

    avg_result = frappe.db.sql(
        """
        SELECT AVG(feedback_rating) * 5 as average
        FROM `tabHD Ticket`
        WHERE feedback_rating > 0
        AND JSON_SEARCH(_assign, 'one', %(agent)s) IS NOT NULL
        """,
        {"agent": agent},
        as_dict=True,
    )
    average_rating = (
        avg_result[0]["average"]
        if avg_result and avg_result[0]["average"] is not None
        else 0
    )

    feedback = frappe.get_list(
        "HD Ticket",
        fields=["name", "feedback_rating", "feedback", "feedback_extra", "contact"],
        filters=[
            ["feedback_rating", ">", 0],
            ["_assign", "like", f"%{agent}%"],
        ],
        order_by="modified desc",
        limit=10,
    )

    return {"average_rating": round(average_rating, 1), "recent_feedbacks": feedback}


@frappe.whitelist()
@agent_only
def get_avg_time_metrics(period: str = "6m"):
    periods = {
        "3m": 3,
        "6m": 6,
        "1y": 12,
    }

    months = periods.get(period, 6)
    agent = frappe.session.user

    # Get monthly averages for the last 'months' months
    result = frappe.db.sql(
        """
        SELECT
            DATE_FORMAT(creation, '%%b') as month,
            YEAR(creation) as year,
            MONTH(creation) as month_num,
            AVG(first_response_time) as avg_first_response,
            AVG(resolution_time) as avg_resolution
        FROM `tabHD Ticket`
        WHERE creation >= DATE_SUB(NOW(), INTERVAL %(months)s MONTH)
        AND JSON_SEARCH(_assign, 'one', %(agent)s) IS NOT NULL
        AND (first_response_time IS NOT NULL OR resolution_time IS NOT NULL)
        GROUP BY YEAR(creation), MONTH(creation)
        ORDER BY YEAR(creation), MONTH(creation)
        """,
        {"months": months, "agent": agent},
        as_dict=1,
    )

    # Create a dict of existing data
    data_dict = {}
    for row in result:
        key = f"{row['year']}-{row['month_num']:02d}"
        data_dict[key] = {
            "month": row["month"],
            "avg_first": row["avg_first_response"] or 0,
            "avg_resolution": row["avg_resolution"] or 0,
        }

    # Generate all months in the period
    import datetime

    now = datetime.datetime.now()
    data = []
    for i in range(months - 1, -1, -1):  # From oldest to newest
        month_date = now - datetime.timedelta(days=30 * i)
        key = f"{month_date.year}-{month_date.month:02d}"
        if key in data_dict:
            data.append(
                [
                    data_dict[key]["month"],
                    data_dict[key]["avg_first"],
                    data_dict[key]["avg_resolution"],
                ]
            )
        else:
            data.append(
                [
                    month_date.strftime("%b"),
                    0,
                    0,
                ]
            )

    # Calculate overall averages for the period
    overall_result = frappe.db.sql(
        """
        SELECT
            AVG(first_response_time) as avg_first_response,
            AVG(resolution_time) as avg_resolution
        FROM `tabHD Ticket`
        WHERE creation >= DATE_SUB(NOW(), INTERVAL %(months)s MONTH)
        AND JSON_SEARCH(_assign, 'one', %(agent)s) IS NOT NULL
        AND (first_response_time IS NOT NULL OR resolution_time IS NOT NULL)
        """,
        {"months": months, "agent": agent},
        as_dict=1,
    )

    overall_avg_first = (
        overall_result[0]["avg_first_response"]
        if overall_result and overall_result[0]["avg_first_response"] is not None
        else 0
    )
    overall_avg_resolution = (
        overall_result[0]["avg_resolution"]
        if overall_result and overall_result[0]["avg_resolution"] is not None
        else 0
    )

    return {
        "data": data,
        "averages": {
            "first_response": overall_avg_first,
            "resolution": overall_avg_resolution,
        },
    }


@frappe.whitelist()
@agent_only
def get_upcoming_sla_violations():
    upcoming_sla_violations = frappe.get_list(
        "HD Ticket",
        fields=[
            "name",
            "subject",
            "status",
            "priority",
            "agent_group",
            "response_by",
            "resolution_by",
            "resolution_date",
            "agreement_status",
            "status_category",
        ],
        filters=[
            ["sla", "!=", ""],
            ["agreement_status", "in", ["First Response Due", "Resolution Due"]],
            ["status_category", "!=", "Closed"],
        ],
        order_by="response_by asc, resolution_by asc",
        limit=5,
    )
    return upcoming_sla_violations

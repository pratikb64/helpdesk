import datetime
import json
from datetime import date, timedelta

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Avg, Cast, Count, Function, Max

from helpdesk.utils import agent_only


def get_default_agent_dashboard():
    return '[{"chart":"recently_assigned_tickets","layout":{"x":17,"y":25,"w":17,"h":27,"i":"0.5901090349104408","minW":16,"minH":27,"maxH":27,"moved":false}},{"chart":"recent_feedback","layout":{"x":34,"y":25,"w":16,"h":27,"i":"0.2090867593567277","minW":16,"minH":27,"maxW":27,"maxH":27,"moved":false}},{"chart":"avg_time_metrics","layout":{"x":0,"y":0,"w":50,"h":25,"i":"0.9444757118289221","moved":false,"minW":18,"minH":24,"maxH":44}},{"chart":"upcoming_sla_violations","layout":{"x":0,"y":52,"w":50,"h":25,"i":"0.644411970698438","moved":false,"minW":25,"minH":25,"maxH":25}},{"chart":"pending_tickets","layout":{"x":0,"y":77,"w":50,"h":24,"i":"0.12878740671098265","moved":false,"minW":25,"minH":24,"maxH":24}},{"chart":"avg_resolution_time","layout":{"x":0,"y":43,"w":17,"h":9,"i":"0.17044916608149618","moved":false,"minW":14,"minH":9,"maxH":9}},{"chart":"avg_first_response_time","layout":{"x":0,"y":34,"w":17,"h":9,"i":"0.408504238844829","moved":false,"minW":14,"minH":9,"maxH":9}},{"chart":"agent_tickets","layout":{"x":0,"y":25,"w":17,"h":9,"i":"0.38621973888392136","moved":false,"minW":14,"minH":9,"maxH":9}}]'


@frappe.whitelist()
@agent_only
def get_dashboard(reset_layout=False):
    dashboard = frappe.db.exists("HD Field Layout", {"user": frappe.session.user})

    if not dashboard:
        dashboard = frappe.get_doc(
            {
                "doctype": "HD Field Layout",
                "user": frappe.session.user,
                "type": "Landing Page",
                "layout": get_default_agent_dashboard(),
            },
        ).insert(ignore_permissions=True)
        frappe.db.commit()  # nosemgrep
        layout = json.loads(get_default_agent_dashboard())
    else:
        dashboard = frappe.db.get_value(
            "HD Field Layout",
            {"user": frappe.session.user},
            ["name", "layout"],
        )
        if reset_layout:
            layout = json.loads(get_default_agent_dashboard())
        else:
            layout = json.loads(dashboard[1])

    for chart in layout:
        method_name = f"get_{chart['chart']}"
        if hasattr(frappe.get_attr("helpdesk.api.agent_dashboard"), method_name):
            method = getattr(
                frappe.get_attr("helpdesk.api.agent_dashboard"), method_name
            )
            chart["data"] = method()
        else:
            chart["data"] = None

    return {
        "layout": layout,
        "default_layout": get_default_agent_dashboard(),
        "dashboard_id": dashboard[0],
    }


@frappe.whitelist()
@agent_only
def get_agent_tickets(period="last month"):
    periods = {"last week": 7, "last month": 30, "last 3 months": 90}
    days = periods.get(period, 7)

    current_from = frappe.utils.add_days(frappe.utils.nowdate(), -(days - 1))
    current_to = frappe.utils.nowdate()
    previous_from = frappe.utils.add_days(frappe.utils.nowdate(), -(2 * days - 1))
    previous_to = frappe.utils.add_days(frappe.utils.nowdate(), -days)

    def get_ticket_data(from_date, to_date):
        ticket = DocType("HD Ticket")
        creation_date = Function("DATE", ticket.creation)
        to_date_plus_one = Function(
            "DATE_ADD", to_date, frappe.qb.terms.PseudoColumn("INTERVAL 1 DAY")
        )

        result = (
            frappe.qb.from_(ticket)
            .select(
                creation_date.as_("date"),
                Count(ticket.name).as_("count"),
            )
            .where(ticket.creation >= from_date)
            .where(ticket.creation < to_date_plus_one)
            .where(
                Function(
                    "JSON_SEARCH", ticket._assign, "one", frappe.session.user
                ).isnotnull()
            )
            .groupby(creation_date)
            .orderby(creation_date)
            .run(as_dict=True)
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


def get_avg_time(from_date, to_date, time_field):
    ticket = DocType("HD Ticket")
    to_date_plus_one = Function(
        "DATE_ADD", to_date, frappe.qb.terms.PseudoColumn("INTERVAL 1 DAY")
    )

    result = (
        frappe.qb.from_(ticket)
        .select(Avg(ticket[time_field]).as_("avg_time"))
        .where(ticket.creation >= from_date)
        .where(ticket.creation < to_date_plus_one)
        .where(
            Function(
                "JSON_SEARCH", ticket._assign, "one", frappe.session.user
            ).isnotnull()
        )
        .where(ticket[time_field].isnotnull())
        .run(as_dict=True)
    )
    return result[0]["avg_time"] if result and result[0]["avg_time"] is not None else 0


def get_avg_time_data(from_date, to_date, field):
    ticket = DocType("HD Ticket")
    creation_date = Function("DATE", ticket.creation)
    to_date_plus_one = Function(
        "DATE_ADD", to_date, frappe.qb.terms.PseudoColumn("INTERVAL 1 DAY")
    )

    result = (
        frappe.qb.from_(ticket)
        .select(
            creation_date.as_("date"),
            Avg(ticket[field]).as_("avg_time"),
        )
        .where(ticket.creation >= from_date)
        .where(ticket.creation < to_date_plus_one)
        .where(
            Function(
                "JSON_SEARCH", ticket._assign, "one", frappe.session.user
            ).isnotnull()
        )
        .where(ticket[field].isnotnull())
        .groupby(creation_date)
        .orderby(creation_date)
        .run(as_dict=True)
    )
    return result


@frappe.whitelist()
@agent_only
def get_avg_first_response_time(period="last month"):
    periods = {"last week": 7, "last month": 30, "last 3 months": 90}
    days = periods.get(period, 7)

    current_from = frappe.utils.add_days(frappe.utils.nowdate(), -days)
    current_to = frappe.utils.nowdate()
    previous_from = frappe.utils.add_days(frappe.utils.nowdate(), -2 * days)
    previous_to = frappe.utils.add_days(frappe.utils.nowdate(), -days)

    current_result = get_avg_time_data(current_from, current_to, "first_response_time")

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
        date_dict[str(row["date"])] = round(row["avg_time"] or 0, 2)

    data = [
        {"date": date, "avg_time": avg_time}
        for date, avg_time in sorted(date_dict.items())
    ]

    return {
        "data": data,
        "average": round(current_avg, 2),
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

    current_result = get_avg_time_data(current_from, current_to, "resolution_time")

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
        date_dict[str(row["date"])] = round(row["avg_time"] or 0, 2)

    data = [
        {"date": date, "avg_time": avg_time}
        for date, avg_time in sorted(date_dict.items())
    ]

    return {
        "data": data,
        "average": round(current_avg, 2),
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
        ticket = DocType("HD Ticket")
        to_date_plus_one = Function(
            "DATE_ADD", to_date, frappe.qb.terms.PseudoColumn("INTERVAL 1 DAY")
        )

        fulfilled_result = (
            frappe.qb.from_(ticket)
            .select(Count(ticket.name).as_("fulfilled_count"))
            .where(ticket.creation >= from_date)
            .where(ticket.creation < to_date_plus_one)
            .where(ticket.agreement_status == "Fulfilled")
            .where(ticket.status.isin(resolved_statuses))
            .where(
                Function(
                    "JSON_SEARCH", ticket._assign, "one", frappe.session.user
                ).isnotnull()
            )
            .run(as_dict=True)
        )

        total_result = (
            frappe.qb.from_(ticket)
            .select(Count(ticket.name).as_("total_count"))
            .where(ticket.creation >= from_date)
            .where(ticket.creation < to_date_plus_one)
            .where(ticket.status.isin(resolved_statuses))
            .where(
                Function(
                    "JSON_SEARCH", ticket._assign, "one", frappe.session.user
                ).isnotnull()
            )
            .run(as_dict=True)
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
    one_week_ago = frappe.utils.add_days(frappe.utils.nowdate(), -7)

    todo = DocType("ToDo")
    assigned_tickets = (
        frappe.qb.from_(todo)
        .select(todo.reference_name)
        .distinct()
        .where(todo.reference_type == "HD Ticket")
        .where(todo.allocated_to == frappe.session.user)
        .where(todo.creation >= one_week_ago)
        .run(as_dict=False)
    )
    ticket_names = [row[0] for row in assigned_tickets]

    if not ticket_names:
        return {"count": 0, "tickets": []}

    allowed_statuses = frappe.get_all(
        "HD Ticket Status", filters={"category": ["!=", "Resolved"]}, pluck="name"
    )

    # Count tickets assigned in past week that are still assigned and not resolved
    count = frappe.db.count(
        "HD Ticket",
        filters=[
            ["name", "in", ticket_names],
            ["_assign", "like", f"%{frappe.session.user}%"],
            ["status", "in", allowed_statuses],
        ],
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
            ["name", "in", ticket_names],
            ["_assign", "like", f"%{frappe.session.user}%"],
            ["status", "in", allowed_statuses],
        ],
        order_by="modified desc",
        limit=5,
    )

    return {"count": count, "tickets": tickets}


@frappe.whitelist()
@agent_only
def get_recent_feedback():
    agent = frappe.session.user
    ticket = DocType("HD Ticket")

    # Get average rating and total feedbacks using query builder
    avg_result = (
        frappe.qb.from_(ticket)
        .select(
            (Avg(ticket.feedback_rating) * 5).as_("average"),
            Count(ticket.name).as_("total_feedbacks"),
        )
        .where(ticket.feedback_rating > 0)
        .where(Function("JSON_SEARCH", ticket._assign, "one", agent).isnotnull())
        .run(as_dict=True)
    )

    average_rating = (
        avg_result[0]["average"]
        if avg_result and avg_result[0]["average"] is not None
        else 0
    )
    total_feedbacks = (
        avg_result[0]["total_feedbacks"]
        if avg_result and avg_result[0]["total_feedbacks"] is not None
        else 0
    )

    # Get recent feedbacks using query builder
    feedback = (
        frappe.qb.from_(ticket)
        .select(
            ticket.name,
            ticket.feedback_rating,
            ticket.feedback,
            ticket.feedback_extra,
            ticket.contact,
        )
        .where(ticket.feedback_rating > 0)
        .where(Function("JSON_SEARCH", ticket._assign, "one", agent).isnotnull())
        .orderby(ticket.modified, order=frappe.qb.desc)
        .limit(10)
        .run(as_dict=True)
    )

    return {
        "average_rating": round(average_rating, 1),
        "total_feedbacks": total_feedbacks,
        "recent_feedbacks": feedback,
    }


@frappe.whitelist()
@agent_only
def get_avg_time_metrics(period: str = "6m"):
    periods = {
        "3m": 90,
        "6m": 180,
        "1y": 365,
    }

    days = periods.get(period, 180)
    agent = frappe.session.user

    current_from = frappe.utils.add_days(frappe.utils.nowdate(), -days)
    current_to = frappe.utils.nowdate()

    ticket = DocType("HD Ticket")
    to_date_plus_one = Function(
        "DATE_ADD", current_to, frappe.qb.terms.PseudoColumn("INTERVAL 1 DAY")
    )

    # Monthly aggregation query using query builder
    month_abbr = Function("DATE_FORMAT", ticket.creation, "%b")
    year_val = Function("YEAR", ticket.creation)
    month_val = Function("MONTH", ticket.creation)

    result = (
        frappe.qb.from_(ticket)
        .select(
            month_abbr.as_("month"),
            year_val.as_("year"),
            month_val.as_("month_num"),
            Avg(ticket.first_response_time).as_("avg_first_response"),
            Avg(ticket.resolution_time).as_("avg_resolution"),
        )
        .where(ticket.creation >= current_from)
        .where(ticket.creation < to_date_plus_one)
        .where(Function("JSON_SEARCH", ticket._assign, "one", agent).isnotnull())
        .where(
            ticket.first_response_time.isnotnull() | ticket.resolution_time.isnotnull()
        )
        .groupby(year_val, month_val)
        .orderby(year_val)
        .orderby(month_val)
        .run(as_dict=True)
    )

    data_dict = {}
    for row in result:
        key = f"{row['year']}-{row['month_num']:02d}"
        data_dict[key] = {
            "month": row["month"],
            "avg_first": round(row["avg_first_response"] or 0),
            "avg_resolution": round(row["avg_resolution"] or 0),
        }

    # Generate all months in the period
    now = datetime.datetime.now()
    data = []
    for i in range(days // 30 - 1, -1, -1):  # Approximate months from days
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

    # Calculate overall averages for the period using query builder
    overall_result = (
        frappe.qb.from_(ticket)
        .select(
            Avg(ticket.first_response_time).as_("avg_first_response"),
            Avg(ticket.resolution_time).as_("avg_resolution"),
        )
        .where(ticket.creation >= current_from)
        .where(ticket.creation < to_date_plus_one)
        .where(Function("JSON_SEARCH", ticket._assign, "one", agent).isnotnull())
        .where(
            ticket.first_response_time.isnotnull() | ticket.resolution_time.isnotnull()
        )
        .run(as_dict=True)
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
def get_pending_tickets():
    allowed_statuses = frappe.get_all(
        "HD Ticket Status", filters={"category": ["=", "Open"]}, pluck="name"
    )

    # Define DocTypes
    ticket = DocType("HD Ticket")
    priority = DocType("HD Ticket Priority")
    communication = DocType("Communication")

    # Subquery for last customer reply (received communications)
    last_customer_subq = (
        frappe.qb.from_(communication)
        .select(
            communication.reference_name,
            Max(communication.creation).as_("last_customer_reply"),
        )
        .where(communication.reference_doctype == "HD Ticket")
        .where(communication.sent_or_received == "Received")
        .groupby(communication.reference_name)
    )

    # Subquery for last agent reply (sent communications)
    last_agent_subq = (
        frappe.qb.from_(communication)
        .select(
            communication.reference_name,
            Max(communication.creation).as_("last_agent_reply"),
        )
        .where(communication.reference_doctype == "HD Ticket")
        .where(communication.sent_or_received == "Sent")
        .groupby(communication.reference_name)
    )

    # Build base query with joins and conditions
    base_query = (
        frappe.qb.from_(ticket)
        .left_join(priority)
        .on(ticket.priority == priority.name)
        .left_join(last_customer_subq)
        .on(Cast(ticket.name, "UNSIGNED") == last_customer_subq.reference_name)
        .left_join(last_agent_subq)
        .on(Cast(ticket.name, "UNSIGNED") == last_agent_subq.reference_name)
        .where(
            Function(
                "JSON_SEARCH", ticket._assign, "one", frappe.session.user
            ).isnotnull()
        )
        .where(ticket.status.isin(allowed_statuses))
        .where(last_customer_subq.last_customer_reply.isnotnull())
        .where(
            last_agent_subq.last_agent_reply.isnull()
            | (
                last_agent_subq.last_agent_reply
                < last_customer_subq.last_customer_reply
            )
        )
    )

    # Count query for total pending tickets
    count_result = base_query.select(Count(ticket.name).as_("total")).run(as_dict=True)
    total_pending_tickets = count_result[0].total if count_result else 0

    # Main query with select, order and limit
    query = (
        base_query.select(
            ticket.name,
            ticket.subject,
            ticket.status,
            ticket.priority,
            priority.integer_value.as_("priority_integer_value"),
            ticket.agent_group,
            ticket.response_by,
            ticket.resolution_by,
            ticket.resolution_date,
            ticket.agreement_status,
            ticket.status_category,
            ticket.first_responded_on,
            ticket.creation,
            last_customer_subq.last_customer_reply,
            last_agent_subq.last_agent_reply,
        )
        .orderby(last_customer_subq.last_customer_reply, order=frappe.qb.desc)
        .limit(5)
    )

    pending_tickets = query.run(as_dict=True)

    # Rename fields to match expected format
    for ticket in pending_tickets:
        ticket["priority.integer_value"] = ticket.pop("priority_integer_value")

    # Get priority range (cache this query as it's used frequently)
    priorities = frappe.get_all("HD Ticket Priority", fields="integer_value")
    if priorities:
        min_priority = min(priorities, key=lambda x: x["integer_value"])[
            "integer_value"
        ]
        max_priority = max(priorities, key=lambda x: x["integer_value"])[
            "integer_value"
        ]
    else:
        min_priority = max_priority = 0

    return {
        "tickets": pending_tickets,
        "total_pending_tickets": total_pending_tickets,
        "min_priority": min_priority,
        "max_priority": max_priority,
    }


@frappe.whitelist()
@agent_only
def get_upcoming_sla_violations(priority=None, order_by="response_by asc"):
    filters = [
        ["sla", "!=", ""],
        ["agreement_status", "in", ["First Response Due", "Resolution Due"]],
        ["status_category", "!=", "Closed"],
        ["_assign", "like", f"%{frappe.session.user}%"],
        ["resolution_by", ">", frappe.utils.now()],
        ["response_by", ">", frappe.utils.now()],
    ]
    if priority:
        filters.append(["priority", "=", priority])

    # Get total count of tickets about to breach SLA
    total_sla_violations_count = frappe.db.count("HD Ticket", filters=filters)

    upcoming_sla_violations = frappe.get_list(
        "HD Ticket",
        fields=[
            "name",
            "subject",
            "status",
            "priority",
            "priority.integer_value",
            "agent_group",
            "response_by",
            "resolution_by",
            "resolution_date",
            "agreement_status",
            "status_category",
            "first_responded_on",
        ],
        filters=filters,
        order_by=order_by,
        limit=5,
    )

    priorities = frappe.get_all("HD Ticket Priority", fields="integer_value")
    min_priority = min(priorities, key=lambda x: x["integer_value"])["integer_value"]
    max_priority = max(priorities, key=lambda x: x["integer_value"])["integer_value"]

    return {
        "upcoming_sla_violations": upcoming_sla_violations,
        "total_sla_violations_count": total_sla_violations_count,
        "min_priority": min_priority,
        "max_priority": max_priority,
    }


@frappe.whitelist()
def generate_data():
    import random
    from datetime import datetime, timedelta

    STATUSES = ["Open", "Replied", "Resolved", "Closed"]
    PRIORITIES = ["Low", "Medium", "High", "Urgent"]
    TICKET_TYPES = ["Question", "Bug", "Incident"]
    TEAMS = [team.name for team in frappe.get_all("HD Team")]
    FEEDBACK_OPTIONS = [
        "Response did not help",
        "No resolution provided",
        "Delayed response time",
        "Adequate help, bit slow",
        "Clear guidance given",
        "Helpful answers, reasonable wait",
        "Quick and precise solutions",
        "Prompt, informative support",
        "Exceptional support experience",
        "Instant, top-notch help",
    ]

    # Create 10 contacts
    contacts = []
    for i in range(10):
        first_name = f"User{i + 1}"
        last_name = "Test"
        email = f"user{i + 1}@example.com"
        contact = frappe.get_doc(
            {
                "doctype": "Contact",
                "first_name": first_name,
                "last_name": last_name,
                "email_id": email,
            }
        ).insert(ignore_permissions=True)
        contacts.append({"email": email, "name": contact.name})

    # Get current user as agent
    agent = frappe.session.user

    # Past 6 months
    now = datetime.now()
    start_date = now - timedelta(days=180)

    # Create tickets for each month
    current_date = start_date
    while current_date <= now:
        # Random number of tickets per month (20-50)
        num_tickets = random.randint(20, 50)

        for _ in range(num_tickets):
            # Random creation date in the month
            days_in_month = (current_date.replace(day=28) + timedelta(days=4)).replace(
                day=1
            ) - timedelta(days=1)
            random_day = random.randint(1, days_in_month.day)
            creation_date = current_date.replace(day=random_day)

            # Random subject
            subjects = [
                "Login issue",
                "Password reset",
                "Billing question",
                "Feature request",
                "Bug report",
                "Account setup",
                "Payment failed",
                "System error",
                "Data sync problem",
                "Performance issue",
            ]
            subject = random.choice(subjects) + f" #{random.randint(1000, 9999)}"

            # Random status
            status = random.choice(STATUSES)

            # Random priority
            priority = random.choice(PRIORITIES)

            # Random ticket type
            ticket_type = random.choice(TICKET_TYPES)

            # Random team
            agent_group = random.choice(TEAMS)

            # Create ticket data
            random_contact = random.choice(contacts)
            ticket_data = {
                "doctype": "HD Ticket",
                "subject": subject,
                "description": f"Detailed description for {subject}",
                "raised_by": random_contact["email"],
                "contact": random_contact["name"],
                "status": status,
                "priority": priority,
                "ticket_type": ticket_type,
                "agent_group": agent_group,
                "creation": creation_date.isoformat(),
            }

            # For resolved/closed tickets, add resolution data
            if status in ["Resolved", "Closed"]:
                # Random resolution time (hours)
                resolution_hours = random.randint(1, 168)  # 1 hour to 1 week
                resolution_time = resolution_hours * 3600  # in seconds

                # First response time (usually less than resolution)
                first_response_hours = random.randint(1, resolution_hours)
                first_response_time = first_response_hours * 3600

                # Resolution date
                resolution_date = creation_date + timedelta(hours=resolution_hours)

                ticket_data.update(
                    {
                        "resolution_time": resolution_time,
                        "first_response_time": first_response_time,
                        "resolution_date": resolution_date.isoformat(),
                        "first_responded_on": (
                            creation_date + timedelta(hours=first_response_hours)
                        ).isoformat(),
                    }
                )

                # Add feedback for some resolved tickets
                if random.random() < 0.7:  # 70% chance
                    feedback_rating = random.randint(1, 5)
                    feedback_option = random.choice(FEEDBACK_OPTIONS)
                    ticket_data.update(
                        {
                            "feedback_rating": feedback_rating,
                            "feedback": feedback_option,
                            "feedback_extra": f"Additional feedback for {subject}",
                            "status": "Closed",
                        }
                    )

                # Set SLA status
                sla_statuses = ["Fulfilled", "Failed"]
                ticket_data["agreement_status"] = random.choice(sla_statuses)

            # Create ticket
            ticket = frappe.get_doc(ticket_data).insert(ignore_permissions=True)
            frappe.db.set_value(
                "HD Ticket", ticket.name, "creation", creation_date.isoformat()
            )
            from frappe.desk.form.assign_to import add

            add(
                {
                    "doctype": "HD Ticket",
                    "name": ticket.name,
                    "assign_to": json.dumps([agent]),
                }
            )

        if current_date.month == 12:
            current_date = current_date.replace(
                year=current_date.year + 1, month=1, day=1
            )
        else:
            current_date = current_date.replace(month=current_date.month + 1, day=1)

    frappe.db.commit()

    return {"message": "Dummy data generated successfully"}

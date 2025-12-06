import frappe

from helpdesk.utils import get_agents_team, is_admin, is_agent


def permission_query(user):
    if not user:
        user = frappe.session.user

    if is_admin(user):
        return

    is_team_restriction_applied = frappe.db.get_single_value(
        "HD Settings", "restrict_tickets_by_agent_group"
    )

    base_filter = "`tabEmail Template`.reference_doctype = 'HD Ticket'"

    if not is_agent(user):
        query = (
            f"({base_filter} AND `tabEmail Template`.owner = {frappe.db.escape(user)})"
        )
        return query

    if is_team_restriction_applied:
        user_team = get_agents_team()
        user_team_names = [team["team_name"] for team in user_team]
        if not user_team_names:
            query = f"({base_filter} AND `tabEmail Template`.owner = {frappe.db.escape(user)})"
            return query

        team_names_escaped = ", ".join(f"'{team}'" for team in user_team_names)

        if is_admin():
            return

        query = f"""(
            {base_filter} AND (
                (`tabEmail Template`.owner = {frappe.db.escape(user)})
                OR 
                (`tabEmail Template`.name IN (
                    SELECT parent FROM `tabHD Canned Response Team` 
                    WHERE team IN ({team_names_escaped})
                ))
            )
        )"""

        return query
    else:
        return base_filter

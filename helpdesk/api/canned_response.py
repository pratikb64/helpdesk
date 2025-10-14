import frappe

from helpdesk.utils import get_agents_team


@frappe.whitelist()
def get_canned_responses():
    user_team = get_agents_team()
    user_team_names = [team["team_name"] for team in user_team]

    QBEmailTemplate = frappe.qb.DocType("Email Template")
    QBChildTeam = frappe.qb.DocType("HD Canned Response Team")

    if user_team_names:
        query = (
            frappe.qb.from_(QBEmailTemplate)
            .left_join(QBChildTeam)
            .on(QBChildTeam.parent == QBEmailTemplate.name)
            .select(QBEmailTemplate.star, QBChildTeam.team)
            .where(QBEmailTemplate.reference_doctype == "HD Ticket")
            .groupby(QBChildTeam.parent)
            .having(
                (QBChildTeam.team.isin(user_team_names)) | (QBChildTeam.team.isnull())
            )
        )
    else:
        query = (
            frappe.qb.from_(QBEmailTemplate)
            .select(QBEmailTemplate.star)
            .where(QBEmailTemplate.reference_doctype == "HD Ticket")
        )

    # # Get templates that either have matching teams or no teams assigned
    # if user_team_names:
    #     # If user has teams, get templates with matching teams OR no teams
    #     query = (
    #         frappe.qb.from_(QBEmailTemplate)
    #         .left_join(QBChildTeam)
    #         .on(QBChildTeam.parent == QBEmailTemplate.name)
    #         .select(QBEmailTemplate.star)
    #         .groupby(QBEmailTemplate.name)
    #         .having(
    #             (QBChildTeam.team.isin(user_team_names)) | (QBChildTeam.team.isnull())
    #         )
    #     )
    # else:
    #     # If user has no teams, only get templates with no teams assigned
    #     query = (
    #         frappe.qb.from_(QBEmailTemplate)
    #         .left_join(QBChildTeam)
    #         .on(QBChildTeam.parent == QBEmailTemplate.name)
    #         .select(QBEmailTemplate.star)
    #         .groupby(QBEmailTemplate.name)
    #         .having(QBChildTeam.team.isnull())
    #     )

    return query.run(as_dict=True)

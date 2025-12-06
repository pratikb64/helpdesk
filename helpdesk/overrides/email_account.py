from email import message_from_string

import frappe
from frappe import _
from frappe.email.doctype.email_account.email_account import EmailAccount
from frappe.email.receive import InboundMail
from utils import get_agents_team, is_admin, is_agent


class CustomEmailAccount(EmailAccount):
    def get_inbound_mails(self) -> list[InboundMail]:
        """retrive and return inbound mails."""
        mails = []

        def process_mail(messages, append_to=None):
            for index, message in enumerate(messages.get("latest_messages", [])):
                try:
                    _msg = message_from_string(
                        message.decode("utf-8", errors="replace")
                    )

                    # Important: If the email is auto-generated, we do not create a ticket
                    if _msg.get("X-Auto-Generated"):
                        continue

                    uid = (
                        messages["uid_list"][index]
                        if messages.get("uid_list")
                        else None
                    )
                    seen_status = messages.get("seen_status", {}).get(uid)
                    if self.email_sync_option != "UNSEEN" or seen_status != "SEEN":
                        _inbound_mail = InboundMail(
                            message,
                            self,
                            frappe.safe_decode(uid),
                            seen_status,
                            append_to,
                        )
                        mails.append(_inbound_mail)
                except Exception as e:
                    # Log the error but continue processing other emails
                    frappe.log_error(
                        title=_(
                            "Error processing email at index {0}, message: {1}"
                        ).format(index, e),
                        message=frappe.get_traceback(),
                    )
                    self.handle_bad_emails(index, message, frappe.get_traceback())
                    continue

        if not self.enable_incoming:
            return []

        try:
            if self.service == "Frappe Mail":
                frappe_mail_client = self.get_frappe_mail_client()
                messages = frappe_mail_client.pull_raw(
                    last_synced_at=self.last_synced_at
                )
                process_mail(messages)
                self.db_set(
                    "last_synced_at", messages["last_synced_at"], update_modified=False
                )
            else:
                email_sync_rule = self.build_email_sync_rule()
                email_server = self.get_incoming_server(
                    in_receive=True, email_sync_rule=email_sync_rule
                )
                if self.use_imap:
                    # process all given imap folder
                    for folder in self.imap_folder:
                        if email_server.select_imap_folder(folder.folder_name):
                            email_server.settings["uid_validity"] = folder.uidvalidity
                            messages = (
                                email_server.get_messages(
                                    folder=f'"{folder.folder_name}"'
                                )
                                or {}
                            )
                            process_mail(messages, folder.append_to)
                else:
                    # process the pop3 account
                    messages = email_server.get_messages() or {}
                    process_mail(messages)

                # close connection to mailserver
                email_server.logout()
        except Exception:
            self.log_error(
                title=_("Error while connecting to email account {0}").format(self.name)
            )
            return []

        return mails


def permission_query(user):
    if not user:
        user = frappe.session.user
    if is_admin(user):
        return

    # Check if team restrictions are enabled (similar to canned responses)
    is_team_restriction_applied = frappe.db.get_single_value(
        "HD Settings", "restrict_tickets_by_agent_group"
    )

    # For normal users (non-agents), only show email accounts they own
    if not is_agent(user):
        query = "`tabEmail Account`.owner = {user}".format(user=frappe.db.escape(user))
        return query

    # For agents, apply team-based restrictions if enabled
    if is_team_restriction_applied:
        teams = get_agents_team()
        user_team_names = [team["team_name"] for team in teams]

        # If agent belongs to a team with ignore_restrictions, show all email accounts
        if any(team.get("ignore_restrictions") for team in teams):
            return  # Return all email accounts

        # If agent has teams, show email accounts based on team membership
        if user_team_names:
            # Show email accounts owned by the user or their team members
            team_names = ", ".join(f"'{team}'" for team in user_team_names)
            query = """(
                `tabEmail Account`.owner = {user} OR 
                `tabEmail Account`.name IN (
                    SELECT DISTINCT ea.name 
                    FROM `tabEmail Account` ea
                    LEFT JOIN `tabHD Team Member` tm ON tm.user = ea.owner
                    WHERE tm.parent IN ({team_names})
                )
            )""".format(
                user=frappe.db.escape(user), team_names=team_names
            )
            return query
        else:
            # Agent has no teams, only show their own email accounts
            query = "`tabEmail Account`.owner = {user}".format(
                user=frappe.db.escape(user)
            )
            return query

    # If team restrictions are not enabled, show email accounts owned by the agent
    query = "`tabEmail Account`.owner = {user}".format(user=frappe.db.escape(user))
    return query

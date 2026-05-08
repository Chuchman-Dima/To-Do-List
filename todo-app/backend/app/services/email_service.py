import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


def send_task_list_email(to_email: str, tasks: list, from_user_email: str) -> None:
    """Send a formatted task list to the given email address."""
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        raise ValueError("SMTP credentials are not configured in .env")

    # Build HTML table
    rows = ""
    status_emoji = {"todo": "⬜", "in_progress": "🔄", "done": "✅"}
    for task in tasks:
        emoji = status_emoji.get(task.status.value, "")
        desc = task.description or "—"
        rows += f"""
        <tr>
            <td style="padding:8px;border:1px solid #ddd">{task.title}</td>
            <td style="padding:8px;border:1px solid #ddd">{desc}</td>
            <td style="padding:8px;border:1px solid #ddd;text-align:center">{emoji} {task.status.value}</td>
        </tr>"""

    html = f"""
    <html><body>
    <h2>📋 Task list shared by {from_user_email}</h2>
    <table style="border-collapse:collapse;width:100%;font-family:sans-serif">
        <thead>
            <tr style="background:#f2f2f2">
                <th style="padding:8px;border:1px solid #ddd;text-align:left">Title</th>
                <th style="padding:8px;border:1px solid #ddd;text-align:left">Description</th>
                <th style="padding:8px;border:1px solid #ddd;text-align:left">Status</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    <p style="color:#888;font-size:12px">Sent via Todo App</p>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📋 {from_user_email} shared their task list with you"
    msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.EMAILS_FROM_EMAIL, to_email, msg.as_string())

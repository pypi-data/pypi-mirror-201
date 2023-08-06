import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SmtpParams:
    def __init__(self, to: list | str, subject: str, body: str, sender: str | None = None):
        self.sender = sender
        self.to = to
        self.subject = subject
        self.body = body


class SmtpClient:
    def __init__(self, host: str, port: int, user: str | None = None, password: str | None = None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def send(self, params: SmtpParams):
        message = MIMEMultipart("alternative")
        if not params.sender:
            params.sender = "test@test.com"
        message["From"] = params.sender
        if type(params.to) == list:
            params.to = ', '.join(params.to)

        message["To"] = params.to
        message["Subject"] = params.subject

        message.attach(MIMEText(params.body, "html"))

        text = message.as_string()

        with smtplib.SMTP(self.host, self.port) as server:
            if self.user is not None and self.password is not None:
                server.login(self.user, self.password)
            server.sendmail(params.sender, params.to, text)


# params = SmtpParams(
#     ["aykut.canturk@opet.com.tr", "ayktcntrk@gmail.com"], "subject-test-123", "body-test")
# client = SmtpClient(
#     "mailapi.opetcloud.net", 25, "bt-opet", "[^tEqls&HXJUwE38baS+U}x4ARsOwS")

# client.send(params)

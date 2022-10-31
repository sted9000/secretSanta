import random
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import os
load_dotenv()

sender_email_address = os.getenv("EMAIL_ADDRESS")
sender_email_password = os.getenv("EMAIL_PASSWORD")
email = {
    "JJ": "JJ@email.com",
    "Lo": "Lo@email.com",
    "Pig": "Pig@email.com",
    "Coco": "Coco@email.com",
    "Rye": "Rye@email.com",
    "Kas": "Kas@email.com",
    "Ted": "Ted@email.com"
}
partners = [["JJ", "Lo"], ["Pig", "Coco"], ["Rye", "Kas"], ["Ted"]]
names = [inner for outer in partners for inner in outer]
recipient = []


def is_partner(potential_santa, potential_recipient):
    for partner in partners:
        if potential_santa in partner and potential_recipient in partner:
            return True
    return False


possible_santa = names.copy()
cont = 0
while cont == 0:
    redo = False
    possible_santa = names.copy()
    for i in range(0, len(names)):
        recip = random.randint(0, len(possible_santa) - 1)
        x = 0
        while x == 0:
            if names[i] == possible_santa[recip]:
                if len(possible_santa) == 1:
                    redo = True
                    x = 1
                else:
                    recip = random.randint(0, len(possible_santa) - 1)
            elif is_partner(names[i], possible_santa[recip]):
                if len(possible_santa) == 1:
                    redo = True
                    x = 1
                else:
                    recip = random.randint(0, len(possible_santa) - 1)
            else:
                x = 1

        if not redo:
            recipient.append(possible_santa[recip])
            possible_santa.pop(recip)
            cont = 1
        else:
            cont = 0


for (s, r) in zip(names, recipient):
    msg = MIMEText(f'{s} you are the secret santa of {r}. Gifts are to be used, handmade, recycled, or re-gifts. No gifts for or gifting of children.')
    msg['Subject'] = 'Secret Santa Assignments'
    msg['From'] = sender_email_address
    msg['To'] = email[s]

    with smtplib.SMTP('smtp.gmail.com', 587) as server:

        # start TLS for security
        server.starttls()

        # Authentication
        server.login(sender_email_address, sender_email_password)

        # sending the mail
        server.sendmail(sender_email_address, email[s], msg.as_string())

        # terminating the session
        server.quit()

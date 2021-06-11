import subprocess
import smtplib
import ssl
import socket

process = subprocess.Popen(['df', '-h'], stdout=subprocess.PIPE)
out, err = process.communicate()
out = out.splitlines()[1:]

# emailhez szukseges valtozok
sender_email = "XXX"  # kuldo e-mail cime
sender_password = "YYY"  # kuldo jelszava
receiver_email = "ZZZ"  # Kinek menjen az e-mail?

lowondiskspace = []


def lss(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1 + ", "


for i in out:
    tmp = str(i).split(' ')
    tmp2 = []
    for x in tmp:
        if x != '':
            tmp2.append(x)
    # print(tmp2[-1].replace("'", "") + " " + tmp2[4].replace("%", ""))
    drive = tmp2[-1].replace("'", "")
    percentage_str = tmp2[4].replace("%", "")
    percentage_int = int(percentage_str)
    if percentage_int >= 90:
        print(drive + " " + percentage_str)
        lowondiskspace.append(drive)
    # print(drive + " " + percentage_str)

szervernev = socket.getfqdn()
liststring = ', '.join([str(elem) for elem in lowondiskspace])

message = """Subject: """ + szervernev + """ - keves a tarhely 
A tarhely 90%-a hasznalatban van bizonyos particiokon.
A kovetkezo particio(k) erintett(ek): """ + liststring

if lowondiskspace:
    with smtplib.SMTP_SSL("mailserver", 465, ssl.create_default_context()) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
        exit()
else:
    print("minden gucci :)")

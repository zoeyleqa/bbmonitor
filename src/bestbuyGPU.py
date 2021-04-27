from os.path import join, dirname
from dotenv import load_dotenv
 
# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')
 
# Load file from the path.
load_dotenv(dotenv_path)

import requests
import time
# import io
import datetime
import webbrowser
import smtplib
import ssl
import os
print(os.environ['HOME'])
from GPUlist import gpu_links

# DO NOT TOUCH -----------------------------------------------
config = {
    "port": 465,  # For SSL
    # port: 587 # For TLS
    "receiver_email": "tunguyen2705@gmail.com", 
    # "receiver_email": "wanhdynamite@gmail.com",
    "headers": {"User-Agent": "Mozilla/5.0"},
    "context": ssl.create_default_context(),
    "headerMsg": """\
From: Best Buy Monitor Bot
MIME-Version: 1.0
Content-type: text/html
Subject: Testing testing!!!

<h2>Sup sup,</h2>
<p>Best Buy item below might be available:</p>
""",
    "footerMsg": """\
<br><hr>
<p>This bot checks and notifies when an item in the list doesn't have the <i>"Sold Out"</i> button. If that's not correct, hmu!!!</p>
<p>-QA-</p>
"""
}

        
def getSkuID(name):
    return gpu_links[name][gpu_links[name].rfind("=")+1:len(gpu_links[name])]


def check():
    # check each gpu
    for gpu_name in gpu_links:
        # only check gpu that was sold out
        if gpu_name in gpuToCheck and not gpuToCheck[gpu_name]:
            gpuToCheck[gpu_name] = check_single(gpu_name)

            # open link and email to notify
            if gpuToCheck[gpu_name]:
                webbrowser.open(gpu_links[gpu_name])
                print("-------------", datetime.datetime.now(),
                      "-------------", "\nIn stock: ", gpu_name, )
                # signal()
                email_me(gpu_name)


def check_single(name):
    source = requests.get(gpu_links[name], headers=config["headers"]).text
    # is_sold_out = source.__contains__("<button type=\"button\" class=\"btn btn-disabled btn-lg btn-block add-to-cart-button\" disabled=\"\" style=\"padding:0 8px\">Sold Out</button></div></div>")
    soldOutBtn = "<button class=\"btn btn-disabled btn-lg btn-block add-to-cart-button\" disabled=\"\" type=\"button\"" + \
        " data-sku-id=\"" + getSkuID(name) + \
        "\" style=\"padding:0 8px\">Sold Out</button>"
    comingSoonBtn = "<button class=\"btn btn-disabled btn-lg btn-block add-to-cart-button\" disabled=\"\" type=\"button\"" + \
        " data-sku-id=\"" + getSkuID(name) + \
        "\" style=\"padding:0 8px\">Coming Soon</button>"
    # debug log
    # if not source.__contains__(soldOutBtn):
    #     print(soldOutBtn)
    #     with io.open('src/log', "w", encoding="utf-8") as f:
    #         f.write(source)

    return not source.__contains__(soldOutBtn) and not source.__contains__(comingSoonBtn)


def signal():
    while True:
        print("FOUND, SCROLL UP")
        time.sleep(30)


def email_me(name):
    msg = config["headerMsg"] + "<h3>" + name + "</h3><br><br>" + gpu_links[name] + "<br>" + config["footerMsg"]
    print('Sending email...')
    # with smtplib.SMTP("smtp.gmail.com", port) as server:
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", config["port"])
        # server.starttls()
        # server.ehlo()
        server.login(os.getenv('SENDER_EMAIL'), os.getenv('PASSWORD'))
        server.sendmail(os.getenv('SENDER_EMAIL'), config["receiver_email"], msg)
        print('----> email sent!')
        server.close()
    except:
        print('nope')
        server.close()


if __name__ == '__main__':
    gpuToCheck = {}
    # assume all are unavailable
    for gpu_name in gpu_links:
        gpuToCheck[gpu_name] = False

    while True:
        print("...just keep swimming...")
        check()
        time.sleep(5)

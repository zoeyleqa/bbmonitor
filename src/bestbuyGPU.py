from os.path import join, dirname
from dotenv import load_dotenv
import requests
import time
import io
from datetime import datetime
import webbrowser
import smtplib
import ssl
import os
from GPUlist import gpu_links

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

config = {
    "port": 465,  # For SSL
    # port: 587 # For TLS
    "receiver_email": "wanhdynamite@gmail.com",
    # "receiver_email": "tunguyen2705@gmail.com",
    "cc": "wanhdynamite@gmail.com",
    "headers": {"User-Agent": "Mozilla/5.0"},
    "context": ssl.create_default_context(),
    "headerMsg": """\
From: Best Buy Monitor Bot
MIME-Version: 1.0
Content-type: text/html
Subject: BestBuy GPU available maybe!!!

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
                print("-------------", datetime.now(),
                      "-------------", "\nIn stock: ", gpu_name, )
                # signal()
                # email_me(gpu_name)


def check_single(name):
    try:
        source = requests.get(gpu_links[name], headers=config["headers"]).text
        soldOutBtn = '<button class="btn btn-disabled btn-lg btn-block add-to-cart-button" disabled="" ' + \
                    'type="button" data-sku-id="'+ getSkuID(name) +'" data-button-state="SOLD_OUT" ' + \
                    'style="padding:0 8px">Sold Out</button>'
        comingSoonBtn = '<button class="btn btn-disabled btn-lg btn-block add-to-cart-button" disabled="" ' + \
                    'type="button" data-sku-id="'+ getSkuID(name) +'" data-button-state="COMING_SOON" ' + \
                    'style="padding:0 8px">Coming Soon</button>'
        unavailableBtn = '<button class="btn btn-disabled btn-lg btn-block add-to-cart-button" disabled="" ' + \
                    'type="button" data-sku-id="'+ getSkuID(name) +'" data-button-state="UNAVAILABLE_NEARBY" ' + \
                    'style="padding:0 8px">Unavailable Nearby</button>'
        # debug log
        # if not source.__contains__(soldOutBtn) and not source.__contains__(comingSoonBtn) and not source.__contains__(unavailableBtn):
        #     now = datetime.now().strftime("%m-%d-%Y-%H%M%S")
        #     with io.open('src/log'+ '-' + now +'.txt', "w", encoding="utf-8") as f:
        #         f.write(soldOutBtn+"\n")
        #         f.write(comingSoonBtn+"\n")
        #         f.write(unavailableBtn+"\n")
        #         f.write("--------------------------------------------------------\n")
        #         f.write(source)
    except:
        print("check single failed ... moving on")
        return False

    return not source.__contains__(soldOutBtn) and not source.__contains__(comingSoonBtn) and not source.__contains__(unavailableBtn)


def signal():
    while True:
        print("FOUND, SCROLL UP")
        time.sleep(30)


def email_me(name):
    msg = config["headerMsg"] + "<h3>" + name + "</h3><br><br>" + \
        gpu_links[name] + "<br>" + config["footerMsg"]
    print('Sending email...')
    # with smtplib.SMTP("smtp.gmail.com", port) as server:
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", config["port"])
        # server.starttls()
        # server.ehlo()
        server.login(os.getenv('SENDER_EMAIL'), os.getenv('PASSWORD'))
        server.sendmail(os.getenv('SENDER_EMAIL'),
                        config["receiver_email"], msg)
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

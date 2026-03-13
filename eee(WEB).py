import requests
import json
import uuid
import random
import string
import time
import base64
import re
from datetime import datetime

def generate_lsd():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(chars) for _ in range(32))



def generate_browser_machine_id():
    return ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=11))
def generate_csrftoken():
    chars = string.ascii_letters + string.digits
    csrftoken = ''.join(random.choices(chars, k=32))
    return csrftoken


def generate_mid():
    timestamp = int(time.time())
    prefix = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    time_hex = hex(timestamp)[2:]
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=14))
    mid = f"{prefix}{time_hex}{suffix}"
    return mid

def send_web_registration_request(email, full_name, username, password, birthday_day, birthday_month, birthday_year):
    current_time = int(time.time())
    client_mutation_id = str(uuid.uuid4())
    waterfall_id =str(uuid.uuid4()) #"db754c01-35a1-4b2f-ad91-4bdaf52314a0"   
    ig_did   = str(uuid.uuid4()).upper()
    machine_id = generate_browser_machine_id()
    encrypted_password = f"#PWD_BROWSER:0:0:{password}"
    csrf_token = generate_csrftoken()
    lsd_token = "AdSocsw7kp61PS0OGAlyfHu2SqQ"#generate_lsd()
    variables = {
        "input": {
            "actor_id": "0",
            "client_mutation_id": client_mutation_id,
            "machine_id": machine_id,
            "reg_data": {
                "birthday_day": birthday_day,
                "birthday_month": birthday_month,
                "birthday_year": birthday_year,
                "contactpoint": {
                    "sensitive_string_value": email
                },
                "contactpoint_type": "EMAIL",
                "custom_gender": "",
                "did_use_age": False,
                "firstname": {
                    "sensitive_string_value": ""
                },
                "fullname": {
                    "sensitive_string_value": full_name
                },
                "ig_age_block_data": None,
                "lastname": {
                    "sensitive_string_value": ""
                },
                "preferred_pronoun": None,
                "reg_passwd__": {
                    "sensitive_string_value": encrypted_password
                },
                "sex": None,
                "use_custom_gender": False,
                "username": {
                    "sensitive_string_value": username
                }
            },
            "waterfall_id": waterfall_id
        }
    }
    
    payload = {
        "av": "0",
        "__d": "www",
        "__user": "0",
        "__a": "1",
        "lsd": "AdSocsw7kp61PS0OGAlyfHu2SqQ",
        "jazoest": "22342",
        "__spin_r": "1034862556",
        "__spin_b": "trunk",
        "__spin_t": str(int(time.time())),
        "__crn": "comet.igweb.PolarisCAAIGRegistrationHomepageRoute",
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "useCAARegistrationFormSubmitMutation",
        "server_timestamps": "true",
        "variables": json.dumps(variables, separators=(',', ':')),
        "doc_id": "25782408224726258"
    }
    
    headers = {
        "Host": "www.instagram.com",
        "Cookie": f"csrftoken={csrf_token}; datr=2JiwaZZwQnWVb1GJvN34Ll9M; ig_did={ig_did}; mid={machine_id}; dpr=1.875; wd=980x460",
        "Sec-Ch-Ua-Full-Version-List": '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.179", "Google Chrome";v="138.0.7204.179"',
        "Sec-Ch-Ua-Platform": '"Linux"',
        "X-Csrftoken": csrf_token,
        "Sec-Ch-Ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "X-Fb-Friendly-Name": "useCAARegistrationFormSubmitMutation",
        "Sec-Ch-Ua-Mobile": "?0",
        "X-Ig-App-Id": "936619743392459",
        "Sec-Ch-Ua-Model": '""',
        "X-Asbd-Id": "359341",
        "X-Fb-Lsd": "AdSocsw7kp61PS0OGAlyfHu2SqQ",
        "Sec-Ch-Prefers-Color-Scheme": "light",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Sec-Ch-Ua-Platform-Version": '""',
        "Accept": "*/*",
        "Origin": "https://www.instagram.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.instagram.com/accounts/emailsignup/?next=",
        
        "Accept-Language": "en-US,en;q=0.9",
        "Priority": "u=1, i"
    }
    
    try:
        response = requests.post("https://www.instagram.com/api/graphql",headers=headers,data=payload,timeout=30 )
        print(f"Response status: {response.text}")
        if response.status_code == 200:
           if response.text.__contains__("ntf_context"):
                ntf_context = re.search(r'"ntf_context":"([^"]+)"', response.text)
                if ntf_context:
                    ntf_context = ntf_context.group(1)
                    print("âRegistration successful. Sending confirmation request...")
                send_confirmation_request(username,password,full_name,email,ntf_context,client_mutation_id, csrf_token, machine_id,ig_did, lsd_token)
        else:
            print(f"â Failed with status: {response.status_code}")
          
            
    except Exception as e:
        print(f"â Error: {e}")
    
    
def send_confirmation_request(username,password,full_name,email,ntf_context,client_mutation_id, csrftoken, mid, ig_did, lsd):
    headers = {
        "Host": "www.instagram.com",
        "Cookie": f"csrftoken={csrftoken}; datr=2JiwaZZwQnWVb1GJvN34Ll9M; ig_did={ig_did}; mid={mid}; dpr=1.875; wd=980x460",
        "Sec-Ch-Ua-Full-Version-List": '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.179", "Google Chrome";v="138.0.7204.179"',
        "Sec-Ch-Ua-Platform": '"Linux"',
        "X-Csrftoken": csrftoken,
        "Sec-Ch-Ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "X-Fb-Friendly-Name": "CAAConfirmationFormDesktopQuery",
        "Sec-Ch-Ua-Mobile": "?0",
        "X-Ig-App-Id": "936619743392459",
        "Sec-Ch-Ua-Model": '""',
        "X-Asbd-Id": "359341",
        "X-Fb-Lsd": lsd,
        "Sec-Ch-Prefers-Color-Scheme": "light",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Sec-Ch-Ua-Platform-Version": '""',
        "Accept": "*/*",
        "Origin": "https://www.instagram.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.instagram.com/accounts/emailsignup/?next=",
        "Accept-Language": "en-US,en;q=0.9",
        "Priority": "u=1, i"
    }
    variables = {
        "args": {
            "context": ntf_context
        },
        "scale": 1
    }
    
    payload = {
        "av": "0",
        "__d": "www",
        "__user": "0",
        "__a": "1",
       
        "lsd": "AdSocsw7kp61PS0OGAlyfHu2SqQ",
        "jazoest": "22342",
        "__spin_r": "1034862556",
        "__spin_b": "trunk",
        "__spin_t": str(int(time.time())),
        "__crn": "comet.igweb.PolarisCAAIGRegistrationHomepageRoute",
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "CAAConfirmationFormDesktopQuery",
        "server_timestamps": "true",
        "variables": json.dumps(variables, separators=(',', ':')),
        "doc_id": "24013423051688880"
    }
    
    try:
        response = requests.post("https://www.instagram.com/api/graphql",headers=headers,data=payload,timeout=30)
        # print(f"Response status: {response.text}")
        if response.status_code == 200 and response.text.__contains__(f"To confirm your account, enter the 6-digit code we sent to {email}"):
            print("âConfirmation request sent successfully.")
            code = input("Enter the 6-digit confirmation code: ")
            send_confirmation_submit_request(username,password,full_name,email,code,ntf_context,client_mutation_id, csrftoken, mid, ig_did, lsd)
   
            
    
    except Exception as e:
        print(f" Unexpected error: {e}")
        
        
        
        
        
def send_confirmation_submit_request(username,password,full_name,email,confirmation_code, ig_reg_data, client_mutation_id, csrf_token, machine_id, ig_did, lsd_token):
    
    headers = {
        "Host": "www.instagram.com",
        "Cookie": f"csrftoken={csrf_token}; datr=2JiwaZzQnWVb1GJvN34Ll9M; ig_did={ig_did}; mid={machine_id}; dpr=1.875; wd=980x460",
        "Sec-Ch-Ua-Full-Version-List": '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.179", "Google Chrome";v="138.0.7204.179"',
        "Sec-Ch-Ua-Platform": '"Linux"',
        "X-Csrftoken": csrf_token,
        "Sec-Ch-Ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "X-Fb-Friendly-Name": "useCAARegistrationFormSubmitMutation",
        "Sec-Ch-Ua-Mobile": "?0",
        "X-Ig-App-Id": "936619743392459",
        "Sec-Ch-Ua-Model": '""',
        "X-Asbd-Id": "359341",
        "X-Fb-Lsd": lsd_token,
        "Sec-Ch-Prefers-Color-Scheme": "light",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Sec-Ch-Ua-Platform-Version": '""',
        "Accept": "*/*",
        "Origin": "https://www.instagram.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.instagram.com/accounts/emailsignup/?next=",
        
        "Accept-Language": "en-US,en;q=0.9",
        "Priority": "u=1, i"
    }

    variables = {
        "input": {
            "actor_id": "0",
            "client_mutation_id": client_mutation_id,
            "conf_code": {
                "sensitive_string_value": confirmation_code
            },
            "ig_reg_data": ig_reg_data,
            "machine_id": machine_id,
            "youth_consent_decision_time": None
        }
    }
    payload = {
        "av": "0",
        "__d": "www",
        "__user": "0",
        "__a": "1",
        "lsd": "AdSocsw7kp61PS0OGAlyfHu2SqQ",
        "jazoest": "22342",
        "__spin_r": "1034862556",
        "__spin_b": "trunk",
        "__spin_t": "1773181144",
        "__crn": "comet.igweb.PolarisCAAIGRegistrationHomepageRoute",
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "useCAAFBConfirmationFormSubmitMutation",
        "server_timestamps": "true",
        "variables": json.dumps(variables, separators=(',', ':')),
        "doc_id": "24050931851170558"
    }
    try:
        response = requests.post("https://www.instagram.com/api/graphql",headers=headers,data=payload,timeout=30)
        # print(f"Response status: {response.text}")
        if response.status_code == 200 and response.text.__contains__(username):
            print("âAccount confirmed and created successfully.")
        elif response.status_code == 200 and response.text.__contains__("\"user_id\":null,"):
            print("â account got banned after confirmation.")
        elif response.text.__contains__("The confirmation code you entered is invalid or has expired. Please make sure you entered your confirmation code correctly."): 
            print("â Invalid or expired confirmation code.")   
        else:
            print(f"â Confirmation failed with status: {response.status_code} and response: {response.text}")
        
    except Exception as e:
        print(f"\nâ Ø®Ø·Ø£: {e}")
        return {"success": False, "error": str(e)}
    
FIRST_NAMES = [
"James","John","Robert","Michael","William","David","Richard","Joseph","Thomas","Charles",
"Christopher","Daniel","Matthew","Anthony","Mark","Donald","Steven","Paul","Andrew","Joshua",
"Kenneth","Kevin","Brian","George","Edward","Ronald","Timothy","Jason","Jeffrey","Ryan",
"Jacob","Gary","Nicholas","Eric","Stephen","Jonathan","Larry","Justin","Scott","Brandon",
"Benjamin","Samuel","Frank","Gregory","Raymond","Alexander","Patrick","Jack","Dennis","Jerry",
"Tyler","Aaron","Jose","Henry","Adam","Douglas","Nathan","Peter","Zachary","Kyle",
"Walter","Harold","Jeremy","Ethan","Carl","Keith","Roger","Gerald","Christian","Terry",
"Sean","Arthur","Austin","Noah","Jesse","Joe","Bryan","Billy","Jordan","Albert",
"Dylan","Bruce","Willie","Gabriel","Alan","Juan","Logan","Wayne","Ralph","Roy",
"Louis","Russell","Vincent","Philip","Bobby","Johnny","Bradley"
]

LAST_NAMES = [
"Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
"Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin",
"Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson",
"Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores",
"Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts",
"Gomez","Phillips","Evans","Turner","Diaz","Parker","Cruz","Edwards","Collins","Reyes",
"Stewart","Morris","Morales","Murphy","Cook","Rogers","Gutierrez","Ortiz","Morgan","Cooper",
"Peterson","Bailey","Reed","Kelly","Howard","Ramos","Kim","Cox","Ward","Richardson",
"Watson","Brooks","Chavez","Wood","James","Bennett","Gray","Mendoza","Ruiz","Hughes"
]
PREFIX = ["real","its","the","official","mr","king","im"]
SUFFIX = ["official","real","live","world","hub"]

SEPARATORS = ["", ".", "_"]
def generate_full_name():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}"   

def generate_strong_password(length=12):
    if length < 8:
        length = 12
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*"
    password = [random.choice(lowercase),random.choice(uppercase),random.choice(digits),random.choice(symbols)]
    all_chars = lowercase + uppercase + digits + symbols
    for _ in range(length - 4):
        password.append(random.choice(all_chars))
    random.shuffle(password)
    return ''.join(password)
def generate_username():

    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    sep = random.choice(SEPARATORS)

    number = random.randint(1, 999999)
    year = random.randint(1980, 2026)

    patterns = [
        f"{first}{sep}{last}",
        f"{first}{sep}{last}{number}",
        f"{first}{sep}{last}{year}",
        f"{first}{number}",
        f"{last}{number}",
        f"{first}{sep}{last}{random.choice(string.ascii_lowercase)}",
        f"{random.choice(PREFIX)}{sep}{first}{sep}{last}",
        f"{first}{sep}{last}{sep}{random.choice(SUFFIX)}",
        f"{first}{sep}{last}{sep}{number}",
        f"{random.choice(PREFIX)}{sep}{first}{number}"
    ]
    return f"{first}{sep}{last}{number}{random.choice(SUFFIX)}"   
    
if __name__ == "__main__":
   email = input("Enter email: ")
   username = generate_username()
   print(f"Generated username: {username}")
   password = generate_strong_password()
   print(f"Generated password: {password}")
   full_name = generate_full_name()
   print(f"Generated full name: {full_name}")
   birthday_day = random.randint(1, 28)
   print(f"Generated birthday day: {birthday_day}")
   birthday_month = random.randint(1, 12)
   print(f"Generated birthday month: {birthday_month}")
   birthday_year = random.randint(1990, 2008)
   print(f"Generated birthday year: {birthday_year}")
   send_web_registration_request(email, full_name, username, password, birthday_day, birthday_month, birthday_year)
   

import random
import re
import secrets
import string
import uuid
import json
import requests 
import time
import base64
import tzlocal
import calendar
from datetime import datetime
from datetime import date
def device_id():
    random_part = ''.join(random.choices(string.hexdigits.lower(), k=16))
    return f"android-{random_part}"

def generate_user_agent():
    INSTAGRAM_VERSION = "361.0.0.46.88"
    phones = [
        {"model": "SM-G935F", "brand": "samsung", "resolution": "900x1600", "dpi": "300dpi"},
        {"model": "SM-N975F", "brand": "samsung", "resolution": "1080x2280", "dpi": "420dpi"},
        {"model": "Pixel 4", "brand": "google", "resolution": "1080x2280", "dpi": "440dpi"},
        {"model": "MI 9", "brand": "Xiaomi", "resolution": "1080x2340", "dpi": "440dpi"},
        {"model": "HD1913", "brand": "OnePlus", "resolution": "1080x2400", "dpi": "420dpi"},
        {"model": "SM-G973F", "brand": "samsung", "resolution": "1080x2280", "dpi": "420dpi"},
        {"model": "Pixel 5", "brand": "google", "resolution": "1080x2340", "dpi": "440dpi"},
    ]
    android_versions = [
        "28/9",
        "29/10", 
        "30/11",
    ]
    phone = random.choice(phones)
    android = random.choice(android_versions)
    app_id = random.randint(674675155, 674675999)
    ua = f"Instagram {INSTAGRAM_VERSION} Android ({android}; {phone['dpi']}; {phone['resolution']}; {phone['brand']}; {phone['model']}; {phone['model']}; intel; en_US; {app_id})"
    
    device_data = {
        "user_agent": ua,
        "android_version": android,
        "device_model": phone['model'],
        "device_brand": phone['brand'],
        "screen_resolution": phone['resolution'],
        "screen_dpi": phone['dpi'],
        "instagram_version": INSTAGRAM_VERSION,
        "app_id": app_id
    }
    
    return ua, device_data

def generate_machine_id():
   return secrets.token_hex(8) 


def send_signup_request():
    user_agent, device_info = generate_user_agent()
    current_device_id = device_id()
    current_qpl_join_id = str(uuid.uuid4())
    current_waterfall_id = str(uuid.uuid4())
    current_qe_device_id = str(uuid.uuid4())
    current_family_device_id = str(uuid.uuid4())
    current_time = datetime.now().timestamp()
    headers = {
        "Host": "b.i.instagram.com",
        "X-Ig-App-Locale": "en_US",
        "X-Ig-Device-Locale": "en_US",
        "X-Ig-Mapped-Locale": "en_US",
        "X-Pigeon-Session-Id": f"UFS-{str(uuid.uuid4())}-0",
        "X-Pigeon-Rawclienttime": str(current_time),
        "X-Ig-Bandwidth-Speed-Kbps": "-1.000",
        "X-Ig-Bandwidth-Totalbytes-B": "0",
        "X-Ig-Bandwidth-Totaltime-Ms": "0",
        "X-Bloks-Version-Id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
        "X-Ig-Www-Claim": "0",
        "X-Bloks-Prism-Button-Version": "CONTROL",
        "X-Bloks-Prism-Colors-Enabled": "false",
        "X-Bloks-Prism-Ax-Base-Colors-Enabled": "false",
        "X-Bloks-Prism-Font-Enabled": "false",
        "X-Bloks-Is-Layout-Rtl": "false",
        "X-Ig-Device-Id": current_qe_device_id,
        "X-Ig-Android-Id": current_device_id,
        "X-Ig-Timezone-Offset": "28800",
        "X-Fb-Connection-Type": "WIFI",
        "X-Ig-Connection-Type": "WIFI",
        "X-Ig-Capabilities": "3brTv10=",
        "X-Ig-App-Id": "567067343352427",
        "Priority": "u=3",
        "User-Agent": user_agent,
        "Accept-Language": "en-US",
        "Ig-Intended-User-Id": "0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Fb-Http-Engine": "Liger",
        "X-Fb-Client-Ip": "True",
        "X-Fb-Server-Cluster": "True",
        "Connection": "keep-alive"
    }
    params_data = {
        "is_from_logged_out": False,
        "logged_out_user": "",
        "qpl_join_id": current_qpl_join_id,
        "family_device_id": current_family_device_id,
        "device_id": current_device_id,
        "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
        "waterfall_id": current_waterfall_id,
        "show_internal_settings": False,
        "last_auto_login_time": 0,
        "disable_auto_login": False,
        "qe_device_id": current_qe_device_id,
        "is_from_logged_in_switcher": False,
        "switcher_logged_in_uid": "",
        "account_list": [],
        "blocked_uid": [],
        "INTERNAL_INFRA_THEME": "HARMONIZATION_F",
        "launched_url": "",
        "sim_phone_numbers": []
    }
    bk_context = {"bloks_version": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf","styles_id": "instagram"}
    payload = {"params": json.dumps(params_data),"bk_client_context": json.dumps(bk_context),"bloks_versioning_id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf"}
    url = "https://b.i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.login.process_client_data_and_redirect/"
    try:
        respo = requests.post(url, headers=headers,data=payload,timeout=15)
        response = respo.text.replace('//', '', 1)
        if str.__contains__(response, "aaccs"):
            aaccs_token = re.search(r'"aaccs\\*":\\*"(.*?)\\\\\\"', response)
            if aaccs_token:
                aaccs_token = aaccs_token.group(1)
            else:
                print("didnt found aaccs token in the response")
                
            aacjid_toekn = re.search(r'"aacjid\\*":\\*"(.*?)\\\\\\"', response)
            if aacjid_toekn:
                aacjid_toekn = aacjid_toekn.group(1)
           
            else:
                print("didnt found aacjid token in the response")
            
            aac_init_timestamp_token= re.search(r'"aac_init_timestamp\\*":(.*?),', response)     
            if aac_init_timestamp_token:
                aac_init_timestamp_token = aac_init_timestamp_token.group(1)
               
            else:
                print("didnt found aac_init_timestamp token in the response")
            email = input("Enter the email: ").strip()
            registration_flow_id= str(uuid.uuid4())
            machine_id= generate_machine_id()
            time.sleep(2)    
            send_email_request(email, aaccs_token, aacjid_toekn, current_device_id, current_waterfall_id, current_qe_device_id, current_family_device_id,user_agent,aac_init_timestamp_token,registration_flow_id,machine_id)
             
    except Exception as e:
        print(f"â Error: {str(e)}")
        return "error"
    

def send_email_request(email,aaccs,aacjid,device_id_val,waterfall_id,qe_device_id,family_device_id,user_agent,aac_init_timestamp,registration_flow_id,machine_id ):

    current_time = datetime.now().timestamp()
    pigeon_session_id = f"UFS-{str(uuid.uuid4())}-0"
    event_request_id = str(uuid.uuid4())
    text_input_id = random.randint(110000000000000, 119999999999999)
    latency_instance_id = float(f"1.{random.randint(10000000000000, 99999999999999)}E14")
    headers = {
        "Host": "i.instagram.com",
        "X-Ig-App-Locale": "en_US",
        "X-Ig-Device-Locale": "en_US",
        "X-Ig-Mapped-Locale": "en_US",
        "X-Pigeon-Session-Id": pigeon_session_id,
        "X-Pigeon-Rawclienttime": str(current_time),
        "X-Ig-Bandwidth-Speed-Kbps": "-1.000",
        "X-Ig-Bandwidth-Totalbytes-B": "0",
        "X-Ig-Bandwidth-Totaltime-Ms": "0",
        "X-Bloks-Version-Id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
        "X-Ig-Www-Claim": "0",
        "X-Bloks-Prism-Button-Version": "CONTROL",
        "X-Bloks-Prism-Colors-Enabled": "false",
        "X-Bloks-Prism-Ax-Base-Colors-Enabled": "false",
        "X-Bloks-Prism-Font-Enabled": "false",
        "X-Bloks-Is-Layout-Rtl": "false",
        "X-Ig-Device-Id": qe_device_id,
        "X-Ig-Family-Device-Id": family_device_id,
        "X-Ig-Android-Id": device_id_val,
        "X-Ig-Timezone-Offset": "28800",
        "X-Ig-Nav-Chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1772845836.640::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_phone:2:button:1772845839.819::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_email:3:button:1772845841.684::",
        "X-Fb-Connection-Type": "WIFI",
        "X-Ig-Connection-Type": "WIFI",
        "X-Ig-Capabilities": "3brTv10=",
        "X-Ig-App-Id": "567067343352427",
        "Priority": "u=3",
        "User-Agent": user_agent,
        "Accept-Language": "en-US",
        "X-Mid": machine_id,
        "Ig-Intended-User-Id": "0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Fb-Http-Engine": "Liger",
        "X-Fb-Client-Ip": "True",
        "X-Fb-Server-Cluster": "True",
        "Connection": "keep-alive"
    }
    client_input_params = {
        "aac": json.dumps({
            "aac_init_timestamp": aac_init_timestamp,
            "aacjid": aacjid,
            "aaccs": aaccs
        }, separators=(',', ':')),
        "device_id": device_id_val,
        "zero_balance_state": "",
        "network_bssid": None,
        "msg_previous_cp": "",
        "email_token": "",
        "switch_cp_first_time_loading": 1,
        "accounts_list": [],
        "email_prefilled": 0,
        "confirmed_cp_and_code": {},
        "family_device_id": family_device_id,
        "block_store_machine_id": "",
        "fb_ig_device_id": [],
        "lois_settings": {"lois_token": ""},
        "cloud_trust_token": None,
        "is_from_device_emails": 0,
        "email": email,
        "switch_cp_have_seen_suma": 0
    }
    server_params = {
        "event_request_id": event_request_id,
        "is_from_logged_out": 0,
        "text_input_id": text_input_id,
        "layered_homepage_experiment_group": None,
        "device_id": device_id_val,
        "login_surface": "unknown",
        "waterfall_id": waterfall_id,
        "INTERNAL__latency_qpl_instance_id": latency_instance_id,
        "flow_info": json.dumps({
            "flow_name": "new_to_family_ig_default",
            "flow_type": "ntf"
        }, separators=(',', ':')),
        "is_platform_login": 0,
        "INTERNAL__latency_qpl_marker_id": 36707139,
        "reg_info": json.dumps({
            "first_name": None,
            "last_name": None,
            "full_name": None,
            "contactpoint": None,
            "ar_contactpoint": None,
            "contactpoint_type": None,
            "is_using_unified_cp": None,
            "unified_cp_screen_variant": "control",
            "is_cp_auto_confirmed": False,
            "is_cp_auto_confirmable": False,
            "is_cp_claimed": False,
            "confirmation_code": None,
            "birthday": None,
            "birthday_derived_from_age": None,
            "age_range": None,
            "did_use_age": None,
            "os_shared_age_range": None,
            "gender": None,
            "use_custom_gender": False,
            "custom_gender": None,
            "encrypted_password": None,
            "username": None,
            "username_prefill": None,
            "fb_conf_source": None,
            "device_id": device_id_val,
            "ig4a_qe_device_id": qe_device_id,
            "family_device_id": family_device_id,
            "user_id": None,
            "safetynet_token": None,
            "skip_slow_rel_check": False,
            "safetynet_response": None,
            "machine_id": machine_id,
            "profile_photo": None,
            "profile_photo_id": None,
            "profile_photo_upload_id": None,
            "avatar": None,
            "email_oauth_token_no_contact_perm": None,
            "email_oauth_token": None,
            "email_oauth_tokens": None,
            "sign_in_with_google_email": None,
            "should_skip_two_step_conf": None,
            "openid_tokens_for_testing": None,
            "encrypted_msisdn": None,
            "encrypted_msisdn_for_safetynet": None,
            "cached_headers_safetynet_info": None,
            "should_skip_headers_safetynet": None,
            "headers_last_infra_flow_id": None,
            "headers_last_infra_flow_id_safetynet": None,
            "headers_flow_id": None,
            "was_headers_prefill_available": None,
            "sso_enabled": None,
            "existing_accounts": None,
            "used_ig_birthday": None,
            "create_new_to_app_account": None,
            "skip_session_info": None,
            "ck_error": None,
            "ck_id": None,
            "ck_nonce": None,
            "should_save_password": None,
            "fb_access_token": None,
            "is_msplit_reg": None,
            "is_spectra_reg": None,
            "dema_account_consent_given": None,
            "spectra_reg_token": None,
            "spectra_reg_guardian_id": None,
            "spectra_reg_guardian_logged_in_context": None,
            "user_id_of_msplit_creator": None,
            "msplit_creator_nonce": None,
            "dma_data_combination_consent_given": None,
            "xapp_accounts": None,
            "fb_device_id": None,
            "fb_machine_id": None,
            "ig_device_id": None,
            "ig_machine_id": None,
            "should_skip_nta_upsell": None,
            "big_blue_token": None,
            "caa_reg_flow_source": "login_home_native_integration_point",
            "ig_authorization_token": None,
            "full_sheet_flow": False,
            "crypted_user_id": None,
            "is_caa_perf_enabled": True,
            "is_preform": True,
            "should_show_rel_error": False,
            "ignore_suma_check": False,
            "dismissed_login_upsell_with_cna": False,
            "ignore_existing_login": False,
            "ignore_existing_login_from_suma": False,
            "ignore_existing_login_after_errors": False,
            "suggested_first_name": None,
            "suggested_last_name": None,
            "suggested_full_name": None,
            "frl_authorization_token": None,
            "post_form_errors": None,
            "skip_step_without_errors": False,
            "existing_account_exact_match_checked": False,
            "existing_account_fuzzy_match_checked": False,
            "email_oauth_exists": False,
            "confirmation_code_send_error": None,
            "is_too_young": False,
            "source_account_type": None,
            "whatsapp_installed_on_client": False,
            "confirmation_medium": None,
            "source_credentials_type": None,
            "source_cuid": None,
            "source_account_reg_info": None,
            "soap_creation_source": None,
            "source_account_type_to_reg_info": None,
            "registration_flow_id": registration_flow_id,
            "should_skip_youth_tos": False,
            "is_youth_regulation_flow_complete": False,
            "is_on_cold_start": False,
            "email_prefilled": False,
            "cp_confirmed_by_auto_conf": False,
            "in_sowa_experiment": False,
            "youth_regulation_config": None,
            "conf_allow_back_nav_after_change_cp": None,
            "conf_bouncing_cliff_screen_type": None,
            "conf_show_bouncing_cliff": None,
            "eligible_to_flash_call_in_ig4a": False,
            "eligible_to_mo_sms_in_ig4a": False,
            "mo_sms_ent_id": None,
            "flash_call_permissions_status": None,
            "gms_incoming_call_retriever_eligibility": None,
            "attestation_result": None,
            "request_data_and_challenge_nonce_string": None,
            "confirmed_cp_and_code": None,
            "notification_callback_id": None,
            "reg_suma_state": 0,
            "is_msplit_neutral_choice": False,
            "msg_previous_cp": None,
            "ntp_import_source_info": None,
            "youth_consent_decision_time": None,
            "sk_pipa_consent_given": None,
            "should_show_spi_before_conf": True,
            "google_oauth_account": None,
            "is_reg_request_from_ig_suma": False,
            "is_toa_reg": False,
            "is_threads_public": False,
            "spc_import_flow": False,
            "caa_play_integrity_attestation_result": None,
            "client_known_key_hash": None,
            "flash_call_provider": None,
            "is_in_gms_experience": None,
            "flash_call_nonce_prefix_details": None,
            "spc_birthday_input": False,
            "failed_birthday_year_count": None,
            "user_presented_medium_source": None,
            "user_opted_out_of_ntp": None,
            "is_from_registration_reminder": False,
            "show_youth_reg_in_ig_spc": False,
            "fb_suma_is_high_confidence": None,
            "screen_visited": ["CAA_REG_CONTACT_POINT_PHONE", "CAA_REG_CONTACT_POINT_EMAIL"],
            "fb_email_login_upsell_skip_suma_post_tos": False,
            "fb_suma_is_from_email_login_upsell": False,
            "fb_suma_is_from_phone_login_upsell": False,
            "should_prefill_cp_in_ar": None,
            "ig_partially_created_account_user_id": None,
            "ig_partially_created_account_nonce": None,
            "ig_partially_created_account_nonce_expiry": None,
            "force_sessionless_nux_experience": False,
            "has_seen_suma_landing_page_pre_conf": False,
            "has_seen_suma_candidate_page_pre_conf": False,
            "has_seen_confirmation_screen": False,
            "suma_on_conf_threshold": -1,
            "move_suma_to_cp_variant": "control",
            "pp_to_nux_eligible": False,
            "should_show_error_msg": True,
            "th_profile_photo_token": None,
            "attempted_silent_auth_in_fb": False,
            "attempted_silent_auth_in_ig": False,
            "cp_suma_results_map": None,
            "source_username": None,
            "next_uri": None,
            "should_use_next_uri": None,
            "linking_entry_point": None,
            "fb_encrypted_partial_new_account_properties": None,
            "starter_pack_name": None,
            "starter_pack_creator_user_ids": None,
            "wa_data_bundle": None,
            "bloks_controller_source": None,
            "airwave_registration_code": None,
            "is_sessionless_nux": None,
            "login_contactpoint": None,
            "login_contactpoint_type": None,
            "is_nta_shortened": False,
            "should_show_bday_after_name_suggestions": None,
            "should_override_back_nav": False,
            "ig_footer_variant": "control",
            "device_network_info": None,
            "is_from_web_lite_reg_controller": None,
            "login_form_siwg_email": None,
            "account_setup_waterfall_id": None,
            "is_wanted_suma_user": False,
            "device_zero_balance_state": None,
            "is_in_nta_single_form": False
        }, separators=(',', ':')),
        "family_device_id": family_device_id,
        "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
        "cp_funnel": 0,
        "cp_source": 0,
        "access_flow_version": "pre_mt_behavior",
        "is_from_logged_in_switcher": 0,
        "current_step": 0,
        "qe_device_id": qe_device_id
    }
    payload = {
        "params": json.dumps({
            "client_input_params": client_input_params,
            "server_params": server_params
        }, separators=(',', ':')),
        "bk_client_context": json.dumps({
            "bloks_version": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
            "styles_id": "instagram"
        }, separators=(',', ':')),
        "bloks_versioning_id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf"
    }
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.reg.async.contactpoint_email.async/"
    
    try:
        response = requests.post(url, headers=headers,data=payload,timeout=30)
        cleaned_response =  response.text.replace('//', '', 1) if response.text.startswith('//') else response.text
       
        if response.status_code == 200:
           
            pattern = r'\\"pre_mt_behavior\\",\s*\\"unknown\\",\s*\\"(.*?)\\"'
            reg_context_token = re.search(pattern, cleaned_response)
            
            if reg_context_token:
                reg_context_token = reg_context_token.group(1)
                code = input("Enter the code: ").strip()
                machine_id = generate_machine_id()
                time.sleep(2)
                send_confirmation_request(code,email,aaccs,aacjid,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context_token,text_input_id,aac_init_timestamp,user_agent,machine_id,registration_flow_id)
                
            else:
                print("don't found reg_context in the response")
       
        
    except Exception as e:
        print(f"â Error: {e}")
        return {"success": False, "error": str(e)}


def send_confirmation_request(code,email,aaccs,aacjid,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context,text_input_id,timestamp,user_agent,machine_id,registration_flow_id):
    current_time = datetime.now().timestamp()
    pigeon_session_id = f"UFS-{str(uuid.uuid4())}-0"
    event_request_id = str(uuid.uuid4())
    
    latency_instance_id = float(f"1.{random.randint(10000000000000, 99999999999999)}E14")
    headers = {
        "Host": "i.instagram.com",
        "X-Ig-App-Locale": "en_US",
        "X-Ig-Device-Locale": "en_US",
        "X-Ig-Mapped-Locale": "en_US",
        "X-Pigeon-Session-Id": pigeon_session_id,
        "X-Pigeon-Rawclienttime": str(current_time),
        "X-Ig-Bandwidth-Speed-Kbps": "-1.000",
        "X-Ig-Bandwidth-Totalbytes-B": "0",
        "X-Ig-Bandwidth-Totaltime-Ms": "0",
        "X-Bloks-Version-Id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
        "X-Ig-Www-Claim": "0",
        "X-Bloks-Prism-Button-Version": "CONTROL",
        "X-Bloks-Prism-Colors-Enabled": "false",
        "X-Bloks-Prism-Ax-Base-Colors-Enabled": "false",
        "X-Bloks-Prism-Font-Enabled": "false",
        "X-Bloks-Is-Layout-Rtl": "false",
        "X-Ig-Device-Id": qe_device_id,
        "X-Ig-Family-Device-Id": family_device_id,
        "X-Ig-Android-Id": device_id_val,
        "X-Ig-Timezone-Offset": "28800",
        "X-Ig-Nav-Chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1772845836.640::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_phone:2:button:1772845839.819::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_email:3:button:1772845841.684::",
        "X-Fb-Connection-Type": "WIFI",
        "X-Ig-Connection-Type": "WIFI",
        "X-Ig-Capabilities": "3brTv10=",
        "X-Ig-App-Id": "567067343352427",
        "Priority": "u=3",
        "User-Agent": user_agent,
        "Accept-Language": "en-US",
        "X-Mid": machine_id,
        "Ig-Intended-User-Id": "0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Fb-Http-Engine": "Liger",
        "X-Fb-Client-Ip": "True",
        "X-Fb-Server-Cluster": "True",
        "Connection": "keep-alive"
    }
    client_input_params = {
        "confirmed_cp_and_code": {},
        "aac": json.dumps({
            "aac_init_timestamp": timestamp,
            "aacjid": aacjid,
            "aaccs": aaccs
        }, separators=(',', ':')),
        "block_store_machine_id": "",
        "code": code,
        "fb_ig_device_id": [],
        "device_id": device_id_val,
        "lois_settings": {"lois_token": ""},
        "cloud_trust_token": None,
        "network_bssid": None
    }
    server_params = {
        "event_request_id": event_request_id,
        "is_from_logged_out": 0,
        "text_input_id": text_input_id,
        "layered_homepage_experiment_group": None,
        "device_id": device_id_val,
        "reg_context": reg_context, 
        "login_surface": "unknown",
        "waterfall_id": waterfall_id,
        "wa_timer_id": "wa_retriever",
        "INTERNAL__latency_qpl_instance_id": latency_instance_id,
        "flow_info": json.dumps({
            "flow_name": "new_to_family_ig_default",
            "flow_type": "ntf"
        }, separators=(',', ':')),
        "is_platform_login": 0,
        "sms_retriever_started_prior_step": 0,
        "INTERNAL__latency_qpl_marker_id": 36707139,
        "reg_info": json.dumps({
            "first_name": None,
            "last_name": None,
            "full_name": None,
            "contactpoint": email,
            "ar_contactpoint": None,
            "contactpoint_type": "email",
            "is_using_unified_cp": False,
            "unified_cp_screen_variant": "control",
            "is_cp_auto_confirmed": False,
            "is_cp_auto_confirmable": False,
            "is_cp_claimed": False,
            "confirmation_code": None,
            "birthday": None,
            "birthday_derived_from_age": None,
            "age_range": None,
            "did_use_age": None,
            "os_shared_age_range": None,
            "gender": None,
            "use_custom_gender": False,
            "custom_gender": None,
            "encrypted_password": None,
            "username": None,
            "username_prefill": None,
            "fb_conf_source": None,
            "device_id": device_id_val,
            "ig4a_qe_device_id": qe_device_id,
            "family_device_id": family_device_id,
            "user_id": None,
            "safetynet_token": None,
            "skip_slow_rel_check": True,
            "safetynet_response": None,
            "machine_id": machine_id,
            "profile_photo": None,
            "profile_photo_id": None,
            "profile_photo_upload_id": None,
            "avatar": None,
            "email_oauth_token_no_contact_perm": None,
            "email_oauth_token": None,
            "email_oauth_tokens": None,
            "sign_in_with_google_email": None,
            "should_skip_two_step_conf": None,
            "openid_tokens_for_testing": None,
            "encrypted_msisdn": None,
            "encrypted_msisdn_for_safetynet": None,
            "cached_headers_safetynet_info": None,
            "should_skip_headers_safetynet": None,
            "headers_last_infra_flow_id": None,
            "headers_last_infra_flow_id_safetynet": None,
            "headers_flow_id": None,
            "was_headers_prefill_available": None,
            "sso_enabled": None,
            "existing_accounts": None,
            "used_ig_birthday": None,
            "create_new_to_app_account": None,
            "skip_session_info": None,
            "ck_error": None,
            "ck_id": None,
            "ck_nonce": None,
            "should_save_password": None,
            "fb_access_token": None,
            "is_msplit_reg": None,
            "is_spectra_reg": None,
            "dema_account_consent_given": None,
            "spectra_reg_token": None,
            "spectra_reg_guardian_id": None,
            "spectra_reg_guardian_logged_in_context": None,
            "user_id_of_msplit_creator": None,
            "msplit_creator_nonce": None,
            "dma_data_combination_consent_given": None,
            "xapp_accounts": None,
            "fb_device_id": None,
            "fb_machine_id": None,
            "ig_device_id": None,
            "ig_machine_id": None,
            "should_skip_nta_upsell": None,
            "big_blue_token": None,
            "caa_reg_flow_source": "login_home_native_integration_point",
            "ig_authorization_token": None,
            "full_sheet_flow": False,
            "crypted_user_id": None,
            "is_caa_perf_enabled": True,
            "is_preform": True,
            "should_show_rel_error": False,
            "ignore_suma_check": False,
            "dismissed_login_upsell_with_cna": False,
            "ignore_existing_login": False,
            "ignore_existing_login_from_suma": False,
            "ignore_existing_login_after_errors": False,
            "suggested_first_name": None,
            "suggested_last_name": None,
            "suggested_full_name": None,
            "frl_authorization_token": None,
            "post_form_errors": None,
            "skip_step_without_errors": False,
            "existing_account_exact_match_checked": False,
            "existing_account_fuzzy_match_checked": False,
            "email_oauth_exists": False,
            "confirmation_code_send_error": None,
            "is_too_young": False,
            "source_account_type": None,
            "whatsapp_installed_on_client": False,
            "confirmation_medium": None,
            "source_credentials_type": None,
            "source_cuid": None,
            "source_account_reg_info": None,
            "soap_creation_source": None,
            "source_account_type_to_reg_info": None,
            "registration_flow_id": registration_flow_id,
            "should_skip_youth_tos": False,
            "is_youth_regulation_flow_complete": False,
            "is_on_cold_start": False,
            "email_prefilled": False,
            "cp_confirmed_by_auto_conf": False,
            "in_sowa_experiment": False,
            "youth_regulation_config": None,
            "conf_allow_back_nav_after_change_cp": None,
            "conf_bouncing_cliff_screen_type": None,
            "conf_show_bouncing_cliff": None,
            "eligible_to_flash_call_in_ig4a": False,
            "eligible_to_mo_sms_in_ig4a": False,
            "mo_sms_ent_id": None,
            "flash_call_permissions_status": None,
            "gms_incoming_call_retriever_eligibility": None,
            "attestation_result": None,
            "request_data_and_challenge_nonce_string": None,
            "confirmed_cp_and_code": None,
            "notification_callback_id": None,
            "reg_suma_state": 0,
            "is_msplit_neutral_choice": False,
            "msg_previous_cp": None,
            "ntp_import_source_info": None,
            "youth_consent_decision_time": None,
            "sk_pipa_consent_given": None,
            "should_show_spi_before_conf": True,
            "google_oauth_account": None,
            "is_reg_request_from_ig_suma": False,
            "is_toa_reg": False,
            "is_threads_public": False,
            "spc_import_flow": False,
            "caa_play_integrity_attestation_result": None,
            "client_known_key_hash": None,
            "flash_call_provider": None,
            "is_in_gms_experience": None,
            "flash_call_nonce_prefix_details": None,
            "spc_birthday_input": False,
            "failed_birthday_year_count": None,
            "user_presented_medium_source": None,
            "user_opted_out_of_ntp": None,
            "is_from_registration_reminder": False,
            "show_youth_reg_in_ig_spc": False,
            "fb_suma_is_high_confidence": None,
            "screen_visited": [
                "CAA_REG_CONTACT_POINT_PHONE",
                "CAA_REG_CONTACT_POINT_EMAIL",
                "CAA_REG_CONFIRMATION_SCREEN"
            ],
            "fb_email_login_upsell_skip_suma_post_tos": False,
            "fb_suma_is_from_email_login_upsell": False,
            "fb_suma_is_from_phone_login_upsell": False,
            "should_prefill_cp_in_ar": None,
            "ig_partially_created_account_user_id": None,
            "ig_partially_created_account_nonce": None,
            "ig_partially_created_account_nonce_expiry": None,
            "force_sessionless_nux_experience": False,
            "has_seen_suma_landing_page_pre_conf": False,
            "has_seen_suma_candidate_page_pre_conf": False,
            "has_seen_confirmation_screen": False,
            "suma_on_conf_threshold": -1,
            "move_suma_to_cp_variant": "control",
            "pp_to_nux_eligible": False,
            "should_show_error_msg": True,
            "th_profile_photo_token": None,
            "attempted_silent_auth_in_fb": False,
            "attempted_silent_auth_in_ig": False,
            "cp_suma_results_map": None,
            "source_username": None,
            "next_uri": None,
            "should_use_next_uri": None,
            "linking_entry_point": None,
            "fb_encrypted_partial_new_account_properties": None,
            "starter_pack_name": None,
            "starter_pack_creator_user_ids": None,
            "wa_data_bundle": None,
            "bloks_controller_source": None,
            "airwave_registration_code": None,
            "is_sessionless_nux": None,
            "login_contactpoint": None,
            "login_contactpoint_type": None,
            "is_nta_shortened": False,
            "should_show_bday_after_name_suggestions": None,
            "should_override_back_nav": False,
            "ig_footer_variant": "control",
            "device_network_info": None,
            "is_from_web_lite_reg_controller": None,
            "login_form_siwg_email": None,
            "account_setup_waterfall_id": None,
            "is_wanted_suma_user": False,
            "device_zero_balance_state": None,
            "is_in_nta_single_form": False
        }, separators=(',', ':')),
        "family_device_id": family_device_id,
        "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
        "access_flow_version": "pre_mt_behavior",
        "is_from_logged_in_switcher": 0,
        "current_step": 3,
        "qe_device_id": qe_device_id
    }
    payload = {
        "params": json.dumps({
            "client_input_params": client_input_params,
            "server_params": server_params
        }, separators=(',', ':')),
        "bk_client_context": json.dumps({
            "bloks_version": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
            "styles_id": "instagram"
        }, separators=(',', ':')),
        "bloks_versioning_id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf"
    }
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.reg.confirmation.async/"
    try:
        response = requests.post(url,headers=headers,data=payload,timeout=30)
        cleaned_response =  response.text.replace('//', '', 1) if response.text.startswith('//') else response.text
        
        if response.status_code == 200:
            pattern = r'\\"pre_mt_behavior\\",\s*\\"unknown\\",\s*\\"(.*?)\\"'
            reg_context_token = re.search(pattern, cleaned_response)
            
            if reg_context_token:
                reg_context_token = reg_context_token.group(1)
                
              
                
            else:
                print("â ï ̧ ØaÙØ¥Ø±Ø3Ø§Ù Ø§ÙØ·ÙØ ̈ ÙÙÙ ÙÙÙØaÙØ§ÙØ1Ø«ÙØ± Ø1ÙÙ Ø±ÙØ2 Ø§ÙØ3ÙØ§Ù ÙÙ Ø§ÙØ±Ø ̄.")
                
            pattern = r'confirmation_code\\+":\\+"([^\\"]+)'
            confirm_code= re.search(pattern, cleaned_response)
            if confirm_code:
                confirm_code = confirm_code.group(1)
       
                password =generate_strong_password(14)
                print(f"[+] Password : {password}")
                time.sleep(2)
                send_password_request(password,email,aaccs,aacjid,confirm_code,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context_token,user_agent,timestamp,machine_id,registration_flow_id)
            else:
                print("don't found confirmation code")
        else:
            print(f"confirmation request failed with status code: {response.status_code}")
        
        
        
    except Exception as e:
        print(f"â Error: {e}")
        


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

def generate_full_name():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}"
def generate_encrypted_password(password, timestamp,account_type="0"):
    return f"#PWD_INSTAGRAM:{account_type}:{timestamp}:{password}"

PREFIX = ["real","its","the","official","mr","king","im"]
SUFFIX = ["official","real","live","world","hub"]

SEPARATORS = ["", ".", "_"]

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
    return f"{first}{sep}{last}{number}"

    # return random.choice(patterns)

def send_password_request(password,email,aaccs,aacjid,confirmation_code,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context,user_agent,timestamp,machine_id,registration_flow_id):
    current_time = int(datetime.now().timestamp())
    current_time_float = datetime.now().timestamp()
    pigeon_session_id = f"UFS-{str(uuid.uuid4())}-0"
    event_request_id = str(uuid.uuid4())
    latency_instance_id = float(f"1.{random.randint(10000000000000, 99999999999999)}E14")
    encrypted_password = generate_encrypted_password(password, current_time)
    safetynet_token = base64.b64encode(f"{email}|{current_time}|safetynet".encode()).decode()
    headers = {
        "Host": "i.instagram.com",
        "X-Ig-App-Locale": "en_US",
        "X-Ig-Device-Locale": "en_US",
        "X-Ig-Mapped-Locale": "en_US",
        "X-Pigeon-Session-Id": pigeon_session_id,
        "X-Pigeon-Rawclienttime": str(current_time_float),
        "X-Ig-Bandwidth-Speed-Kbps": "-1.000",
        "X-Ig-Bandwidth-Totalbytes-B": "0",
        "X-Ig-Bandwidth-Totaltime-Ms": "0",
        "X-Bloks-Version-Id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
        "X-Ig-Www-Claim": "0",
        "X-Bloks-Prism-Button-Version": "CONTROL",
        "X-Bloks-Prism-Colors-Enabled": "false",
        "X-Bloks-Prism-Ax-Base-Colors-Enabled": "false",
        "X-Bloks-Prism-Font-Enabled": "false",
        "X-Bloks-Is-Layout-Rtl": "false",
        "X-Ig-Device-Id": qe_device_id,
        "X-Ig-Family-Device-Id": family_device_id,
        "X-Ig-Android-Id": device_id_val,
        "X-Ig-Timezone-Offset": "28800",
        "X-Ig-Nav-Chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1772845836.640::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_phone:2:button:1772845839.819::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_email:3:button:1772845841.684::",
        "X-Fb-Connection-Type": "WIFI",
        "X-Ig-Connection-Type": "WIFI",
        "X-Ig-Capabilities": "3brTv10=",
        "X-Ig-App-Id": "567067343352427",
        "Priority": "u=3",
        "User-Agent": user_agent,
        "Accept-Language": "en-US",
        "X-Mid": machine_id,
        "Ig-Intended-User-Id": "0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Fb-Http-Engine": "Liger",
        "X-Fb-Client-Ip": "True",
        "X-Fb-Server-Cluster": "True",
        "Connection": "keep-alive"
    }
    client_input_params = {
        "spi_action": 1,
        "safetynet_response": "API_ERROR: class com.google.android.gms.common.api.ApiException:7: ",
        "caa_play_integrity_attestation_result": "",
        "aac": json.dumps({
            "aac_init_timestamp": timestamp,
            "aacjid": aacjid,
            "aaccs": aaccs
        }, separators=(',', ':')),
        "safetynet_token": safetynet_token,
        "whatsapp_installed_on_client": 0,
        "zero_balance_state": "",
        "network_bssid": None,
        "machine_id": machine_id,
        "headers_last_infra_flow_id_safetynet": "",
        "system_permissions_status": {
            "READ_CONTACTS": "GRANTED",
            "GET_ACCOUNTS": "GRANTED",
            "READ_PHONE_STATE": "GRANTED",
            "READ_PHONE_NUMBERS": "GRANTED"
        },
        "email_oauth_token_map": {},
        "block_store_machine_id": "",
        "fb_ig_device_id": [],
        "encrypted_msisdn_for_safetynet": "",
        "lois_settings": {"lois_token": ""},
        "cloud_trust_token": None,
        "client_known_key_hash": "",
        "encrypted_password": encrypted_password
    }
    server_params = {
        "event_request_id": event_request_id,
        "flow_modifier": json.dumps({
            "flow_name": "new_to_family_ig_default",
            "flow_type": "ntf"
        }, separators=(',', ':')),
        "is_from_logged_out": 0,
        "layered_homepage_experiment_group": None,
        "device_id": device_id_val,
        "reg_context": reg_context,
        "login_surface": "unknown",
        "waterfall_id": waterfall_id,
        "INTERNAL__latency_qpl_instance_id": latency_instance_id,
        "flow_info": json.dumps({
            "flow_name": "new_to_family_ig_default",
            "flow_type": "ntf"
        }, separators=(',', ':')),
        "is_platform_login": 0,
        "INTERNAL__latency_qpl_marker_id": 36707139,
        "reg_info": json.dumps({
            "first_name": None,
            "last_name": None,
            "full_name": None,
            "contactpoint": email,
            "ar_contactpoint": None,
            "contactpoint_type": "email",
            "is_using_unified_cp": False,
            "unified_cp_screen_variant": "control",
            "is_cp_auto_confirmed": False,
            "is_cp_auto_confirmable": False,
            "is_cp_claimed": False,
            "confirmation_code": confirmation_code,
            "birthday": None,
            "birthday_derived_from_age": None,
            "age_range": None,
            "did_use_age": None,
            "os_shared_age_range": None,
            "gender": None,
            "use_custom_gender": False,
            "custom_gender": None,
            "encrypted_password": None,
            "username": None,
            "username_prefill": None,
            "fb_conf_source": None,
            "device_id": device_id_val,
            "ig4a_qe_device_id": qe_device_id,
            "family_device_id": family_device_id,
            "user_id": None,
            "safetynet_token": None,
            "skip_slow_rel_check": True,
            "safetynet_response": None,
            "machine_id": machine_id,
            "profile_photo": None,
            "profile_photo_id": None,
            "profile_photo_upload_id": None,
            "avatar": None,
            "email_oauth_token_no_contact_perm": None,
            "email_oauth_token": None,
            "email_oauth_tokens": [],
            "sign_in_with_google_email": None,
            "should_skip_two_step_conf": None,
            "openid_tokens_for_testing": None,
            "encrypted_msisdn": None,
            "encrypted_msisdn_for_safetynet": None,
            "cached_headers_safetynet_info": None,
            "should_skip_headers_safetynet": None,
            "headers_last_infra_flow_id": None,
            "headers_last_infra_flow_id_safetynet": None,
            "headers_flow_id": None,
            "was_headers_prefill_available": None,
            "sso_enabled": None,
            "existing_accounts": None,
            "used_ig_birthday": None,
            "create_new_to_app_account": None,
            "skip_session_info": None,
            "ck_error": None,
            "ck_id": None,
            "ck_nonce": None,
            "should_save_password": True,
            "fb_access_token": None,
            "is_msplit_reg": None,
            "is_spectra_reg": None,
            "dema_account_consent_given": None,
            "spectra_reg_token": None,
            "spectra_reg_guardian_id": None,
            "spectra_reg_guardian_logged_in_context": None,
            "user_id_of_msplit_creator": None,
            "msplit_creator_nonce": None,
            "dma_data_combination_consent_given": None,
            "xapp_accounts": None,
            "fb_device_id": None,
            "fb_machine_id": None,
            "ig_device_id": None,
            "ig_machine_id": None,
            "should_skip_nta_upsell": None,
            "big_blue_token": None,
            "caa_reg_flow_source": "login_home_native_integration_point",
            "ig_authorization_token": None,
            "full_sheet_flow": False,
            "crypted_user_id": None,
            "is_caa_perf_enabled": True,
            "is_preform": True,
            "should_show_rel_error": False,
            "ignore_suma_check": False,
            "dismissed_login_upsell_with_cna": False,
            "ignore_existing_login": False,
            "ignore_existing_login_from_suma": False,
            "ignore_existing_login_after_errors": False,
            "suggested_first_name": None,
            "suggested_last_name": None,
            "suggested_full_name": None,
            "frl_authorization_token": None,
            "post_form_errors": None,
            "skip_step_without_errors": False,
            "existing_account_exact_match_checked": False,
            "existing_account_fuzzy_match_checked": False,
            "email_oauth_exists": False,
            "confirmation_code_send_error": None,
            "is_too_young": False,
            "source_account_type": None,
            "whatsapp_installed_on_client": False,
            "confirmation_medium": None,
            "source_credentials_type": None,
            "source_cuid": None,
            "source_account_reg_info": None,
            "soap_creation_source": None,
            "source_account_type_to_reg_info": None,
            "registration_flow_id": registration_flow_id,
            "should_skip_youth_tos": False,
            "is_youth_regulation_flow_complete": False,
            "is_on_cold_start": False,
            "email_prefilled": False,
            "cp_confirmed_by_auto_conf": False,
            "in_sowa_experiment": False,
            "youth_regulation_config": None,
            "conf_allow_back_nav_after_change_cp": None,
            "conf_bouncing_cliff_screen_type": None,
            "conf_show_bouncing_cliff": None,
            "eligible_to_flash_call_in_ig4a": False,
            "eligible_to_mo_sms_in_ig4a": False,
            "mo_sms_ent_id": None,
            "flash_call_permissions_status": None,
            "gms_incoming_call_retriever_eligibility": None,
            "attestation_result": None,
            "request_data_and_challenge_nonce_string": None,
            "confirmed_cp_and_code": None,
            "notification_callback_id": None,
            "reg_suma_state": 0,
            "is_msplit_neutral_choice": False,
            "msg_previous_cp": None,
            "ntp_import_source_info": None,
            "youth_consent_decision_time": None,
            "sk_pipa_consent_given": None,
            "should_show_spi_before_conf": True,
            "google_oauth_account": None,
            "is_reg_request_from_ig_suma": False,
            "is_toa_reg": False,
            "is_threads_public": False,
            "spc_import_flow": False,
            "caa_play_integrity_attestation_result": None,
            "client_known_key_hash": None,
            "flash_call_provider": None,
            "is_in_gms_experience": None,
            "flash_call_nonce_prefix_details": None,
            "spc_birthday_input": False,
            "failed_birthday_year_count": None,
            "user_presented_medium_source": None,
            "user_opted_out_of_ntp": None,
            "is_from_registration_reminder": False,
            "show_youth_reg_in_ig_spc": False,
            "fb_suma_is_high_confidence": None,
            "screen_visited": [
                "CAA_REG_CONTACT_POINT_PHONE",
                "CAA_REG_CONTACT_POINT_EMAIL",
                "CAA_REG_CONFIRMATION_SCREEN",
                "CAA_REG_PASSWORD"
            ],
            "fb_email_login_upsell_skip_suma_post_tos": False,
            "fb_suma_is_from_email_login_upsell": False,
            "fb_suma_is_from_phone_login_upsell": False,
            "should_prefill_cp_in_ar": None,
            "ig_partially_created_account_user_id": None,
            "ig_partially_created_account_nonce": None,
            "ig_partially_created_account_nonce_expiry": None,
            "force_sessionless_nux_experience": False,
            "has_seen_suma_landing_page_pre_conf": False,
            "has_seen_suma_candidate_page_pre_conf": False,
            "has_seen_confirmation_screen": False,
            "suma_on_conf_threshold": -1,
            "move_suma_to_cp_variant": "control",
            "pp_to_nux_eligible": False,
            "should_show_error_msg": True,
            "th_profile_photo_token": None,
            "attempted_silent_auth_in_fb": False,
            "attempted_silent_auth_in_ig": False,
            "cp_suma_results_map": None,
            "source_username": None,
            "next_uri": None,
            "should_use_next_uri": None,
            "linking_entry_point": None,
            "fb_encrypted_partial_new_account_properties": None,
            "starter_pack_name": None,
            "starter_pack_creator_user_ids": None,
            "wa_data_bundle": None,
            "bloks_controller_source": None,
            "airwave_registration_code": None,
            "is_sessionless_nux": None,
            "login_contactpoint": None,
            "login_contactpoint_type": None,
            "is_nta_shortened": False,
            "should_show_bday_after_name_suggestions": None,
            "should_override_back_nav": False,
            "ig_footer_variant": "control",
            "device_network_info": None,
            "is_from_web_lite_reg_controller": None,
            "login_form_siwg_email": None,
            "account_setup_waterfall_id": None,
            "is_wanted_suma_user": False,
            "device_zero_balance_state": None,
            "is_in_nta_single_form": False
        }, separators=(',', ':')),
        "family_device_id": family_device_id,
        "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
        "access_flow_version": "pre_mt_behavior",
        "is_from_logged_in_switcher": 0,
        "current_step": 4,
        "qe_device_id": qe_device_id
    }
    payload = {
        "params": json.dumps({
            "client_input_params": client_input_params,
            "server_params": server_params
        }, separators=(',', ':')),
        "bk_client_context": json.dumps({
            "bloks_version": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
            "styles_id": "instagram"
        }, separators=(',', ':')),
        "bloks_versioning_id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf"
    }
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.reg.password.async/"
    try:
        response = requests.post(url,headers=headers,data=payload,timeout=30)
        cleaned_response =  response.text.replace('//', '', 1) if response.text.startswith('//') else response.text
  
        if response.status_code == 200:
            pattern = r'\\"pre_mt_behavior\\",\s*\\"unknown\\",\s*\\"(.*?)\\"'
            reg_context_token = re.search(pattern, cleaned_response)
            if reg_context_token:
                reg_context_token = reg_context_token.group(1)
          
                birthday_data = generate_birthday(18, 30)
                print(f"[+] birthday  : {birthday_data['date_string']} | age: {birthday_data['age']}")
                time.sleep(2)
                send_birthday_request(birthday_data['date_string'],birthday_data['timestamp'],password,birthday_data['age'],email,confirmation_code,password,timestamp,safetynet_token,aaccs,aacjid,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context_token,get_timezone_from_api(),user_agent,machine_id,os_age_range=f"{birthday_data['age']}",should_skip_youth_tos=1,is_youth_regulation_flow_complete=1)
            else:
                print("done but reg context token not found")  
    
            
        else:
            print(f"â Failed to create password")
            print(f"ð Response text: {response.text[:500]}")
        
        
        
    except Exception as e:
        print(f"â Error: {e}")
        return {"success": False, "error": str(e)}

def get_local_timezone():
    try:
        local_tz = tzlocal.get_localzone()
        return str(local_tz)
    except:
        offset = datetime.datetime.now().astimezone().utcoffset()
        if offset:
            hours = offset.total_seconds() / 3600
            if hours > 0:
                return f"Etc/GMT-{int(hours)}"
            else:
                return f"Etc/GMT+{int(abs(hours))}"
            
    return "America/New_York"

def get_timezone_from_api():
    try:
        response = requests.get('https://ipapi.co/timezone/', timeout=5)
        if response.status_code == 200:
            timezone = response.text.strip()
  
            return timezone
    except:
        pass
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('timezone'):
  
                return data['timezone']
    except:
        pass
    return get_local_timezone()

def generate_birthday(min_age=18, max_age=30):
    age = random.randint(min_age, max_age)
    today = date.today()
    birth_year = today.year - age
    birth_month = random.randint(1, 12)
    last_day = calendar.monthrange(birth_year, birth_month)[1]
    birth_day = random.randint(1, last_day)
    birth_date = date(birth_year, birth_month, birth_day)
    birthday_data = {
        "date_string": birth_date.strftime("%d-%m-%Y"),  
        "timestamp": int(time.mktime(birth_date.timetuple())),  
        "year": birth_year,
        "month": birth_month,
        "day": birth_day,
        "age": age
    }
    
    return birthday_data

def send_birthday_request(birthday_date_string,birthday_timestamp,password,age,email,confirm_code,enquired_password,timestamp,safetynet_token,aaccs,aacjid,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context,client_timezone,user_agent,machine_id,os_age_range="",should_skip_youth_tos=0,is_youth_regulation_flow_complete=0,registration_flow_id=None):

    current_time = datetime.now().timestamp()
    pigeon_session_id = f"UFS-{str(uuid.uuid4())}-0"
    latency_instance_id = float(f"1.{random.randint(10000000000000, 99999999999999)}E14")
    headers = {
        "Host": "i.instagram.com",
        "X-Ig-App-Locale": "en_US",
        "X-Ig-Device-Locale": "en_US",
        "X-Ig-Mapped-Locale": "en_US",
        "X-Pigeon-Session-Id": pigeon_session_id,
        "X-Pigeon-Rawclienttime": str(current_time),
        "X-Ig-Bandwidth-Speed-Kbps": "-1.000",
        "X-Ig-Bandwidth-Totalbytes-B": "0",
        "X-Ig-Bandwidth-Totaltime-Ms": "0",
        "X-Bloks-Version-Id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
        "X-Ig-Www-Claim": "0",
        "X-Bloks-Prism-Button-Version": "CONTROL",
        "X-Bloks-Prism-Colors-Enabled": "false",
        "X-Bloks-Prism-Ax-Base-Colors-Enabled": "false",
        "X-Bloks-Prism-Font-Enabled": "false",
        "X-Bloks-Is-Layout-Rtl": "false",
        "X-Ig-Device-Id": qe_device_id,
        "X-Ig-Family-Device-Id": family_device_id,
        "X-Ig-Android-Id": device_id_val,
        "X-Ig-Timezone-Offset": "28800",
        "X-Ig-Nav-Chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1772845836.640::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_phone:2:button:1772845839.819::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_email:3:button:1772845841.684::",
        "X-Fb-Connection-Type": "WIFI",
        "X-Ig-Connection-Type": "WIFI",
        "X-Ig-Capabilities": "3brTv10=",
        "X-Ig-App-Id": "567067343352427",
        "Priority": "u=3",
        "User-Agent": user_agent,
        "Accept-Language": "en-US",
        "X-Mid": machine_id,
        "Ig-Intended-User-Id": "0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Fb-Http-Engine": "Liger",
        "X-Fb-Client-Ip": "True",
        "X-Fb-Server-Cluster": "True",
        "Connection": "keep-alive"
    }
    client_input_params = {
        "client_timezone": client_timezone,
        "aac": json.dumps({
            "aac_init_timestamp": timestamp,
            "aacjid": aacjid,
            "aaccs": aaccs
        }, separators=(',', ':')),
        "birthday_or_current_date_string": birthday_date_string,
        "os_age_range": os_age_range,
        "birthday_timestamp": birthday_timestamp,
        "lois_settings": {"lois_token": ""},
        "cloud_trust_token": None,
        "zero_balance_state": "",
        "network_bssid": None,
        "should_skip_youth_tos": should_skip_youth_tos,
        "is_youth_regulation_flow_complete": is_youth_regulation_flow_complete
    }
    server_params = {
        "is_from_logged_out": 0,
        "layered_homepage_experiment_group": None,
        "device_id": device_id_val,
        "reg_context": reg_context,
        "login_surface": "unknown",
        "waterfall_id": waterfall_id,
        "INTERNAL__latency_qpl_instance_id": latency_instance_id,
        "flow_info": json.dumps({
            "flow_name": "new_to_family_ig_default",
            "flow_type": "ntf"
        }, separators=(',', ':')),
        "is_platform_login": 0,
        "INTERNAL__latency_qpl_marker_id": 36707139,
        "reg_info": json.dumps({
            "first_name": None,
            "last_name": None,
            "full_name": None,
            "contactpoint": email,  
            "ar_contactpoint": None,
            "contactpoint_type": "email",
            "is_using_unified_cp": False,
            "unified_cp_screen_variant": "control",
            "is_cp_auto_confirmed": False,
            "is_cp_auto_confirmable": False,
            "is_cp_claimed": False,
            "confirmation_code": confirm_code , 
            "birthday": birthday_date_string,
            "birthday_derived_from_age": None,
            "age_range": None,
            "did_use_age": False,
            "os_shared_age_range": None,
            "gender": None,
            "use_custom_gender": False,
            "custom_gender": None,
            "encrypted_password": enquired_password,
            "username": None,
            "username_prefill": None,
            "fb_conf_source": None,
            "device_id": device_id_val,
            "ig4a_qe_device_id": qe_device_id,
            "family_device_id": family_device_id,
            "user_id": None,
            "safetynet_token": safetynet_token,
            "skip_slow_rel_check": True,
            "safetynet_response": "API_ERROR: class com.google.android.gms.common.api.ApiException:7: ",
            "machine_id": machine_id,
            "profile_photo": None,
            "profile_photo_id": None,
            "profile_photo_upload_id": None,
            "avatar": None,
            "email_oauth_token_no_contact_perm": None,
            "email_oauth_token": None,
            "email_oauth_tokens": [],
            "sign_in_with_google_email": None,
            "should_skip_two_step_conf": None,
            "openid_tokens_for_testing": None,
            "encrypted_msisdn": None,
            "encrypted_msisdn_for_safetynet": None,
            "cached_headers_safetynet_info": None,
            "should_skip_headers_safetynet": None,
            "headers_last_infra_flow_id": None,
            "headers_last_infra_flow_id_safetynet": None,
            "headers_flow_id": None,
            "was_headers_prefill_available": None,
            "sso_enabled": None,
            "existing_accounts": None,
            "used_ig_birthday": None,
            "create_new_to_app_account": None,
            "skip_session_info": None,
            "ck_error": None,
            "ck_id": None,
            "ck_nonce": None,
            "should_save_password": True,
            "fb_access_token": None,
            "is_msplit_reg": None,
            "is_spectra_reg": None,
            "dema_account_consent_given": None,
            "spectra_reg_token": None,
            "spectra_reg_guardian_id": None,
            "spectra_reg_guardian_logged_in_context": None,
            "user_id_of_msplit_creator": None,
            "msplit_creator_nonce": None,
            "dma_data_combination_consent_given": None,
            "xapp_accounts": None,
            "fb_device_id": None,
            "fb_machine_id": None,
            "ig_device_id": None,
            "ig_machine_id": None,
            "should_skip_nta_upsell": None,
            "big_blue_token": None,
            "caa_reg_flow_source": "login_home_native_integration_point",
            "ig_authorization_token": None,
            "full_sheet_flow": False,
            "crypted_user_id": None,
            "is_caa_perf_enabled": True,
            "is_preform": True,
            "should_show_rel_error": False,
            "ignore_suma_check": False,
            "dismissed_login_upsell_with_cna": False,
            "ignore_existing_login": False,
            "ignore_existing_login_from_suma": False,
            "ignore_existing_login_after_errors": False,
            "suggested_first_name": None,
            "suggested_last_name": None,
            "suggested_full_name": None,
            "frl_authorization_token": None,
            "post_form_errors": None,
            "skip_step_without_errors": False,
            "existing_account_exact_match_checked": False,
            "existing_account_fuzzy_match_checked": False,
            "email_oauth_exists": False,
            "confirmation_code_send_error": None,
            "is_too_young": False,
            "source_account_type": None,
            "whatsapp_installed_on_client": False,
            "confirmation_medium": None,
            "source_credentials_type": None,
            "source_cuid": None,
            "source_account_reg_info": None,
            "soap_creation_source": None,
            "source_account_type_to_reg_info": None,
            "registration_flow_id": registration_flow_id,
            "should_skip_youth_tos": False,
            "is_youth_regulation_flow_complete": False,
            "is_on_cold_start": False,
            "email_prefilled": False,
            "cp_confirmed_by_auto_conf": False,
            "in_sowa_experiment": False,
            "youth_regulation_config": None,
            "conf_allow_back_nav_after_change_cp": None,
            "conf_bouncing_cliff_screen_type": None,
            "conf_show_bouncing_cliff": None,
            "eligible_to_flash_call_in_ig4a": False,
            "eligible_to_mo_sms_in_ig4a": False,
            "mo_sms_ent_id": None,
            "flash_call_permissions_status": None,
            "gms_incoming_call_retriever_eligibility": None,
            "attestation_result": None,
            "request_data_and_challenge_nonce_string": None,
            "confirmed_cp_and_code": None,
            "notification_callback_id": None,
            "reg_suma_state": 0,
            "is_msplit_neutral_choice": False,
            "msg_previous_cp": None,
            "ntp_import_source_info": None,
            "youth_consent_decision_time": None,
            "sk_pipa_consent_given": None,
            "should_show_spi_before_conf": True,
            "google_oauth_account": None,
            "is_reg_request_from_ig_suma": False,
            "is_toa_reg": False,
            "is_threads_public": False,
            "spc_import_flow": False,
            "caa_play_integrity_attestation_result": None,
            "client_known_key_hash": None,
            "flash_call_provider": None,
            "is_in_gms_experience": None,
            "flash_call_nonce_prefix_details": None,
            "spc_birthday_input": False,
            "failed_birthday_year_count": None,
            "user_presented_medium_source": None,
            "user_opted_out_of_ntp": None,
            "is_from_registration_reminder": False,
            "show_youth_reg_in_ig_spc": False,
            "fb_suma_is_high_confidence": None,
            "screen_visited": [
                "CAA_REG_CONTACT_POINT_PHONE",
                "CAA_REG_CONTACT_POINT_EMAIL",
                "CAA_REG_CONFIRMATION_SCREEN",
                "CAA_REG_PASSWORD",
                "bloks.caa.reg.birthday"
            ],
            "fb_email_login_upsell_skip_suma_post_tos": False,
            "fb_suma_is_from_email_login_upsell": False,
            "fb_suma_is_from_phone_login_upsell": False,
            "should_prefill_cp_in_ar": None,
            "ig_partially_created_account_user_id": None,
            "ig_partially_created_account_nonce": None,
            "ig_partially_created_account_nonce_expiry": None,
            "force_sessionless_nux_experience": False,
            "has_seen_suma_landing_page_pre_conf": False,
            "has_seen_suma_candidate_page_pre_conf": False,
            "has_seen_confirmation_screen": False,
            "suma_on_conf_threshold": -1,
            "move_suma_to_cp_variant": "control",
            "pp_to_nux_eligible": False,
            "should_show_error_msg": True,
            "th_profile_photo_token": None,
            "attempted_silent_auth_in_fb": False,
            "attempted_silent_auth_in_ig": False,
            "cp_suma_results_map": None,
            "source_username": None,
            "next_uri": None,
            "should_use_next_uri": None,
            "linking_entry_point": None,
            "fb_encrypted_partial_new_account_properties": None,
            "starter_pack_name": None,
            "starter_pack_creator_user_ids": None,
            "wa_data_bundle": None,
            "bloks_controller_source": None,
            "airwave_registration_code": None,
            "is_sessionless_nux": None,
            "login_contactpoint": None,
            "login_contactpoint_type": None,
            "is_nta_shortened": False,
            "should_show_bday_after_name_suggestions": None,
            "should_override_back_nav": False,
            "ig_footer_variant": "control",
            "device_network_info": None,
            "is_from_web_lite_reg_controller": None,
            "login_form_siwg_email": None,
            "account_setup_waterfall_id": None,
            "is_wanted_suma_user": False,
            "device_zero_balance_state": None,
            "is_in_nta_single_form": False
        }, separators=(',', ':')),
        "family_device_id": family_device_id,
        "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
        "access_flow_version": "pre_mt_behavior",
        "is_from_logged_in_switcher": 0,
        "current_step": 6,
        "qe_device_id": qe_device_id
    }
    payload = {
        "params": json.dumps({
            "client_input_params": client_input_params,
            "server_params": server_params
        }, separators=(',', ':')),
        "bk_client_context": json.dumps({
            "bloks_version": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
            "styles_id": "instagram"
        }, separators=(',', ':')),
        "bloks_versioning_id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf"
    }
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.reg.birthday.async/"
    
    try:        
        response = requests.post(url,headers=headers,data=payload,timeout=30)
        cleaned_response =  response.text.replace('//', '', 1) if response.text.startswith('//') else response.text

        if response.status_code == 200:
            pattern = r'\\"pre_mt_behavior\\",\s*\\"unknown\\",\s*\\"(.*?)\\"'
            reg_context_token = re.search(pattern, cleaned_response)
            if reg_context_token:
                reg_context_token = reg_context_token.group(1)
                full_name = generate_full_name()
                print(f"[+] Full name  : {full_name}")
                time.sleep(2)
                send_name_request(full_name,email,aaccs,aacjid,password,enquired_password,safetynet_token,timestamp,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context_token,user_agent,machine_id,registration_flow_id,confirm_code,birthday_date_string)
               
            else:
                print("Done Step 2 but couldn't find reg_context_token in the response.") 
        
      
        
    except Exception as e:
        print(f"â Error: {e}")
        return {"success": False, "error": str(e)}

def send_name_request(full_name,email,aaccs,aacjid,password,enquired_password,safetynet_token,timestamp,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context,user_agent,machine_id,registration_flow_id,confirmation_code,birthday,age_range="o18"):
    current_time = datetime.now().timestamp()
    pigeon_session_id = f"UFS-{str(uuid.uuid4())}-0"
    latency_instance_id = float(f"1.{random.randint(10000000000000, 99999999999999)}E14")
    headers = {
        "Host": "i.instagram.com",
        "X-Ig-App-Locale": "en_US",
        "X-Ig-Device-Locale": "en_US",
        "X-Ig-Mapped-Locale": "en_US",
        "X-Pigeon-Session-Id": pigeon_session_id,
        "X-Pigeon-Rawclienttime": str(current_time),
        "X-Ig-Bandwidth-Speed-Kbps": "-1.000",
        "X-Ig-Bandwidth-Totalbytes-B": "0",
        "X-Ig-Bandwidth-Totaltime-Ms": "0",
        "X-Bloks-Version-Id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
        "X-Ig-Www-Claim": "0",
        "X-Bloks-Prism-Button-Version": "CONTROL",
        "X-Bloks-Prism-Colors-Enabled": "false",
        "X-Bloks-Prism-Ax-Base-Colors-Enabled": "false",
        "X-Bloks-Prism-Font-Enabled": "false",
        "X-Bloks-Is-Layout-Rtl": "false",
        "X-Ig-Device-Id": qe_device_id,
        "X-Ig-Family-Device-Id": family_device_id,
        "X-Ig-Android-Id": device_id_val,
        "X-Ig-Timezone-Offset": "28800",
        "X-Ig-Nav-Chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1772845836.640::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_phone:2:button:1772845839.819::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_email:3:button:1772845841.684::",
        "X-Fb-Connection-Type": "WIFI",
        "X-Ig-Connection-Type": "WIFI",
        "X-Ig-Capabilities": "3brTv10=",
        "X-Ig-App-Id": "567067343352427",
        "Priority": "u=3",
        "User-Agent": user_agent,
        "Accept-Language": "en-US",
        "X-Mid": machine_id,
        "Ig-Intended-User-Id": "0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Fb-Http-Engine": "Liger",
        "X-Fb-Client-Ip": "True",
        "X-Fb-Server-Cluster": "True",
        "Connection": "keep-alive"
    }
    client_input_params = {
        "accounts_list": [],
        "aac": json.dumps({
            "aac_init_timestamp": timestamp,
            "aacjid": aacjid,
            "aaccs": aaccs
        }, separators=(',', ':')),
        "lois_settings": {"lois_token": ""},
        "cloud_trust_token": None,
        "zero_balance_state": "",
        "network_bssid": None,
        "name": full_name
    }
    server_params = {
        "is_from_logged_out": 0,
        "layered_homepage_experiment_group": None,
        "device_id": device_id_val,
        "reg_context": reg_context,
        "login_surface": "unknown",
        "waterfall_id": waterfall_id,
        "INTERNAL__latency_qpl_instance_id": latency_instance_id,
        "flow_info": json.dumps({
            "flow_name": "new_to_family_ig_default",
            "flow_type": "ntf"
        }, separators=(',', ':')),
        "is_platform_login": 0,
        "INTERNAL__latency_qpl_marker_id": 36707139,
        "reg_info": json.dumps({
            "first_name": None,
            "last_name": None,
            "full_name": full_name,
            "contactpoint": email,
            "ar_contactpoint": None,
            "contactpoint_type": "email",
            "is_using_unified_cp": False,
            "unified_cp_screen_variant": "control",
            "is_cp_auto_confirmed": False,
            "is_cp_auto_confirmable": False,
            "is_cp_claimed": False,
            "confirmation_code": confirmation_code,
            "birthday": birthday,
            "birthday_derived_from_age": None,
            "age_range": age_range,
            "did_use_age": False,
            "os_shared_age_range": None,
            "gender": None,
            "use_custom_gender": False,
            "custom_gender": None,
            "encrypted_password": enquired_password,
            "username": None,
            "username_prefill": None,
            "fb_conf_source": None,
            "device_id": device_id_val,
            "ig4a_qe_device_id": qe_device_id,
            "family_device_id": family_device_id,
            "user_id": None,
            "safetynet_token": safetynet_token,
            "skip_slow_rel_check": True,
            "safetynet_response": "API_ERROR: class com.google.android.gms.common.api.ApiException:7: ",
            "machine_id": machine_id,
            "profile_photo": None,
            "profile_photo_id": None,
            "profile_photo_upload_id": None,
            "avatar": None,
            "email_oauth_token_no_contact_perm": None,
            "email_oauth_token": None,
            "email_oauth_tokens": [],
            "sign_in_with_google_email": None,
            "should_skip_two_step_conf": None,
            "openid_tokens_for_testing": None,
            "encrypted_msisdn": None,
            "encrypted_msisdn_for_safetynet": None,
            "cached_headers_safetynet_info": None,
            "should_skip_headers_safetynet": None,
            "headers_last_infra_flow_id": None,
            "headers_last_infra_flow_id_safetynet": None,
            "headers_flow_id": None,
            "was_headers_prefill_available": None,
            "sso_enabled": None,
            "existing_accounts": None,
            "used_ig_birthday": None,
            "create_new_to_app_account": None,
            "skip_session_info": None,
            "ck_error": None,
            "ck_id": None,
            "ck_nonce": None,
            "should_save_password": True,
            "fb_access_token": None,
            "is_msplit_reg": None,
            "is_spectra_reg": None,
            "dema_account_consent_given": None,
            "spectra_reg_token": None,
            "spectra_reg_guardian_id": None,
            "spectra_reg_guardian_logged_in_context": None,
            "user_id_of_msplit_creator": None,
            "msplit_creator_nonce": None,
            "dma_data_combination_consent_given": None,
            "xapp_accounts": None,
            "fb_device_id": None,
            "fb_machine_id": None,
            "ig_device_id": None,
            "ig_machine_id": None,
            "should_skip_nta_upsell": None,
            "big_blue_token": None,
            "caa_reg_flow_source": "login_home_native_integration_point",
            "ig_authorization_token": None,
            "full_sheet_flow": False,
            "crypted_user_id": None,
            "is_caa_perf_enabled": True,
            "is_preform": True,
            "should_show_rel_error": False,
            "ignore_suma_check": False,
            "dismissed_login_upsell_with_cna": False,
            "ignore_existing_login": False,
            "ignore_existing_login_from_suma": False,
            "ignore_existing_login_after_errors": False,
            "suggested_first_name": None,
            "suggested_last_name": None,
            "suggested_full_name": full_name,
            "frl_authorization_token": None,
            "post_form_errors": None,
            "skip_step_without_errors": False,
            "existing_account_exact_match_checked": False,
            "existing_account_fuzzy_match_checked": False,
            "email_oauth_exists": False,
            "confirmation_code_send_error": None,
            "is_too_young": False,
            "source_account_type": None,
            "whatsapp_installed_on_client": False,
            "confirmation_medium": None,
            "source_credentials_type": None,
            "source_cuid": None,
            "source_account_reg_info": None,
            "soap_creation_source": None,
            "source_account_type_to_reg_info": None,
            "registration_flow_id": registration_flow_id,
            "should_skip_youth_tos": False,
            "is_youth_regulation_flow_complete": False,
            "is_on_cold_start": False,
            "email_prefilled": False,
            "cp_confirmed_by_auto_conf": False,
            "in_sowa_experiment": False,
            "youth_regulation_config": None,
            "conf_allow_back_nav_after_change_cp": None,
            "conf_bouncing_cliff_screen_type": None,
            "conf_show_bouncing_cliff": None,
            "eligible_to_flash_call_in_ig4a": False,
            "eligible_to_mo_sms_in_ig4a": False,
            "mo_sms_ent_id": None,
            "flash_call_permissions_status": None,
            "gms_incoming_call_retriever_eligibility": None,
            "attestation_result": None,
            "request_data_and_challenge_nonce_string": None,
            "confirmed_cp_and_code": None,
            "notification_callback_id": None,
            "reg_suma_state": 0,
            "is_msplit_neutral_choice": False,
            "msg_previous_cp": None,
            "ntp_import_source_info": None,
            "youth_consent_decision_time": None,
            "sk_pipa_consent_given": None,
            "should_show_spi_before_conf": True,
            "google_oauth_account": None,
            "is_reg_request_from_ig_suma": False,
            "is_toa_reg": False,
            "is_threads_public": False,
            "spc_import_flow": False,
            "caa_play_integrity_attestation_result": None,
            "client_known_key_hash": None,
            "flash_call_provider": None,
            "is_in_gms_experience": None,
            "flash_call_nonce_prefix_details": None,
            "spc_birthday_input": False,
            "failed_birthday_year_count": None,
            "user_presented_medium_source": None,
            "user_opted_out_of_ntp": None,
            "is_from_registration_reminder": False,
            "show_youth_reg_in_ig_spc": False,
            "fb_suma_is_high_confidence": None,
            "screen_visited": [
                "CAA_REG_CONTACT_POINT_PHONE",
                "CAA_REG_CONTACT_POINT_EMAIL",
                "CAA_REG_CONFIRMATION_SCREEN",
                "CAA_REG_PASSWORD",
                "bloks.caa.reg.birthday",
                "CAA_REG_IG_NAME_SCREEN"
            ],
            "fb_email_login_upsell_skip_suma_post_tos": False,
            "fb_suma_is_from_email_login_upsell": False,
            "fb_suma_is_from_phone_login_upsell": False,
            "should_prefill_cp_in_ar": None,
            "ig_partially_created_account_user_id": None,
            "ig_partially_created_account_nonce": None,
            "ig_partially_created_account_nonce_expiry": None,
            "force_sessionless_nux_experience": False,
            "has_seen_suma_landing_page_pre_conf": False,
            "has_seen_suma_candidate_page_pre_conf": False,
            "has_seen_confirmation_screen": False,
            "suma_on_conf_threshold": -1,
            "move_suma_to_cp_variant": "control",
            "pp_to_nux_eligible": False,
            "should_show_error_msg": True,
            "th_profile_photo_token": None,
            "attempted_silent_auth_in_fb": False,
            "attempted_silent_auth_in_ig": False,
            "cp_suma_results_map": None,
            "source_username": None,
            "next_uri": None,
            "should_use_next_uri": None,
            "linking_entry_point": None,
            "fb_encrypted_partial_new_account_properties": None,
            "starter_pack_name": None,
            "starter_pack_creator_user_ids": None,
            "wa_data_bundle": None,
            "bloks_controller_source": None,
            "airwave_registration_code": None,
            "is_sessionless_nux": None,
            "login_contactpoint": None,
            "login_contactpoint_type": None,
            "is_nta_shortened": False,
            "should_show_bday_after_name_suggestions": None,
            "should_override_back_nav": False,
            "ig_footer_variant": "control",
            "device_network_info": None,
            "is_from_web_lite_reg_controller": None,
            "login_form_siwg_email": None,
            "account_setup_waterfall_id": None,
            "is_wanted_suma_user": False,
            "device_zero_balance_state": None,
            "is_in_nta_single_form": False
        }, separators=(',', ':')),
        "family_device_id": family_device_id,
        "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
        "access_flow_version": "pre_mt_behavior",
        "is_from_logged_in_switcher": 0,
        "current_step": 7,
        "qe_device_id": qe_device_id
    }
    payload = {
        "params": json.dumps({
            "client_input_params": client_input_params,
            "server_params": server_params
        }, separators=(',', ':')),
        "bk_client_context": json.dumps({
            "bloks_version": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
            "styles_id": "instagram"
        }, separators=(',', ':')),
        "bloks_versioning_id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf"
    }

    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.reg.name_vtwo.async/"
    
    try:
      
        
        response = requests.post(url,headers=headers,data=payload,timeout=30)
        cleaned_response =  response.text.replace('//', '', 1) if response.text.startswith('//') else response.text
        
        if response.status_code == 200:
            pattern = r'\\"pre_mt_behavior\\",\s*\\"unknown\\",\s*\\"(.*?)\\"'
            reg_context_token = re.search(pattern, cleaned_response)
            if reg_context_token:
                reg_context_token = reg_context_token.group(1)
                username_prefill = email.split('@')[0]
                username = generate_username()
                time.sleep(2)
                send_username_request(username,full_name,email,password,aacjid,aaccs,user_agent,username_prefill,enquired_password,safetynet_token,timestamp,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context_token,machine_id,registration_flow_id,confirmation_code,birthday)
                
            else:
                print("Done Step 2 but couldn't find reg_context_token in the response.") 
                  
           
        
        
        
    except Exception as e:
        print(f"â Error: {e}")
        return {"success": False, "error": str(e)}
    
    
def send_username_request(username,full_name,email,password,aacjid,aaccs,user_agent,username_prefill,enquired_password,safetynet_token,timestamp,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context,machine_id,registration_flow_id,confirmation_code,birthday,age_range="o18"):
    current_time = datetime.now().timestamp()
    pigeon_session_id = f"UFS-{str(uuid.uuid4())}-0"
    event_request_id = str(uuid.uuid4())
    text_input_id = random.randint(135000000000000, 135999999999999)
    latency_instance_id = float(f"1.{random.randint(10000000000000, 99999999999999)}E14")
    suggestions_container_id = random.randint(135000000000000, 135999999999999)
    screen_id = random.randint(135000000000000, 135999999999999)
    input_id = random.randint(135000000000000, 135999999999999)
    headers = {
        "Host": "i.instagram.com",
        "X-Ig-App-Locale": "en_US",
        "X-Ig-Device-Locale": "en_US",
        "X-Ig-Mapped-Locale": "en_US",
        "X-Pigeon-Session-Id": pigeon_session_id,
        "X-Pigeon-Rawclienttime": str(current_time),
        "X-Ig-Bandwidth-Speed-Kbps": "-1.000",
        "X-Ig-Bandwidth-Totalbytes-B": "0",
        "X-Ig-Bandwidth-Totaltime-Ms": "0",
        "X-Bloks-Version-Id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
        "X-Ig-Www-Claim": "0",
        "X-Bloks-Prism-Button-Version": "CONTROL",
        "X-Bloks-Prism-Colors-Enabled": "false",
        "X-Bloks-Prism-Ax-Base-Colors-Enabled": "false",
        "X-Bloks-Prism-Font-Enabled": "false",
        "X-Bloks-Is-Layout-Rtl": "false",
        "X-Ig-Device-Id": qe_device_id,
        "X-Ig-Family-Device-Id": family_device_id,
        "X-Ig-Android-Id": device_id_val,
        "X-Ig-Timezone-Offset": "28800",
        "X-Ig-Nav-Chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1772845836.640::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_phone:2:button:1772845839.819::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_email:3:button:1772845841.684::",
        "X-Fb-Connection-Type": "WIFI",
        "X-Ig-Connection-Type": "WIFI",
        "X-Ig-Capabilities": "3brTv10=",
        "X-Ig-App-Id": "567067343352427",
        "Priority": "u=3",
        "User-Agent": user_agent,
        "Accept-Language": "en-US",
        "X-Mid": machine_id,
        "Ig-Intended-User-Id": "0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Fb-Http-Engine": "Liger",
        "X-Fb-Client-Ip": "True",
        "X-Fb-Server-Cluster": "True",
        "Connection": "keep-alive"
    }
    client_input_params = {
        "validation_text": username,
        "aac": json.dumps({
            "aac_init_timestamp": timestamp,
            "aacjid": aacjid,
            "aaccs": aaccs
        }, separators=(',', ':')),
        "family_device_id": family_device_id,
        "device_id": device_id_val,
        "lois_settings": {"lois_token": ""},
        "cloud_trust_token": None,
        "zero_balance_state": "",
        "network_bssid": None,
        "qe_device_id": qe_device_id
    }
    server_params = {
        "event_request_id": event_request_id,
        "is_from_logged_out": 0,
        "text_input_id": text_input_id,
        "layered_homepage_experiment_group": None,
        "device_id": device_id_val,
        "reg_context": reg_context,
        "login_surface": "unknown",
        "waterfall_id": waterfall_id,
        "INTERNAL__latency_qpl_instance_id": latency_instance_id,
        "flow_info": json.dumps({
            "flow_name": "new_to_family_ig_default",
            "flow_type": "ntf"
        }, separators=(',', ':')),
        "is_platform_login": 0,
        "INTERNAL__latency_qpl_marker_id": 36707139,
        "reg_info": json.dumps({
            "first_name": None,
            "last_name": None,
            "full_name": full_name,
            "contactpoint": email,
            "ar_contactpoint": None,
            "contactpoint_type": "email",
            "is_using_unified_cp": False,
            "unified_cp_screen_variant": "control",
            "is_cp_auto_confirmed": False,
            "is_cp_auto_confirmable": False,
            "is_cp_claimed": False,
            "confirmation_code": confirmation_code,
            "birthday": birthday,
            "birthday_derived_from_age": None,
            "age_range": age_range,
            "did_use_age": False,
            "os_shared_age_range": None,
            "gender": None,
            "use_custom_gender": False,
            "custom_gender": None,
            "encrypted_password": enquired_password,
            "username": None,
            "username_prefill": username_prefill,
            "fb_conf_source": None,
            "device_id": device_id_val,
            "ig4a_qe_device_id": qe_device_id,
            "family_device_id": family_device_id,
            "user_id": None,
            "safetynet_token":safetynet_token,
            "skip_slow_rel_check": True,
            "safetynet_response": "API_ERROR: class com.google.android.gms.common.api.ApiException:7: ",
            "machine_id": machine_id,
            "profile_photo": None,
            "profile_photo_id": None,
            "profile_photo_upload_id": None,
            "avatar": None,
            "email_oauth_token_no_contact_perm": None,
            "email_oauth_token": None,
            "email_oauth_tokens": [],
            "sign_in_with_google_email": None,
            "should_skip_two_step_conf": None,
            "openid_tokens_for_testing": None,
            "encrypted_msisdn": None,
            "encrypted_msisdn_for_safetynet": None,
            "cached_headers_safetynet_info": None,
            "should_skip_headers_safetynet": None,
            "headers_last_infra_flow_id": None,
            "headers_last_infra_flow_id_safetynet": None,
            "headers_flow_id": None,
            "was_headers_prefill_available": None,
            "sso_enabled": None,
            "existing_accounts": None,
            "used_ig_birthday": None,
            "create_new_to_app_account": None,
            "skip_session_info": None,
            "ck_error": None,
            "ck_id": None,
            "ck_nonce": None,
            "should_save_password": True,
            "fb_access_token": None,
            "is_msplit_reg": None,
            "is_spectra_reg": None,
            "dema_account_consent_given": None,
            "spectra_reg_token": None,
            "spectra_reg_guardian_id": None,
            "spectra_reg_guardian_logged_in_context": None,
            "user_id_of_msplit_creator": None,
            "msplit_creator_nonce": None,
            "dma_data_combination_consent_given": None,
            "xapp_accounts": None,
            "fb_device_id": None,
            "fb_machine_id": None,
            "ig_device_id": None,
            "ig_machine_id": None,
            "should_skip_nta_upsell": None,
            "big_blue_token": None,
            "caa_reg_flow_source": "login_home_native_integration_point",
            "ig_authorization_token": None,
            "full_sheet_flow": False,
            "crypted_user_id": None,
            "is_caa_perf_enabled": True,
            "is_preform": True,
            "should_show_rel_error": False,
            "ignore_suma_check": False,
            "dismissed_login_upsell_with_cna": False,
            "ignore_existing_login": False,
            "ignore_existing_login_from_suma": False,
            "ignore_existing_login_after_errors": False,
            "suggested_first_name": None,
            "suggested_last_name": None,
            "suggested_full_name": None,
            "frl_authorization_token": None,
            "post_form_errors": None,
            "skip_step_without_errors": False,
            "existing_account_exact_match_checked": False,
            "existing_account_fuzzy_match_checked": False,
            "email_oauth_exists": False,
            "confirmation_code_send_error": None,
            "is_too_young": False,
            "source_account_type": None,
            "whatsapp_installed_on_client": False,
            "confirmation_medium": None,
            "source_credentials_type": None,
            "source_cuid": None,
            "source_account_reg_info": None,
            "soap_creation_source": None,
            "source_account_type_to_reg_info": None,
            "registration_flow_id": registration_flow_id,
            "should_skip_youth_tos": False,
            "is_youth_regulation_flow_complete": False,
            "is_on_cold_start": False,
            "email_prefilled": False,
            "cp_confirmed_by_auto_conf": False,
            "in_sowa_experiment": False,
            "youth_regulation_config": None,
            "conf_allow_back_nav_after_change_cp": None,
            "conf_bouncing_cliff_screen_type": None,
            "conf_show_bouncing_cliff": None,
            "eligible_to_flash_call_in_ig4a": False,
            "eligible_to_mo_sms_in_ig4a": False,
            "mo_sms_ent_id": None,
            "flash_call_permissions_status": None,
            "gms_incoming_call_retriever_eligibility": None,
            "attestation_result": None,
            "request_data_and_challenge_nonce_string": None,
            "confirmed_cp_and_code": None,
            "notification_callback_id": None,
            "reg_suma_state": 0,
            "is_msplit_neutral_choice": False,
            "msg_previous_cp": None,
            "ntp_import_source_info": None,
            "youth_consent_decision_time": None,
            "sk_pipa_consent_given": None,
            "should_show_spi_before_conf": True,
            "google_oauth_account": None,
            "is_reg_request_from_ig_suma": False,
            "is_toa_reg": False,
            "is_threads_public": False,
            "spc_import_flow": False,
            "caa_play_integrity_attestation_result": None,
            "client_known_key_hash": None,
            "flash_call_provider": None,
            "is_in_gms_experience": None,
            "flash_call_nonce_prefix_details": None,
            "spc_birthday_input": False,
            "failed_birthday_year_count": None,
            "user_presented_medium_source": None,
            "user_opted_out_of_ntp": None,
            "is_from_registration_reminder": False,
            "show_youth_reg_in_ig_spc": False,
            "fb_suma_is_high_confidence": None,
            "screen_visited": [
                "CAA_REG_CONTACT_POINT_PHONE",
                "CAA_REG_CONTACT_POINT_EMAIL",
                "CAA_REG_CONFIRMATION_SCREEN",
                "CAA_REG_PASSWORD",
                "bloks.caa.reg.birthday",
                "CAA_REG_IG_NAME_SCREEN",
                "CAA_REG_IG_USERNAME"
            ],
            "fb_email_login_upsell_skip_suma_post_tos": False,
            "fb_suma_is_from_email_login_upsell": False,
            "fb_suma_is_from_phone_login_upsell": False,
            "should_prefill_cp_in_ar": None,
            "ig_partially_created_account_user_id": None,
            "ig_partially_created_account_nonce": None,
            "ig_partially_created_account_nonce_expiry": None,
            "force_sessionless_nux_experience": False,
            "has_seen_suma_landing_page_pre_conf": False,
            "has_seen_suma_candidate_page_pre_conf": False,
            "has_seen_confirmation_screen": False,
            "suma_on_conf_threshold": -1,
            "move_suma_to_cp_variant": "control",
            "pp_to_nux_eligible": False,
            "should_show_error_msg": True,
            "th_profile_photo_token": None,
            "attempted_silent_auth_in_fb": False,
            "attempted_silent_auth_in_ig": False,
            "cp_suma_results_map": None,
            "source_username": None,
            "next_uri": None,
            "should_use_next_uri": None,
            "linking_entry_point": None,
            "fb_encrypted_partial_new_account_properties": None,
            "starter_pack_name": None,
            "starter_pack_creator_user_ids": None,
            "wa_data_bundle": None,
            "bloks_controller_source": None,
            "airwave_registration_code": None,
            "is_sessionless_nux": None,
            "login_contactpoint": None,
            "login_contactpoint_type": None,
            "is_nta_shortened": False,
            "should_show_bday_after_name_suggestions": None,
            "should_override_back_nav": False,
            "ig_footer_variant": "control",
            "device_network_info": None,
            "is_from_web_lite_reg_controller": None,
            "login_form_siwg_email": None,
            "account_setup_waterfall_id": None,
            "is_wanted_suma_user": False,
            "device_zero_balance_state": None,
            "is_in_nta_single_form": False
        }, separators=(',', ':')),
        "family_device_id": family_device_id,
        "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
        "suggestions_container_id": suggestions_container_id,
        "action": 1,
        "screen_id": screen_id,
        "access_flow_version": "pre_mt_behavior",
        "post_tos": 0,
        "input_id": input_id,
        "is_from_logged_in_switcher": 0,
        "current_step": 8,
        "qe_device_id": qe_device_id
    }
    payload = {
        "params": json.dumps({
            "client_input_params": client_input_params,
            "server_params": server_params
        }, separators=(',', ':')),
        "bk_client_context": json.dumps({
            "bloks_version": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
            "styles_id": "instagram"
        }, separators=(',', ':')),
        "bloks_versioning_id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf"
    }
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.reg.username_ig.async/"
          
    try:
        response = requests.post(url,headers=headers,data=payload, timeout=30)
        cleaned_response =  response.text.replace('//', '', 1) if response.text.startswith('//') else response.text
      
        if response.status_code == 200 and cleaned_response.__contains__(username)and not cleaned_response.__contains__("username_is_taken"):
            print(f'[+] username : "{username}"')
            pattern = r'\\"pre_mt_behavior\\",\s*\\"unknown\\",\s*\\"(.*?)\\"'
            reg_context_token = re.search(pattern, cleaned_response)
            if reg_context_token:
                reg_context_token = reg_context_token.group(1)
                time.sleep(2)
                send_create_account_request(full_name,username,password,email,user_agent,safetynet_token,timestamp,enquired_password,aaccs,aacjid,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context_token,machine_id,registration_flow_id,confirmation_code,birthday)
            
            else:
                print("done but reg context token not found") 
        elif cleaned_response.__contains__("username_is_taken"):
            print(f"â The username '{username}' is already taken. Retrying with a new username...")
            new_username = generate_username()
            send_username_request(new_username,full_name,email,password,aacjid,aaccs,user_agent,username_prefill,enquired_password,safetynet_token,timestamp,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context,machine_id,registration_flow_id,confirmation_code,birthday)   

    except Exception as e:
        print(f"â Error: {e}")
        return {"success": False, "error": str(e)} 
    
def send_create_account_request(full_name,username,password,email,user_agent,safetynet_token,timestamp,encrypted_password,aaccs,aacjid,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context,machine_id,registration_flow_id,confirmation_code,birthday,age_range="o18"):
    current_time = datetime.now().timestamp()
    pigeon_session_id = f"UFS-{str(uuid.uuid4())}-0"
    event_request_id = str(uuid.uuid4())
    latency_instance_id = float(f"{random.randint(1, 9)}.{random.randint(10000000000000, 99999999999999)}E13")
    headers = {
        "Host": "i.instagram.com",
        "X-Ig-App-Locale": "en_US",
        "X-Ig-Device-Locale": "en_US",
        "X-Ig-Mapped-Locale": "en_US",
        "X-Pigeon-Session-Id": pigeon_session_id,
        "X-Pigeon-Rawclienttime": str(current_time),
        "X-Ig-Bandwidth-Speed-Kbps": "-1.000",
        "X-Ig-Bandwidth-Totalbytes-B": "0",
        "X-Ig-Bandwidth-Totaltime-Ms": "0",
        "X-Bloks-Version-Id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
        "X-Ig-Www-Claim": "0",
        "X-Bloks-Prism-Button-Version": "CONTROL",
        "X-Bloks-Prism-Colors-Enabled": "false",
        "X-Bloks-Prism-Ax-Base-Colors-Enabled": "false",
        "X-Bloks-Prism-Font-Enabled": "false",
        "X-Bloks-Is-Layout-Rtl": "false",
        "X-Ig-Device-Id": qe_device_id,
        "X-Ig-Family-Device-Id": family_device_id,
        "X-Ig-Android-Id": device_id_val,
        "X-Ig-Timezone-Offset": "28800",
        "X-Ig-Nav-Chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1772845836.640::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_phone:2:button:1772845839.819::,IgCdsScreenNavigationLoggerModule:com.bloks.www.bloks.caa.reg.contactpoint_email:3:button:1772845841.684::",
        "X-Fb-Connection-Type": "WIFI",
        "X-Ig-Connection-Type": "WIFI",
        "X-Ig-Capabilities": "3brTv10=",
        "X-Ig-App-Id": "567067343352427",
        "Priority": "u=3",
        "User-Agent": user_agent,
        "Accept-Language": "en-US",
        "X-Mid": machine_id,
        "Ig-Intended-User-Id": "0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Fb-Http-Engine": "Liger",
        "X-Fb-Client-Ip": "True",
        "X-Fb-Server-Cluster": "True",
        "Connection": "keep-alive"
    }
    client_input_params = {
        "ck_error": "",
        "aac": json.dumps({
            "aac_init_timestamp": timestamp,
            "aacjid": aacjid,
            "aaccs": aaccs
        }, separators=(',', ':')),
        "device_id": device_id_val,
        "waterfall_id": waterfall_id,
        "zero_balance_state": "",
        "network_bssid": None,
        "failed_birthday_year_count": "",
        "headers_last_infra_flow_id": "",
        "ig_partially_created_account_nonce_expiry": 0,
        "machine_id": machine_id,
        "should_ignore_existing_login": 0,
        "reached_from_tos_screen": 1,
        "ig_partially_created_account_nonce": "",
        "ck_nonce": "",
        "force_sessionless_nux_experience": 0,
        "lois_settings": {"lois_token": ""},
        "ig_partially_created_account_user_id": 0,
        "cloud_trust_token": None,
        "ck_id": "",
        "no_contact_perm_email_oauth_token": "",
        "encrypted_msisdn": ""
    }
    server_params = {
        "event_request_id": event_request_id,
        "is_from_logged_out": 0,
        "layered_homepage_experiment_group": None,
        "device_id": device_id_val,
        "reg_context": reg_context,
        "login_surface": "unknown",
        "waterfall_id": waterfall_id,
        "INTERNAL__latency_qpl_instance_id": latency_instance_id,
        "flow_info": json.dumps({
            "flow_name": "new_to_family_ig_default",
            "flow_type": "ntf"
        }, separators=(',', ':')),
        "is_platform_login": 0,
        "should_ignore_suma_check": 0,
        "INTERNAL__latency_qpl_marker_id": 36707139,
        "bloks_controller_source": "bk_caa_reg_tos_screen",
        "reg_info": json.dumps({
            "first_name": None,
            "last_name": None,
            "full_name": full_name,
            "contactpoint": email,
            "ar_contactpoint": None,
            "contactpoint_type": "email",
            "is_using_unified_cp": False,
            "unified_cp_screen_variant": "control",
            "is_cp_auto_confirmed": False,
            "is_cp_auto_confirmable": False,
            "is_cp_claimed": False,
            "confirmation_code": confirmation_code,
            "birthday": birthday,
            "birthday_derived_from_age": None,
            "age_range": age_range,
            "did_use_age": False,
            "os_shared_age_range": None,
            "gender": None,
            "use_custom_gender": False,
            "custom_gender": None,
            "encrypted_password": encrypted_password,
            "username": username,
            "username_prefill": username,
            "fb_conf_source": None,
            "device_id": device_id_val,
            "ig4a_qe_device_id": qe_device_id,
            "family_device_id": family_device_id,
            "user_id": None,
            "safetynet_token": safetynet_token,
            "skip_slow_rel_check": True,
            "safetynet_response": "API_ERROR: class com.google.android.gms.common.api.ApiException:7: ",
            "machine_id": machine_id,
            "profile_photo": None,
            "profile_photo_id": None,
            "profile_photo_upload_id": None,
            "avatar": None,
            "email_oauth_token_no_contact_perm": None,
            "email_oauth_token": None,
            "email_oauth_tokens": [],
            "sign_in_with_google_email": None,
            "should_skip_two_step_conf": None,
            "openid_tokens_for_testing": None,
            "encrypted_msisdn": None,
            "encrypted_msisdn_for_safetynet": None,
            "cached_headers_safetynet_info": None,
            "should_skip_headers_safetynet": None,
            "headers_last_infra_flow_id": None,
            "headers_last_infra_flow_id_safetynet": None,
            "headers_flow_id": None,
            "was_headers_prefill_available": None,
            "sso_enabled": None,
            "existing_accounts": None,
            "used_ig_birthday": None,
            "create_new_to_app_account": None,
            "skip_session_info": None,
            "ck_error": None,
            "ck_id": None,
            "ck_nonce": None,
            "should_save_password": True,
            "fb_access_token": None,
            "is_msplit_reg": None,
            "is_spectra_reg": None,
            "dema_account_consent_given": None,
            "spectra_reg_token": None,
            "spectra_reg_guardian_id": None,
            "spectra_reg_guardian_logged_in_context": None,
            "user_id_of_msplit_creator": None,
            "msplit_creator_nonce": None,
            "dma_data_combination_consent_given": None,
            "xapp_accounts": None,
            "fb_device_id": None,
            "fb_machine_id": None,
            "ig_device_id": None,
            "ig_machine_id": None,
            "should_skip_nta_upsell": None,
            "big_blue_token": None,
            "caa_reg_flow_source": "lid_landing_screen",
            "ig_authorization_token": None,
            "full_sheet_flow": False,
            "crypted_user_id": None,
            "is_caa_perf_enabled": True,
            "is_preform": True,
            "should_show_rel_error": False,
            "ignore_suma_check": False,
            "dismissed_login_upsell_with_cna": False,
            "ignore_existing_login": False,
            "ignore_existing_login_from_suma": False,
            "ignore_existing_login_after_errors": False,
            "suggested_first_name": None,
            "suggested_last_name": None,
            "suggested_full_name": None,
            "frl_authorization_token": None,
            "post_form_errors": None,
            "skip_step_without_errors": False,
            "existing_account_exact_match_checked": False,
            "existing_account_fuzzy_match_checked": False,
            "email_oauth_exists": False,
            "confirmation_code_send_error": None,
            "is_too_young": False,
            "source_account_type": None,
            "whatsapp_installed_on_client": False,
            "confirmation_medium": None,
            "source_credentials_type": None,
            "source_cuid": None,
            "source_account_reg_info": None,
            "soap_creation_source": None,
            "source_account_type_to_reg_info": None,
            "registration_flow_id": registration_flow_id,
            "should_skip_youth_tos": False,
            "is_youth_regulation_flow_complete": False,
            "is_on_cold_start": False,
            "email_prefilled": False,
            "cp_confirmed_by_auto_conf": False,
            "in_sowa_experiment": False,
            "youth_regulation_config": None,
            "conf_allow_back_nav_after_change_cp": None,
            "conf_bouncing_cliff_screen_type": None,
            "conf_show_bouncing_cliff": None,
            "eligible_to_flash_call_in_ig4a": False,
            "eligible_to_mo_sms_in_ig4a": False,
            "mo_sms_ent_id": None,
            "flash_call_permissions_status": None,
            "gms_incoming_call_retriever_eligibility": None,
            "attestation_result": None,
            "request_data_and_challenge_nonce_string": None,
            "confirmed_cp_and_code": None,
            "notification_callback_id": None,
            "reg_suma_state": 0,
            "is_msplit_neutral_choice": False,
            "msg_previous_cp": None,
            "ntp_import_source_info": None,
            "youth_consent_decision_time": None,
            "sk_pipa_consent_given": None,
            "should_show_spi_before_conf": True,
            "google_oauth_account": None,
            "is_reg_request_from_ig_suma": False,
            "is_toa_reg": False,
            "is_threads_public": False,
            "spc_import_flow": False,
            "caa_play_integrity_attestation_result": None,
            "client_known_key_hash": None,
            "flash_call_provider": None,
            "is_in_gms_experience": None,
            "flash_call_nonce_prefix_details": None,
            "spc_birthday_input": False,
            "failed_birthday_year_count": None,
            "user_presented_medium_source": None,
            "user_opted_out_of_ntp": None,
            "is_from_registration_reminder": False,
            "show_youth_reg_in_ig_spc": False,
            "fb_suma_is_high_confidence": None,
            "screen_visited": [
                "CAA_REG_CONTACT_POINT_PHONE",
                "CAA_REG_CONTACT_POINT_EMAIL",
                "CAA_REG_CONFIRMATION_SCREEN",
                "CAA_REG_PASSWORD",
                "bloks.caa.reg.birthday",
                "CAA_REG_IG_NAME_SCREEN",
                "CAA_REG_IG_USERNAME"
            ],
            "fb_email_login_upsell_skip_suma_post_tos": False,
            "fb_suma_is_from_email_login_upsell": False,
            "fb_suma_is_from_phone_login_upsell": False,
            "should_prefill_cp_in_ar": None,
            "ig_partially_created_account_user_id": None,
            "ig_partially_created_account_nonce": None,
            "ig_partially_created_account_nonce_expiry": None,
            "force_sessionless_nux_experience": False,
            "has_seen_suma_landing_page_pre_conf": False,
            "has_seen_suma_candidate_page_pre_conf": False,
            "has_seen_confirmation_screen": False,
            "suma_on_conf_threshold": -1,
            "move_suma_to_cp_variant": "control",
            "pp_to_nux_eligible": False,
            "should_show_error_msg": True,
            "th_profile_photo_token": None,
            "attempted_silent_auth_in_fb": False,
            "attempted_silent_auth_in_ig": False,
            "cp_suma_results_map": None,
            "source_username": None,
            "next_uri": None,
            "should_use_next_uri": None,
            "linking_entry_point": None,
            "fb_encrypted_partial_new_account_properties": None,
            "starter_pack_name": None,
            "starter_pack_creator_user_ids": None,
            "wa_data_bundle": None,
            "bloks_controller_source": None,
            "airwave_registration_code": None,
            "is_sessionless_nux": None,
            "login_contactpoint": None,
            "login_contactpoint_type": None,
            "is_nta_shortened": False,
            "should_show_bday_after_name_suggestions": None,
            "should_override_back_nav": False,
            "ig_footer_variant": "control",
            "device_network_info": None,
            "is_from_web_lite_reg_controller": None,
            "login_form_siwg_email": None,
            "account_setup_waterfall_id": None,
            "is_wanted_suma_user": None,
            "device_zero_balance_state": None,
            "is_in_nta_single_form": False
        }, separators=(',', ':')),
        "family_device_id": family_device_id,
        "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
        "access_flow_version": "pre_mt_behavior",
        "app_id": 0,
        "is_from_logged_in_switcher": 0,
        "current_step": 9,
        "qe_device_id": qe_device_id
    }
    payload = {
        "params": json.dumps({
            "client_input_params": client_input_params,
            "server_params": server_params
        }, separators=(',', ':')),
        "bk_client_context": json.dumps({
            "bloks_version": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
            "styles_id": "instagram"
        }, separators=(',', ':')),
        "bloks_versioning_id": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf"
    }
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.reg.create.account.async/"
    
    try:
        response = requests.post(url,headers=headers,data=payload,timeout=30 )
        cleaned_response =  response.text.replace('//', '', 1) if response.text.startswith('//') else response.text
        with open("response.txt", "w", encoding="utf-8") as f:
            f.write(cleaned_response)
        if response.status_code == 200 and  cleaned_response.__contains__("Bearer"):
            session = re.search(r'Bearer IGT:2:(.*?),',response.text).group(1).strip()
            session = session[:-8]
            full=base64.b64decode(session).decode('utf-8')
            if "sessionid"  in full:
                sessionid = re.search(r'"sessionid":"(.*?)"}',full).group(1).strip()
                print(f'[+] account created successfully! username: "{username}" \n[+] password: "{password}" \n email: "{email}\n Sessionid: "{sessionid}"')
        elif response.status_code == 200 and cleaned_response.__contains__("challenge_required"):
            print(f'[+] account created successfully but challenge required! username: "{username}" \n[+] password: "{password}" \n email: "{email}"')
        elif cleaned_response.__contains__("Try Again Later"):
            print("Instagram is block you")
        elif cleaned_response.__contains__("We're sorry, but something went wrong. Please try again."):
            # print("Instagram is block you")
            send_create_account_request(full_name,username,password,email,user_agent,safetynet_token,timestamp,encrypted_password,aaccs,aacjid,device_id_val,waterfall_id,qe_device_id,family_device_id,reg_context,machine_id,registration_flow_id,confirmation_code,birthday,age_range)
        else:
            print(f"â Failed to create account. Status Code: {response.status_code}, Response: {cleaned_response}")
    except Exception as e:
        print(f"â Error: {e}")
        return {"success": False, "error": str(e)}   
    

if __name__ == "__main__":
    send_signup_request()
    

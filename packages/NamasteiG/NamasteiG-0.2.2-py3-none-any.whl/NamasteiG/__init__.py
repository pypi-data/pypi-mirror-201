import uuid
import string
import requests
import sys
import random
import secrets
import time
from urllib.parse   import urlencode
import base64
from Cryptodome.Cipher import AES, PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes

value=[]
value1=[]

def password_encrypt(password):
    resp = requests.get('https://i.instagram.com/api/v1/qe/sync/')
    publickeyid = int(resp.headers.get('ig-set-password-encryption-key-id'))
    publickey = resp.headers.get('ig-set-password-encryption-pub-key')
    session_key = get_random_bytes(32)
    iv = get_random_bytes(12)
    timestamp = str(int(time.time()))
    decoded_publickey = base64.b64decode(publickey.encode())
    recipient_key = RSA.import_key(decoded_publickey)
    cipher_rsa = PKCS1_v1_5.new(recipient_key)
    rsa_encrypted = cipher_rsa.encrypt(session_key)
    cipher_aes = AES.new(session_key, AES.MODE_GCM, iv)
    cipher_aes.update(timestamp.encode())
    aes_encrypted, tag = cipher_aes.encrypt_and_digest(password.encode("utf8"))
    size_buffer = len(rsa_encrypted).to_bytes(2, byteorder='little')
    payload = base64.b64encode(b''.join([
        b"\x01",
        publickeyid.to_bytes(1, byteorder='big'),
        iv,
        size_buffer,
        rsa_encrypted,
        tag,
        aes_encrypted
    ]))
    return payload.decode()



class Instagram:

    def __init__(self,User,Password):
        self.user = User
        self.passw=Password
        self.PigeonSession = f'UFS-{str(uuid.uuid4())}-0'
        self.IgDeviceId = uuid.uuid4()
        self.IgFamilyDeviceId = uuid.uuid4()
        self.AndroidID = f'android-{secrets.token_hex(8)}'
        rnd=str(random.randint(150, 999))
        self.UserAgent = "Instagram 276.1.0.26.103 Android (" + ["23/6.0", "24/7.0", "25/7.1.1", "26/8.0", "27/8.1", "28/9.0"][random.randint(0, 5)] + "; " + str(random.randint(100, 1300)) + "dpi; " + str(random.randint(200, 2000)) + "x" + str(random.randint(200, 2000)) + "; " + ["SAMSUNG", "HUAWEI", "LGE/lge", "HTC", "ASUS", "ZTE", "ONEPLUS", "XIAOMI", "OPPO", "VIVO", "SONY", "REALME"][random.randint(0, 11)] + "; SM-T" + rnd + "; SM-T" + rnd + "; qcom; en_US; 460846236)"
        self.Blockversion = '0620e51c315c4db6af09d9ba44f8802cb1253abbf7902647f6e1e0e327c8d93f'

    def generate_jazoest(self,symbols):
        amount = sum(ord(s) for s in symbols)
        return f'2{amount}'

    def GetMid(self):
        data = urlencode({
            'device_id': str(self.AndroidID),
            'token_hash': '',
            'custom_device_id': str(self.IgDeviceId),
            'fetch_reason': 'token_expired',
        })
        headers = {
            'Host': 'b.i.instagram.com',
            'X-Ig-App-Locale': 'en_US',
            'X-Ig-Device-Locale': 'en_US',
            'X-Ig-Mapped-Locale': 'en_US',
            'X-Pigeon-Session-Id': str(self.PigeonSession),
            'X-Pigeon-Rawclienttime': str(round(time.time(), 3)),
            'X-Ig-Bandwidth-Speed-Kbps': f'{random.randint(1000, 9999)}.000',
            'X-Ig-Bandwidth-Totalbytes-B': f'{random.randint(10000000, 99999999)}',
            'X-Ig-Bandwidth-Totaltime-Ms': f'{random.randint(10000, 99999)}',
            'X-Bloks-Version-Id': str(self.Blockversion),
            'X-Ig-Www-Claim': '0',
            'X-Bloks-Is-Layout-Rtl': 'false',
            'X-Ig-Device-Id': str(self.IgDeviceId),
            'X-Ig-Android-Id': str(self.AndroidID),
            'X-Ig-Timezone-Offset': '-21600',
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-Capabilities': '3brTv10=',
            'X-Ig-App-Id': '567067343352427',
            'Priority': 'u=3',
            'User-Agent': str(self.UserAgent),
            'Accept-Language': 'en-US',
            'Ig-Intended-User-Id': '0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': str(len(data)),
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
            'Connection': 'close',
        }
        requests.post('https://b.i.instagram.com/api/v1/zr/tokens/', headers=headers, data=data)
        headers.update({'X-Ig-Family-Device-Id': str(self.IgFamilyDeviceId)})
        requests.post('https://b.i.instagram.com/api/v1/zr/tokens/', headers=headers, data=data)
        data = f'signed_body=SIGNATURE.%7B%22phone_id%22%3A%22{self.IgFamilyDeviceId}%22%2C%22usage%22%3A%22prefill%22%7D'
        updict = {"Content-Length": str(len(data))}
        headers = {key: updict.get(key, headers[key]) for key in headers}
        requests.post(
            'https://b.i.instagram.com/api/v1/accounts/contact_point_prefill/',
            headers=headers,
            data=data)
        data = urlencode({
            'signed_body': 'SIGNATURE.{"bool_opt_policy":"0","mobileconfigsessionless":"","api_version":"3","unit_type":"1","query_hash":"1fe1eeee83cc518f2c8b41f7deae1808ffe23a2fed74f1686f0ab95bbda55a0b","device_id":"'+str(self.IgDeviceId)+'","fetch_type":"ASYNC_FULL","family_device_id":"'+str(self.IgFamilyDeviceId).upper()+'"}',
        })
        updict = {"Content-Length": str(len(data))}
        headers = {key: updict.get(key, headers[key]) for key in headers}
        return requests.post('https://b.i.instagram.com/api/v1/launcher/mobileconfig/', headers=headers, data=data).headers['ig-set-x-mid']

    def Login(self,PassWordEnc=None):
        mid=self.GetMid()
        if PassWordEnc==None:
            self.datapassword=f'#PWD_INSTAGRAM:0:{round(time.time())}:{self.passw}'
        else:
            self.datapassword = f'#PWD_INSTAGRAM:4:{round(time.time())}:{password_encrypt(self.passw)}'
        data = urlencode({
            'signed_body': 'SIGNATURE.{"jazoest":"' + str(self.generate_jazoest(
                str(self.IgFamilyDeviceId))) + '","country_codes":"[{\\"country_code\\":\\"91\\",\\"source\\":[\\"sim\\"]},{\\"country_code\\":\\"1\\",\\"source\\":[\\"default\\"]}]","phone_id":"' + str(
                self.IgFamilyDeviceId) + '","enc_password":"'+str(self.datapassword) + '","username":"' + str(self.user) + '","adid":"' + str(uuid.uuid4()) + '","guid":"' + str(
                self.IgDeviceId) + '","device_id":"' + str(
                self.AndroidID) + '","google_tokens":"[]","login_attempt_count":"0"}',
        })
        headers = {
            'Host': 'i.instagram.com',
            'X-Ig-App-Locale': 'en_US',
            'X-Ig-Device-Locale': 'en_US',
            'X-Ig-Mapped-Locale': 'en_US',
            'X-Pigeon-Session-Id': str(self.PigeonSession),
            'X-Pigeon-Rawclienttime': str(round(time.time(), 3)),
            'X-Ig-Bandwidth-Speed-Kbps': f'{random.randint(1000, 9999)}.000',
            'X-Ig-Bandwidth-Totalbytes-B': f'{random.randint(10000000, 99999999)}',
            'X-Ig-Bandwidth-Totaltime-Ms': f'{random.randint(10000, 99999)}',
            'X-Bloks-Version-Id': self.Blockversion,
            'X-Ig-Www-Claim': '0',
            'X-Bloks-Is-Layout-Rtl': 'false',
            'X-Ig-Device-Id':str(self.IgDeviceId),
            'X-Ig-Family-Device-Id': str(self.IgFamilyDeviceId),
            'X-Ig-Android-Id': str(self.AndroidID),
            'X-Ig-Timezone-Offset': '-21600',
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-Capabilities': '3brTv10=',
            'X-Ig-App-Id': '567067343352427',
            'Priority': 'u=3',
            'User-Agent': self.UserAgent,
            'Accept-Language': 'en-US',
            'X-Mid': mid,
            'Ig-Intended-User-Id': '0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': str(len(data)),
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }
        response = requests.post('https://i.instagram.com/api/v1/accounts/login/', headers=headers, data=data)
        self.response = response
        self.mid = mid

        if 'ig-set-authorization' in response.headers:
            self.sessionid=response.headers['ig-set-authorization'].split(':')[2]

            self.userid = response.headers['ig-set-ig-u-ds-user-id']
            if response.headers['ig-set-ig-u-rur']== '':
                # self.igrur=''.join(random.choices(string.ascii_lowercase+string.digits,k=72))
                headers.update({'Authorization': f'Bearer IGT:2:{self.sessionid}','Ig-U-Ds-User-Id': str(self.userid)})

                data = urlencode({
                    'signed_body': 'SIGNATURE.{"bool_opt_policy":"0","mobileconfig":"","api_version":"3","unit_type":"2","query_hash":"a3a7bb403417698d19de759f72db51546595de24705e3e25c613ff716dc07eee","_uid":"'+str(self.userid)+'","device_id":"'+str(self.IgDeviceId)+'","_uuid":"'+str(self.IgDeviceId)+'","fetch_type":"ASYNC_FULL"}',
                })
                updict = {"Content-Length": str(len(data)),'Ig-Intended-User-Id': str(self.userid),'Host': 'b.i.instagram.com'}
                headers = {key: updict.get(key, headers[key]) for key in headers}
                response1 = requests.post('https://b.i.instagram.com/api/v1/launcher/mobileconfig/', headers=headers, data=data)
                self.xclaim = response1.headers['x-ig-set-www-claim']
                self.igrur = response1.headers['ig-set-ig-u-rur'].split(':')[1]
                self.igid = response1.headers['ig-set-ig-u-shbid'].split(',')[0]

                self.shbid = response.headers['ig-set-ig-u-shbid']
                self.shbts = response.headers['ig-set-ig-u-shbts']
                self.urur = response.headers['ig-set-ig-u-rur']

            else:
                self.igrur = response.headers['ig-set-ig-u-rur'].split(':')[1]
                self.xclaim = response.headers['x-ig-set-www-claim']


            value = {
                "Response": self.response,
                "Mid": self.mid,
                'PigeonSession': self.PigeonSession,
                "IgDeviceId": self.IgDeviceId,
                "IgFamilyDeviceId": self.IgFamilyDeviceId,
                "AndroidID": self.AndroidID,
                'UserAgent': self.UserAgent,
                'BlockVersion': self.Blockversion,
                'igrur': self.igrur,
                'Xclaim': self.xclaim,
                'BearerToken': self.sessionid,
                'igid':self.igid,
            }

        else:
            print(response.text)
            sys.exit()

        #     value = {
        #         "Response": self.response,
        #         "Mid": self.mid,
        #         'PigeonSession': self.PigeonSession,
        #         "IgDeviceId": self.IgDeviceId,
        #         "IgFamilyDeviceId": self.IgFamilyDeviceId,
        #         "AndroidID": self.AndroidID,
        #         'UserAgent': self.UserAgent,
        #         'BlockVersion': self.Blockversion
        #     }
        #
        # return value
    def head(self):
        headers = {
            'Host': 'i.instagram.com',
            'X-Ig-App-Locale': 'en_US',
            'X-Ig-Device-Locale': 'en_US',
            'X-Ig-Mapped-Locale': 'en_US',
            'X-Pigeon-Session-Id': str(self.PigeonSession),
            'X-Pigeon-Rawclienttime': str(round(time.time(), 3)),
            'X-Ig-Bandwidth-Speed-Kbps': f'{random.randint(1000, 9999)}.000',
            'X-Ig-Bandwidth-Totalbytes-B': f'{random.randint(10000000, 99999999)}',
            'X-Ig-Bandwidth-Totaltime-Ms': f'{random.randint(10000, 99999)}',
            'X-Ig-App-Startup-Country': 'US',
            'X-Bloks-Version-Id': str(self.Blockversion),
            'X-Ig-Www-Claim': str(self.xclaim),
            'X-Bloks-Is-Layout-Rtl': 'false',
            'X-Ig-Device-Id': str(self.IgDeviceId),
            'X-Ig-Family-Device-Id': str(self.IgFamilyDeviceId),
            'X-Ig-Android-Id': str(self.AndroidID),
            'X-Ig-Timezone-Offset': '-21600',
            'X-Ig-Nav-Chain': f'ExploreFragment:explore_popular:2:main_search:{round(time.time(), 3)}::,TopSearchChildFragment:blended_search:3:button:{round(time.time(), 3)}::,UserDetailFragment:profile:4:search_result:{round(time.time(), 3)}::,ProfileMediaTabFragment:profile:5:button:{round(time.time(), 3)}::,FollowListFragment:followers:6:button:{round(time.time(), 3)}::',
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-Capabilities': '3brTv10=',
            'X-Ig-App-Id': '567067343352427',
            'Priority': 'u=3',
            'User-Agent': str(self.UserAgent),
            'Accept-Language': 'en-US',
            'Authorization': 'Bearer IGT:2:' + str(self.sessionid),
            'X-Mid': str(self.mid),
            'Ig-U-Shbid': str(self.shbid),
            'Ig-U-Shbts': str(self.shbts),
            'Ig-U-Ds-User-Id': str(self.userid),
            'Ig-U-Rur': str(self.urur),
            'Ig-Intended-User-Id': str(self.userid),
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }
        return headers

    def Scrape_Followers(self,UserID,Next_Max_Id=None):
        global value
        self.value=value
        self.UserID1=UserID
        self.ranktoken=str(uuid.uuid4())
        if Next_Max_Id == None:
            params = {
                'search_surface': 'follow_list_page',
                'query': '',
                'enable_groups': 'true',
                'rank_token': str(self.ranktoken),
            }
        else:
            params = {
                'search_surface': 'follow_list_page',
                'max_id': str(self.maxid),
                'query': '',
                'enable_groups': 'true',
                'rank_token': str(self.ranktoken),
            }
        response = requests.get(
            f'https://i.instagram.com/api/v1/friendships/{self.UserID1}/followers/',
            params=params,
            headers=Instagram.head(self),
        )
        if 'Oops, an error occurred.' in response.text:
            print('Oops, an error occurred.')
        elif 'The link you followed may be broken, or the page may have been removed' in response.text:
            print('The link you followed may be broken, or the page may have been removed')
        elif 'Please wait a few minutes before you try again.' in response.text:
            print(response.text)
        elif "challenge_required" in response.text:
            print(response.text)
        elif 'next_max_id' in response.text:

            try:
                self.xclaim = response.headers['x-ig-set-www-claim']
                self.shbid = response.headers['ig-set-ig-u-shbid']
                self.shbts = response.headers['ig-set-ig-u-shbts']
                self.urur = response.headers['ig-set-ig-u-rur']

                self.maxid=response.json()['next_max_id']
                for Items in response.json()['users']:
                    value.append(Items)
                Instagram.Scrape_Followers(self,self.UserID1,self.maxid)
            except Exception as key:
                print(key)
                return value
        else:
            try:

                self.xclaim = response.headers['x-ig-set-www-claim']
                self.shbid = response.headers['ig-set-ig-u-shbid']
                self.shbts = response.headers['ig-set-ig-u-shbts']
                self.urur = response.headers['ig-set-ig-u-rur']

                for Items in response.json()['users']:
                    value.append(Items)
            except Exception as key:
                print(key)

                pass
        return value
    def Scrape_Followings(self,UserID,Next_Max_Id=None):
        global value1
        self.value1 = value1
        self.UserID1 = UserID
        self.ranktoken = str(uuid.uuid4())
        if Next_Max_Id == None:
            params = {
            'includes_hashtags': 'true',
            'search_surface': 'follow_list_page',
            'query': '',
            'enable_groups': 'true',
            'rank_token': str(self.ranktoken),
            }
        else:
            params = {
                'includes_hashtags': 'true',
                'search_surface': 'follow_list_page',
                'max_id': str(self.maxid),
                'query': '',
                'enable_groups': 'true',
                'rank_token':str(self.ranktoken),
            }

        response = requests.get(
            f'https://i.instagram.com/api/v1/friendships/{self.UserID1}/following/',
            params=params,
            headers=Instagram.head(self),
        )
        if 'Oops, an error occurred.' in response.text:
            print('Oops, an error occurred.')
        elif 'The link you followed may be broken, or the page may have been removed' in response.text:
            print('The link you followed may be broken, or the page may have been removed')
        elif 'Please wait a few minutes before you try again.' in response.text:
            print(response.text)
        elif "challenge_required" in response.text:
            print(response.text)
        elif 'next_max_id' in response.text:

            try:

                self.xclaim = response.headers['x-ig-set-www-claim']
                self.shbid = response.headers['ig-set-ig-u-shbid']
                self.shbts = response.headers['ig-set-ig-u-shbts']
                self.urur = response.headers['ig-set-ig-u-rur']




                self.maxid=response.json()['next_max_id']
                for Items in response.json()['users']:
                    value1.append(Items)
                Instagram.Scrape_Followings(self,self.UserID1,self.maxid)
            except Exception as key:
                print(key)
                return value1
        else:
            try:

                self.xclaim = response.headers['x-ig-set-www-claim']
                self.shbid = response.headers['ig-set-ig-u-shbid']
                self.shbts = response.headers['ig-set-ig-u-shbts']
                self.urur = response.headers['ig-set-ig-u-rur']



                for Items in response.json()['users']:
                    value1.append(Items)
            except Exception as key:
                print(key)
        return value1

    def Follow_UserID(self,FollowID):
        self.FollowID=FollowID
        try:

            data = {
                'signed_body': 'SIGNATURE.{"user_id":"'+str(self.FollowID)+'","radio_type":"wifi-none","_uid":"'+str(self.userid)+'","device_id":"'+str(self.AndroidID)+'","_uuid":"'+str(self.IgDeviceId)+'","nav_chain":"ExploreFragment:explore_popular:2:main_search:'+str(round(time.time(), 3))+'::,TopSearchChildFragment:blended_search:3:button:'+str(round(time.time(), 3))+'::,UserDetailFragment:profile:4:search_result:'+str(round(time.time(), 3))+'::,ProfileMediaTabFragment:profile:5:button:'+str(round(time.time(), 3))+'::,FollowListFragment:followers:6:button:'+str(round(time.time(), 3))+'::,UserDetailFragment:profile:10:button:'+str(round(time.time(), 3))+'::"}',
            }

            response = requests.post(
                f'https://i.instagram.com/api/v1/friendships/create/{self.FollowID}/',
                headers=Instagram.head(self),
                data=data,
            )
            return response.text

        except Exception as E:
            print(E)



# if __name__ == '__main__':
#     ig=Instagram('','')
#     ig.Login()
#     print(ig.Follow_UserID('4567890'))




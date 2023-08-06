from Crypto.Util.Padding import pad, unpad
from base64 import b64encode as b64e, urlsafe_b64decode as b64d
from Crypto.Cipher import AES
from requests import get, post
from aiohttp import ClientSession as cs
from random import choice, randint
from websocket import create_connection as cc
from json import loads, dumps
from websockets import connect as cc_async
from time import time
from asyncio import run
from pathlib import Path
from PIL import Image
from io import BytesIO
from mutagen.mp3 import MP3
from tinytag import TinyTag
from re import findall

class Nany:

    def __init__(self, auth):
        self.key = bytearray(self.secret(auth), 'UTF-8')
        self.iv = bytearray.fromhex('0' * 32)
       
    def replaceCharAt(self, e, t, i):
        return e[0:t] + i + e[t + len(i):]

    def secret(self, e):
        t, n, s = e[0:8], e[16:24] + e[0:8] + e[24:32] + e[8:16], 0
        while s < len(n):
            e = n[s]
            if e >= '0' and e <= '9':
                t = chr((ord(e[0]) - ord('0') + 5) %10 + ord('0'))
                n = self.replaceCharAt(n, s, t)
            else:
                t = chr((ord(e[0]) - ord('a') + 9) %26 + ord('a'))
                n = self.replaceCharAt(n, s, t)
            s += 1
        return n

    def encrypt(self, text):
        return b64e(AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(pad(text.encode('UTF-8'), AES.block_size))).decode('UTF-8')

    def decrypt(self, text):
        return unpad(AES.new(self.key, AES.MODE_CBC, self.iv).decrypt(b64d(text.encode('UTF-8'))), AES.block_size).decode('UTF-8')

class Socket:
    
    def __init__(self, auth):
        self.auth = auth
        self.crypto = Nany(auth)
        self.hs_data = {
            'api_version': '5',
            'auth': auth,
            'method': 'handShake'
        }
        self.req_clients = {
            'web': {
                'app_name': 'Main',
                'app_version': '4.1.7',
                'platform': 'Web',
                'package': 'web.rubika.ir',
                'lang_code': 'fa'
            },
            'android': {
                'app_name': 'Main',
                'app_version': '3.0.9',
                'platform': 'Android',
                'package': 'ir.resaneh1.iptv',
                'lang_code': 'fa'
            }
        }
        del auth

    def get_server(self, type):
        if type == 'api':
            return 'https://messengerg2c2.iranlms.ir'
        else:
            return choice(list(get('https://getdcmess.iranlms.ir/').json()['data'][type].values()))

    def handler(self):
        print('connecting to the web socket...')
        ws = cc(self.get_server('socket'))
        ws.send(dumps(self.hs_data))
        if loads(ws.recv())['status'] == 'OK':
            print('connected')
            while True:
                try:
                    recv = loads(ws.recv())
                    if recv['type'] == 'messenger':
                        yield loads(self.crypto.decrypt(recv['data_enc']))
                    else:
                        continue
                except:
                    del ws
                    ws = cc(self.get_server('socket'))
                    ws.send(dumps(self.hs_data))
                    continue

    async def handler_async(self):
        print('connecting to the web socket...')
        async for ws in cc_async(self.get_server('socket')):
            try:
                await ws.send(dumps(self.hs_data))
                while True:
                    recv = loads(await ws.recv())
                    if recv != {"status":"OK","status_det":"OK"}:
                        if recv['type'] == 'messenger':
                            yield loads(self.crypto.decrypt(recv['data_enc']))
                    else:
                        continue
            except:
                continue

    def method(self, method, data, api_version = 5):
        if api_version == 5:
            data = {
                'api_version': str(api_version),
                'auth': self.auth,
                'data_enc': self.crypto.encrypt(
                    dumps(
                        {
                            'method': method,
                            'input': data,
                            'client': self.req_clients['web']
                        }
                    )
                )
            }
        else:
            data = {
                'api_version': api_version,
                'auth': self.auth,
                'client': self.req_clients['android'],
                'method': method,
                'data_enc': self.crypto.encrypt(dumps(data))
            }
        while True:
            result = loads(
                self.crypto.decrypt(
                    post(
                        json = data,
                        url = self.get_server('api')
                        ).json()['data_enc']
                    )
                )

            if result['status'] == 'OK':
                return result['data']
            elif result['status'] in ['ERROR_GENERIC', 'ERROR_ACTION']:
                for i in [
                    ('INVALID_AUTH', 'Auth Key vared shodeh na moatabar ast !'),
                    ('NOT_REGISTERED', 'Vorudi method na moatabar ast !'),
                    ('INVALID_INPUT', 'Vorudi method na moatabar ast !'),
                    ('TOO_REQUESTS', 'Darkhast bish az had !')
                ]:
                    if result['status_det'] == i[0]:
                        raise IndexError(i[1])
            else:
                continue

    async def method_async(self, method, data, api_version = 5):
        if api_version == 5:
            data = {
                'api_version': str(api_version),
                'auth': self.auth,
                'data_enc': self.crypto.encrypt(
                    dumps(
                        {
                            'method': method,
                            'input': data,
                            'client': self.req_clients['web']
                        }
                    )
                )
            }
        else:
            data = {
                'api_version': str(api_version),
                'auth': self.auth,
                'client': self.req_clients['android'],
                'method': method,
                'data_enc': self.crypto.encrypt(dumps(data))
            }
        while True:
            async with cs() as result:
                async with result.post(self.get_server('api'), json = data) as result:
                    if result.status == 200:
                        result = loads(self.crypto.decrypt((await result.json())['data_enc']))
                        if result['status'] == 'OK':
                            return result['data']
                        elif result['status'] in ['ERROR_GENERIC', 'ERROR_ACTION']:
                            for i in [
                                ('INVALID_AUTH', 'Auth Key vared shodeh na moatabar ast !'),
                                ('NOT_REGISTERED', 'Vorudi method na moatabar ast !'),
                                ('INVALID_INPUT', 'Vorudi method na moatabar ast !'),
                                ('TOO_REQUESTS', 'Darkhast bish az had !')
                            ]:
                                if result['status_det'] == i[0]:
                                    raise IndexError(i[1])
                    elif result.status == 502:
                        continue
                    else:
                        raise IndexError(result)
                        
class Messages:

    def __init__(self, data):
        self.data = data

    def Chat_id(self):
        try:
            return self.data['message_updates'][0]['object_guid']
        except KeyError:
            try:
                return self.data['object_guid']
            except:
                pass

    def Author_id(self):
        try:
            return self.data['message_updates'][0]['message']['author_object_guid']
        except KeyError:
            try:
                return self.data['last_message']['author_object_guid']
            except:
                pass

    def Message_id(self):
        try:
            return self.data['message_updates'][0]['message_id']
        except KeyError:
            try:
                return self.data['last_message']['message_id']
            except:
                pass

    def Reply_To_Message_id(self):
        try:
            return self.data['message_updates'][0]['message'].get('reply_to_message_id', 'None')
        except KeyError:
            pass

    def text(self):
        try:
            return self.data['message_updates'][0]['message'].get('text', 'None')
        except KeyError:
            try:
                return self.data['last_message'].get('text', 'None')
            except:
                pass

    def Chat_Type(self):
        try:
            return self.data['message_updates'][0]['type']
        except KeyError:
            try:
                return self.data['abs_object']['type']
            except:
                pass

    def Author_Type(self):
        try:
            return self.data['message_updates'][0]['message']['author_type']
        except KeyError:
            try:
                return self.data['last_message']['author_type']
            except:
                pass

    def Message_Type(self):
        try:
            return self.data['message_updates'][0]['message']['type']
        except KeyError:
            return self.data['last_message']['type']
        except:
            pass

    def is_Forward(self):
        try:
            return 'forwarded_from' in self.data['message_updates'][0]['message']
        except KeyError:
            pass
    
    def is_Event(self):
        try:
            return 'event_data' in self.data['message_updates'][0]['message']
        except KeyError:
            return self.Message_Type() == 'Other'
        except:
            pass

    def is_User_Chat(self):
        return self.Chat_Type() == "User"

    def is_Group_Chat(self):
        return self.Chat_Type() == "Group"

    def is_Channel_Chat(self):
        return self.Chat_Type() == "Channel"

    def Chat_Title(self):
        try:
            return self.data["show_notifications"][0].get("title", "None")
        except KeyError:
            try:
                return self.data['abs_object']['title']
            except:
                pass

    def Author_Title(self):
        try:
            return self.data["show_notifications"][0].get("text", "None:Text").split(":")[0] if self.is_group_chat() else self.chat_title()
        except KeyError:
            try:
                return self.data['last_message'].get('author_title', 'None')
            except:
                pass

    def Event_Type(self):
        try:
            return self.data['message_updates'][0]['message']['event_data']['type']
        except KeyError:
                pass

    def Event_id(self):
        try:
            return self.data["message_updates"][0]["message"]["event_data"]["performer_object"]["object_guid"]
        except KeyError:
                pass

class tools:

    def get_File_Name(file):
        return file if not 'http' in file else f'pyrubi {randint(1, 100)}.{format}'

    def get_File_Size(file):
        return str(len(get(file).content if 'http' in file else open(file,'rb').read()))

    def get_Thumbnail(image_bytes):
        image = Image.open(BytesIO(image_bytes))
        width, height = image.size
        if height > width:
            new_height = 40
            new_width  = round(new_height * width / height)
        else:
            new_width = 40
            new_height = round(new_width * height / width)
        image = image.resize((new_width, new_height), Image.ANTIALIAS)
        changed_image = BytesIO()
        image.save(changed_image, format='PNG')
        return b64e(changed_image.getvalue())

    def get_image_Size(image_bytes):
        width, height = Image.open(BytesIO(image_bytes)).size
        return width , height

    def get_Voice_Duration(voice_bytes):
        file = BytesIO()
        file.write(voice_bytes)
        file.seek(0)
        return MP3(file).info.length

    def get_Video_Duration(video_bytes):
        return round(TinyTag.get(video_bytes).duration * 1000)

    def get_Music_Artist(music):
        return str(TinyTag.get(music).artist)

    def get_Mime_From_URL(url):
        if '?' in url:
            return url.split('/')[-1].split('?')[0].split('.')[-1]
        elif '.' in url:
            return url.split('.')[-1]
        else:
            return '.pyrubi'

    def Check_Metadata(text):
        g = 0
        if text is None:
            return ([], text)
        results = []
        real_text = text.replace('**', '').replace('__', '').replace('``', '').replace('@@', '')
        bolds = findall(r'\*\*(.*?)\*\*' , text)
        italics = findall(r'\_\_(.*?)\_\_' , text)
        monos = findall(r'\`\`(.*?)\`\`' , text)
        mentions = findall(r'\@\@(.*?)\@\@' , text)
        mention_ids = findall(r'\@\@\((.*?)\)' , text)
        print(mention_ids)
        for bIndex , bWord in zip([real_text.index(i) for i in bolds] , bolds):
            results.append(
                {
                    'from_index' : bIndex,
                    'length' : len(bWord),
                    'type' : 'Bold'
                }
            )
        for iIndex , iWord in zip([real_text.index(i) for i in italics] , italics):
            results.append(
                {
                    'from_index' : iIndex,
                    'length' : len(iWord),
                    'type' : 'Italic'
                }
            )
        for mIndex , mWord in zip([real_text.index(i) for i in monos] , monos):
            results.append(
                {
                    'from_index' : mIndex,
                    'length' : len(mWord),
                    'type' : 'Mono'
                }
            )
        for meIndex , meWord in zip([real_text.index(i) for i in mentions] , mentions):
            results.append(
                {
                    'type': 'MentionText',
                    'from_index': meIndex,
                    'length': len(meWord),
                    'mention_text_object_guid': mention_ids[g] if '@(' in text else '@'
                }
            )
            if '@(' in text:
                real_text = real_text.replace(f'({mention_ids[g]})', '') 
            g += 1
        print(real_text)
        print(results)
        return (results, real_text)

class bot:

    def __init__(self, auth):
        self.auth = auth
        self.ws = Socket(auth).handler
        self.method = Socket(auth).method
        self.crypto = Nany(auth)
        self.got_messages_update = []
        self.filters = {
            'chat_filter': [],
            'message_filter': []
        }
        del auth

    def Add_Filter(self, chat_filter = [], message_filter = []):
        self.filters['chat_filter'] = chat_filter
        self.filters['message_filter'] = message_filter

    def on_Message(self):
        for recv in self.ws():
            if not Messages(recv).Chat_Type() in self.filters['chat_filter'] and not Messages(recv).Message_Type() in self.filters['message_filter']:
                yield recv
            else:
                continue

    def get_Chat_Update(self, chat_id):
        return self.method(
            'getMessagesUpdates',
            {
                'object_guid': chat_id,
                'state': str(round(time()) - 200)
            }
        )['updated_messages']

    def get_Chats_Update(self):
        while True:
            chats_update = self.method('getChatsUpdates', {'state': str(round(time()) - 200)})['chats'][0]
            if not Messages(chats_update).Message_id() in self.got_messages_update:
                if not Messages(chats_update).Chat_Type() in self.filters['chat_filter'] and not Messages(chats_update).Message_Type() in self.filters['message_filter']:
                    self.got_messages_update.append(Messages(chats_update).Message_id())
                    return chats_update
                else:
                    continue
            else:
                continue

    def SendMessage(self, chat_id, custom_text, message_id = None):
        metadata = tools.Check_Metadata(custom_text)
        data = {
            'object_guid': chat_id,
            'rnd': str(randint(10000000, 999999999)),
            'text': metadata[1].strip(),
            'reply_to_message_id': message_id,
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return self.method('sendMessage', data)

    def Reply(self, data, custom_text):
        msg = Messages(data)
        return self.SendMessage(
            msg.Chat_id(),
            custom_text,
            msg.Message_id()
        )

    def SendPhoto(self, chat_id, file, caption = None, message_id = None, thumbnail = None):
        req = self.Upload_File(file)
        size = tools.get_image_Size(open(file,'rb').read() if not 'http' in file else get(file).content)
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': {
                'dc_id': req[0]['dc_id'],
                'file_id': req[0]['id'],
                'type':'Image',
                'file_name': tools.get_File_Name(file),
                'size': tools.get_File_Size(file),
                'mime': 'png',
                'access_hash_rec': req[1],
                'width': size[0],
                'height': size[1],
                'thumb_inline': tools.get_thumbnail(open(file,'rb').read() if thumbnail == None and not 'http' in file else open(thumbnail,'rb').read() if not 'http' in file else get(file).content).decode('utf-8')
            },
            'object_guid': chat_id,
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id,
            'text': metadata[1]
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return self.method('sendMessage', data)

    def SendVideo(self, chat_id, file, caption = None, message_id = None):
        req = self.Upload_File(file)
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': {
                'file_id': req[0]['id'],
                'mime': 'mp4',
                'dc_id': req[0]['dc_id'],
                'access_hash_rec': req[1],
                'file_name': tools.get_File_Name(file),
                'thumb_inline': '/9j/4AAQSkZJRgABAQAAAQABAAD/4gIoSUNDX1BST0ZJTEUAAQEAAAIYAAAAAAIQAABtbnRyUkdC\nIFhZWiAAAAAAAAAAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAA\nAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlk\nZXNjAAAA8AAAAHRyWFlaAAABZAAAABRnWFlaAAABeAAAABRiWFlaAAABjAAAABRyVFJDAAABoAAA\nAChnVFJDAAABoAAAAChiVFJDAAABoAAAACh3dHB0AAAByAAAABRjcHJ0AAAB3AAAADxtbHVjAAAA\nAAAAAAEAAAAMZW5VUwAAAFgAAAAcAHMAUgBHAEIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFhZWiAA\nAAAAAABvogAAOPUAAAOQWFlaIAAAAAAAAGKZAAC3hQAAGNpYWVogAAAAAAAAJKAAAA+EAAC2z3Bh\ncmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABYWVogAAAAAAAA9tYAAQAAAADT\nLW1sdWMAAAAAAAAAAQAAAAxlblVTAAAAIAAAABwARwBvAG8AZwBsAGUAIABJAG4AYwAuACAAMgAw\nADEANv/bAEMADQkKCwoIDQsKCw4ODQ8TIBUTEhITJxweFyAuKTEwLiktLDM6Sj4zNkY3LC1AV0FG\nTE5SU1IyPlphWlBgSlFST//bAEMBDg4OExETJhUVJk81LTVPT09PT09PT09PT09PT09PT09PT09P\nT09PT09PT09PT09PT09PT09PT09PT09PT09PT//AABEIAGQAOAMBIgACEQEDEQH/xAAWAAEBAQAA\nAAAAAAAAAAAAAAAAAQf/xAAXEAEBAQEAAAAAAAAAAAAAAAAAAREx/8QAFQEBAQAAAAAAAAAAAAAA\nAAAAAAH/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwDMFRRAwACiAACiwAAEQqKi\nqtEAU0QRQADqKBgCCKixVDgYIAIFCiqgAKAiBQqiACixFgACIFCqIAKLAAARCFBRABX/2Q==\n',
                'width': 240,
                'height': 240,
                'time': tools.get_Video_Duration(file),
                'size': tools.get_File_Size(file),
                'type': 'Video'
            },
            'object_guid': chat_id,
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id,
            'text': metadata[1]
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return self.method('sendMessage', data)

    def Send_Gif(self, chat_id, file, caption = None, message_id = None):
        req = self.Upload_File(file)
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': {
                'file_id': req[0]['id'],
                'mime': 'mp4',
                'dc_id': req[0]['dc_id'],
                'access_hash_rec': req[1],
                'file_name': tools.get_File_Name(file),
                'width': 240,
                'height': 240,
                'time': tools.get_Video_Duration(file),
                'size': tools.get_File_Size(file),
                'type': 'Gif',
                'is_round': False,
            },
            'object_guid': chat_id,
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id,
            'text': metadata[1]
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return self.method('sendMessage',data)

    def SendVoice(self, chat_id, file, caption = None, message_id = None, time = None):
        req = self.Upload_File(file)
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': {
                'dc_id': req[0]['dc_id'],
                'file_id': req[0]['id'],
                'type': 'Voice',
                'file_name': tools.get_File_Name(file),
                'size': tools.get_File_Size(file),
                'time': int(tools.get_Voice_Duration(open(file,'rb').read()) if time == None else time) * 1000 if not 'http' in file else 1,
                'mime': 'ogg',
                'access_hash_rec': req[1],
            },
            'object_guid': chat_id,
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id,
            'text': metadata[1]
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return self.method('sendMessage', data)

    def Send_Music(self, chat_id, file, caption = None, message_id = None):
        req = self.Upload_File(file)
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': {
                'file_id': req[0]['id'],
                'mime': 'mp3',
                'dc_id': req[0]['dc_id'],
                'access_hash_rec': req[1],
                'file_name': tools.get_File_Name(file),
                'width': 0,
                'height': 0,
                'time': tools.get_Voice_Duration(open(file,'rb').read()) if not 'http' in file else 1,
                'size': tools.get_File_Size(file),
                'type': 'Music',
                'music_performer': tools.get_Music_Artist(file) if not 'http' in file else 'Pyrubi Library',
                'is_round': False
            },
            'is_mute': False,
            'object_guid': chat_id,
            'text': metadata[1],
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return self.method('sendMessage', data)

    def Send_File(self, chat_id, file, caption = None, message_id = None):
        req = self.Upload_File(file)
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': {
                'dc_id': req[0]['dc_id'],
                'file_id': req[0]['id'],
                'type': 'File',
                'file_name': file if not 'http' in file else f'pyrubi {randint(1, 100)}.{tools.get_Mime_From_URL(file)}',
                'size': tools.get_File_Size(file),
                'mime': file.split('.')[-1] if not 'http' in file else tools.get_Mime_From_URL(file),
                'access_hash_rec': req[1]
            },
            'object_guid': chat_id,
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id,
            'text': metadata[1]
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return self.method('sendMessage', data)

    def Send_Sticker(self, chat_id, message_id = None):
        stickers = choice(self.method('getMyStickerSets',{})['sticker_sets'])
        return self.method(
            'sendMessage',
            {
                'sticker': choice(stickers['top_stickers']),
                'object_guid': chat_id,
                'rnd': str(randint(100000,999999999)),
                'reply_to_message_id': message_id
            }
        )

    def send_Poll(self, chat_id, text_question = None, options = [], message_id = None, multiple_answers = False, anonymous = True,  quiz = False):
        return self.method(
            'createPoll',
            {
                'allows_multiple_answers': multiple_answers,
                'correct_option_index': None,
                'is_anonymous': anonymous,
                'object_guid': chat_id,
                'options': options if len(options) == 2 else ['This poll was created with "Pyrubi Library"', 'حداقل باید دو گزینه برای نظر سنجی بگزارید !'],
                'question': text_question if text_question != None else 'هیچ متنی تنظیم نشده است !',
                'reply_to_message_id': message_id,
                'rnd': randint(100000000, 999999999),
                'type': 'Quiz' if quiz else 'Regular'
            }
        )

    def Send_Chat_Activity(self, chat_id, action):
        return self.method(
            'sendChatActivity',
            {
                'object_guid': chat_id,
                'activity': action
            }
        )

    def edit_Message(self, chat_id, new_text, message_id):
        metadata = tools.Check_Metadata(new_text)
        data = {
            'object_guid': chat_id,
            'text': metadata[1].strip(),
            'message_id': message_id,
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return self.method('editMessage', data)['message_update']

    def Forward_Message(self, from_chat_id, message_ids, to_chat_id):
        return self.method(
            'forwardMessages',
            {
                'from_object_guid': from_chat_id,
                'message_ids': message_ids,
                'rnd': str(randint(100000,999999999)),
                'to_object_guid': to_chat_id
            }
        )

    def Resend_Message(self, chat_id, file_inline, caption = None, message_id = None):
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': file_inline,
            'object_guid': chat_id,
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id,
            'text': caption
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return self.method(
            'sendMessage',
            data
        )

    def Pin_Message(self, chat_id, message_id):
        return self.method(
            'setPinMessage',
            {
                'object_guid': chat_id,
                'message_id': message_id,
                'action': 'Pin'
            }
        )

    def Unpin_Message(self, chat_id, message_id):
        return self.method(
            'setPinMessage',
            {
                'object_guid': chat_id,
                'message_id': message_id,
                'action': 'Unpin'
            }
        )

    def Search_Message(self, chat_id, text):
        return self.method(
            'searchChatMessages',
            {
                'object_guid': chat_id,
                'search_text': text,
                'type':'Text'
            }
        )['message_ids']

    def SeenMessage(self, chat_id, message_id):
        return self.method('seenChats', {'seen_list': {chat_id: int(message_id)}})

    def DeleteMessage(self, chat_id, message_ids = [], type = 'Global'):
        return self.method(
            'deleteMessages',
            {
                'object_guid': chat_id,
                'message_ids': message_ids,
                'type': type
            }
        )['message_updates']

    def get_Chat_Messages(self, chat_id, middle_message_id):
        return self.method(
            'getMessagesInterval',
            {
                'object_guid':chat_id,
                'middle_message_id':middle_message_id
            }
        )['messages']

    def get_Messages_info(self, chat_id, messages_ids = []):
        return self.method(
            'getMessagesByID',
            {
                'object_guid': chat_id,
                'message_ids': messages_ids
            }
        )['messages']

    def get_link_info(self, url):
        return self.method('getLinkFromAppUrl', {'app_url': url})['link']['open_chat_data']

    def get_Post_info_By_link(self, post_link):
        """This method will be removed in the next update !"""
        return self.method('getLinkFromAppUrl', {'app_url': post_link})['link']['open_chat_data']

    def get_Chats(self, start_id = None):
        return self.method('getChats', {'start_id': start_id})

    def Search_Chats(self, text):
        return self.method('searchGlobalObjects',{'search_text': text})['objects']

    def get_Chat_info(self, chat_id):
        if chat_id.startswith('u'): data = 'User'
        elif chat_id.startswith('g'): data = 'Group'
        elif chat_id.startswith('c'): data = 'Channel'
        elif chat_id.startswith('b'): data = 'Bot'
        elif chat_id.startswith('s'): data = 'Service'
        return self.method(f'get{data}Info',{f'{data.lower()}_guid': chat_id})

    def get_Chat_info_By_Username(self, username):
        return self.method('getObjectByUsername', {'username': username.replace('@', '')})

    def get_last_Chat_Message_id(self, chat_id):
        return self.get_Chat_info(chat_id)['chat']['last_message_id']

    def get_Chat_last_Message(self, chat_id):
        return self.get_Chat_info(chat_id)['chat']['last_message']

    def Delete_Chat_History(self, chat_id):
        return self.method(
            'deleteChatHistory',
            {
                'object_guid': chat_id,
                'last_message_id': self.get_last_Chat_Message_id(chat_id)
            }
        )['chat_update']

    def Delete_User_Chat(self, user_id, last_deleted_message_id):
        return self.method(
            'deleteUserChat',
            {
                'user_guid': user_id,
                'last_deleted_message_id': last_deleted_message_id
            }
        )

    def Add_Group_Members(self, group_id, member_ids = []):
        return self.method(
            'addGroupMembers',
            {
                'group_guid': group_id,
                'member_guids': member_ids
            }
        )

    def Add_Channel_Members(self, channel_id, member_ids = []):
        return self.method(
            'addChannelMembers',
            {
                'channel_guid': channel_id,
                'member_guids': member_ids
            }
        )

    def Ban_Group_Member(self, group_id, member_id):
        return self.method(
            'banGroupMember',
            {
                'group_guid': group_id,
                'member_guid': member_id,
                'action': 'Set'
            }
        )

    def Set_Group_Access(self, group_id, view_members = False, view_admins = False ,send_message = False, add_member = False):
        access = []
        if view_members:
            access.append('ViewMembers')
        if view_admins:
            access.append('ViewAdmins')
        if send_message:
            access.append('SendMessages')
        if add_member:
            access.append('AddMember')
        return self.method(
            'setGroupDefaultAccess',
            {
                'access_list': access,
                'group_guid': group_id
            }
        )

    def get_Group_Members(self, group_id, start_id = None):
        return self.method(
            'getGroupAllMembers',
            {
                'group_guid': group_id,
                'start_id': start_id
            }
        )['in_chat_members']

    def get_Group_Admins(self, group_id, only_ids = True):
        data = self.method('getGroupAdminMembers', {'group_guid': group_id})
        return [i['member_guid'] for i in data['in_chat_members']] if only_ids else data['in_chat_members']

    def get_Group_link(self, group_id):
        return self.method('getGroupLink',{'group_guid': group_id})['join_link']

    def Set_Group_link(self, group_id):
        return self.method('setGroupLink', {'group_guid': group_id})['join_link']

    def Set_Group_Timer(self, group_id, time):
        return self.method(
            'editGroupInfo',
            {
                'group_guid': group_id,
                'slow_mode': int(time),
                'updated_parameters': ['slow_mode']
            }
        )['group']

    def Set_Group_Admin(self, group_id, user_id, access = []):
        return self.method(
            'setGroupAdmin',
            {
                'group_guid': group_id,
                'member_guid': user_id,
                'access_list': access,
                'action': 'SetAdmin',
            }
        )['in_chat_member']

    def Delete_Group_Admin(self, group_id, user_id):
        return self.method(
            'setGroupAdmin',
            {
                'group_guid': group_id,
                'member_guid': user_id,
                'action': 'UnsetAdmin',
            }
        )['in_chat_member']

    def AddGroup(self, group_name, member_ids = []):
        return self.method(
            'addGroup',
            {
                'title': group_name,
                'member_guids': member_ids
            }
        )
    
    def JoinGroup(self, group_link):
        return self.method('joinGroup', {'hash_link': group_link.split('/')[-1]})

    def LeaveGroup(self, group_guid):
        return self.method('leaveGroup', {'group_guid': group_guid})

    def get_Channel_link(self, channel_id):
        return self.method('getChannelLink',{'channel_guid': channel_id})['join_link']

    def AddChannel(self, channel_name, member_ids = [], channel_type = 'Public'):
        return self.method(
            'addChannel',
            {
                'channel_type': channel_type,
                'title': channel_name,
                'member_guids': member_ids
            }
        )

    def JoinChannel(self, channel_id):
        return self.method(
            'joinChannelAction',
            {
                'action': 'Join',
                'channel_guid': channel_id
            }
        )

    def Join_Channel_By_link(self, channel_link):
        return self.method('joinChannelByLink', {'hash_link': channel_link.split('/')[-1]})

    def LeaveChannel(self, channel_id):
        return self.method(
            'joinChannelAction',
            {
                'action': 'Leave',
                'channel_guid': channel_id
            }
        )

    def Block_User(self, user_id):
        return self.method(
            'setBlockUser',
            {
                'user_guid': user_id,
                'action': 'Block'
            }
        )['chat_update']

    def Unblock_User(self, user_id):
        return self.method(
            'setBlockUser',
            {
                'user_guid': user_id,
                'action': 'Unblock'
            }
        )['chat_update']

    def edit_Profile(self, **kwargs):
        if 'username' in list(kwargs.keys()):
            return self.method(
                'updateUsername',
                {
                    'username': kwargs.get('username'),
                    'updated_parameters': ['username']
                }
            )['user']
        else:
            return self.method(
                'updateProfile',
                {
                    'first_name': kwargs.get('first_name'),
                    'last_name': kwargs.get('last_name'),
                    'bio': kwargs.get('bio'),
                    'updated_parameters': list(kwargs.keys())
                }
            )['user']

    def get_Me(self):
        return post(
            json={
                'data': {},
                'method': 'getUser',
                'api_version': '2',
                'auth': self.auth,
                'client': {
                    'app_name': 'Mian',
                    'package': 'm.rubika.ir',
                    'app_version': '1.2.1',
                    'platform': 'PWA'
                }
            },
            url='https://messengerg2c1.iranlms.ir'
        ).json()['data']['user']

    def Request_File(self, file):
        return self.method(
            'requestSendFile',
            {
                'file_name': str(file.split('/')[-1]),
                'mime': file.split('.')[-1],
                'size': Path(file).stat().st_size if not 'http' in file else len(get(file).content)
            }
        )

    def Upload_File(self, file):
        req = self.Request_File(file)
        bytef = open(file,'rb').read() if not 'http' in file else get(file).content
        url = req['upload_url']
        size = str(Path(file).stat().st_size) if not 'http' in file else str(len(get(file).content))
        header = {
            'auth': self.auth,
            'Host': req['upload_url'].replace('https://','').replace('/UploadFile.ashx',''),
            'chunk-size': size,
            'file-id': str(req['id']),
            'access-hash-send': req['access_hash_send'],
            'content-type': 'application/octet-stream',
            'content-length': size,
        }
        while True:
            try:
                if len(bytef) <= 131072:
                    print('YES')
                    header['part-number'], header['total-part'] = '1', '1'
                    j = post(data = bytef ,url = url, headers = header).text
                    return [req, loads(j)['data']['access_hash_rec']]
                else:
                    t = len(bytef) // 131072 + 1
                    for i in range(1, t+1):
                        if i != t:
                            k = (i - 1) * 131072
                            header['chunk-size'], header['part-number'], header['total-part'] = '131072', str(i),str(t)
                            post(data = bytef[k:k + 131072], url = url, headers = header).text
                        else:
                            k = (i - 1) * 131072
                            header['chunk-size'], header['part-number'], header['total-part'] = str(len(bytef[k:])), str(i),str(t)
                            p = post(data = bytef[k:], url = url, headers = header).text
                    return [req, loads(p)['data']['access_hash_rec']]
            except:
                 continue

class bot_async:

    def __init__(self, auth):
        self.auth = auth
        self.crypto = Nany(auth)
        self.ws = Socket(auth).handler_async
        self.method = Socket(auth).method_async
        self.got_messages_update = []
        self.filters = {
            'chat_filter': [],
            'message_filter': []
        }
        del auth

    async def add_filter(self, chat_filter = [], message_filter = []):
        self.filters['chat_filter'] = chat_filter
        self.filters['message_filter'] = message_filter

    def on_message(self, msg):
        async def main():
            async for recv in self.ws():
                if not Messages(recv).Chat_Type() in self.filters['chat_filter'] and not Messages(recv).Message_Type() in self.filters['message_filter']:
                    await msg(recv)
                else:
                    continue
        run(main())

    async def get_chat_update(self, chat_id):
        while True:
            return (await self.method(
                'getMessagesUpdates',
                {
                    'object_guid': chat_id,
                    'state': str(round(time()) - 200)
                }
            ))['updated_messages']

    async def get_chats_update(self):
        while True:
            chats_update = (await self.method('getChatsUpdates', {'state': str(round(time()) - 200)}))['chats'][0]
            if not Messages(chats_update).message_id() in self.got_messages_update:
                if not Messages(chats_update).Chat_Type() in self.filters['chat_filter'] and not Messages(chats_update).Message_Type() in self.filters['message_filter']:
                    self.got_messages_update.append(Messages(chats_update).message_id())
                    return chats_update
                else:
                    continue
            else:
                continue

    async def send_text(self, chat_id, custom_text, message_id = None):
        metadata = tools.Check_Metadata(custom_text)
        data = {
            'object_guid': chat_id,
            'rnd': str(randint(10000000, 999999999)),
            'text': metadata[1].strip(),
            'reply_to_message_id': message_id,
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return await self.method('sendMessage', data)

    async def reply(self, data, custom_text):
        msg = Messages(data)
        return await self.send_text(
            msg.Chat_id(),
            custom_text,
            msg.Message_id()
        )

    async def send_image(self, chat_id, file, caption = None, message_id = None, thumbnail = None):
        req = await self.Upload_File(file)
        size = tools.get_image_Size(open(file,'rb').read() if not 'http' in file else get(file).content)
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': {
                'dc_id': req[0]['dc_id'],
                'file_id': req[0]['id'],
                'type':'Image',
                'file_name': tools.get_File_Name(file),
                'size': tools.get_File_Size(file),
                'mime': 'png',
                'access_hash_rec': req[1],
                'width': size[0],
                'height': size[1],
                'thumb_inline': tools.get_thumbnail(open(file,'rb').read() if thumbnail == None and not 'http' in file else open(thumbnail,'rb').read() if not 'http' in file else get(file).content).decode('utf-8')
            },
            'object_guid': chat_id,
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id,
            'text': metadata[1]
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return await self.method('sendMessage', data)

    async def send_video(self, chat_id, file, caption = None, message_id = None):
        req = await self.Upload_File(file)
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': {
                'file_id': req[0]['id'],
                'mime': 'mp4',
                'dc_id': req[0]['dc_id'],
                'access_hash_rec': req[1],
                'file_name': tools.get_File_Name(file),
                'thumb_inline': '/9j/4AAQSkZJRgABAQAAAQABAAD/4gIoSUNDX1BST0ZJTEUAAQEAAAIYAAAAAAIQAABtbnRyUkdC\nIFhZWiAAAAAAAAAAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAA\nAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlk\nZXNjAAAA8AAAAHRyWFlaAAABZAAAABRnWFlaAAABeAAAABRiWFlaAAABjAAAABRyVFJDAAABoAAA\nAChnVFJDAAABoAAAAChiVFJDAAABoAAAACh3dHB0AAAByAAAABRjcHJ0AAAB3AAAADxtbHVjAAAA\nAAAAAAEAAAAMZW5VUwAAAFgAAAAcAHMAUgBHAEIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFhZWiAA\nAAAAAABvogAAOPUAAAOQWFlaIAAAAAAAAGKZAAC3hQAAGNpYWVogAAAAAAAAJKAAAA+EAAC2z3Bh\ncmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABYWVogAAAAAAAA9tYAAQAAAADT\nLW1sdWMAAAAAAAAAAQAAAAxlblVTAAAAIAAAABwARwBvAG8AZwBsAGUAIABJAG4AYwAuACAAMgAw\nADEANv/bAEMADQkKCwoIDQsKCw4ODQ8TIBUTEhITJxweFyAuKTEwLiktLDM6Sj4zNkY3LC1AV0FG\nTE5SU1IyPlphWlBgSlFST//bAEMBDg4OExETJhUVJk81LTVPT09PT09PT09PT09PT09PT09PT09P\nT09PT09PT09PT09PT09PT09PT09PT09PT09PT//AABEIAGQAOAMBIgACEQEDEQH/xAAWAAEBAQAA\nAAAAAAAAAAAAAAAAAQf/xAAXEAEBAQEAAAAAAAAAAAAAAAAAAREx/8QAFQEBAQAAAAAAAAAAAAAA\nAAAAAAH/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwDMFRRAwACiAACiwAAEQqKi\nqtEAU0QRQADqKBgCCKixVDgYIAIFCiqgAKAiBQqiACixFgACIFCqIAKLAAARCFBRABX/2Q==\n',
                'width': 240,
                'height': 240,
                'time': tools.get_Video_Duration(file),
                'size': tools.get_File_Size(file),
                'type': 'Video'
            },
            'object_guid': chat_id,
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id,
            'text': metadata[1]
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return await self.method('sendMessage', data)

    async def send_gif(self, chat_id, file, caption = None, message_id = None):
        req = await self.Upload_File(file)
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': {
                'file_id': req[0]['id'],
                'mime': 'mp4',
                'dc_id': req[0]['dc_id'],
                'access_hash_rec': req[1],
                'file_name': tools.get_File_Name(file),
                'width': 240,
                'height': 240,
                'time': tools.get_Video_Duration(file),
                'size': tools.get_File_Size(file),
                'type': 'Gif',
                'is_round': False,
            },
            'object_guid': chat_id,
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id,
            'text': metadata[1]
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return await self.method('sendMessage',data)

    async def send_voice(self, chat_id, file, caption = None, message_id = None, time = None):
        req = await self.Upload_File(file)
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': {
                'dc_id': req[0]['dc_id'],
                'file_id': req[0]['id'],
                'type': 'Voice',
                'file_name': tools.get_File_Name(file),
                'size': tools.get_File_Size(file),
                'time': int(tools.get_Voice_Duration(open(file,'rb').read()) if time == None else time) * 1000 if not 'http' in file else 1,
                'mime': 'ogg',
                'access_hash_rec': req[1],
            },
            'object_guid': chat_id,
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id,
            'text': metadata[1]
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return await self.method('sendMessage', data)

    async def send_music(self, chat_id, file, caption = None, message_id = None):
        req = await self.Upload_File(file)
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': {
                'file_id': req[0]['id'],
                'mime': 'mp3',
                'dc_id': req[0]['dc_id'],
                'access_hash_rec': req[1],
                'file_name': tools.get_File_Name(file),
                'width': 0,
                'height': 0,
                'time': tools.get_Voice_Duration(open(file,'rb').read()) if not 'http' in file else 1,
                'size': tools.get_File_Size(file),
                'type': 'Music',
                'music_performer': tools.get_Music_Artist(file) if not 'http' in file else 'Pyrubi Library',
                'is_round': False
            },
            'is_mute': False,
            'object_guid': chat_id,
            'text': metadata[1],
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return await self.method('sendMessage', data)

    async def send_file(self, chat_id, file, caption = None, message_id = None):
        req = await self.Upload_File(file)
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': {
                'dc_id': req[0]['dc_id'],
                'file_id': req[0]['id'],
                'type': 'File',
                'file_name': file if not 'http' in file else f'pyrubi {randint(1, 100)}.{tools.get_mime_from_url(file)}',
                'size': tools.get_File_Size(file),
                'mime': file.split('.')[-1] if not 'http' in file else tools.get_mime_from_url(file),
                'access_hash_rec': req[1]
            },
            'object_guid': chat_id,
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id,
            'text': metadata[1]
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return await self.method('sendMessage', data)

    async def send_sticker(self, chat_id, message_id = None):
        stickers = choice(await self.method('getMyStickerSets',{})['sticker_sets'])
        return await self.method(
            'sendMessage',
            {
                'sticker': choice(stickers['top_stickers']),
                'object_guid': chat_id,
                'rnd': str(randint(100000,999999999)),
                'reply_to_message_id': message_id
            }
        )

    async def send_poll(self, chat_id, text_question = None, options = [], message_id = None, multiple_answers = False, anonymous = True,  quiz = False):
        return await self.method(
            'createPoll',
            {
                'allows_multiple_answers': multiple_answers,
                'correct_option_index': None,
                'is_anonymous': anonymous,
                'object_guid': chat_id,
                'options': options if len(options) == 2 else ['This poll was created with "Pyrubi Library"', 'حداقل باید دو گزینه برای نظر سنجی بگزارید !'],
                'question': text_question if text_question != None else 'هیچ متنی تنظیم نشده است !',
                'reply_to_message_id': message_id,
                'rnd': randint(100000000, 999999999),
                'type': 'Quiz' if quiz else 'Regular'
            }
        )

    async def send_chat_activity(self, chat_id, action):
        return await self.method(
            'sendChatActivity',
            {
                'object_guid': chat_id,
                'activity': action
            }
        )

    async def edit_message(self, chat_id, new_text, message_id):
        metadata = tools.Check_Metadata(new_text)
        data = {
            'object_guid': chat_id,
            'text': metadata[1].strip(),
            'message_id': message_id,
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return (await self.method('editMessage', data))['message_update']

    async def forward_message(self, from_chat_id, message_ids, to_chat_id):
        return (await self.method(
            'forwardMessages',
            {
                'from_object_guid': from_chat_id,
                'message_ids': message_ids,
                'rnd': str(randint(100000,999999999)),
                'to_object_guid': to_chat_id
            }
        ))

    async def resend_message(self, chat_id, file_inline, caption = None, message_id = None):
        metadata = tools.Check_Metadata(caption)
        data = {
            'file_inline': file_inline,
            'object_guid': chat_id,
            'rnd': str(randint(100000,999999999)),
            'reply_to_message_id': message_id,
            'text': caption
        }
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return await self.method(
            'sendMessage',
            data
        )

    async def pin_message(self, chat_id, message_id):
        return (await self.method(
            'setPinMessage',
            {
                'object_guid': chat_id,
                'message_id': message_id,
                'action': 'Pin'
            }
        ))

    async def unpin_message(self, chat_id, message_id):
        return await self.method(
            'setPinMessage',
            {
                'object_guid': chat_id,
                'message_id': message_id,
                'action': 'Unpin'
            }
        )

    async def search_message(self, chat_id, text):
        return (await self.method(
            'searchChatMessages',
            {
                'object_guid': chat_id,
                'search_text': text,
                'type':'Text'
            }
        ))['message_ids']

    async def seen_message(self, chat_id, message_id):
        return await self.method('seenChats', {'seen_list': {chat_id: int(message_id)}})

    async def delete_message(self, chat_id, message_ids = [], type = 'Global'):
        return (await self.method(
            'deleteMessages',
            {
                'object_guid': chat_id,
                'message_ids': message_ids,
                'type': type
            }
        ))['message_updates']

    async def get_chat_messages(self, chat_id, middle_message_id):
        return (await self.method(
            'getMessagesInterval',
            {
                'object_guid':chat_id,
                'middle_message_id':middle_message_id
            }
        ))['messages']

    async def get_messages_info(self, chat_id, messages_ids = []):
        return (await self.method(
            'getMessagesByID',
            {
                'object_guid': chat_id,
                'message_ids': messages_ids
            }
        ))['messages']

    async def get_link_info(self, url):
        return (await self.method('getLinkFromAppUrl', {'app_url': url}))['link']['open_chat_data']

    async def get_post_info_by_link(self, post_link):
        """This method will be removed in the next update !"""
        return await self.method('getLinkFromAppUrl', {'app_url': post_link})

    async def get_chats(self, start_id = None):
        return await self.method('getChats', {'start_id': start_id})

    async def search_chats(self, text):
        return (await self.method('searchGlobalObjects',{'search_text': text}))['objects']

    async def get_chat_info(self, chat_id):
        if chat_id.startswith('u'): data = 'User'
        elif chat_id.startswith('g'): data = 'Group'
        elif chat_id.startswith('c'): data = 'Channel'
        elif chat_id.startswith('b'): data = 'Bot'
        elif chat_id.startswith('s'): data = 'Service'
        return await self.method(f'get{data}Info',{f'{data.lower()}_guid': chat_id})

    async def get_chat_info_by_username(self, username):
        return await self.method('getObjectByUsername', {'username': username.replace('@', '')})

    async def get_last_Chat_Message_id(self, chat_id):
        return (await self.get_chat_info(chat_id))['chat']['last_message_id']

    async def get_chat_last_message(self, chat_id):
        return (await self.get_chat_info(chat_id))['chat']['last_message']

    async def delete_chat_history(self, chat_id):
        return (await self.method(
            'deleteChatHistory',
            {
                'object_guid': chat_id,
                'last_message_id': await self.get_last_Chat_Message_id(chat_id)
            }
        ))['chat_update']

    async def delete_user_chat(self, user_id, last_deleted_message_id):
        return await self.method(
            'deleteUserChat',
            {
                'user_guid': user_id,
                'last_deleted_message_id': last_deleted_message_id
            }
        )

    async def add_group_members(self, group_id, member_ids = []):
        return await self.method(
            'addGroupMembers',
            {
                'group_guid': group_id,
                'member_guids': member_ids
            }
        )

    async def add_channel_members(self, channel_id, member_ids = []):
        return await self.method(
            'addChannelMembers',
            {
                'channel_guid': channel_id,
                'member_guids': member_ids
            }
        )

    async def ban_group_member(self, group_id, member_id):
        return await self.method(
            'banGroupMember',
            {
                'group_guid': group_id,
                'member_guid': member_id,
                'action': 'Set'
            }
        )

    async def set_group_access(self, group_id, view_members = False, view_admins = False ,send_message = False, add_member = False):
        access = []
        if view_members:
            access.append('ViewMembers')
        if view_admins:
            access.append('ViewAdmins')
        if send_message:
            access.append('SendMessages')
        if add_member:
            access.append('AddMember')
        return await self.method(
            'setGroupDefaultAccess',
            {
                'access_list': access,
                'group_guid': group_id
            }
        )

    async def get_group_members(self, group_id, start_id = None):
        return (await self.method(
            'getGroupAllMembers',
            {
                'group_guid': group_id,
                'start_id': start_id.replace('@', '') if start_id != None else start_id
            }
        ))['in_chat_members']

    async def get_group_admins(self, group_id, only_ids = True):
        data = await self.method('getGroupAdminMembers', {'group_guid': group_id})
        return [i['member_guid'] for i in data['in_chat_members']] if only_ids else data['in_chat_members']

    async def get_group_link(self, group_id):
        return (await self.method('getGroupLink',{'group_guid': group_id}))['join_link']

    async def set_group_link(self, group_id):
        return (await self.method('setGroupLink', {'group_guid': group_id}))['join_link']

    async def set_group_timer(self, group_id, time):
        return (await self.method(
            'editGroupInfo',
            {
                'group_guid': group_id,
                'slow_mode': int(time),
                'updated_parameters': ['slow_mode']
            }
        ))['group']

    async def set_group_admin(self, group_id, user_id, access = []):
        return (await self.method(
            'setGroupAdmin',
            {
                'group_guid': group_id,
                'member_guid': user_id,
                'access_list': access,
                'action': 'SetAdmin',
            }
        ))['in_chat_member']

    async def delete_group_admin(self, group_id, user_id):
        return (await self.method(
            'setGroupAdmin',
            {
                'group_guid': group_id,
                'member_guid': user_id,
                'action': 'UnsetAdmin',
            }
        ))['in_chat_member']

    async def create_group(self, group_name, member_ids = []):
        return await self.method(
            'addGroup',
            {
                'title': group_name,
                'member_guids': member_ids
            }
        )
    
    async def join_group(self, group_link):
        return await self.method('joinGroup', {'hash_link': group_link.split('/')[-1]})

    async def leave_group(self, group_guid):
        return await self.method('leaveGroup', {'group_guid': group_guid})

    async def get_channel_link(self, channel_id):
        return (await self.method('getChannelLink', {'channel_guid': channel_id}))['join_link']

    async def create_channel(self, channel_name, member_ids = [], channel_type = 'Public'):
        self.method(
            'addChannel',
            {
                'channel_type': channel_type,
                'title': channel_name,
                'member_guids': member_ids
            }
        )

    async def join_channel(self, channel_id):
        return await self.method(
            'joinChannelAction',
            {
                'action': 'Join',
                'channel_guid': channel_id
            }
        )

    async def join_channel_by_link(self, channel_link):
        return await self.method('joinChannelByLink', {'hash_link': channel_link.split('/')[-1]})

    async def leave_channel(self, channel_id):
        return await self.method(
            'joinChannelAction',
            {
                'action': 'Leave',
                'channel_guid': channel_id
            }
        )

    async def block_user(self, user_id):
        return (await self.method(
            'setBlockUser',
            {
                'user_guid': user_id,
                'action': 'Block'
            }
        ))['chat_update']

    async def unblock_user(self, user_id):
        return await self.method(
            'setBlockUser',
            {
                'user_guid': user_id,
                'action': 'Unblock'
            }
        )['chat_update']

    async def edit_profile(self, **kwargs):
        if 'username' in list(kwargs.keys()):
            return (await self.method(
                'updateUsername',
                {
                    'username': kwargs.get('username'),
                    'updated_parameters': ['username']
                }
            ))['user']
        else:
            return (await self.method(
                'updateProfile',
                {
                    'first_name': kwargs.get('first_name'),
                    'last_name': kwargs.get('last_name'),
                    'bio': kwargs.get('bio'),
                    'updated_parameters': list(kwargs.keys())
                }
            ))['user']

    async def get_me(self):
        async with cs() as result:
            data = {
                'data': {},
                'method': 'getUser',
                'api_version': '2',
                'auth': self.auth,
                'client': {
                    'app_name': 'Mian',
                    'package': 'm.rubika.ir',
                    'app_version': '1.2.1',
                    'platform': 'PWA'
                }
            }
            async with result.post('https://messengerg2c1.iranlms.ir', json = data) as result:
                return (await result.json())['data']['user']

    async def request_file(self, file):
        return await self.method(
            'requestSendFile',
            {
                'file_name': str(file.split('/')[-1]),
                'mime': file.split('.')[-1],
                'size': Path(file).stat().st_size if not 'http' in file else len(get(file).content)
            }
        )

    async def Upload_File(self, file):
        req = await self.request_file(file)
        bytef = open(file,'rb').read() if not 'http' in file else get(file).content
        url = req['upload_url']
        size = str(Path(file).stat().st_size) if not 'http' in file else str(len(get(file).content))
        header = {
            'auth': self.auth,
            'Host': req['upload_url'].replace('https://','').replace('/UploadFile.ashx',''),
            'chunk-size': size,
            'file-id': str(req['id']),
            'access-hash-send': req['access_hash_send'],
            'content-type': 'application/octet-stream',
            'content-length': size,
        }
        while True:
            try:
                if len(bytef) <= 131072:
                    print('YES')
                    header['part-number'], header['total-part'] = '1', '1'
                    j = post(data = bytef ,url = url, headers = header).text
                    return [req, loads(j)['data']['access_hash_rec']]
                else:
                    t = len(bytef) // 131072 + 1
                    for i in range(1, t+1):
                        if i != t:
                            k = (i - 1) * 131072
                            header['chunk-size'], header['part-number'], header['total-part'] = '131072', str(i),str(t)
                            post(data = bytef[k:k + 131072], url = url, headers = header).text
                        else:
                            k = (i - 1) * 131072
                            header['chunk-size'], header['part-number'], header['total-part'] = str(len(bytef[k:])), str(i),str(t)
                            p = post(data = bytef[k:], url = url, headers = header).text
                    return [req, loads(p)['data']['access_hash_rec']]
            except:
                 continue
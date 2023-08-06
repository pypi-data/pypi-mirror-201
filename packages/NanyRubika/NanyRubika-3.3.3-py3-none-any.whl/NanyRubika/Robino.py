#Created By Nanymous_Team
from requests import get,post
from NanyRubika.encryption import encryption
from random import randint, choice
from NanyRubika.Copyright import *
from NanyRubika.server import Server
from pathlib import Path
from json import loads,dumps


class Robino:
	def __init__(self, auth):
		self.auth = auth
		
	def _getUrl():
		return choice(Server.rubino)
		
		
	def _request(self,inData,method):
		data = {"api_version": "0","auth": self.auth,"client": {"app_name": "Main","app_version": "3.0.2","lang_code": "fa","package": "app.rbmain.a","platform": "Android"},"data": inData,"method": method}
		while True:
			try:
				return post(Robino._getUrl(),json=data).json()
			except:
				continue
	
	
	
	def Follow(self,Follow_id,Profile_id=None):
		inData = {"f_type": "Follow","followee_id": Follow_id,"profile_id": Profile_id}
		method = 'requestFollow'
		while True:
			try:
				return self._request(inData,method)
			except:continue
		
		
	def getPostByShareLink(self,link,Profile_id=None):
		if link.startswith("post/"):
			print(link)
			god = link.split("post/")
			print(link)
			inData = {"share_string":god,"profile_id":Profile_id}
		else:
			inData = {"share_string":link,"profile_id":Profile_id}
		method = "getPostByShareLink"
		while True:
			try:
				return self._request(inData,method).get('data')
			except:continue
			
			
	def addPostViewCount(self,Post_id,Post_Profile_id):
		inData = {"post_id":Post_id,"post_profile_id":Post_Profile_id}
		method = "addPostViewCount"
		while True:
			try:
				return self._request(inData,method)
			except:continue
	
	def getProfileStories(self,Profile_id=None):
		inData = {"limit": 100, "profile_id": Profile_id}
		method = "getProfileStories"
		while True:
			try:
				return self._request(inData,method)
			except:continue
	
	def requestUploadFile(self,file,size=None, Type="Picture",prof=None):
		inData = {
			"file_name": file.split("/")[-1],
			"file_size": size or Path(file).stat().st_size, 
			"file_type": Type,
			"profile_id": prof}
		method = "requestUploadFile"
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
	@staticmethod
	def _getThumbInline(image_bytes:bytes):
		import io, base64, PIL.Image
		im = PIL.Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		if height > width:
			new_height = 40
			new_width  = round(new_height * width / height)
		else:
			new_width  = 40
			new_height = round(new_width * height / width)
		im = im.resize((new_width, new_height), PIL.Image.ANTIALIAS)
		changed_image = io.BytesIO()
		im.save(changed_image, format='PNG')
		changed_image = changed_image.getvalue()
		return base64.b64encode(changed_image)

	@staticmethod
	def _getImageSize(image_bytes:bytes):
		import io, PIL.Image
		im = PIL.Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		return [width , height]
	
	def upload(self,file,Type):
		if not "http" in file:
			REQUEST = self.requestUploadFile(file)["data"]
			bytef = open(file,"rb").read()
			file_id = REQUEST["file_id"]
			hash_send = REQUEST["hash_file_request"]
			url = REQUEST["server_url"]
			header = {
				'auth':self.auth,
				'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
				'chunk-size':str(Path(file).stat().st_size),
				'file-id':str(file_id),
				'hash-file-request':hash_send,
				"content-type": "application/octet-stream",
				"content-length": str(Path(file).stat().st_size),
				"accept-encoding": "gzip",
				"user-agent": "okhttp/3.12.1",
				"part-number":"1",
				"total-part":"1"}
			j = post(data=bytef,url=url,headers=header).text
			j = loads(j)['data']['hash_file_receive']


			return [REQUEST, j]
		else:
			REQUEST = {
			"file_name": file.split("/")[-1],
			"file_size": size or Path(file).stat().st_size, 
			"file_type": Type,
			"profile_id": ""}
			method = "requestUploadFile"
			while True:
				try:
					return self._request(inData,method)
				except:continue
				bytef = get(file).content
				file_id = REQUEST["file_id"]
				hash_send = REQUEST["hash_file_request"]
				url = REQUEST["server_url"]
				header = {
				'auth':self.auth,
				'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
				'chunk-size':str(Path(file).stat().st_size),
				'file-id':str(file_id),
				'hash-file-request':hash_send,
				"content-type": "application/octet-stream",
				"content-length": str(Path(file).stat().st_size),
				"accept-encoding": "gzip",
				"user-agent": "okhttp/3.12.1",
				"part-number":"1",
				"total-part":"1"}
				j = post(data=bytef,url=url,headers=header).text
				j = loads(j)['data']['hash_file_receive']
				return [REQUEST, j]
	
	
	def getStoryIds(self,target_profile_id,profile_id=None):
		inData = {"profile_id":profile_id,"target_profile_id":target_profile_id}
		method = 'getStoryIds'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
	def getComments(self,Post_id,Post_Profile_id,Profile_id=None):
		inData = {"equal": False, "limit": 100, "sort": "FromMax", "post_id": Post_id, "profile_id": Profile_id, "post_profile_id": Post_Profile_id}
		method = "getComments"
		while True:
			try:
				return self._request(inData,method)
			except:continue
	
	def updateProfile(self,Profile_id=None):
		inData = {"profile_id":Profile_id,"profile_status":"Public"}
		method = 'updateProfile'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
	def addPost(self,file,caption=None,is_multi_file=None,post_type="Picture",prof=None):
		urespone = self.upload(file,post_type)
		hashFile = urespone[1]
		fileID = urespone[0]["file_id"]
		thumbnailID = urespone[0]["file_id"]
		thumbnailHash = urespone[1]
		inData = {"caption": caption, "file_id": fileID, "hash_file_receive": hashFile, "height": 800, "width": 800, "is_multi_file": is_multi_file, "post_type": post_type, "rnd": randint(100000, 999999999), "thumbnail_file_id": thumbnailID, "thumbnail_hash_file_receive": thumbnailHash, "profile_id": prof}
		method = "addPost"
		while True:
			try:
				return self._request(inData,method)
			except:continue
	def getRecentFollowingPosts(self,Profile_id=None):
		inData = {"equal":False,"limit":30,"sort":"FromMax","profile_id":Profile_id}
		method = 'getRecentFollowingPosts'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def getProfileList(self):
		inData = {"equal":False,"limit":10,"sort":"FromMax"}
		method = 'getProfileList'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def getMyProfileInfo(self,Profile_id=None):
		inData = {"profile_id":Profile_id}
		method = 'getMyProfileInfo'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def Like(self,Post_id,Post_Profile_id,Profile_id=None):
		inData ={"action_type":"Like","post_id":Post_id,"post_profile_id":Post_Profile_id,"profile_id":Profile_id}
		method = 'likePostAction'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
	def getShareLink(self,Post_id,Post_Profile_id,prof=None):
		inData = {"post_id":Post_id,"post_profile_id":Post_Profile_id,"profile_id":prof}
		method = 'getShareLink'
		while True:
			try:
				return self._request(inData,method)
			except:continue
	
	def isExistUsername(self,username):
		if username.startswith("@"):
			username = username.split("@")[1]
			inData = {"username": username}
		else:
			inData = {"username": username}
		method = "isExistUsername"
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
	def addViewStory(self,Story_Profile_id,ids,Profile_id=None):
		indata = {"profile_id":Profile_id,"story_ids":[ids],"story_profile_id":Story_Profile_id}
		method = 'addViewStory'
		while True:
			try:
				return self._request(indata,method)
			except:continue
			
			
	def createPage(self,Name,username,Bio=None):
		inData = {"bio": Bio,"name": Name,"username": username}
		method = 'createPage'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def Comment(self,Message,Post_id,Post_Profile_id,Profile_id=None):
		inData = {"content": Message,"post_id": Post_id,"post_profile_id": Post_Profile_id,"rnd":f"{randint(100000,999999999)}" ,"profile_id":Profile_id}
		method = 'addComment'
		while True:
			try:
				return self._request(inData,method)
			except:continue
		
		
	def UnLike(self,Post_id,Post_Profile_id,Profile_id=None):
		inData = {"action_type":"Unlike","post_id":Post_id,"post_profile_id":Post_Profile_id,"profile_id":Profile_id}
		method ='likePostAction'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def SavePost(self,Post_id,Post_Profile_id,Profile_id=None):
		inData = {"action_type":"Bookmark","post_id":Post_id,"post_profile_id":Post_Profile_id,"profile_id":Profile_id}
		method ='postBookmarkAction'
		while True:
			try:
				return self._request(inData,method)
			except:continue


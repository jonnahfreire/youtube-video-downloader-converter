__author__ = 'Jonnas Freire'
__version__ = '1.1.4'
__license__ = 'MIT'

from tkinter import Tk, messagebox, filedialog
import subprocess, os, sys

from moviepy.video.io.VideoFileClip import VideoFileClip
import psutil
from pytube import YouTube
import eel
import requests

class Search:

	def __init__(self, query:str) -> None:
		self.id_ref = "videoRenderer"
		self.thumbnail_ref = '"url":"https://i'
		self.title_ref = '"title":{"runs":[{"text":"'
		self.duration_ref = '"}},"simpleText":"'

		url = f"https://www.youtube.com/results?search_query={query}"

		"Makes a request to get the data"
		response = requests.get(url)
		self.lines = response.content.decode('utf-8')

	def get_video_info(self) -> list:
	    video_info = []
	    id_list = []
	    scape = ['\\u', '\"', '\\', '|', '?','.',':','u0026']

	    for __ in range(self.lines.count(self.id_ref)):
	    	"GET VIDEO ID"
	    	id_start_pos = str(self.lines).find(self.id_ref)+27
	    	id_end_pos = str(self.lines).find('"', id_start_pos)
	    	video_id = str(self.lines[id_start_pos:id_end_pos])

	    	"Verify if video_id length is equal to 11 and if there's not repeated video_id"
	    	if video_id not in id_list and len(video_id) == 11:
	    		id_list.append(video_id)
		    	url = f'https://www.youtube.com/watch?v={video_id}'

		    	"GET VIDEO THUMBNAIL"
		    	thumb_start_pos = str(self.lines).find(self.thumbnail_ref, id_end_pos)+15
		    	thumb_end_pos = str(self.lines).find("?", thumb_start_pos)
		    	thumbnail = 'https://'+str(self.lines[thumb_start_pos: thumb_end_pos])

		    	"GET VIDEO TITLE"
		    	title_start_pos = str(self.lines).find(self.title_ref, thumb_end_pos)+26
		    	title_end_pos = str(self.lines).find("}", title_start_pos)-1
		    	title = str(self.lines[title_start_pos: title_end_pos])

		    	"GET VIDEO DURATION"
		    	duration_start_pos = str(self.lines).find(self.duration_ref, title_end_pos)+18
		    	duration_end_pos = str(self.lines).find("}", duration_start_pos)-1
		    	
		    	duration = str(self.lines[duration_start_pos: duration_end_pos])
		    	
		    	"Verify if duration contains hour, minutes and seconds"
		    	if len(duration.split(':')) == 3:
		    		duration_hour = duration.split(':')[0]
		    		duration_min = duration.split(':')[1]
		    		duration_sec = duration.split(':')[2]
		    		duration = duration_hour +':'+duration_min+':'+duration_sec
					
		    	else:
		    		duration_min = duration.split(':')[0]
		    		duration_sec = str(int(duration.split(':')[1]))
		    		
		    		if int(duration_sec) < 10 and int(duration_sec) > 1:
		    			duration_sec = str(int(duration.split(':')[1])-1)
		    			duration_sec = '0'+duration_sec
		    		
		    		duration = duration_min+':'+duration_sec

		    	lines_start_pos = str(self.lines).find(self.id_ref, duration_end_pos)+27
		    	lines_end_pos = str(self.lines).find('"', lines_start_pos)
		    	self.lines = str(self.lines[lines_end_pos:])

		    	"Scapes the characters that may break the execution"
		    	for char in title:
		    		e_comercial = title.find('u0026')
		    		if e_comercial > 0:
		    			title = title.replace(str(title[int(e_comercial):int(e_comercial)+6]), '& ')
		    		
		    		if char in scape:
		    			title = title.replace(char, '')

		    	video_data = {
		    		'title':title,
		    		'thumbnail':thumbnail,
		    		'url':url,
		    		'duration':duration
		    	}

		    	video_info.append(video_data)

	    return video_info



eel.init('static')

def audio_downloader(link:str, title:str, file_path:str) -> None:

	"Sets a temporary path to save the downloaded file"
	temp_path = os.path.join(os.getcwd(), 'temp')
	file_name = ''

	try:
		yt = YouTube(link)
		"Selects the media streams"
		stream = yt.streams.filter(progressive=True, file_extension='mp4')

		"Get the highest resolution"
		data = stream.get_highest_resolution()

		"Clear the characters that may break the program execution"
		scape = ['\\u', '\"', '\\', '|', ':', ',', '/', '.']
		
		for char in title:
			if char in scape:
				file_name = str(title).replace(char,'')
		

		"Downloads the file"
		data.download(temp_path, filename=file_name)

		"selects the file.mp4"
		video = VideoFileClip(os.path.join(temp_path, f"{file_name}.mp4"))
		if file_path:
			"Converts the file.mp4 in file.mp3"
			video.audio.write_audiofile(os.path.join(file_path, f"{file_name}.mp3"))
		
		"Kill the process of convertion - binary: ffmpeg-win32-v4.2.2.exe"
		for proc in psutil.process_iter():
		    if 'ffmpeg' in proc.name():
		    	proc.kill()

		"Verify the OS platform"
		if sys.platform == 'win32':
			subprocess.call(["del", f'{temp_path}\\{file_name}.mp4'], shell=True)
		else:
			subprocess.call(["rm", f'{temp_path}\\{file_name}.mp4'], shell=True)
		
		"Calls the front-end function to show download finished process"
		eel.download_concluded(title)

	except:
		"If ocurrs an exception in convertion, deletes the downloaded file"
		if sys.platform == 'win32':
			subprocess.call(["del", f'{temp_path}\\{file_name}.mp4'], shell=True)
		else:
			subprocess.call(["rm", f'{temp_path}\\{file_name}.mp4'], shell=True)

		eel.msg_error(title)



def vd_downloader(link:str, title:str) -> None:

	try:
		"Sets the standard path"
		path = os.path.join(os.environ['USERPROFILE'], 'Desktop')

		yt = YouTube(link)

		"Selects the stream with the highest resolution to download"
		stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()

		stream.download(path, filename=title)

		"Calls the front-end function to show download finished process"
		eel.download_concluded(title)

	except:
		eel.msg_error(title)


@eel.expose
def search(query: str ='') -> list:

	"Makes a search with the query specified"
	video_info = Search(query).get_video_info()
	
	return video_info
	

@eel.expose
def verify(link:str, title:str, file_format:str) -> None:

	if file_format == 'mp4':
		eel.spawn(vd_downloader(link, title))

	elif file_format == 'mp3':
		path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
		eel.spawn(audio_downloader(link, title, path))



@eel.expose
def open_file_path() -> str:

	"Open a file dialog to select a folder to save the file to"
	root = Tk()
	root.iconbitmap('static/src/images/downloader.ico')
	root.withdraw()
	file = filedialog.askdirectory()
	
	root.destroy()
	return file



@eel.expose
def open_file_name() -> str:

	"Open a file dialog to select a file.mp4 to convert"
	root = Tk()
	root.iconbitmap('static/src/images/downloader.ico')
	root.withdraw()
	file_name = filedialog.askopenfilenames(
		title='Selecione um arquivo',
		filetypes=(
			('mp4 files','*.mp4'),
			('all files','*.*')
		))

	if file_name != '' or len(file_name) > 0:
		file_name = file_name[0]
	
	if '.mp4' in file_name:
		root.destroy()
		return file_name
	else:
		messagebox.showinfo('Erro', 'Por favor selecione um arquivo no formato MP4')
		root.destroy()



def converter(path:str, media_file:str, save_file_to_path:str) -> None:
	
	def msg_sucess_with_path(save_file_to_path:str, mp3_file:str) -> None:
		root = Tk()
		root.iconbitmap('static/src/images/downloader.ico')
		root.withdraw()
		messagebox.showinfo('Sucesso', f'Arquivo convertido com sucesso\nsalvo em: {save_file_to_path}/{mp3_file}.mp3')
		root.destroy()

	def msg_sucess_with_absolute_path(path:str, mp3_file:str) -> None:
		root = Tk()
		root.iconbitmap('static/src/images/downloader.ico')
		root.withdraw()
		messagebox.showinfo('Sucesso', f'Arquivo convertido com sucesso\nsalvo em: {path}{mp3_file}.mp3')
		root.destroy()

	def msg_error() -> None:
		root = Tk()
		root.iconbitmap('static/src/images/downloader.ico')
		root.withdraw()
		messagebox.showinfo('Erro', 'Desculpe, não foi possível converter o arquivo')
		root.destroy()

	try:
		video = VideoFileClip(media_file) 
		mp3_file = media_file[media_file.rindex('/')+1:media_file.rindex('.mp4')]
		
		if save_file_to_path != '':
			video.audio.write_audiofile(os.path.join(save_file_to_path, f"{mp3_file}.mp3"))
			eel.cv_loader_stop()
			msg_sucess_with_path(save_file_to_path, mp3_file)
			
		else:
			video.audio.write_audiofile(os.path.join(path, f"{mp3_file}.mp3"))
			eel.cv_loader_stop()
			msg_sucess_with_absolute_path(path, mp3_file)
			

		"Kill ffmpeg process"
		for proc in psutil.process_iter():
		    if 'ffmpeg' in proc.name():
		    	proc.kill()
	except:
		msg_error()


@eel.expose
def converter_params(path:str, media_file:str, save_file_to_path:str) -> None:
	eel.spawn(converter(path, media_file, save_file_to_path))


eel.start("index.html", size=(800, 650), position=(500,100))

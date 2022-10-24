import requests
from bs4 import BeautifulSoup
import re
import cv2
import os
import numpy as np
from math import sqrt
import tensorflow as tf
from tensorflow.keras.models import load_model
import imghdr

# Script Created by peterdallhansen 2022 github.com/peterdallhansen
# Uses the dominant colors of the image
# To determine the hair color

#pip install opencv-python

def start():


	classurl = [
		
		"https://www.lectio.dk/lectio/31/login.aspx?prevurl=subnav%2fmembers.aspx%3fklasseid%3d45857758048%26showstudents%3d1",
		"https://www.lectio.dk/lectio/31/login.aspx?prevurl=subnav%2fmembers.aspx%3fklasseid%3d45857770414%26showstudents%3d1",
		"https://www.lectio.dk/lectio/31/login.aspx?prevurl=subnav%2fmembers.aspx%3fklasseid%3d45857778621%26showstudents%3d1",
		"https://www.lectio.dk/lectio/31/login.aspx?prevurl=subnav%2fmembers.aspx%3fklasseid%3d45857818535%26showstudents%3d1",
		"https://www.lectio.dk/lectio/31/login.aspx?prevurl=subnav%2fmembers.aspx%3fklasseid%3d45857861596%26showstudents%3d1"


		]
	


	COLORS = (
		(110, 44, 0 ),
		(248, 196, 113)
		
		
		
		)



	print("Lectio.dk login credentials")

	print("Username:")
	user_ = input()
	print("Password:")
	pass_ = input()
	
	def classid_input(message):
		try:
			id = int(input(message))
			return id
		except:
			return classid_input("enter a number: \n")

	classid = classid_input("Select Class: (0-" + str(len(classurl) - 1) + ") \n")
	
	if((classid < 0) or (classid > len(classurl) - 1)):
		classid = classid_input("Select Class: (0-" + str(len(classurl)) + ") \n")
	payload = {
    
		'time': '0',
		'__EVENTTARGET': 'm$Content$submitbtn2',
		'__EVENTARGUMENT': '',
		'__LASTFOCUS': '',
		'__SCROLLPOSITION': '',
		'__VIEWSTATEX': 'wwAAAGlpZQotOTA0NjQxOTI2aWwCawCBbAJoaWRsAmcDaWwCawFlA29mZmwCZwNpZGwCZwVpZGwCgWlkbAJnCWlkbASBaWwCawJlFE4mIzIzMDtydW0gR3ltbmFzaXVtZGcJaWRsAoFpZGwCgWlqaWwCawNwZGRkZHIBZR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X19sAmUMbSRDaG9vc2VUZXJtZRZtJENvbnRlbnQkQXV0b2xvZ2luQ2J4BAAAABNWYWxpZGF0ZVJlcXVlc3RNb2RlDGF1dG9jb21wbGV0ZQlpbm5lcmh0bWwHQ2hlY2tlZAD0nvsxY7wDI1o3xUUJ64ypm7UkZA==',
		'__VIEWSTATEY_KEY': '',
		'__VIEWSTATE': '',
		'__EVENTVALIDATION': 'oWV1CGHJSKGiWZGJESpuJV9osp+WAYcaAbLw+7JqDCFQbA+pFyxSD3CAge+yf41e4clK0C7zYL1dtOpd60q0sRBk7oCjDZLNoIuqdbliFxJVgyhQC1H7MU0JeiJLYxiPsN5L18H+2fnsRG1X6nx8C3wCTG0Rkl+l0KdVQ8pUQpYiLJcze2o9JQfJ6CsDPNRY8d4lc8bMx0bCAi/cG+usQm35vznifAiL2qdq//IL7NA=',
		'm$Content$username': user_,
		'm$Content$password': pass_,
	
		'LectioPostbackId': ''
	}
	

	n = 0
	path = "images/"


	
		
	def closest_color(rgb):
		r, g, b = rgb
		color_diffs = []
		for color in COLORS:
			cr, cg, cb = color
			color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
			color_diffs.append((color_diff, color))
		return min(color_diffs)[1]

		
		
		

	print("Establishing Connection to server...")
	#Login to Lectio Server
	url = classurl[classid]
	s = requests.Session()
	r = s.post(url, payload)
	r.raise_for_status()

	soup = BeautifulSoup(r.text, "html.parser")


	images = soup.find_all('img', {'src': re.compile("/lectio/31/GetImage.aspx")})	


	if(len(images) == 0):
		print("Login Unsuccesful \n")
		start()

	print("Succesful")
	print("Downloading Images...")


	print("Dominant Color Windows?(Y/N)")
	dom = input()

	print("Use Machine Learning Model For Detection (Longer wait time) (Y/N)")
	mLearn = input()

	#Download images to folder
	def download_jpg(imgurl, file_path, file_name):
		full_path = file_path + file_name + '.jpg'
		var = s.get(imgurl)
		with open(full_path, 'wb') as f:
			f.write(var.content)


	#Create directory
	cwd = os.getcwd()
	if not os.path.exists(cwd + "/images"):
		try:
			os.makedirs(cwd +"/images")
		except OSError:
			print("Creation of the directory %s failed " % cwd + "/images")
		print("Created Directory " + cwd +"/images")

	if not os.path.exists(cwd + "/images/Results"):
		try:
			os.makedirs(cwd +"/images/Results")
		except OSError:
			print("Creation of the directory %s failed " % cwd + "/images/Results")
				
		print("Created Directory " + cwd +"/images/Results")
  
	
	if os.path.exists(cwd + "/images/Results"):
		print("Directory Found")



	for image in images:
		n +=1
		print(image['src'])
	
		download_jpg("https://lectio.dk" + image['src'], path ,  str(n))
		img = cv2.imread("images/" + str(n) + ".jpg")
		imgResized = cv2.resize(img, (400,400))
		imgCropped = imgResized[35:60,150:250]
		cv2.imwrite("images/" + str(n) +  "cropped.jpg", imgCropped)
		img = cv2.imread("images/" + str(n) + "cropped.jpg")

		def create_bar(height, width, color):
			bar =np.zeros((height,width,3),np.uint8)
			bar[:] = color
			red,green, blue = int(color[2]), int(color[1]), int(color[0])
			return bar, (red,green,blue)

		height, width, _ = np.shape(img)
		data = np.reshape(img, (height * width, 3))
		data = np.float32(data)

		number_clusters = 1
		criteria = (cv2.TermCriteria_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
		flags = cv2.KMEANS_RANDOM_CENTERS
		compactsness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)

	
		print(centers)


		bars = []
		rgb_values = []
		

		for index, row in enumerate(centers):
			bar, rgb = create_bar(200,200,row)
			bars.append(bar)
			rgb_values.append(rgb)
		img = cv2.imread("images/" + str(n) + ".jpg")
	
		#Sorts based on sum of rgb values

		if(mLearn == "Y"):

			img = cv2.imread("images/" + str(n) + ".jpg")
			resize = tf.image.resize(img, (256,256))

			new_model = load_model('models/imageclassifier.h5')
			yhat = new_model.predict(np.expand_dims(resize/255, 0))

			if yhat < 0.5: 
				 cv2.imwrite("images/Results/" + "Blonde_"+ str(n) + ".jpg", img)
			else:
				cv2.imwrite("images/Results/" + "Brunette_" + str(n) + ".jpg", img)
		elif(mLearn != "Y"):

			for index, row in enumerate(rgb_values):
				if(rgb[0] + rgb[1] + rgb[2] > 300):
					cv2.imwrite("images/Results/" + "Blonde_"+ str(n) + ".jpg", img)
				else:
					cv2.imwrite("images/Results/" + "Brunette_" + str(n) + ".jpg", img)
			
			img_bar = np.hstack(bars)
		if(dom == "Y"):
			cv2.imshow('Dominant colors' + str(n), img_bar)
	
	
	#possible better sorting

	#for index, row in enumerate(rgb_values):
	#		if(closest_color((rgb[0],rgb[1],rgb[2])) == (248, 196, 113)):
	#			cv2.imwrite("images/Results/" + "Blonde_"+ str(n) + ".jpg", img)
	#		else:
	#			cv2.imwrite("images/Results/" + "Brunette_" + str(n) + ".jpg", img)
			




		

	
	print("Download complete")


	print("Starting Color Sorting...")


	print("Program ended succesfully \nOpening \images\ in file explorer")

	
	

	
	os.startfile("images")
	cv2.waitKey(0)

	print("r to restart")
	RESTART = input()
	if(RESTART == 'r'):
		start()

start()
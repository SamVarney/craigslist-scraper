from craigslist import CraigslistHousing
'''
        base_filters = {
        'query': {'url_key': 'query', 'value': None},
        'search_titles': {'url_key': 'srchType', 'value': 'T'},
        'has_image': {'url_key': 'hasPic', 'value': 1},
        'posted_today': {'url_key': 'postedToday', 'value': 1},
        'search_distance': {'url_key': 'search_distance', 'value': None},
        'zip_code': {'url_key': 'postal', 'value': None},
        }

extra_filters = {
        'private_room': {'url_key': 'private_room', 'value': 1},
        'private_bath': {'url_key': 'private_bath', 'value': 1},
        'cats_ok': {'url_key': 'pets_cat', 'value': 1},
        'dogs_ok': {'url_key': 'pets_dog', 'value': 1},
        'min_price': {'url_key': 'min_price', 'value': None},
        'max_price': {'url_key': 'max_price', 'value': None},
        'min_ft2': {'url_key': 'minSqft', 'value': None},
        'max_ft2': {'url_key': 'maxSqft', 'value': None},
        'min_bedrooms': {'url_key': 'min_bedrooms', 'value': None},
        'max_bedrooms': {'url_key': 'max_bedrooms', 'value': None},
        'min_bathrooms': {'url_key': 'min_bathrooms', 'value': None},
        'max_bathrooms': {'url_key': 'max_bathrooms', 'value': None},
        'no_smoking': {'url_key': 'no_smoking', 'value': 1},
        'is_furnished': {'url_key': 'is_furnished', 'value': 1},
        'wheelchair_acccess': {'url_key': 'wheelchaccess', 'value': 1},
        }


'''

def crawl():
	redwoodcity_zipcodes = {94063,94061,94027}
	posted_today = True
	fileName = 'redwoodcity_new housing.txt'
	
	
	result_file = open(fileName,'w')
	counter = 0
	
	for zipcode in redwoodcity_zipcodes:
		cl_h = CraigslistHousing(site='sfbay', area='pen', category='apa',
		filters={'min_price':2000, 'max_price': 3200, 'private_room': True, 'has_image':True, 'min_bedrooms':2, 'zip_code':zipcode, 'posted_today':posted_today})
		
		#filters={'min_price':2000, 'max_price': 3200, 'private_room': True, 'has_image':True, 'min_bedrooms':2, 'zip_code':zipcode})
		
		for result in cl_h.get_results(sort_by='newest', geotagged=True):
			#print result 
			result_file.write('\n' + result['name'] + '\n')
			result_file.write('\t' + 'Post ID: ' + result['id'] + '\n')
			result_file.write('\t' + 'Price: ' + result['price'] + '\n')
			result_file.write('\t' + 'City: ' + result['where'] + '\n')
			result_file.write('\t' + 'Sqft: ' + result['area'] + '\n')
			result_file.write('\t' + 'Link: ' + result['url'] + '\n')
			result_file.write('\n-------------------------------\n')
			counter += 1
			
	result_file.close()
		
	contents = open(fileName, 'r').read()
	#print contents
		
	return fileName, counter
		
		
#send results
# Import smtplib for the actual sending function
def send_results(fileName, counter):
	# Send the message via our own SMTP server.
	import smtplib
	import email.message
	'''
	message = email.message.Message()
	message['From'] = 'samuel.j.varney@gmail.com'
	message['To'] = ['samvarney@me.com']
	message['Subject'] = str(counter) + ' New Redwood City Houses Posted Today - Sams Scraper Bot'
	
	body = open(fileName, 'r').read()
	message.set_payload(body);
	'''
	
	gmail_user = 'samuel.j.varney@gmail.com'  
	gmail_password = 'Saemsaem22'
	
	sent_from = gmail_user  
	#to = ['Mattgroetelaars@gmail.com', 'michellefatdds@gmail.com']  
	#to = ['samvarney@me.com', 'michellefatdds@gmail.com', 'Mattgroetelaars@gmail.com']
	to = ['samvarney@me.com']
	subject = str(counter) + ' New Redwood City Houses Posted Today - Sams Scraper Bot'  
	body = open(fileName, 'r').read()
	
	email_text = """\
From:%s 
To:%s  
Subject:%s
%s
""" % (sent_from, ", ".join(to), subject, body)
	
	#email_text = body
	
	
	print email_text
	
	try:  
	    server = smtplib.SMTP_SSL('smtp.gmail.com')
	    print server.ehlo()
	    server.set_debuglevel(2)
	    #server.debug_level(2)
	    
	    server.login(gmail_user, gmail_password)
	    server.sendmail(sent_from, to, email_text)
	    #print sever.sendmail(message)
	    #server.send()
	    
	
	    print 'Email sent!'
	except smtplib.SMTPException:
	    print 'Something went wrong...'
	
	server.close()
	    
	    
	    
file_name, counter = crawl()
print file_name, counter
send_results(file_name, counter)

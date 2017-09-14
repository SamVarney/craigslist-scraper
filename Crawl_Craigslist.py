from craigslist import CraigslistHousing

''' **************BELOW ARE THE FILTERS THAT THE SCRAPER ACCEPTS************

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
    '''**************CRAWL CRAIGSLIST SETTINGS*************************************'''
    redwoodcity_zipcodes = {94063, 94061, 94027}
    posted_today = True
    minimum_rent = 2000
    maximum_rent = 3400
    minimum_bedrooms = 2
    posted_today = True #(either True or None)
    fileName = 'redwoodcity_new housing.txt'
    '''**********END OF SETTINGS (CAN ADD MORE FILTERS TO THE REQUEST)***************'''

    result_file = open(fileName, 'w')
    num_results = 0

    for zipcode in redwoodcity_zipcodes:
        cl_h = CraigslistHousing(site='sfbay', area='pen', category='apa',
                                 filters={'min_price': minimum_rent, 'max_price': maximum_rent, 'private_room': True, 'has_image': True,
                                          'min_bedrooms': minimum_bedrooms, 'zip_code': zipcode, 'posted_today': posted_today})


        for result in cl_h.get_results(sort_by='newest', geotagged=True):
            result_file.write('\n' + str(result['name']) + '\n')
            result_file.write('\t' + 'Post ID: ' + str(result['id']) + '\n')
            result_file.write('\t' + 'Price: ' + str(result['price']) + '\n')
            result_file.write('\t' + 'City: ' + str(result['where']) + '\n')
            result_file.write('\t' + 'Sqft: ' + str(result['area']) + '\n')
            result_file.write('\t' + 'Link: ' + str(result['url']) + '\n')
            result_file.write('\n-------------------------------\n')
            num_results += 1

    result_file.close()

    contents = open(fileName, 'r').read()
    print(contents)

    return fileName, num_results


# send results
def send_results(fileName, num_results):

    import smtplib

    gmail_user = 'samuel.j.varney@gmail.com'
    gmail_password = 'Saemsaem22'
    to = ['samvarney@me.com'] #A list of addresses to send results too


    sent_from = gmail_user

    subject = str(num_results) + ' New Redwood City Houses Posted Today - Sams Scraper Bot'

    body = open(fileName, 'r').read() #Open the results file that the scraper saved

    #construct email text
    email_text = """\
From:%s 
To:%s  
Subject:%s
%s
""" % (sent_from, ", ".join(to), subject, body)

    print(email_text)


    #now try to send the email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.ehlo()
        server.set_debuglevel(2)

        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        print('Email sent!')

    except smtplib.SMTPException:
        print('Something went wrong...')

    server.close()



file_name, num_results = crawl() # get results

print(file_name, num_results)

send_results(file_name, num_results) #Email results out to everyone

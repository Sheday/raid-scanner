from init import *

def scrape_for_raids():
    print 'Going to scrape for raids in cycles.'
    while True:
        response = requests.get("https://go.airathias.tv/raids")
        if response.status_code == 200:
            process_response(BeautifulSoup(response.text, 'html.parser'))
            print "Cycle complete. Sleeping for {0} seconds now...".format(TIME_BETWEEN_CYCLES)
        else:
            print "Failed to retrieve the page. Status code: {0}".format(response.status_code)
        sleep(TIME_BETWEEN_CYCLES)

def process_response(data):
    raids = data.find_all('div', attrs = {"class" : "solo-pokemon"})
    print 'Found {0} raids. Inserting them into the database.'.format(len(raids))
    for index, raid in enumerate(raids):
        pokemon = raid.h2.text
        level = raid['class'][-1].split('-')[-1]
        location = raid.find_all('a')[0]['href']
        location_name = raid.h4.text
        start_time = raid.find_all('a')[1]['href'].split('om ')[1].split(' op')[0].split(':')
        starts_at = datetime.today().replace(hour = int(start_time[0]), minute = int(start_time[1]), second = 0)
        expires_at = starts_at.replace(hour = starts_at.hour + 2) # Assume all raids last 2 hours

        # Insert raid into database
        entry = Raid(
            pokemon = pokemon,
            level = level,
            location = location,
            location_name = location_name,
            start_time = start_time,
            starts_at = starts_at,
            expires_at = expires_at
        )
        try:
            entry.save()
            print 'Added a new raid to the database. Location: {0}. Pokemon: {1}. Started at {2}'.format(
                location_name, pokemon, starts_at.strftime('%H:%M'))
        except IntegrityError:
            print 'This raid has already been added in a previous cycle. Skipping.'

        print 'Progress: {0}/{1}'.format(index + 1, len(raids))

scrape_for_raids()

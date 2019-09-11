import googlemaps
key = 'AIzaSyBbGXoi2IXRvt7FJuTy3tnEBcv91BOitXk'  # env
gmaps = googlemaps.Client(key=key)

def place_point_POI(longitude, latitude):
    places_result = gmaps.places_nearby(location=longitude + ',' + latitude, radius='5000', language='fr-CA')
    dict = []
    try:
        for place_p in places_result['results']:
            place_point = {}
            id = place_p['id']
            place_point['id'] = id

            id_place = place_p['place_id']
            place_point['place_id'] = id_place

            result_detail = gmaps.place(place_id=id_place)
            adresse = result_detail['result']
            place_point['street'] = adresse['formatted_address']
            # print(result_detail['rating'])
            # place_point['rating'] = adresse['rating']
            place_point['website'] = adresse['website']
            place_point['name'] = place_p['name']

            geo = place_p['geometry']
            place_point['latitude'] = geo['location']['lat']
            place_point['longitude'] = geo['location']['lng']

            photo = place_p['photos']

            url = "https://maps.googleapis.com/maps/api/place/" \
                  "photo?key=AIzaSyBbGXoi2IXRvt7FJuTy3tnEBcv91BOitXk&photoreference=" + photo[0]['photo_reference'] \
                  + "&maxheight=500"

            place_point['url_photo'] = url

            dest = place_point
            dict.append(dest)
    except:
        pass
    return dict
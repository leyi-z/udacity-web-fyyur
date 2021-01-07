from app import *

s=db.session()

v1 = Venue(name='Old Forest', city='Huzhou', state='ZJ', address='423 Bleh Rd', phone='22457')
v2 = Venue(name='Random Park', city='Huzhou', state='ZJ', address='85 Forest St', phone='24813')
v3 = Venue(name='Thunderdome', city='Goleta', state='CA', address='7792 UCSB Ave', phone='26792')
v4 = Venue(name='Bleh Plaza', city='Goleta', state='CA', address='562 Bleh Rd', phone='25468')
v5 = Venue(name='Bleh Mall', city='Ventura', state='CA', address='354 Bleh Rd', phone='27745')
v6 = Venue(name='Bleh Stadium', city='Dallas', state='TX', address='71 Pecan Blvd', phone='23334')

a1 = Artist(name='Thig n Bear', city='Portsmouth', state='NH', phone='47982')
a2 = Artist(name='Thog', city='Hong Kong', state='HK', phone='44431')
a3 = Artist(name='Ngwah', city='Hong Kong', state='HK', phone='49193')
a4 = Artist(name='Mudkip', city='Fiji', state='PO', phone='49243')
a5 = Artist(name='Little Heads', city='Hawaii', state='PO', phone='43432')
a6 = Artist(name='Creepy Bean', city='Honululu', state='PO', phone='47789')

s.add_all([v1,v2,v3,v4,v5,v6,a1,a2,a3,a4,a5,a6])
s.commit()


s1 = Show(artist_id=1, venue_id=2, start_time="2020-04-01T20:00:00.000Z")
s2 = Show(artist_id=2, venue_id=1, start_time="2030-05-21T21:30:00.000Z")
s3 = Show(artist_id=3,  venue_id=3, start_time="2024-06-15T23:00:00.000Z")
s4 = Show(artist_id=2, venue_id=2, start_time="2020-04-01T20:00:00.000Z")
s5 = Show(artist_id=1, venue_id=4, start_time="2026-05-21T21:30:00.000Z")
s6 = Show(artist_id=3,  venue_id=6, start_time="2019-06-15T23:00:00.000Z")
s7 = Show(artist_id=1, venue_id=2, start_time="2019-05-21T21:30:00.000Z")
s8 = Show(artist_id=3,  venue_id=4, start_time="2019-06-15T23:00:00.000Z")
s9 = Show(artist_id=4,  venue_id=6, start_time="2019-06-15T23:00:00.000Z")
s10 = Show(artist_id=6, venue_id=2, start_time="2019-05-21T21:30:00.000Z")
s11 = Show(artist_id=5,  venue_id=5, start_time="2019-06-15T23:00:00.000Z")


s.add_all([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11])
s.commit()



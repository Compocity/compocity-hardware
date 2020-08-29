import requests

# url = 'https://jsonplaceholder.typicode.com/posts/1'
url = 'https://us-central1-compocity-e650d.cloudfunctions.net/api'
# myobj = {'somekey': 'somevalue'}

r = requests.get(url)

# print(r.status_code)
# print(r.headers)
print(r.content)

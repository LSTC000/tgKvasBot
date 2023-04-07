from fake_useragent import UserAgent


ua = UserAgent()
HEADERS = {
    'user-agent': ua.random
}

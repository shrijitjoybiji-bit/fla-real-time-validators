"""Shared accepted/rejected strings (>= 5 each) used by tests and the demo."""
CASES = {
    "password": {
        "accept": ["Abcdef1!", "Passw0rd#2026", "Hello@World9", "xY7$abcdefgh", "Zz9_zzzzz", "A1b2C3d4!"],
        "reject": ["abcdefg1!", "ABCDEFG1!", "Abcdefgh!", "Abcdefg1", "Ab1!", "Abc def1!", ""],
    },
    "email": {
        "accept": ["user@example.com", "john.doe@mail.co.in", "a_b-c@sub.domain.org",
                   "x1@y2.io", "first.last99@my-site.com"],
        "reject": ["user@@example.com", "user@example", "@example.com", "user@example.c",
                   "user.@example.com", "user..name@example.com", "user@-example.com",
                   "user@example.com.", "user name@example.com", "user@exa_mple.com"],
    },
    "atm_pin": {
        "accept": ["4821", "0000", "123456", "007531", "9999"],
        "reject": ["123", "12345", "12a4", "", "12 34", "1234567"],
    },
    "atm_session": {
        "accept": ["C", "WC", "WWC", "WWCW", "CC"],
        "reject": ["", "W", "WW", "WWW", "WWWC"],
    },
}

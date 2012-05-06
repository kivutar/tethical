import Character

# A client is trying to log into the server. Let's check its credentials and sent it back a reply
def execute(server, iterator, source):
    login = iterator.getString()
    password = iterator.getString()

    # since the server code is not connected to the database yet,
    # we authenticate the client if login == password
    if login != password:
        server.send.LOGIN_FAIL('Wrong credentials.', source)
    elif server.sessions.has_key(source):
        server.send.LOGIN_FAIL('Already logged in.', source)
    elif login in server.players.keys():
        server.send.LOGIN_FAIL('Username already in use.', source)
    else:
        server.players[login] = source
        server.sessions[source] = {}
        server.sessions[source]['login'] = login
        print login, 'logged in.'
        # since the server code is not connected to the database yet,
        # we generate a random team for each player
        server.sessions[source]['characters'] = []
        for i in range(10):
            server.charid = server.charid + 1
            char = Character.Random(server.charid)
            server.sessions[source]['characters'].append(char)
            server.chars.append(char)
        server.send.LOGIN_SUCCESS(source)
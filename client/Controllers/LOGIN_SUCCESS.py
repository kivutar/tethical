# Successfully logged into the server, display the party list
def execute(client, iterator):
    client.loginwindow.commandanddestroy(client.send.GET_PARTIES)
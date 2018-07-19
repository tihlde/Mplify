import binascii
import hashlib
import os
import time


import json
from aiohttp import web

from db import mysql_connect
from auth import requires_auth

DB_PASSWORD = ''
DB_USER = ''
DB_NAME = ''
loop = None


@requires_auth
async def get_member(request):
    (conn, cur) = await mysql_connect()

    """ Returns all members with 'first_name' or 'last_name' ==  search_string
        
        Keyword arguments:
        request -- http-request object
        search_string -- retrieved from '/api/user/{name}'
        
    NOT FINISHED: Needs to incorporate admin-authentication method
    """

    try:
        name = str(request.match_info['name'])
        await cur.execute("SELECT * FROM user WHERE  first_name = %s OR last_name = %s", (name, name))
        r = await cur.fetchall()
        return web.json_response(json.dumps(r, default=str))

    finally:
        await cur.close()
        conn.close()


@requires_auth
async def get_all_members(request):
    (conn, cur) = await mysql_connect()

    """ Returns all members 

    NOT FINISHED: Needs to incorporate admin-authentication method
    """

    try:
        await cur.execute("SELECT * FROM user")
        r = await cur.fetchall()
        return web.json_response(json.dumps(r, default=str))

    finally:
        await cur.close()
        conn.close()

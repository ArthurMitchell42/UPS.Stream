#!/usr/bin/python3

import os
import cgi, cgitb
cgitb.enable()    
#cgitb.enable(display=1, logdir="/config")    

html_head_top = \
"""Content-Type: text/html\n\n<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="/fontawesome/css/all.css">
    """

html_head_main = \
"""    <title>{}</title>"""

html_head_style_start = \
"""    <style>"""

html_style_end = \
"""</style>"""

html_head_javascript = \
"""
<script>
</script>
"""

html_head_bottom = \
"""</head>"""

html_body_top = \
"""<body>"""

html_body_bottom = \
"""
</body>
"""

html_html_bottom = \
"""</html>"""

##################################################
# Main function
##################################################
def main():
    windowtitle = "Command Parse"

    if "SCRIPT_NAME" in os.environ:
        scriptname=os.environ["SCRIPT_NAME"]
    else:
        scriptname="Not found"

    form = cgi.FieldStorage()

    print(html_head_top)
    print(html_head_main.format(windowtitle))
    print(html_head_style_start)
    print(html_style_end)

    print(html_head_bottom)

    print(html_body_top)

    print("<font size=+3>CGI form data</font></br>")
    print("Script name: ", scriptname)
    
    print("<br>")

    for param in form:
        print("<b> {} </b>: {} </br>".format(param, form[param].value ) )
    
    print("<br>")

    print("<font size=+3>Environment</font></br>")
    for param in os.environ.keys():
        print("<b> {} </b>: {}</br>".format(param, os.environ[param]))

    username = 'monuser'
    password = 'secret'
    server_address = ''
    server_port = 3493
    interval = 30

    if os.path.exists('/config/config.txt'):
        with open('/config/config.txt') as f:
            for line in f:
                fields = line.strip().split()
                if fields[0] == 'name':
                    username = fields[1]
                elif fields[0] == 'pass':
                    password = fields[1]
                elif fields[0] == 'addr':
                    server_address = fields[1]
                elif fields[0] == 'port':
                    server_port = int(fields[1])
                elif fields[0] == 'time':
                    interval = int(fields[1])
        print("Config:<br> - Username: {}<br> - Password: {}<br> - Server address: {}<br> - Port: {}<br> - Poll interval: {}<br>".format( username, password, server_address, server_port, interval ))
    else:
        print("Config file does not exist<br>")

    print(html_body_bottom)
    print(html_html_bottom)
    return

if __name__ == '__main__':
    main()

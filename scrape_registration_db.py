#!/usr/bin/env python

# Copyright (C) 2015  James Tatum

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# The purpose of this script is to take input in the form of a
# comma-delimited staff list, read a list of IDs, then log in to wordpress
# and scrape the event espresso database for certain elements. In This case,
# a builtin field called name, a user-defined field called fanname-11,
# and a user-defined selection.
#
# There are many things about this script that could be improved. It started
# out with BeautifulSoup but the HTML is irregular enough that parsing it
# with some Janky regular expressions turned out much faster. The WordPress
# login routine or the cookie storage routine is currently broken. The
# script logs in fresh every request.

import csv
import re
import requests
import sys
import traceback

# Cookie jar
COOKIES = {}


def get_regex(attr):
    return re.compile(attr + r'</span>(.+)\t</p>')


def get_regex_question(question):
    return re.compile(
        'id="' + question + '" class="regular-text " value="(.+)"  title=""  '
                            '/')


def display_preference(html):
    if 'value="Fan Name Only" selected="selected"' in html:
        return 'Fan Name Only'
    if 'value="Legal Name Only" selected="selected"' in html:
        return 'Legal Name Only'
    if 'value="Legal Name First" selected="selected"' in html:
        return 'Legal Name First'
    if 'value="Fan Name First" selected="selected"' in html:
        return 'Fan Name First'
    if 'value="First &quot;Fan&quot; Last" selected="selected"' in html:
        return 'First "Fan" Last'
    if 'value="" selected="selected"' in html:
        return None


def read_csv(file_):
    result = []
    reader = csv.reader(file_)
    for row in reader:
        # Todo: Accept row containing the ID as a parameter
        id_ = row[7]
        try:
            int(id_)
        except ValueError:
            result.append(None)
        else:
            result.append(id_)
    return result


def match_attr(attr, html):
    return get_regex(attr).search(html).groups()[0]


def match_question(question, html):
    return get_regex_question(question).search(html).groups()[0]


def get_url(id_):
    if id_ is None:
        return None
    return 'https://reg.furtherconfusion.org/wp-admin/admin.php?page' \
           '=espresso_registrations&action=view_registration&_REG_ID=' + id_


def post_url(url, data=None):
    global COOKIES
    if data is None:
        data = {}
    r = requests.post(url, cookies=COOKIES, data=data)
    COOKIES = r.cookies
    return r.text


def fetch_url(url):
    global COOKIES
    r = requests.post(url, cookies=COOKIES)
    COOKIES = r.cookies
    return r.text


def wp_login(username, password, url):
    fetch_url('https://reg.furtherconfusion.org/wp-login.php')
    return post_url('https://reg.furtherconfusion.org/wp-login.php',
                    data={'log': username, 'pwd': password,
                          'wp-submit': 'Log In', 'redirect_to': url,
                          'testcookie': '1'})


def main(username, password):
    # Todo: The writey-bits don't need to be in scope with the readey-bits. Refactor that
    # Todo: Accept filenames as parameters (and maybe use argparse for all these arguments)
    with open('/Users/jtatum/Downloads/fc15s.csv') as f:
        with open('/Users/jtatum/Downloads/fc15o.csv', 'wb') as out:
            writer = csv.writer(out)
            array = read_csv(f)
            for id_ in array:
                row = [id_]
                url = get_url(id_)
                if url is None:
                    writer.writerow(row)
                    continue

                # Todo: This is a bit daft, but I couldn't get just regular
                # GETs after a login to work.
                html = wp_login(username, password, get_url(id_))
                # Todo: I should check for an empty response here. I think
                # that means the reg has been trashed.
                try:
                    row.append(display_preference(html))
                    row.append(match_attr('Name', html))
                    row.append(match_question('fanname-11', html))
                except StandardError:
                    row.append('Error reading value')
                    traceback.print_exc()
                    print 'ID: %s, url: %s' % (id_, url)
                    writer.writerow(row)
                    continue

                writer.writerow(row)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: %s <username> <password>' % sys.argv[0]
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])

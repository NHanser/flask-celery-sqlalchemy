# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from __future__ import print_function  # Use print() instead of print
from flask import url_for


def test_page_urls(myapp):
    # Visit home page
    response = myapp.test_client.get(url_for('core_bp.home_page'), follow_redirects=True)
    assert response.status_code==200

    # Login as user and visit User page
    response = myapp.test_client.post(url_for('security.login'), follow_redirects=True,
                           data=dict(email='user@example.com', password='Password1'))
    assert response.status_code==200
    response = myapp.test_client.get(url_for('users_bp.user_profile_page'), follow_redirects=True)
    assert response.status_code==200

    # Edit User Profile page
    #response = myapp.test_client.get(url_for('main.user_profile_page'), follow_redirects=True)
    #assert response.status_code==200
    #response = myapp.test_client.post(url_for('main.user_profile_page'), follow_redirects=True,
    #                       data=dict(first_name='User', last_name='User'))

    # Logout
    response = myapp.test_client.get(url_for('security.logout'), follow_redirects=True)
    assert response.status_code==200

    # Login as admin and visit Admin page
    response = myapp.test_client.post(url_for('security.login'), follow_redirects=True,
                           data=dict(email='admin@example.com', password='Password1'))
    assert response.status_code==200
    response = myapp.test_client.get(url_for('admin.index'), follow_redirects=True)
    assert response.status_code==200

    # Logout
    response = myapp.test_client.get(url_for('security.logout'), follow_redirects=True)
    assert response.status_code==200

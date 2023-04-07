import requests

api_url = 'http://localhost:5000'

def test_login_with_wrong_username(start_api):
    response = requests.post(
        f'{api_url}/user/login',
        json={
            'username': 'wrong_admin',
            'password': 'admin'
        }
    )

    assert response.status_code == 404

def test_login_with_wrong_password():
    response = requests.post(
        f'{api_url}/user/login',
        json={
            'username': 'admin',
            'password': 'wrong_password'
        }
    )

    assert response.status_code == 404

def test_login_with_admin_user():
    response = requests.post(
        f'{api_url}/user/login',
        json={
            'username': 'admin',
            'password': 'admin'
        }
    )

    assert response.status_code == 200

def test_create_owner_without_jwt():
    response = requests.post(
        f'{api_url}/owner/register',
        json={
            'name': 'owner',
            'email': 'invalid_email'
        }
    )
    assert response.status_code == 403

def test_create_owner_with_invalid_email(access_token: str):
    response = requests.post(
        f'{api_url}/owner/register',
        json={
            'name': 'owner',
            'email': 'invalid_email'
        },
        headers=access_token
    )
    assert response.status_code == 400

def test_create_owner_with_empty_name(access_token: str):
    response = requests.post(
        f'{api_url}/owner/register',
        json={
            'name': '',
            'email': 'owner@gmail.com'
        },
        headers=access_token
    )
    assert response.status_code == 400

def test_create_owner_with_empty_email(access_token: str):
    response = requests.post(
        f'{api_url}/owner/register',
        json={
            'name': 'owner',
            'email': 'owner'
        },
        headers=access_token
    )
    assert response.status_code == 400

def test_create_owner(access_token: str):
    response = requests.post(
        f'{api_url}/owner/register',
        json={
            'name': 'owner',
            'email': 'owner@gmail.com'
        },
        headers=access_token
    )
    assert response.status_code == 200

def test_create_owner_with_same_email(access_token: str):
    response = requests.post(
        f'{api_url}/owner/register',
        json={
            'name': 'owner',
            'email': 'owner@gmail.com'
        },
        headers=access_token
    )
    assert response.status_code == 409

def test_remove_owner(access_token: str):
    response = requests.delete(
        f'{api_url}/owner/delete/owner@gmail.com',
        headers=access_token
    )
    assert response.status_code == 200

def test_remove_same_owner_and_get_error(access_token: str):
    response = requests.delete(
        f'{api_url}/owner/delete/owner@gmail.com',
        headers=access_token
    )
    assert response.status_code == 404

def test_recreate_owner(access_token: str):
    response = requests.post(
        f'{api_url}/owner/register',
        json={
            'name': 'owner',
            'email': 'owner@gmail.com'
        },
        headers=access_token
    )
    assert response.status_code == 200

def test_recreate_owner(access_token: str):
    response = requests.post(
        f'{api_url}/owner/register',
        json={
            'name': 'owner',
            'email': 'owner@gmail.com'
        },
        headers=access_token
    )
    assert response.status_code == 200

def test_create_second_owner(access_token: str):
    response = requests.post(
        f'{api_url}/owner/register',
        json={
            'name': 'owner2',
            'email': 'owner2@gmail.com'
        },
        headers=access_token
    )
    assert response.status_code == 200

def test_create_car_to_first_owner(access_token: str):
    response = requests.post(
        f'{api_url}/car/register',
        json={
            'car_color': 'blue',
            'car_type': 'sedan',
            'owner_email': 'owner@gmail.com'
        },
        headers=access_token
    )
    assert response.status_code == 200

def test_create_second_car_to_first_owner(access_token: str):
    response = requests.post(
        f'{api_url}/car/register',
        json={
            'car_color': 'gray',
            'car_type': 'convertible',
            'owner_email': 'owner@gmail.com'
        },
        headers=access_token
    )
    assert response.status_code == 200

def test_create_third_car_to_first_owner(access_token: str):
    response = requests.post(
        f'{api_url}/car/register',
        json={
            'car_color': 'yellow',
            'car_type': 'hatch',
            'owner_email': 'owner@gmail.com'
        },
        headers=access_token
    )
    assert response.status_code == 200

def test_create_four_car_to_first_owner_and_get_error(access_token: str):
    response = requests.post(
        f'{api_url}/car/register',
        json={
            'car_color': 'yellow',
            'car_type': 'convertible',
            'owner_email': 'owner@gmail.com'
        },
        headers=access_token
    )
    assert response.status_code == 403

def test_delete_invalid_car_from_owner_1(access_token: str):
    response = requests.delete(
        f'{api_url}/car/delete',
        json={
            'car_uuid': 'foo'
        },
        headers=access_token
    )
    assert response.status_code == 404

def test_delete_car_from_owner_1(access_token: str):
    response = requests.get(
        f'{api_url}/owner/about/owner@gmail.com',
        headers=access_token
    ).json()
    car_1 = response['cars'][0]['uuid']

    response = requests.delete(
        f'{api_url}/car/delete/{car_1}',
        json={
            'car_uuid': 'foo'
        },
        headers=access_token
    )
    assert response.status_code == 200

def delete_owner_from_system(access_token: str):
    response = requests.delete(
        f'{api_url}/owner/delete/owner@gmail.com',
        headers=access_token
    )

    assert response == 200
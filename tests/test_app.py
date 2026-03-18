from fastapi import status

def test_get_activities(client):
    # Arrange

    # Act
    response = client.get('/activities')

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, dict)
    assert 'Chess Club' in data


def test_signup_for_activity(client):
    # Arrange
    email = 'test@mergington.edu'

    # Act
    response = client.post('/activities/Chess Club/signup', params={'email': email})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': f'Signed up {email} for Chess Club'}


def test_duplicate_signup_returns_400(client):
    # Arrange
    email = 'duplicate@mergington.edu'
    client.post('/activities/Chess Club/signup', params={'email': email})

    # Act
    response2 = client.post('/activities/Chess Club/signup', params={'email': email})

    # Assert
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert response2.json()['detail'] == 'Student already signed up for this activity'


def test_remove_participant(client):
    # Arrange
    email = 'removeme@mergington.edu'
    client.post('/activities/Chess Club/signup', params={'email': email})

    # Act
    remove = client.delete('/activities/Chess Club/participants', params={'email': email})

    # Assert
    assert remove.status_code == status.HTTP_200_OK
    assert remove.json() == {'message': f'Removed {email} from Chess Club'}


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    email = 'missing@mergington.edu'

    # Act
    response = client.delete('/activities/Chess Club/participants', params={'email': email})

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Participant not found'


def test_activity_not_found_returns_404(client):
    # Arrange
    activity = 'NoSuchActivity'

    # Act
    response = client.post(f'/activities/{activity}/signup', params={'email': 'x@y.com'})

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Activity not found'

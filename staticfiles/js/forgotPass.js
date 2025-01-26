function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}

document.getElementById('username').addEventListener('input', function () {
    const username = this.value.trim();
    const feedback = document.getElementById('username-feedback');
    const inputField = this;

    if (!username) {
        feedback.textContent = '';
        inputField.classList.remove('is-invalid', 'is-valid');
        return;
    }

    fetch(`/validate-username/?username=${username}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (!data.is_taken) {
            feedback.textContent = 'This username does not exist.';
            inputField.classList.add('is-invalid');
            inputField.classList.remove('is-valid');
        } else {
            feedback.textContent = 'Username exists!';
            inputField.classList.add('is-valid');
            inputField.classList.remove('is-invalid');
        }
    })
    .catch(error => {
        feedback.textContent = 'An error occurred. Please try again later.';
        inputField.classList.add('is-invalid');
        inputField.classList.remove('is-valid');
        console.error('Error:', error);
    });
});

document.getElementById('Confirmpassword').addEventListener('input', function () {
    const password = document.getElementById('Newpassword').value;
    const confirmPassword = this.value.trim();
    const feedback = document.getElementById('password-feedback');
    const inputField = this;

    if (!confirmPassword) {
        feedback.textContent = '';
        inputField.classList.remove('is-invalid', 'is-valid');
        return;
    }

    if (password !== confirmPassword) {
        feedback.textContent = 'Passwords do not match.';
        inputField.classList.add('is-invalid');
        inputField.classList.remove('is-valid');
    } else {
        feedback.textContent = 'Passwords match!';
        inputField.classList.add('is-valid');
        inputField.classList.remove('is-invalid');
    }
});
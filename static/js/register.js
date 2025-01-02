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

    const numberRegex = /^[0-9]+$/;
    const startsWithNumberRegex = /^[0-9]/;
    const containsSpaceRegex = /\s/;
    const userNameRegex = /^[a-zA-Z]+^[0-9]+$/;

    if(!userNameRegex.test(username))
    {
        feedback.textContent = 'Username should be Combination of Alphabets & Numbers';
        inputField.classList.add('is-invalid');
        inputField.classList.remove('is-valid');
        return;
    }

    if (numberRegex.test(username)) {
        feedback.textContent = 'Username cannot be just numbers.';
        inputField.classList.add('is-invalid');
        inputField.classList.remove('is-valid');
        return;
    }

    if (startsWithNumberRegex.test(username)) {
        feedback.textContent = 'Username cannot start with a number.';
        inputField.classList.add('is-invalid');
        inputField.classList.remove('is-valid');
        return;
    }
    if (containsSpaceRegex.test(username)) {
        feedback.textContent = 'Username cannot contain spaces.';
        inputField.classList.add('is-invalid');
        inputField.classList.remove('is-valid');
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
        if (data.is_taken) {
            feedback.textContent = 'This username is already taken.';
            inputField.classList.add('is-invalid');
            inputField.classList.remove('is-valid');
        } else {
            feedback.textContent = 'Username is available!';
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

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhone(phone) {
    const phoneRegex = /^\d{10}$/;
    return phoneRegex.test(phone);
}

// Validate Email
document.getElementById('email').addEventListener('input', function () {
    const email = this.value.trim();
    const feedback = document.getElementById('email-feedback');
    const inputField = this;

    if (!email) {
        feedback.textContent = '';
        inputField.classList.remove('is-invalid', 'is-valid');
        return;
    }

    if (!isValidEmail(email)) {
        feedback.textContent = 'Invalid email format.';
        inputField.classList.add('is-invalid');
        inputField.classList.remove('is-valid');
        return;
    }

    fetch(`/validate-email/?email=${email}`, {
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
        if (data.is_taken) {
            feedback.textContent = 'This email is already in use.';
            inputField.classList.add('is-invalid');
            inputField.classList.remove('is-valid');
        } else {
            feedback.textContent = 'Email is available!';
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

document.getElementById('phone').addEventListener('input', function () {
    const phone = this.value.trim();
    const feedback = document.getElementById('phone-feedback');
    const inputField = this;

    if (!phone) {
        feedback.textContent = '';
        inputField.classList.remove('is-invalid', 'is-valid');
        return;
    }

    if (!isValidPhone(phone)) {
        feedback.textContent = 'Phone number must be exactly 10 digits.';
        inputField.classList.add('is-invalid');
        inputField.classList.remove('is-valid');
    } else {
        feedback.textContent = 'Valid phone number!';
        inputField.classList.add('is-valid');
        inputField.classList.remove('is-invalid');
    }
});
document.getElementById('confirm_password').addEventListener('input', function () {
    const password = document.getElementById('password').value;
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

// Validate Password Matching
document.getElementById('confirm_password').addEventListener('input', function () {
    const password = document.getElementById('password').value;
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

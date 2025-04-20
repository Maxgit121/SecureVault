// Password Manager JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility
    const togglePassword = document.getElementById('togglePassword');
    const passwordField = document.getElementById('passwordField');
    
    if (togglePassword && passwordField) {
        togglePassword.addEventListener('click', function() {
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            
            // Toggle eye icon
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    }
    
    // Generate random password
    const generatePasswordBtn = document.getElementById('generatePassword');
    
    if (generatePasswordBtn && passwordField) {
        generatePasswordBtn.addEventListener('click', function() {
            const password = generateStrongPassword();
            passwordField.value = password;
            // If we have a strength meter, update it
            updatePasswordStrength(password);
        });
    }
    
    // Check password strength on input
    if (passwordField) {
        passwordField.addEventListener('input', function() {
            updatePasswordStrength(this.value);
        });
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Function to copy text to clipboard
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    
    if (element) {
        // Select the text
        element.select();
        element.setSelectionRange(0, 99999); // For mobile devices
        
        // Copy to clipboard
        navigator.clipboard.writeText(element.value)
            .then(() => {
                // Create a toast notification
                showToast('Copied to clipboard!');
            })
            .catch(err => {
                console.error('Failed to copy: ', err);
                showToast('Failed to copy to clipboard', 'danger');
            });
    }
}

// Function to show toast notification
function showToast(message, type = 'success') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0 position-fixed bottom-0 end-0 m-3`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Append to body
    document.body.appendChild(toast);
    
    // Initialize Bootstrap toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 3000
    });
    
    // Show toast
    bsToast.show();
    
    // Remove from DOM after hiding
    toast.addEventListener('hidden.bs.toast', function() {
        document.body.removeChild(toast);
    });
}

// Generate a strong random password
function generateStrongPassword(length = 16) {
    const lowercase = 'abcdefghijklmnopqrstuvwxyz';
    const uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const numbers = '0123456789';
    const symbols = '!@#$%^&*()_+{}:"<>?|[];\',./`~';
    
    const allChars = lowercase + uppercase + numbers + symbols;
    
    // Ensure at least one of each character type
    let password = 
        lowercase.charAt(Math.floor(Math.random() * lowercase.length)) +
        uppercase.charAt(Math.floor(Math.random() * uppercase.length)) +
        numbers.charAt(Math.floor(Math.random() * numbers.length)) +
        symbols.charAt(Math.floor(Math.random() * symbols.length));
        
    // Fill up the rest of the password
    for (let i = 4; i < length; i++) {
        password += allChars.charAt(Math.floor(Math.random() * allChars.length));
    }
    
    // Shuffle the password
    return shuffleString(password);
}

// Shuffle a string
function shuffleString(string) {
    const array = string.split('');
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array.join('');
}

// Update password strength meter
function updatePasswordStrength(password) {
    const strengthMeter = document.querySelector('.password-strength');
    
    if (!strengthMeter || !password) return;
    
    let strength = 0;
    
    // Length check
    if (password.length >= 8) strength += 1;
    if (password.length >= 12) strength += 1;
    
    // Character type checks
    if (/[a-z]/.test(password)) strength += 1;
    if (/[A-Z]/.test(password)) strength += 1;
    if (/[0-9]/.test(password)) strength += 1;
    if (/[^a-zA-Z0-9]/.test(password)) strength += 1;
    
    // Update UI
    strengthMeter.classList.remove('strength-weak', 'strength-medium', 'strength-strong');
    
    if (strength < 3) {
        strengthMeter.classList.add('strength-weak');
    } else if (strength < 5) {
        strengthMeter.classList.add('strength-medium');
    } else {
        strengthMeter.classList.add('strength-strong');
    }
}

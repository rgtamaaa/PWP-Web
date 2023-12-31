document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    // Silakan gantikan dengan kode validasi yang Anda inginkan
    console.log('Username:', username);
    console.log('Password:', password);
});
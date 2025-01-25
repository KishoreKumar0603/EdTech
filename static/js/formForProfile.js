function toggleSidebar() {
    document.getElementById("sidebarMenu").classList.toggle("show");
}
function triggerFileUpload() {
    document.getElementById('profilePicture').click();
}

document.getElementById('profilePicture').addEventListener('change', function() {
    if (this.files.length > 0) {
        document.querySelector('form').submit();
    }
});


function enableEditing() {
    document.getElementById("username").removeAttribute("readonly");
    document.getElementById("firstName").removeAttribute("readonly");
    document.getElementById("lastName").removeAttribute("readonly");
    document.getElementById("email").removeAttribute("readonly");
    document.getElementById("phone").removeAttribute("readonly");

    document.getElementById("saveButton").removeAttribute("disabled");
}
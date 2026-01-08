// Dashboard file explorer logic

document.addEventListener('DOMContentLoaded', function() {
    const uploadInput = document.getElementById('material-upload-input');
    const uploadForm = document.getElementById('material-upload-form');
    if (uploadForm && uploadInput) {
        uploadInput.addEventListener('change', function() {
            uploadForm.submit();
        });
    }
});

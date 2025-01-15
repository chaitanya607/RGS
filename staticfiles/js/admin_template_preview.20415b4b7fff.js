console.log("JavaScript file loaded");

document.addEventListener('DOMContentLoaded', function() {
    const templateField = document.querySelector('select[name="template"]');

    if (templateField) {
        templateField.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const templateContent = selectedOption.getAttribute('data-content') || 'No content available.';

            // Ensure the preview div exists in the DOM
            let previewDiv = document.getElementById('template-preview');
            if (!previewDiv) {
                previewDiv = document.createElement('div');
                previewDiv.id = 'template-preview';
                this.parentNode.appendChild(previewDiv);
            }

            previewDiv.innerHTML = templateContent;
        });
    }
});

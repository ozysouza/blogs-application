document.addEventListener('DOMContentLoaded', function() {
    ClassicEditor
        .create(document.querySelector('#ckeditor'), {
            toolbar: {
                items: [
                    'undo', 'redo', 'heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote', '|',
                    '|', 'imageUpload', 'mediaEmbed', '|', 'insertTable', 'tableColumn', 'tableRow', 'mergeTableCells',
                ]
            },
            language: 'en',
            table: {
                contentToolbar: [ 'tableColumn', 'tableRow', 'mergeTableCells' ]
            },
            licenseKey: '',
        })
        .then(ckeditor => {
            console.log('Editor was initialized', ckeditor);
        })
        .catch(error => {
            console.error(error.stack);
        });
});

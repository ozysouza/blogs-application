import {
    ClassicEditor,
    Essentials,
    Bold,
    Italic,
    Font,
    Paragraph,
    Undo,
    Heading,
    Link,
    List,
    BlockQuote,
    MediaEmbed,
    Table,
    TableToolbar,
} from 'ckeditor5';

// Initialize CKEditor with the desired plugins and toolbar items
document.addEventListener('DOMContentLoaded', function () {
    ClassicEditor
        .create(document.querySelector('#ckeditor'), {
            plugins: [
                Essentials, Bold, Italic, Font, Paragraph, Undo, Heading, Link, List,
                BlockQuote, MediaEmbed, Table, TableToolbar
            ],
            toolbar: {
                items: [
                    'undo', 'redo', 'heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', '|', 'mediaEmbed', '|',
                    'insertTable', 'tableColumn', 'tableRow', 'mergeTableCells'
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
            console.error('There was a problem initializing the editor.', error);
        });
});

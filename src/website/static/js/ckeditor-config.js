import {
    BlockQuote,
    Bold,
    ClassicEditor,
    Essentials,
    Font,
    Heading,
    Italic,
	Image,
	ImageCaption,
	ImageStyle,
	ImageToolbar,
	ImageInsert,
	ImageResize,
    Link,
    List,
    MediaEmbed,
    Paragraph,
    Table,
    TableToolbar,
    SimpleUploadAdapter,
    Undo
} from 'ckeditor5';

document.addEventListener('DOMContentLoaded', function () {
    ClassicEditor
        .create(document.querySelector('#ckeditor'), {
            plugins: [
                Bold, BlockQuote, Essentials, Font, Heading, Italic, Image, ImageCaption, ImageInsert, ImageResize, ImageStyle, ImageToolbar,
                Link, List, MediaEmbed, Paragraph, Table, TableToolbar, SimpleUploadAdapter, Undo
            ],
            toolbar: {
                items: [
                    'undo', 'redo', 'heading',
                    '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote',
                    '|', 'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor',
                    '|', 'imageInsert',
                    '|', 'mediaEmbed',
                    '|','insertTable', 'tableColumn', 'tableRow', 'mergeTableCells'
                ]
            },
            image: {
                toolbar: [
                    'toggleImageCaption',
                    'imageTextAlternative',
                    '|',
                    'imageStyle:inline',
                    'imageStyle:block',
                    'imageStyle:wrapText',
                    '|',
                    'resizeImage:25',
                    'resizeImage:50',
                    'resizeImage:original',
                ],
                resizeOptions: [
                    {
                        name: 'resizeImage:original',
                        value: null,
                        icon: 'original'
                    },
                    {
                        name: 'resizeImage:25',
                        value: '25',
                        icon: 'small'
                    },
                    {
                        name: 'resizeImage:50',
                        value: '50',
                        icon: 'medium'
                    }
                ],
                resizeUnit: '%'
            },
            table: {
                contentToolbar: [ 'tableColumn', 'tableRow', 'mergeTableCells' ]
            },
            simpleUpload: {
                uploadUrl: '/upload-image',
            },
             language: 'en',
        })
        .then(ckeditor => {
            console.log('Editor was initialized', ckeditor);
        })
        .catch(error => {
            console.error('There was a problem initializing the editor.', error);
        });
});

document.addEventListener('DOMContentLoaded', function () {
    ClassicEditor
        .create(document.querySelector('#commentCkeditor'), {
            plugins: [
                Bold, BlockQuote, Essentials, Font, Heading, Italic
            ],
            toolbar: {
                items: [
                    'undo', 'redo', 'heading',
                    '|', 'bold', 'italic', 'link', 'blockQuote'
                ]
            },
             language: 'en',
        })
        .then(ckeditor => {
            console.log('Editor was initialized', ckeditor);
        })
        .catch(error => {
            console.error('There was a problem initializing the editor.', error);
        });
});


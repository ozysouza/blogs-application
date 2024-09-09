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
	ImageUpload,
	ImageResize,
    Link,
    List,
    MediaEmbed,
    Paragraph,
    Table,
    TableToolbar,
    Undo
} from 'ckeditor5';

document.addEventListener('DOMContentLoaded', function () {
    ClassicEditor
        .create(document.querySelector('#ckeditor'), {
            plugins: [
                Essentials, Bold, Italic, Image, ImageInsert, ImageToolbar, ImageStyle, ImageCaption, ImageResize,
                Font, Paragraph, Undo, Heading, Link, List, BlockQuote, MediaEmbed, Table, TableToolbar
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
            language: 'en',
            table: {
                contentToolbar: [ 'tableColumn', 'tableRow', 'mergeTableCells' ]
            },
        })
        .then(ckeditor => {
            console.log('Editor was initialized', ckeditor);
        })
        .catch(error => {
            console.error('There was a problem initializing the editor.', error);
        });
});

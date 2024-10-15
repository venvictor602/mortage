/* FORM WIZARD VALIDATION SIGN UP ======================================== */

jQuery(function ($) {
    "use strict";

    // Update the form action to point to the Django route
    $('form#custom').attr('action', "{%url 'upload-repayment'%}");

    $('#custom').stepy({
        backLabel: 'Previous',
        block: true,
        errorImage: false,
        nextLabel: 'Next',
        titleClick: true,
        description: true,
        legend: false,
        validate: true
    });


    $('#custom').validate({

        errorPlacement: function(error, element) {
            $('#custom .stepy-error').append(error);
        },
        rules: {
            'firstname': 'required',
            'lastname': 'required',
            'email': 'required',
            'telephone': 'required',
            'address': 'required',
            'city': 'required',
            'zip_code': 'required',
            'country': 'required',
            'terms': 'required' // BE CAREFUL: last has no comma
        },
        messages: {
            'firstname': { required: 'Name required' },
            'lastname': { required: 'Last name required' },
            'email': { required: 'Invalid e-mail!' },
            'telephone': { required: 'Telephone required' },
            'address': { required: 'Address required' },
            'city': { required: 'City required' },
            'zip_code': { required: 'Zip code required' },
            'country': { required: 'Country required' },
            'terms': { required: 'Please accept terms' },
        },
        submitHandler: function(form){
            // Ensure CSRF token is included in the submission
            const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
            
            if (csrfToken) {
                // Add CSRF token to form submission
                $('<input>').attr({
                    type: 'hidden',
                    name: 'csrfmiddlewaretoken',
                    value: csrfToken
                }).appendTo(form);
            }
            
            // Check if the honeypot field is empty (anti-spam measure)
            if ($('input#website').val().length == 0) {
                form.submit(); // If everything is valid, submit the form
            }
        }
    });

});

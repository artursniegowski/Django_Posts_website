"use strict";
// To solve the CSRF token error while trying to create a post
// CRSF - tokens are cookies - so we can set it accordingly
// so we can get the cookie, and set the request header to use X-CSRFToken
// so if we in the future make an ajax request we dont have to apply crsf token 
// to all of our ajax requests 
// Ajax token is goign to be set on the cookie , so we dont have to set it on every singel Ajax request 
$.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;


            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');

                for (let i = 0; i < cookies.length; i += 1) {
                    const cookie = jQuery.trim(cookies[i]);

                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }

            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    },
});

// 
// Togling a modal !
// with javascript
// selecting element with class js-toggle-modal and adding two eventlistene on click
const $modal_element = $(".js-modal");
const $modal_text_element = $(".js-post-text");
$(document).on("click", ".js-toggle-modal", function(e) {
    // preventing the main event which here is click on the link to happen
    e.preventDefault() // so if it is a link dont do go anywhere, dont do anything

    // making the modal to appear reappear
    $modal_element.toggleClass("hidden")
})
.on("click", ".js-submit", function(e) {
    e.preventDefault() // preventing natural behaior on the browser

    const textToPost = $modal_text_element.val().trim()
    // selecting the button that was just clicked
    const $btn_submit = $(this)
    
    // if text empty
    if(!textToPost.length) {
        return false
    }
    
    
    // setting properties of the clicked button
    // disabling it and adding replacing text to posting
    $btn_submit.prop("disabled", true).text("Posting!")
    $.ajax({
        type: 'POST',
        url: $modal_text_element.data("post-url"), // similar to console.log($modal_text_element.attr("data-post-url"))
        data: {
            text: textToPost,
        },
        success: (dataHtml) => { // it will return some html
            $modal_element.addClass("hidden"); // making the modal to disapear
            $("#posts-container").prepend(dataHtml); // add some html to index.html returned from the success 
            // enabling the posting buttona and changign its name to org vvalue
            $btn_submit.prop("disabled", false).text("Create Post"); 
            $modal_text_element.val(""); // erase the value in the text modal
        },
        error: (error) => {
            console.warn(error);
            $btn_submit.prop("disabled", false).text("Error"); 
        },
    })
})
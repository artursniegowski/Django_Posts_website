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

// Modal create a post !! 
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
.on("click", ".js-submit", function(e) {  // clicking the submit button on the modal
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
        // data can be cahed and attr cant. make sense to use data on kind of const data
        // that dosent change and to sue attr on data that will be changed
        url: $modal_text_element.data("post-url"), // similar to $modal_text_element.attr("data-post-url")
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
// Following button
// adding another chained event listener for the follow profile button
.on("click", "#js-follow-button-detail-user", function (e) { 
    e.preventDefault() // preventing a link to go anywehre or a button from submititng a form
                        // preventing its natuaral behaviour

    // grabing the following button
    // const $followUserButton = $("#js-follow-button-detail-user");
    // instead we can use this bc we alredy grabbed the button with the eventlistener !
    const follow_action = $(this).attr("data-action-for-following")

    // ajaxing data to our database  
    $.ajax({
        type: 'POST',
        url: $(this).data("follow-url"), // similar to $("#js-follow-button-detail-user").attr("data-follow-url")
        data: {
            // .data("user-name") - when we use data it is going to be cacheed - so it wont work if we change it in the future
            // this is why we have to use attr bc we will change the value !
            follow_action: follow_action, //.data("action-for-following")
            // and here we can use data and this can be cached bc user-name will not change and this is why it wont be a prblem
            // if the user-name will be cached
            username_to_follow: $(this).data("user-name"), //.attr("data-user-name")
        },
        success: (data) => { // it will return some data in json format
            $("#js-follow-button-text").text(data.wording) // chanign text of the button
            if (follow_action == 'follow') {
                // change wording to unfollow
                $(this).attr("data-action-for-following",'unfollow')

            } else {
                // change the wording to follow
                $(this).attr("data-action-for-following",'follow')

            }

            // init the value of followers
            $("#js-total-number-of-followers").text(data['followers'])

        },
        error: (error) => {
            console.warn(error);
        },
    })
}) 
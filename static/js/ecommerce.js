 $(document).ready(function(){
            <!-- Contact Form Handler -->
            var contactForm = $('.contact-form')
            var contactFormMethod = contactForm.attr('method')
            var contactFormEndPoint = contactForm.attr('action')
            var thisForm = $(this)

            function displaySubmitStatus(submitButton, defaultText, doSubmit){
                if (doSubmit){
                    submitButton.addClass('disabled')
                    submitButton.html('<i class="fa fa-spin fa-spinner"></i> Submiting...')

                }else{
                    submitButton.addClass('disabled')
                    submitButton.html(defaultText)
                }

            }
            contactForm.submit(function(event){
                var contactFormSubmitButton = contactForm.find('[type="submit"]')
                var contactFormSubmitButtonText = contactFormSubmitButton.text()

                event.preventDefault()

                displaySubmitStatus(contactFormSubmitButton, '', true)

                var contactFormData = contactForm.serialize()
                $.ajax({
                    method:contactFormMethod,
                    url:contactFormEndPoint,
                    data:contactFormData,


                    success: function(data){
                        contactForm[0].reset()
                        $.alert({
                            theme: 'supervan',
                            title: 'Alert!',
                            content: 'Message Sent Successfully',
                        })
                        setTimeout(function(){
                            displaySubmitStatus(contactFormSubmitButton, contactFormSubmitButtonText, false)
                        }, 500)

                    },
                    error: function(error){
                        console.log(error.responseJSON)
                        var jsonResponseErrorData = error.responseJSON
                        var msg
                        $.each(jsonResponseErrorData, function(key, value){
                            msg += key + ': ' + value[0].message + '<br/>'
                        })
                        $.alert({
                            theme: 'supervan',
                            title: 'Alert!',
                            content: msg,
                        })
                        setTimeout(function(){
                            displaySubmitStatus(contactFormSubmitButton, contactFormSubmitButtonText, false)
                        }, 500)

                    }
                })
            })

            <!-- Search Form -->
            var searchForm = $('.search-form')
            var searchInput = searchForm.find('[name="q"]')
            var typingTimer
            var typingInterval = 500

            var searchButton = searchForm.find('[type="submit"]')

            searchInput.keyup(function(event){
                clearTimeout(typingTimer)
                typingTimer = setTimeout(doAutoSerch, typingInterval)

            })
            searchInput.keydown(function(event){
                clearTimeout(typingTimer)

            })

            function displaySpinner(){
                searchButton.addClass('disabled')
                searchButton.html('<i class="fa fa-spin fa-spinner"></i> Searching...')
            }

            function doAutoSerch(){
                displaySpinner()
                var query = searchInput.val()
                setTimeout(function(){
                    window.location.href = '/search/?q=' + query
                }, 1000)


            }

            <!-- Cart and Add Products Handler -->
            var productUpdateForm = $('.update-cart-form')
            productUpdateForm.submit(function(event){
            event.preventDefault()

                var thisForm = $(this)
                var action = thisForm.attr('data-endpoint')
                var formMethod = thisForm.attr('method')
                var formData = thisForm.serialize()
                var submitSpan = thisForm.find('.submit-span')

                $.ajax({
                    url: action,
                    method: formMethod,
                    data: formData,
                    success: function(data){


                        if (data.productAdded){
                            submitSpan.html(' In Cart <button class="btn btn-link" type="submit">Remove?</button> ')

                        }else if(data.productRemoved) {
                            submitSpan.html(' <button class="btn btn-success" type="submit">Add To Cart</button> ')
                        }


                        var currentPath = window.location.href

                        if(currentPath.indexOf('cart') != -1){

                            refreshCart()
                        }
                        var cartCount = $('.cart-count')
                        cartCount.text(data.CartItemCount)

                    },
                    error: function(errorData){

                        console.log('Error')
                        console.log(errorData)
                        $.alert({
                            theme: 'supervan',
                            title: 'Alert!',
                            content: msg,
                        })

                    }


                 })
            })

            function refreshCart(){

                var cartTable = $('.cart-table')
                var cartBody = cartTable.find('.cart-body')
                var productFields = cartBody.find('.cart-product-fields')

                var refreshCartUrl = 'api/cart/'
                var data = {};
                var refreshCartMethod = 'GET'
                var currentUrl = window.location.href

                $.ajax({
                    url: refreshCartUrl,
                    method: refreshCartMethod,
                    data: data,
                    success: function(data){

                        var cartItemRemoveForm = $('.remove-cart-items-form')

                        if(data.products.length > 0){
                            cartBody.find('.cart-subtotal').text(data.subtotal)
                            cartBody.find('.cart-total').text(data.total)
                             i = data.products.length

                            productFields.html('')
                            $.each(data.products, function(index, value){
                            console.log(value)
                            var newCartItemRemoveForm = cartItemRemoveForm.clone()
                            newCartItemRemoveForm.css('display', 'block')
                            newCartItemRemoveForm.find('.cart-item-product-id').val(value.id)

                             cartBody.prepend('<tr> <th scope=\"row\">' + i +  '</th> <td><a href="' + value.url + '">' + value.object_title + '</a>' + newCartItemRemoveForm.html() + '</td>' + '<td>' + value.object_price + '</td></tr>')

                             i--

                            })

                        }else{

                            window.location.href = currentUrl


                        }

                        console.log('Success...')
                        console.log(data)

                    },
                    error: function(errorData){

                        console.log('Error Encountered...')
                        console.log(errorData)

                    }

                })

            }
        })
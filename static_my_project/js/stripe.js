$(document).ready(function(){

var stripeFormModule = $('.stripe-payment-form')
var stripeModuleToken = stripeFormModule.attr('data-token')
var stripeModuleNextUrl = stripeFormModule.attr('data-next-url')
var stripeModuleButtonTitle = stripeFormModule.attr('btn-title') || 'Submit Card Details'
var stripeTemplate = $.templates('#stripeTemplate')
var stripeTemplateDataContext = {

    name: 'Stripe',
    nextUrl: stripeModuleNextUrl,
    publicKey: stripeModuleToken,
    buttonTitle: stripeModuleButtonTitle

}
var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
stripeFormModule.html(stripeTemplateHtml)

var paymentForm = $('.payment-form')

if (paymentForm == 1){

var pubKey = paymentForm.attr('data-token')
var nextUrl = paymentForm.attr('data-next-url')


// Create a Stripe client.
var stripe = Stripe(pubKey);

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element.
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.on('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission.
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();

  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      // Send the token to your server.
      stripeTokenHandler(nextUrl, result.token);
    }
  });
});

function redirectToNext(nextpath, timeOffSet){
    if(nextpath){
        setTimeout(function(){
            window.location.href = nextpath
        }, timeOffSet)
    }
}

// Submit the form with the token ID.
function stripeTokenHandler(nextUrl, token) {

    var paymentMethodEndPoint = '/stripe/create'

    var data = {
        'token': token.id

    }

    $.ajax({
        data: data,
        url: paymentMethodEndPoint,
        method: 'POST',
        success: function(data){
            var successMessage = data.message || 'Success, Card Added Successfully'
            card.clear()
            if(nextUrl){
                successMessage = successMessage + "<br/><br/> <i class = 'fa fa-spin fa fa-spinner'> </i> Redirecting..."
            }
            if ($.alert){
                $.alert(successMessage)

            }else{
                alert(successMessage)
            }
            redirectToNext(nextUrl, 1500)
        },
        error: function(error){
            console.log(error)
        }


    })

  // Insert the token ID into the form so it gets submitted to the server
  var form = document.getElementById('payment-form');
  var hiddenInput = document.createElement('input');
  hiddenInput.setAttribute('type', 'hidden');
  hiddenInput.setAttribute('name', 'stripeToken');
  hiddenInput.setAttribute('value', token.id);
  form.appendChild(hiddenInput);

  // Submit the form
  form.submit();
}



}

})

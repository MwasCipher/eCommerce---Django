//$(document).ready(function(){
//
//var stripeFormModule = $('.stripe-payment-form')
//var stripeModuleToken = stripeFormModule.attr('data-token')
//var stripeModuleNextUrl = stripeFormModule.attr('data-next-url')
//var stripeModuleButtonTitle = stripeFormModule.attr('btn-title') || 'Submit Card Details'
//var stripeTemplate = $.templates('#stripeTemplate')
//var stripeTemplateDataContext = {
//
//    name: 'Stripe',
//    next_url: stripeModuleNextUrl,
//    public_key: stripeModuleToken,
//    buttonTitle: stripeModuleButtonTitle
//
//}
//var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
//stripeFormModule.html(stripeTemplateHtml)
//
//var paymentForm = $('.payment-form')
//
//if (paymentForm == 1){
//
//var pubKey = paymentForm.attr('data-token')
//var nextUrl = paymentForm.attr('data-next-url')
//
//
//// Create a Stripe client.
//var stripe = Stripe(pubKey);
//
//// Create an instance of Elements.
//var elements = stripe.elements();
//
//// Custom styling can be passed to options when creating an Element.
//// (Note that this demo uses a wider set of styles than the guide below.)
//var style = {
//  base: {
//    color: '#32325d',
//    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
//    fontSmoothing: 'antialiased',
//    fontSize: '16px',
//    '::placeholder': {
//      color: '#aab7c4'
//    }
//  },
//  invalid: {
//    color: '#fa755a',
//    iconColor: '#fa755a'
//  }
//};
//
//// Create an instance of the card Element.
//var card = elements.create('card', {style: style});
//
//// Add an instance of the card Element into the `card-element` <div>.
//card.mount('#card-element');
//
//// Handle real-time validation errors from the card Element.
//card.on('change', function(event) {
//  var displayError = document.getElementById('card-errors');
//  if (event.error) {
//    displayError.textContent = event.error.message;
//  } else {
//    displayError.textContent = '';
//  }
//});
//
//// Handle form submission.
////var form = document.getElementById('payment-form');
////form.addEventListener('submit', function(event) {
////  event.preventDefault();
////
////  var loadingButton = $('.btn-load')
////
////  var loadTime = 1500
////  var errorHtml = '<i class="fa fa-warning"></i>An Error Occurred'
////  var LoadingHtml = '<i class="fa fa-spin fa-spinner">Loading...</i>'
////  var errorClass = 'class="btn btn-danger disabled my-3" '
////  var loadingClass = 'class="btn btn-success disabled my-3" '
////
////  stripe.createToken(card).then(function(result) {
////    if (result.error) {
////      // Inform the user if there was an error.
////      var errorElement = document.getElementById('card-errors');
////      errorElement.textContent = result.error.message;
////    } else {
////      // Send the token to your server.
////      stripeTokenHandler(nextUrl, result.token);
////    }
////  });
////});
//var form = $('#payment-form');
//var loadingButton = form.find('.btn-load')
//var loadingButtonDefaultHtml = loadingButton.html()
//var loadingButtonDefaultClasses = loadingButton.attr('class')
//
//
//form.on('submit', function(event) {
//  event.preventDefault();
//  var $this = $(this)
//  var loadingButton = $this.find('.btn-load')
//  loadingButton.blur()
//
//  var loadTime = 1500
//  var currentTimeout
//  var errorHtml = '<i class="fa fa-warning"></i>An Error Occurred'
//  var LoadingHtml = '<i class="fa fa-spin fa-spinner">Loading...</i>'
//  var errorClass = 'class="btn btn-danger disabled my-3" '
//  var loadingClass = 'class="btn btn-success disabled my-3" '
//
//  stripe.createToken(card).then(function(result) {
//    if (result.error) {
//      // Inform the user if there was an error.
//      var errorElement = $('#card-errors');
//      errorElement.textContent = result.error.message;
//      currentTimeout = displayButtonStatus(loadingButton, errorHtml, errorClass, 1000, currentTimeout)
//    } else {
//        currentTimeout = displayButtonStatus(loadingButton, loadingHtml, loadingClass, 2000, currentTimeout)
//      // Send the token to your server.
//      stripeTokenHandler(nextUrl, result.token);
//    }
//  });
//});
//
//function displayButtonStatus(element, newHtml, newClasses, loadTime, timeout){
////    if(timeout){
////    clearTimeout(timeout)
////
////    }
//    if(!loadTime){
//        loadTime = 1500
//    }
////    var defaultHtml = element.html()
////    var defaultClasses = element.attr('class')
//    element.html(newHtml)
//    element.removeClass(loadingButtonDefaultClasses)
//    element.addClass(newClasses)
//
//    setTimeout(function(){
//
//        element.html(loadingButtonDefaultHtml)
//        element.addClass(loadingButtonDefaultClasses)
//        element.removeClass(newClasses)
//
//
//    }, loadTime)
//
//}
//
//function redirectToNext(nextpath, timeOffSet){
//    if(nextpath){
//        setTimeout(function(){
//            window.location.href = nextpath
//        }, timeOffSet)
//    }
//}
//
//// Submit the form with the token ID.
//function stripeTokenHandler(nextUrl, token) {
//
//    var paymentMethodEndPoint = '/stripe/create'
//
//    var data = {
//        'token': token.id
//
//    }
//
//    $.ajax({
//        data: data,
//        url: paymentMethodEndPoint,
//        method: 'POST',
//        success: function(data){
//            var successMessage = data.message || 'Success, Card Added Successfully'
//            card.clear()
//            if(nextUrl){
//                successMessage = successMessage + "<br/><br/> <i class = 'fa fa-spin fa fa-spinner'> </i> Redirecting..."
//            }
//            if ($.alert){
//                $.alert(successMessage)
//
//            }else{
//                alert(successMessage)
//            }
//
//            loadingButton.html(loadingButtonDefaultHtml)
//            loadingButton.attr('class', loadingButtonDefaultClasses)
//            redirectToNext(nextUrl, 1500)
//        },
//        error: function(error){
//            $alert({'title': 'An Error Occurred', 'content': 'Please ReEnter Card Details Again...' })
//            loadingButton.html(loadingButtonDefaultHtml)
//            loadingButton.attr('class', loadingButtonDefaultClasses)
//            console.log(error)
//        }
//
//
//    })
//
//  // Insert the token ID into the form so it gets submitted to the server
//  var form = document.getElementById('payment-form');
//  var hiddenInput = document.createElement('input');
//  hiddenInput.setAttribute('type', 'hidden');
//  hiddenInput.setAttribute('name', 'stripeToken');
//  hiddenInput.setAttribute('value', token.id);
//  form.appendChild(hiddenInput);
//
//  // Submit the form
//  form.submit();
//}
//
//
//
//}
//
//})

$(document).ready(function(){

var stripe;
var orderData = {
  items: [{ id: "photo-subscription" }],
  currency: "usd"
};

// Disable the button until we have Stripe set up on the page
document.querySelector("button").disabled = true;

fetch("/stripe-key")
  .then(function(result) {
    return result.json();
  })
  .then(function(data) {
    return setupElements(data);
  })
  .then(function({ stripe, card, clientSecret }) {
    document.querySelector("button").disabled = false;

    var form = document.getElementById("payment-form");
    form.addEventListener("submit", function(event) {
      event.preventDefault();
      pay(stripe, card, clientSecret);
    });
  });

var setupElements = function(data) {
  stripe = Stripe(data.publishableKey);
  /* ------- Set up Stripe Elements to use in checkout form ------- */
  var elements = stripe.elements();
  var style = {
    base: {
      color: "#32325d",
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "16px",
      "::placeholder": {
        color: "#aab7c4"
      }
    },
    invalid: {
      color: "#fa755a",
      iconColor: "#fa755a"
    }
  };

  var card = elements.create("card", { style: style });
  card.mount("#card-element");

  return {
    stripe: stripe,
    card: card,
    clientSecret: data.clientSecret
  };
};

var handleAction = function(clientSecret) {
  stripe.handleCardAction(clientSecret).then(function(data) {
    if (data.error) {
      showError("Your card was not authenticated, please try again");
    } else if (data.paymentIntent.status === "requires_confirmation") {
      fetch("/pay", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          paymentIntentId: data.paymentIntent.id
        })
      })
        .then(function(result) {
          return result.json();
        })
        .then(function(json) {
          if (json.error) {
            showError(json.error);
          } else {
            orderComplete(clientSecret);
          }
        });
    }
  });
};

/*
 * Collect card details and pay for the order
 */
var pay = function(stripe, card) {
  changeLoadingState(true);

  // Collects card details and creates a PaymentMethod
  stripe
    .createPaymentMethod("card", card)
    .then(function(result) {
      if (result.error) {
        showError(result.error.message);
      } else {
        orderData.paymentMethodId = result.paymentMethod.id;

        return fetch("/pay", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(orderData)
        });
      }
    })
    .then(function(result) {
      return result.json();
    })
    .then(function(response) {
      if (response.error) {
        showError(response.error);
      } else if (response.requiresAction) {
        // Request authentication
        handleAction(response.clientSecret);
      } else {
        orderComplete(response.clientSecret);
      }
    });
};

/* ------- Post-payment helpers ------- */

/* Shows a success / error message when the payment is complete */
var orderComplete = function(clientSecret) {
  stripe.retrievePaymentIntent(clientSecret).then(function(result) {
    var paymentIntent = result.paymentIntent;
    var paymentIntentJson = JSON.stringify(paymentIntent, null, 2);

    document.querySelector(".sr-payment-form").classList.add("hidden");
    document.querySelector("pre").textContent = paymentIntentJson;

    document.querySelector(".sr-result").classList.remove("hidden");
    setTimeout(function() {
      document.querySelector(".sr-result").classList.add("expand");
    }, 200);

    changeLoadingState(false);
  });
};

var showError = function(errorMsgText) {
  changeLoadingState(false);
  var errorMsg = document.querySelector(".sr-field-error");
  errorMsg.textContent = errorMsgText;
  setTimeout(function() {
    errorMsg.textContent = "";
  }, 4000);
};

// Show a spinner on payment submission
var changeLoadingState = function(isLoading) {
  if (isLoading) {
    document.querySelector("button").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("button").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
};

})

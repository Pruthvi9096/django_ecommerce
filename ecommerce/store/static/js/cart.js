var updateButtons = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateButtons.length; i++) {
    updateButtons[i].addEventListener('click', function () {
        let productId = this.dataset.product;
        let action = this.dataset.action;

        if (user === 'AnonymousUser') {
            addCookieItem(productId, action);
        }
        else {
            updateCartItem(productId, action);
        }
    })
}

function addCookieItem(productId,action){
    if (action == "add") {
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':1};
        }
        else{
            cart[productId]['quantity'] += 1;
        }
    }
    if (action == "remove") {
        cart[productId]['quantity'] -= 1;
        if (cart[productId]['quantity'] <= 0){
            delete cart[productId];
        }
    }
    document.cookie = "cart="+JSON.stringify(cart)+";domain=;path=/"
    location.reload();
    
}

function updateCartItem(productId, action) {
    console.log(productId, action);

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log(data);
            location.reload();
        })

}

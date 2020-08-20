
var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var product_id = this.dataset.product
        var action = this.dataset.action

        console.log('product_id:',
         product_id, 'Action:', action)

        // Authenticate the user
        console.log('USER:', user)
        if (user == 'AnonymousUser'){
            add_cookie_item(product_id, action)
        }else{
            update_user_order(product_id, action)
        }

    })
} // for ends

// Get items from cookie
function add_cookie_item(product_id, action){
    console.log('User is not authenticated.');
    
    // add item 
    if (action == 'add'){
        if (cart[product_id] == undefined){
            cart[product_id] = {'quantity':1}
        }else{
            cart[product_id]['quantity'] += 1
        }
    } // add item if ends


    // remove item
    if (action == 'remove'){
        
        cart[product_id]['quantity'] -= 1

        if (cart[product_id]['quantity'] <= 0){
            console.log('Item should be deleted');
            delete cart[product_id];
        }
    } // remove item if ends

    console.log('Car:', cart);
    // overide the cookie
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload()

 } //add_cookie_item func ends 


function update_user_order(product_id, action){
    console.log('User is authenticated, sending data...')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'product_id':product_id, 'action':action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('Data: ', data)
        location.reload()
    });


} // func ends

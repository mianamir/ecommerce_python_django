
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
            console.log('User is not authenticated.')
        }else{
            update_user_order(product_id, action)
        }

    })
} // for ends

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

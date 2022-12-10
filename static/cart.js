document.addEventListener("DOMContentLoaded", function (){
    let btns = document.getElementsByClassName('addtocart');
        for (let i = 0; i <btns.length; i++) {
            btns[i].addEventListener('click', function (event) {
                 let productId = this.dataset.product
                 let action = this.dataset.action
                location.reload()
                 console.log('poductId:', productId, 'action:', action)
                 console.log('USER:', user)
                if (user === 'AnonymousUser') {
                    console.log('User not logged')
                }else{
                    updateCart(productId, action)
                }
            })
        }}
)

function updateCart(productId, action) {
    console.log('sending data')
    var url = '/update_cart/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
    })
}
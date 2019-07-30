var buscar = (function(){
    var pintar_data = function (data) {
        div = document.getElementById('result');
        div.innerHTML = ""
        ul = document.createElement('ul');
        link = location.pathname + 'add/';

        for(let elem of data) {
            href = link + elem.username + '/'
            li = document.createElement('li')
            a = document.createElement('a');
            a.href = href 
            a.text = "Agregar"
            li.innerHTML = elem.username 
            li.appendChild(a)
            ul.appendChild(li)
        }
    
        div.appendChild(ul)
    }
    
    
    let form = document.getElementById("form-search-user");
    let url = form.getAttribute('action');
    let username = form.username.value;
    url = `${url}?username=${username}`
    
    fetch(url, {
        method: 'GET'
    })
        .then(data => {
            return data.json()
        })
        .then(d => {
            pintar_data(d)
        })
        .catch(err => {
            console.log("error")
        })
})
let btn = document.getElementById('btnBuscar')
btn.onclick = buscar


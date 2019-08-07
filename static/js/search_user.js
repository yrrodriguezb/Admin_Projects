var buscar = (function(){
    var template = `
    <div class="tags has-addons has-margin-t-6">
        <span class="tag is-info">{{ username }}</span>
        <a class="tag" href="{{ href }}">
            <span class="icon has-text-info">
                <i class="fas fa-plus"></i>
            </span>
        </a>
    </div>
    `;

    var pintar_data = function (data) {
        div = document.getElementById('result');
        div.innerHTML = ""
        
        link = location.pathname + 'add/';

        for(let elem of data) {
            href = link + elem.username + '/'

            t = template
                .replace('{{ username }}', elem.username)
                .replace('{{ href }}', href);
            
            div.innerHTML += t; 
        }
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
            console.log("Error: ", err)
        })
})
let btn = document.getElementById('btnBuscar')
btn.onclick = buscar


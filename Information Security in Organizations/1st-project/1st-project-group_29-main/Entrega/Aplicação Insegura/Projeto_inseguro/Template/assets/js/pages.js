// About ---------------------------------------------------------------------------------------------------------------------
function about() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/about")

    xhr.onreadystatechange = () => {                                            
        // Call a function when the state changes.
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            //open( xhr.response ); //abre uma janela vazia só (do open, o xhr.response é o texto/html do products.html)     
            window.location = 'http://127.0.0.1:13000/about' 

        }
    }
    xhr.send()
}
// Inicio ---------------------------------------------------------------------------------------------------------------------
function inicio() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/index")

    xhr.onreadystatechange = () => {                                            
        // Call a function when the state changes.
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            //open( xhr.response ); //abre uma janela vazia só (do open, o xhr.response é o texto/html do products.html)     
            window.location = 'http://127.0.0.1:13000/inicio'

        }
    }
    xhr.send()

}
//Login --------------------------------------------------------------------------------------------------------------------

function login() {
window.location = 'http://127.0.0.1:13000/' 
}

// Shop --------------------------------------------------------------------------------------------------------------------
function products() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/products")

    xhr.onreadystatechange = () => {                                            
        // Call a function when the state changes.
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            //open( xhr.response ); //abre uma janela vazia só (do open, o xhr.response é o texto/html do products.html)     
            window.location = 'http://127.0.0.1:13000/products' 

        }
    }
    xhr.send()
}


// Contactos ---------------------------------------------------------------------------------------------------------------------

function contact() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/contact")

    xhr.onreadystatechange = () => {                                            
        // Call a function when the state changes.
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            //open( xhr.response ); //abre uma janela vazia só (do open, o xhr.response é o texto/html do products.html)     
            window.location = 'http://127.0.0.1:13000/contact' 

        }
    }
    xhr.send()
}

// logout -----------------------------------------------------------------------------------------------------------------------
function logout() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/logout")

    xhr.onreadystatechange = () => {                                            
        // Call a function when the state changes.
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            //open( xhr.response ); //abre uma janela vazia só (do open, o xhr.response é o texto/html do products.html)     
            window.location = 'http://127.0.0.1:13000/' 

        }
    }
    xhr.send()
}

// cart -------------------------------------------------------------------------------------------------------------------------

function cart() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/cart")

    xhr.onreadystatechange = () => {                                            
        // Call a function when the state changes.
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            //open( xhr.response ); //abre uma janela vazia só (do open, o xhr.response é o texto/html do products.html)     
            window.location = 'http://127.0.0.1:13000/cart' 

        }
    }
    xhr.send()
}
// profile ------------------------------------------------------------------------------------------------------------------------

function profile() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/profile")

    xhr.onreadystatechange = () => {                                            
        // Call a function when the state changes.
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            //open( xhr.response ); //abre uma janela vazia só (do open, o xhr.response é o texto/html do products.html)     
            window.location = 'http://127.0.0.1:13000/profile' 

        }
    }
    xhr.send()
}



// atualizar o nome de utilizador na respetiva caixa de texto
function update_username() {
    var algo;
    xhr = new XMLHttpRequest();
    xhr.open("GET", "/session_checker")

    xhr.onreadystatechange = () => {                                            
    
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            response = JSON.parse( xhr.response );  
            //algo = response.username
            document.getElementById("username").value=response.username;
            //return algo               //não dá para retorna um valor em concreto duma função assíncrona, porque pelo tempo que o readystatechange mudar, já a função retornou algo. Só dá para chamar outras funções ou fazer alerts do valor recebido assincronamente, porque podem e são invocaddas quando o readystatechange muda, enquanto que o return só pode ocorrer uma vez e ocorre antes dessa condição
        }
    }
    xhr.send();
}

// ler o que foi inserido nos campos de texto
function get_password_values() {

    new_pw = document.getElementById("new_password").value
        if(new_pw != null && new_pw != "") {
            get_user_name_and_id_password( new_pw ) 
        }
        else {
            alert("Os dois campos da nova password não são indênticos.")
        }

}

// obter id e nome do utilizador a partir da sessão atual
function get_user_name_and_id_password( new_pw ) {
    xhr = new XMLHttpRequest();
    xhr.open("GET", "/session_checker")

    xhr.onreadystatechange = () => {                                            
    
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            response = JSON.parse( xhr.response );  
            change_password(response.userID, new_pw)
        }
    }
    xhr.send();
}


// pedir ao ao servidor para mudar password
function change_password(user_id, new_pw) {
    xhr = new XMLHttpRequest();
    xhr.open("POST", "/change_password")



    var data = new FormData();
    data.append("user_id", user_id)
    data.append("new_pw", new_pw)
    xhr.send(data)

    xhr.onreadystatechange = () => {                                            
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            response = JSON.parse( xhr.response );  
            if (response.status == true) {
                alert(response.result)
                logout()
                window.location = 'http://127.0.0.1:13000/inicio'
            }
            else {
                alert(response.result)
            }
        }
    }

}
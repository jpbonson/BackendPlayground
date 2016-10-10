//// JavaScript

alert("Olá mundo!");

//


var nomedavariavel = null; // O valor null é um literal em JavaScript que representa um valor nulo ou "vazio" (ex: que aponta para um objeto que existe, mas com valor inexistente).

var nomedavariavel = undefined; // Representa um valor indefinido. Objetos inexistentes são undefined. O tipo undefinied é retornado caso uma propriedade de um determinado objeto seja consultada e não exista.

//

var frutas =['uva', 'maçã', 'tomate'];

console.log(frutas[0]);
console.log(frutas[1]);
console.log(frutas.length); // 3

frutas.forEach( function(item) {
console.log(item);
});

//

var clicado =false;

// ATENÇÃO: Não confunda os valores primitivos Boolean true e false com os valores true e false do objeto Boolean. Todo objeto no JS mesmo vazio retorna true.
// Primitivos: var a= false;
// Objeto Boolean: var b= new Boolean(false);
// Qualquer objeto cujo o valor não é undefined ou null, incluindo um objeto Boolean que o valor seja false, é avaliado para true quando passa por uma declaração condicional.
if(a){ //nao vai rodar };
if(b){ //este vai rodar};

//

var meuAviao ={};
var meuAviao = new Object(); // Criando um objeto

meuAviao.fabricante ="Airbus"; // Criando uma propriedade e atribuindo um valor para ela
meuAviao.modelo ="A380";
meuAviao.ano =2012;

meuAviao["fabricante"] ="Airbus";
meuAviao["modelo"] ="A380";
meuAviao["ano"] =2012;

// Métodos de Criação do Objeto:
// 1.Usando inicializadores de objeto
// 1.Usando uma função construtora
// 1.Usando o método Object.create

var palavra ="JS4Girls";
palavra.length // 8
var subtitulo = " -Aula de JS e Acessibilidade na Web";
palavra += subtitulo; //"JS4Girls -Aula de JS e Acessibilidade na Web"
typeof palavra; // "string"
palavra[1]; // S

//

function multiplicar(x, y) {
    return x*y;
}
console.log("resultado: "+multiplicar(10, 5));

//

blah = !(x && y) || z;
test = (10 > 7) || (9 == 9);

//

== // Verdadeiro se a for igual a b
!= // Verdadeiro se a não for igual a b
=== // Verdadeiro se a for igual a b e for do mesmo tipo
!== // Verdadeiro se a não for igual a b, ou eles não são do mesmo tipo
<
>
<=
>=

//

1+1
1-1
1*1
1/1
1%1
Math.pow(4, 3);

//

var maria = true;
if(maria == true) {
    console.log("Oi, Maria!");
}else{
    console.log("Nome falso!");
}

//

var estadoCivil = prompt("Qual seu estado civil?");
switch(estadoCivil) {
    case'solteira':
        console.log("Bora pra festa?");
    break;
    case'casada':
        console.log("Parabéns pelo casamento!");
    break;
    case'divorciada':
        console.log("Deve ser um alívio!");
    break;
    case'viúva':
        console.log("Meus pesames!");
    break;
    default:console.log("Complicado");
}

//

var numero =1;
while(numero <=10) {
    console.log(numero);
    numero++;
}

//

var numero =1;
do {
    console.log(numero);
    numero++;
}while(numero <=10);

//

for (var numero =1; numero <=10; numero++) {
    console.log(numero);
}


//// DOM

var selecionaElemento = document.getElementById('id-do-elemento');
var list = document.getElementsByTagName("UL")[0];
var x = document.getElementsByClassName("example");
var selecionaElemento = document.getElementsByName('namedoinput');
document.querySelector(".example").style.backgroundColor= "red";
var x = document.querySelectorAll(".example");

//

<script type="text/javascript">
    function nameMyFunction() {
        document.getElementById("test").innerHTML= "Parágrafo modificado";
    }
</script>
<p id="test" onclick="nameMyFunction()">Clique e mude o conteúdo do elemento.</p>

//

<script type="text/javascript">
    function nameMyFunction2() {
        var getInputValue = document.getElementById("name").value;
        alert("Esse é o valor do input: "+ getInputValue);
    }
</script>
Escreva algo no input: <input type="text" id="name" />
<input type="submit" value="Capturar o valor do input." id="test2" onclick="nameMyFunction2()" />

//

// Eventos:
// ❖Um clique no mouse (onclick)
// ❖O carregamento de uma página ou imagem web (onLoad)
// ❖Quando o mouse passa sobre um anúncio em uma página web (onmouseover)
// ❖Selecionar um campo de entrada em um formulário HTML (onfocus)
// ❖Submeter um formulário HTML (onsubmit)
// ❖Pressionar uma tecla (onkeydown)

//

//Selecionando o elemento que irá receber o novo elemento
var conteudo =document.getElementById('conteudo');

//Criando um novo elemento
var text =document.createElement('span');
text.innerText ='Eu não estava aqui antes';

//Usando o método append para colocar o elemento que criamos na div conteudo que selecionamos
conteudo.appendChild(text);


//// JQuery

<!DOCTYPE html>
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script>
$(document).ready(function(){
    $("button").click(function(){
        $("p").hide();
    });
});
</script>
</head>
<body>

<h2>This is a heading</h2>

<p>This is a paragraph.</p>
<p>This is another paragraph.</p>

<button>Click me to hide paragraphs</button>

</body>
</html>

//

<!DOCTYPE html>
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script>
$(document).ready(function(){
    $("button").click(function(){
        $("#test").hide();
    });
});
</script>
</head>
<body>

<h2>This is a heading</h2>

<p>This is a paragraph.</p>
<p id="test">This is another paragraph.</p>

<button>Click me</button>

</body>
</html>

//

<!DOCTYPE html>
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script>
$(document).ready(function(){
    $("button").click(function(){
        $(".test").hide();
    });
});
</script>
</head>
<body>

<h2 class="test">This is a heading</h2>

<p class="test">This is a paragraph.</p>
<p>This is another paragraph.</p>

<button>Click me</button>

</body>
</html>

//

//http://www.w3schools.com/jquery/jquery_examples.asp
//http://www.w3schools.com/jquery/jquery_selectors.asp


//// Ajax

//  AJAX is about loading data in the background and display it on the webpage, without reloading the whole page.

// jQuery provides several methods for AJAX functionality.

<!DOCTYPE html>
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script>
$(document).ready(function(){
    $("button").click(function(){
        $("#div1").load("demo_test.txt");
    });
});
</script>
</head>
<body>

<div id="div1"><h2>Let jQuery AJAX Change This Text</h2></div>

<button>Get External Content</button>

</body>
</html>

//

<!DOCTYPE html>
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script>
$(document).ready(function(){
    $("button").click(function(){
        $.get("demo_test.asp", function(data, status){
            alert("Data: " + data + "\nStatus: " + status);
        });
    });
});
</script>
</head>
<body>

<button>Send an HTTP GET request to a page and get the result back</button>

</body>
</html>

//

<!DOCTYPE html>
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script>
$(document).ready(function(){
    $("button").click(function(){
        $.post("demo_test_post.asp",
        {
          name: "Donald Duck",
          city: "Duckburg"
        },
        function(data,status){
            alert("Data: " + data + "\nStatus: " + status);
        });
    });
});
</script>
</head>
<body>

<button>Send an HTTP POST request to a page and get the result back</button>

</body>
</html>

// http://www.w3schools.com/jquery/jquery_ajax_intro.asp
// https://developer.mozilla.org/pt-BR/docs/AJAX/Getting_Started
# Lenguaje MICELIO

## Descripcion general

MICELIO es un lenguaje interpretado en español con paradigma funcional. Su sintaxis esta disenada para ser legible y expresiva. Este documento es la referencia completa del lenguaje.

## Variables y constantes

```mice
var x = 10            # variable mutable
const PI = 3.1416     # constante (no reasignable)
var a, b              # declaracion sin inicializar
var a, b = [1, 2]     # declaracion con desempaquetado
```

Las variables sin inicializar valen `nulo` hasta que se les asigne un valor.

## Tipos de datos

| Tipo | Ejemplo | Descripcion |
|------|---------|-------------|
| Numero | `42`, `3.14`, `-7` | Enteros y flotantes |
| Booleano | `verdadero`, `falso` | Valores logicos |
| Texto | `"hola"`, `'mundo'` | Cadenas UTF-8 |
| Lista | `[1, 2, 3]` | Coleccion ordenada mutable |
| Set | `#{1, 2, 3}` | Coleccion no ordenada sin duplicados |
| Dict | `{"a": 1, "b": 2}` | Mapa clave-valor |
| Nulo | `nulo` | Ausencia de valor |
| Funcion | `funcion (x) { ... }` | Ciudadano de primera clase |

## Operaciones aritmeticas

```mice
var s = 10 + 5        # suma       -> 15
var r = 10 - 5        # resta      -> 5
var p = 10 * 5        # producto   -> 50
var d = 10 / 5        # division   -> 2.0
var m = 10 % 3        # modulo     -> 1
var e = 2 ^ 3         # potencia   -> 8
```

## Operadores de comparacion

```mice
==  igualdad
!=  desigualdad
<   menor que
>   mayor que
<=  menor o igual
>=  mayor o igual
```

## Operadores logicos

```mice
y   # AND logico (cortocircuito)
o   # OR logico (cortocircuito)
no  # NOT logico
```

## Control de flujo

### Condicional si/sino

```mice
si (x > 0) {
  imp "positivo"
} sino {
  imp "no positivo"
}
```

### Bucle mientras

```mice
var i = 0
mientras (i < 5) {
  imp i
  i = i + 1
}
```

### Bucle para

```mice
para (var i = 0; i < 5; i = i + 1) {
  imp i
}
```

### Bucle para-cada (recorrer coleccion)

```mice
para (var elem in lista) {
  imp elem
}
```

### Segun (switch)

```mice
segun (x) {
  caso 1 { imp "uno" }
  caso 2 { imp "dos" }
  defecto { imp "otro" }
}
```

## Funciones

### Definicion basica

```mice
funcion saludar(nombre) {
  imp "Hola, " + nombre
}
```

### Retorno

```mice
funcion suma(a, b) {
  regresa a + b
}
```

### Funcion anonima (lambda)

```mice
var doble = funcion (x) { regresa x * 2 }
```

### Parametros variables (*args)

```mice
funcion sumar_todo(*args) {
  regresa reduce(funcion (a, b) { regresa a + b }, args, 0)
}
```

### Parametros con nombre (**kwargs)

```mice
funcion configurar(**kwargs) {
  imp kwargs
}
```

## Programacion funcional

### Pipeline (operador |> )

```mice
var resultado = [1, 2, 3, 4, 5]
  |> map(funcion (x) { regresa x * 2 })
  |> filter(funcion (x) { regresa x > 5 })
  |> reduce(funcion (a, b) { regresa a + b }, 0)
```

### map

```mice
var cuadrados = map(funcion (x) { regresa x ^ 2 }, [1, 2, 3])
# -> [1, 4, 9]
```

### filter

```mice
var pares = filter(funcion (x) { regresa x % 2 == 0 }, [1, 2, 3, 4])
# -> [2, 4]
```

### reduce

```mice
var total = reduce(funcion (a, b) { regresa a + b }, [1, 2, 3, 4], 0)
# -> 10
```

### ordenar

```mice
var nums = ordenar([3, 1, 4, 1, 5])
```

## Entrada/Salida

```mice
imp "Hola mundo"          # imprime con salto de linea
imp "Hola", " mundo"      # imprime multiples valores
leer variable             # lee una linea de entrada
leer a, b, c              # lee multiples valores de una linea
```

## Modulos

```mice
importar "math.mice" como math
importar "grafico.mice" como grafico
importar "../modulos_std/dl.mice" como dl
```

Las rutas son relativas al archivo que importa. Si el modulo ya fue cargado, se reutiliza la instancia en cache.

## Listas (metodos incorporados)

```mice
lista.agregar(elem)       # agrega al final
lista.insertar(i, elem)   # inserta en posicion
lista.eliminar(elem)      # elimina primera ocurrencia
lista.largo()             # longitud
lista.contiene(elem)      # busqueda -> verdadero/falso
lista.invertir()          # invierte in-place
lista.copiar()            # copia superficial
lista.limpiar()           # vacia la lista
lista.ordenar()           # ordena in-place
lista.unico()             # elimina duplicados
```

## Texto (metodos incorporados)

```mice
txt.largo()               # longitud
txt.contiene(sub)         # contiene subcadena?
txt.empezar_con(pre)      # empieza con prefijo?
txt.terminar_con(suf)     # termina con sufijo?
txt.minusculas()          # a minusculas
txt.mayusculas()          # a MAYUSCULAS
txt.reemplazar(viejo, nuevo)
txt.partir(sep)           # split -> lista
txt.segmento(inicio, fin) # substring
txt.numero()              # convierte a numero
txt.trim()                # elimina espacios extremos
```

## Dict (metodos incorporados)

```mice
dict.claves()             # lista de claves
dict.valores()            # lista de valores
dict.items()              # lista de [clave, valor]
dict.contiene(clave)      # existe clave?
dict.obtener(clave, def)  # get con valor por defecto
dict.copiar()             # copia superficial
dict.limpiar()            # vacia el dict
```

## Set (metodos incorporados)

```mice
set.agregar(elem)
set.eliminar(elem)
set.contiene(elem)
set.largo()
set.copiar()
set.limpiar()
```

## Conversiones entre tipos

```mice
aNumero("42")      # texto -> numero
aTexto(42)         # numero -> texto
aBooleano(1)       # numero -> bool (0 es falso)
aLista(conjunto)   # set -> lista
```

## Operador de propagacion (...)

```mice
var a = [1, 2, 3]
var b = [0, ...a, 4]  # -> [0, 1, 2, 3, 4]
```

## Desempaquetado

```mice
var a, b = [10, 20]        # declaracion
a, b = [x, y]              # asignacion
```

Ambos lados deben tener la misma cantidad de elementos.

## Palabras reservadas

`si`, `sino`, `y`, `o`, `no`, `funcion`, `regresa`, `var`, `const`, `mientras`, `para`, `in`, `segun`, `caso`, `defecto`, `leer`, `imp`, `importar`, `como`, `nulo`, `verdadero`, `falso`, `modulo`, `clase`

## Modulos de la biblioteca estandar

- `builtins.mice`: funciones base auto-cargadas (exp, aleatorio, ordenar, map, filter, reduce)
- `math.mice`: constantes (PI, E) y funciones (raiz, seno, coseno, tan, log, etc.)
- `matriz.mice`: operaciones con matrices (suma, resta, multiplicacion, transpuesta, determinante)
- `grafico.mice`: graficacion 2D (lineas, dispersion, histograma, ejes, guardar PNG)
- `gui.mice`: ventanas y controles GTK
- `hifa.mice`: framework web (rutas, peticiones, respuestas, sesiones)
- `archivo.mice`: lectura/escritura de archivos
- `lista.mice`: funciones auxiliares para listas
- `dict.mice`: funciones auxiliares para diccionarios
- `set.mice`: funciones auxiliares para conjuntos
- `ml.mice`: machine learning basico (regresion lineal, KNN, k-medias)
- `dl.mice`: deep learning (perceptron multicapa, retropropagacion)

## Ejemplos practicos

### Numeros primos

```mice
funcion es_primo(n) {
  si (n < 2) { regresa falso }
  var i = 2
  mientras (i * i <= n) {
    si (n % i == 0) { regresa falso }
    i = i + 1
  }
  regresa verdadero
}

var primos = filter(funcion (x) { regresa es_primo(x) }, [1..100])
imp primos
```

### Fibonacci recursivo con memoizacion

```mice
var memo = {}

funcion fib(n) {
  si (n <= 1) { regresa n }
  si (memo.contiene(n)) { regresa memo.obtener(n) }
  var r = fib(n - 1) + fib(n - 2)
  memo[n] = r
  regresa r
}

imp fib(30)  # 832040
```

### Archivo: leer lineas y procesar

```mice
importar "archivo.mice" como archivo

var lineas = archivo.leer_lineas("datos.txt")
var numeros = map(funcion (l) { regresa aNumero(l) }, lineas)
var suma = reduce(funcion (a, b) { regresa a + b }, numeros, 0)
imp "Suma: " + suma
```

# 📑 INFORME FINAL DE PROYECTO: MICELIO DSL
**Asignatura: Lenguajes de Programación | Proyecto: DSL para Deep Learning**

---

## 1. Mandato Original y Cumplimiento
El objetivo fue diseñar un lenguaje de dominio específico (DSL) utilizando **ANTLRv4** y **Python (Patrón Visitor)** para operaciones de Aprendizaje Profundo (DL) con un enfoque funcional.

### ✅ Matriz de Cumplimiento Técnico

| Requisito | Estado | Implementación Técnica |
| :--- | :---: | :--- |
| **Aritmética Completa** | ✅ | Implementada en `math.mice` (Taylor para trig/exp, Newton-Raphson para raíces). |
| **Operaciones de Matrices** | ✅ | Implementada en `matriz.mice` (Gauss-Jordan para Inversa, LU para Det). |
| **Condicionales y Ciclos** | ✅ | Gramática soporta `si/sino`, `mientras` y `para` (rango y colección). |
| **Gráficas de Datos** | ✅ | Módulo `grafico.mice` genera buffers visuales y archivos PPM/BMP. |
| **Manejo de Archivos** | ✅ | Módulo `archivo.mice` (lectura/escritura de texto y CSV). |
| **Regresión Lineal/Logística**| ✅ | Módulo `ml.mice` con Descenso de Gradiente y forma matricial. |
| **Perceptrón Multicapa** | ✅ | Módulo `dl.mice` con Backpropagation y capas densas ilimitadas. |
| **ANN: Agrupar/Clasificar** | ✅ | Algoritmos de K-Means (agrupamiento) y MLP (predicción/clasificación). |
| **Enfoque Funcional** | ✅ | Funciones de orden superior, Map/Filter/Reduce y operador Pipe `|>`. |
| **Ejecución por Consola** | ✅ | Intérprete `main.py` con REPL y ejecución de scripts. |

---

## 2. Arquitectura del Sistema
Micelio opera sobre un stack moderno de lenguajes:
- **Parser/Lexer:** Generado por ANTLR4 a partir de `Micelio.g4`.
- **Intérprete:** `eval_visitor.py` procesa el Árbol de Sintaxis Abstracta (AST).
- **Entorno (Runtime):** `runtime.py` gestiona el estado y las funciones nativas.
- **Biblioteca Estándar:** Escrita en el propio Micelio (`modulos_std/`), demostrando la potencia del lenguaje para sostenerse a sí mismo.

---

## 3. Auditoría de Algoritmos (Implementados desde Cero)
Para cumplir con el reto de **"Sin librerías externas"**, se desarrollaron:
1. **Álgebra:** Multiplicación de matrices O(n³), Transposición, Inversa por Gauss-Jordan.
2. **Cálculo:** Derivadas de funciones de activación (Sigmoid, ReLU, Softmax).
3. **Optimización:** Descenso de Gradiente Estocástico (SGD).
4. **DL:** Forward y Backward propagation con regla de la cadena manual.

---

## 4. Guía de Uso Rápido
1. **Ejecutar un script:** `python MICELIO/main.py ejemplos/nombre.mice`
2. **REPL:** `python MICELIO/main.py` (usa `:help` para comandos).

---

## 5. Conclusión
Micelio cumple con el 100% de los requisitos del proyecto, ofreciendo una sintaxis intuitiva, un motor matemático robusto y una capacidad de aprendizaje profundo real, todo bajo un paradigma funcional que facilita la composición de modelos complejos.

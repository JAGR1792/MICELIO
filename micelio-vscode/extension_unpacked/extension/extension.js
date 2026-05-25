const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

// ─── Base de conocimiento del lenguaje ────────────────────────────────────

const KEYWORDS = [
  'si', 'sino', 'segun', 'caso', 'defecto',
  'para', 'hasta', 'inc', 'en',
  'mientras', 'romper', 'continuar', 'regresa',
  'importar', 'como',
  'var', 'const', 'funcion', 'set', 'dict',
  'verdadero', 'falso', 'nulo',
  'y', 'o', 'no', 'in'
];

const BUILTINS = {
  'imp': { params: ['...valores'], doc: 'Imprime valores en la consola' },
  'leer': { params: ['ruta'], doc: 'Lee el contenido de un archivo de texto' },
  'tipo': { params: ['valor'], doc: 'Obtiene el tipo de un valor' },
  'longitud': { params: ['coleccion'], doc: 'Obtiene la longitud de una colección' },
  'map': { params: ['funcion', 'lista'], doc: 'Aplica una función a cada elemento de una lista' },
  'filter': { params: ['predicado', 'lista'], doc: 'Filtra elementos según un predicado' },
  'reduce': { params: ['funcion', 'lista', 'inicial'], doc: 'Reduce una lista a un valor aplicando una función binaria' },
  'ordenar': { params: ['lista'], doc: 'Ordena una lista (Quicksort)' },
  'rango': { params: ['*args'], doc: 'Genera una lista de números. Uso: rango(fin) o rango(inicio, fin)' },
  'aNumero': { params: ['valor'], doc: 'Convierte un valor a número' },
  'aEntero': { params: ['valor'], doc: 'Convierte a entero' },
  'aFlotante': { params: ['valor'], doc: 'Convierte a flotante' },
  'aTexto': { params: ['valor'], doc: 'Convierte cualquier valor a texto' },
  'aBooleano': { params: ['valor'], doc: 'Convierte a booleano' },
  'aCaracter': { params: ['codigo'], doc: 'Convierte código numérico a carácter' },
  'aCodigo': { params: ['caracter'], doc: 'Obtiene el código numérico de un carácter' },
  'aBinario': { params: ['n'], doc: 'Convierte un número a binario' },
  'aOctal': { params: ['n'], doc: 'Convierte un número a octal' },
  'aHexadecimal': { params: ['n'], doc: 'Convierte un número a hexadecimal' },
  'aBase': { params: ['n', 'base'], doc: 'Convierte un número a la base dada' },
  'desdeBinario': { params: ['texto'], doc: 'Convierte texto binario a número' },
  'desdeOctal': { params: ['texto'], doc: 'Convierte texto octal a número' },
  'desdeHexadecimal': { params: ['texto'], doc: 'Convierte texto hexadecimal a número' },
  'desdeBase': { params: ['texto', 'base'], doc: 'Convierte texto en base arbitraria a número' },
  'exp': { params: ['x'], doc: 'Exponencial e^x por serie de Taylor' },
  'aleatorio': { params: [], doc: 'Genera un número pseudoaleatorio entre 0 y 1' },
  'abs': { params: ['x'], doc: 'Valor absoluto' },
  'maximo': { params: ['a', 'b'], doc: 'Máximo de dos números' },
  'minimo': { params: ['a', 'b'], doc: 'Mínimo de dos números' },
  'max_lista': { params: ['lista'], doc: 'Valor máximo en una lista' },
  'min_lista': { params: ['lista'], doc: 'Valor mínimo en una lista' },
  'suma': { params: ['lista'], doc: 'Suma de todos los elementos de una lista' },
  'producto': { params: ['lista'], doc: 'Producto de todos los elementos de una lista' },
  'promedio': { params: ['lista'], doc: 'Promedio de los elementos de una lista' },
  'contar': { params: ['predicado', 'lista'], doc: 'Cuenta elementos que cumplen el predicado' },
  'todos': { params: ['predicado', 'lista'], doc: '¿Todos los elementos cumplen el predicado?' },
  'alguno': { params: ['predicado', 'lista'], doc: '¿Algún elemento cumple el predicado?' },
  'primero': { params: ['lista'], doc: 'Primer elemento de una lista' },
  'ultimo': { params: ['lista'], doc: 'Último elemento de una lista' },
  'invertir': { params: ['lista'], doc: 'Invierte una lista' },
  'concatenar': { params: ['lista1', 'lista2'], doc: 'Concatena dos listas' },
  'claves': { params: ['diccionario'], doc: 'Obtiene las claves de un diccionario' },
  'valores': { params: ['diccionario'], doc: 'Obtiene los valores de un diccionario' },
  'items': { params: ['diccionario'], doc: 'Obtiene pares [clave, valor] de un diccionario' },
  'error': { params: ['mensaje'], doc: 'Lanza un error con el mensaje dado' }
};

const KEYWORD_DOCS = {
  'si': 'Condicional if. Uso: si (condicion) { ... } [ sino { ... } ]',
  'sino': 'Bloque else. Debe ir tras un bloque si { }',
  'mientras': 'Bucle condicional. Uso: mientras (condicion) { ... }',
  'para': 'Iteración sobre lista. Uso: para elemento en lista { ... }',
  'funcion': 'Define una función. Uso: funcion nombre(parametros) { ... }',
  'var': 'Declara una variable mutable',
  'const': 'Declara una constante inmutable',
  'regresa': 'Retorna un valor desde una función',
  'importar': 'Importa un módulo. Uso: importar "ruta" como alias',
  'romper': 'Sale del bucle actual',
  'continuar': 'Salta a la siguiente iteración del bucle',
  'verdadero': 'Valor booleano verdadero (true)',
  'falso': 'Valor booleano falso (false)',
  'nulo': 'Valor nulo (null)',
  'y': 'Operador lógico AND',
  'o': 'Operador lógico OR',
  'no': 'Operador lógico NOT',
  'in': 'Operador de pertenencia. Uso: valor in lista',
  'segun': 'Switch case. Uso: segun (expr) { caso val: ... defecto: ... }',
  'dict': 'Crea un diccionario. Uso: dict("clave", valor, ...)',
  'set': 'Crea un conjunto. Uso: set(elementos)'
};

const DL_FUNCTIONS = [
  'sigmoid', 'relu', 'tanh', 'mse', 'binary_crossentropy',
  'crear_capa', 'fc', 'forward', 'backward',
  'suma_matrices', 'resta_matrices', 'multiplicar',
  'hadamard', 'traspuesta', 'aplicar', 'inicializar_pesos'
];

// ─── Utilidades ──────────────────────────────────────────────────────────

function getImportedModules(document) {
  const imports = {};
  const importRegex = /importar\s+["']([^"']+)["']\s+como\s+([A-Za-z_][A-Za-z0-9_]*)/g;
  for (let i = 0; i < document.lineCount; i++) {
    const line = document.lineAt(i).text;
    let match;
    while ((match = importRegex.exec(line)) !== null) {
      imports[match[2]] = match[1];
    }
  }
  return imports;
}

function extractFunctionsFromFile(filePath) {
  if (!fs.existsSync(filePath)) return [];
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const matches = [
      ...content.matchAll(/\bfuncion\s+([A-Za-z_][A-Za-z0-9_]*)/g),
      ...content.matchAll(/\bconst\s+([A-Za-z_][A-Za-z0-9_]*)\s*=/g),
    ];
    const names = new Set();
    matches.forEach(m => names.add(m[1]));
    return Array.from(names);
  } catch (e) {
    return [];
  }
}

function extractLocalSymbols(document) {
  const symbols = [];
  for (let i = 0; i < document.lineCount; i++) {
    const text = document.lineAt(i).text;
    const fnMatch = text.match(/\bfuncion\s+([A-Za-z_][A-Za-z0-9_]*)/);
    if (fnMatch) {
      symbols.push({ name: fnMatch[1], kind: vscode.SymbolKind.Function, line: i });
      continue;
    }
    const varMatch = text.match(/^\s*(var|const)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=/);
    if (varMatch) {
      symbols.push({ name: varMatch[2], kind: vscode.SymbolKind.Variable, line: i });
    }
  }
  return symbols;
}

function resolveModulePath(modulePath, document) {
  let fullPath = modulePath;
  if (!path.isAbsolute(fullPath) && !fs.existsSync(fullPath)) {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (workspaceFolder) {
      fullPath = path.join(workspaceFolder, 'MICELIO', 'modulos_std', modulePath);
      if (!fullPath.endsWith('.mice')) fullPath += '.mice';
    }
  }
  return fullPath;
}

function isPipeLinePrefix(textBeforeCursor) {
  return /^\s*\|>.*$/.test(textBeforeCursor);
}

async function insertPipeContinuation(editor) {
  const selection = editor.selection;
  const line = editor.document.lineAt(selection.active.line);
  const before = line.text.slice(0, selection.active.character);
  if (!selection.isEmpty || !isPipeLinePrefix(before)) {
    await vscode.commands.executeCommand('default:type', { text: '\n' });
    return;
  }
  const indent = (before.match(/^\s*/) || [''])[0];
  const text = `\n${indent}|> `;
  await editor.edit((editBuilder) => {
    editBuilder.insert(selection.active, text);
  });
}

// ─── Provider: Compleciones ──────────────────────────────────────────────

class MicelioCompletionProvider {
  provideCompletionItems(document, position) {
    const lineText = document.lineAt(position.line).text;
    const beforeCursor = lineText.slice(0, position.character);
    const items = [];

    // 1. Compleción de miembros de módulo: ALIAS.
    const moduleMatch = beforeCursor.match(/([A-Za-z_][A-Za-z0-9_]*)\s*\.\s*$/);
    if (moduleMatch) {
      const alias = moduleMatch[1];
      const imports = getImportedModules(document);
      if (alias in imports) {
        const fullPath = resolveModulePath(imports[alias], document);
        const functions = extractFunctionsFromFile(fullPath);
        functions.forEach(name => {
          const item = new vscode.CompletionItem(name, vscode.CompletionItemKind.Function);
          item.detail = `Función/constante de ${alias}`;
          items.push(item);
        });
        return items;
      }
    }

    // 2. Palabras clave
    KEYWORDS.forEach(kw => {
      const item = new vscode.CompletionItem(kw, vscode.CompletionItemKind.Keyword);
      item.detail = 'Palabra clave de Micelio';
      item.documentation = KEYWORD_DOCS[kw] || '';
      items.push(item);
    });

    // 3. Funciones builtin
    Object.keys(BUILTINS).forEach(name => {
      const info = BUILTINS[name];
      const item = new vscode.CompletionItem(name, vscode.CompletionItemKind.Function);
      item.detail = `builtin(${info.params.join(', ')})`;
      item.documentation = info.doc;
      items.push(item);
    });

    // 4. Símbolos locales (funciones y variables del documento actual)
    const localSymbols = extractLocalSymbols(document);
    localSymbols.forEach(sym => {
      const item = new vscode.CompletionItem(sym.name,
        sym.kind === vscode.SymbolKind.Function
          ? vscode.CompletionItemKind.Function
          : vscode.CompletionItemKind.Variable);
      item.detail = sym.kind === vscode.SymbolKind.Function ? 'Función local' : 'Variable local';
      items.push(item);
    });

    // 5. Funciones de DL/ml/matriz (comunes)
    DL_FUNCTIONS.forEach(name => {
      const item = new vscode.CompletionItem(name, vscode.CompletionItemKind.Function);
      item.detail = 'Función de ML/DL/Matriz';
      items.push(item);
    });

    return items;
  }
}

// ─── Provider: Hover ─────────────────────────────────────────────────────

class MicelioHoverProvider {
  provideHover(document, position) {
    const range = document.getWordRangeAtPosition(position, /[A-Za-z_][A-Za-z0-9_]*/);
    if (!range) return null;
    const word = document.getText(range);

    // Palabra clave
    if (KEYWORD_DOCS[word]) {
      return new vscode.Hover({
        language: 'micelio',
        value: `**${word}** — Palabra clave de Micelio\n\n${KEYWORD_DOCS[word]}`
      });
    }

    // Función builtin
    if (BUILTINS[word]) {
      const info = BUILTINS[word];
      const params = info.params.map(p => `\`${p}\``).join(', ');
      return new vscode.Hover({
        language: 'micelio',
        value: `**${word}(${info.params.join(', ')})** — Función incorporada\n\n${info.doc}\n\n**Parámetros:** ${params}`
      });
    }

    // Símbolo local
    const localSymbols = extractLocalSymbols(document);
    const sym = localSymbols.find(s => s.name === word);
    if (sym) {
      const kind = sym.kind === vscode.SymbolKind.Function ? 'Función' : 'Variable';
      return new vscode.Hover(`**${word}** — ${kind} local (línea ${sym.line + 1})`);
    }

    return null;
  }
}

// ─── Provider: Signature Help ────────────────────────────────────────────

class MicelioSignatureProvider {
  provideSignatureHelp(document, position) {
    const lineText = document.lineAt(position.line).text;
    const beforeCursor = lineText.slice(0, position.character);

    const callMatch = beforeCursor.match(/([A-Za-z_][A-Za-z0-9_]*)\s*\([^)]*$/);
    if (!callMatch) return null;

    const funcName = callMatch[1];
    const info = BUILTINS[funcName];
    if (!info) return null;

    const sig = new vscode.SignatureHelp();
    const signature = new vscode.SignatureInformation(
      `${funcName}(${info.params.join(', ')})`,
      info.doc
    );
    signature.parameters = info.params.map(p =>
      new vscode.ParameterInformation(p)
    );
    sig.signatures = [signature];
    sig.activeSignature = 0;

    // Calcular índice del parámetro activo según las comas
    const argsPart = beforeCursor.slice(beforeCursor.indexOf('(') + 1);
    sig.activeParameter = (argsPart.match(/,/g) || []).length;
    if (sig.activeParameter >= info.params.length) {
      sig.activeParameter = info.params.length - 1;
    }

    return sig;
  }
}

// ─── Provider: Document Symbols ──────────────────────────────────────────

class MicelioDocumentSymbolProvider {
  provideDocumentSymbols(document) {
    const symbols = extractLocalSymbols(document);
    return symbols.map(sym => {
      const range = new vscode.Range(sym.line, 0, sym.line, document.lineAt(sym.line).text.length);
      return new vscode.SymbolInformation(
        sym.name,
        sym.kind,
        range,
        range,
        document.uri
      );
    });
  }
}

// ─── Provider: Definición ────────────────────────────────────────────────

class MicelioDefinitionProvider {
  provideDefinition(document, position) {
    const range = document.getWordRangeAtPosition(position, /[A-Za-z_][A-Za-z0-9_]*/);
    if (!range) return null;
    const word = document.getText(range);

    const localSymbols = extractLocalSymbols(document);
    const sym = localSymbols.find(s => s.name === word);
    if (sym) {
      const line = document.lineAt(sym.line);
      const match = line.text.match(new RegExp(word));
      if (match) {
        const start = new vscode.Position(sym.line, match.index);
        const end = new vscode.Position(sym.line, match.index + word.length);
        return new vscode.Location(document.uri, new vscode.Range(start, end));
      }
    }

    // Buscar en módulos importados
    const imports = getImportedModules(document);
    const aliasMatch = word.split('.');
    if (aliasMatch.length === 2 && imports[aliasMatch[0]]) {
      const fullPath = resolveModulePath(imports[aliasMatch[0]], document);
      if (fs.existsSync(fullPath)) {
        const content = fs.readFileSync(fullPath, 'utf8');
        const lines = content.split('\n');
        const targetFn = aliasMatch[1];
        for (let i = 0; i < lines.length; i++) {
          if (new RegExp(`\\bfuncion\\s+${targetFn}\\b`).test(lines[i])) {
            const uri = vscode.Uri.file(fullPath);
            const matchIndex = lines[i].indexOf(targetFn);
            const pos = new vscode.Position(i, matchIndex);
            return new vscode.Location(uri, pos);
          }
        }
      }
    }

    return null;
  }
}

// ─── Activación ──────────────────────────────────────────────────────────

function activate(context) {
  // Comando: pipe enter
  context.subscriptions.push(
    vscode.commands.registerCommand('micelio.enterPipe', async () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) {
        await vscode.commands.executeCommand('default:type', { text: '\n' });
        return;
      }
      await insertPipeContinuation(editor);
    })
  );

  // Completion provider
  context.subscriptions.push(
    vscode.languages.registerCompletionItemProvider(
      'micelio',
      new MicelioCompletionProvider(),
      '.', ...KEYWORDS.map(k => k[0])
    )
  );

  // Hover provider
  context.subscriptions.push(
    vscode.languages.registerHoverProvider('micelio', new MicelioHoverProvider())
  );

  // Signature help provider
  context.subscriptions.push(
    vscode.languages.registerSignatureHelpProvider('micelio', new MicelioSignatureProvider(), '(', ',')
  );

  // Document symbols provider
  context.subscriptions.push(
    vscode.languages.registerDocumentSymbolProvider('micelio', new MicelioDocumentSymbolProvider())
  );

  // Definition provider
  context.subscriptions.push(
    vscode.languages.registerDefinitionProvider('micelio', new MicelioDefinitionProvider())
  );
}

function deactivate() {}

module.exports = { activate, deactivate };

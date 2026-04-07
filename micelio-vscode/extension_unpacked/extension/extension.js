const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

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

// Extrae funciones y constantes de un archivo .mice
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

// Obtiene módulos importados en el documento
function getImportedModules(document) {
  const imports = {};
  const importRegex = /importar\s+["']([^"']+)["']\s+como\s+([A-Za-z_][A-Za-z0-9_]*)/g;
  
  for (let i = 0; i < document.lineCount; i++) {
    const line = document.lineAt(i).text;
    let match;
    while ((match = importRegex.exec(line)) !== null) {
      const modulePath = match[1];
      const alias = match[2];
      imports[alias] = modulePath;
    }
  }
  
  return imports;
}

function activate(context) {
  // Comando: pipe enter continuation
  const disposable = vscode.commands.registerCommand('micelio.enterPipe', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      await vscode.commands.executeCommand('default:type', { text: '\n' });
      return;
    }
    await insertPipeContinuation(editor);
  });
  context.subscriptions.push(disposable);

  // CompletionItemProvider para autocomplete de módulos
  const completionProvider = vscode.languages.registerCompletionItemProvider(
    'micelio',
    {
      provideCompletionItems(document, position, token, context) {
        const lineText = document.lineAt(position.line).text;
        const beforeCursor = lineText.slice(0, position.character);
        
        // Detecta patrón: ALIAS.
        const match = beforeCursor.match(/([A-Za-z_][A-Za-z0-9_]*)\s*\.\s*$/);
        if (!match) return [];
        
        const alias = match[1];
        const imports = getImportedModules(document);
        
        if (!(alias in imports)) return [];
        
        // Resuelve la ruta del módulo
        const modulePath = imports[alias];
        let fullPath = modulePath;
        
        // Busca en modulos_std/ si no existe ruta absoluta
        if (!path.isAbsolute(fullPath) && !fs.existsSync(fullPath)) {
          const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
          if (workspaceFolder) {
            fullPath = path.join(workspaceFolder, 'MICELIO', 'modulos_std', modulePath);
            if (!fullPath.endsWith('.mice')) fullPath += '.mice';
          }
        }
        
        // Extrae funciones del módulo
        const functions = extractFunctionsFromFile(fullPath);
        
        const completions = functions.map(name => {
          const item = new vscode.CompletionItem(name, vscode.CompletionItemKind.Function);
          item.detail = `Función/constante de ${alias}`;
          return item;
        });
        
        return completions;
      }
    },
    '.'
  );
  context.subscriptions.push(completionProvider);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
};

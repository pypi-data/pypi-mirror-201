// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module theme-dark-extension
 */
import { IThemeManager } from '@jupyterlab/apputils';
import { ITranslator } from '@jupyterlab/translation';
import { NotebookActions, INotebookTracker } from '@jupyterlab/notebook';
import { Widget } from '@lumino/widgets';
import { ICommandPalette } from '@jupyterlab/apputils';

class AssistantSidebar extends Widget {
  constructor() {
    super();
    this.id = 'assistant-panel';
    this.addClass('assistant-panel');
    this.title.caption = 'Assistant';
    this.title.iconClass = 'fa fa-robot';
  }
}

function waitForNonNullVariable(reader, callback) {
  var variable = reader(); 
  if (variable !== null) {
    callback(variable);
  } else {
    setTimeout(function() {
      waitForNonNullVariable(reader, callback);
    }, 100); // Wait 1 second before checking again
  }
}
function replaceCurrentCell(tracker, code) {
  const currentNotebook = tracker.currentWidget;
  if (!currentNotebook) {
    return;
  }
  const index = currentNotebook.content.activeCellIndex;
  var cell; 
  if (code.startsWith("pip") || code.startsWith("gcloud")) {
    code = "!" + code;
    cell = currentNotebook.content.model.contentFactory.createCodeCell({});
    cell.value.text = code;
    //add cell at the beginning of the notebook
    currentNotebook.content.model.cells.insert(0, newCell);
    console.log("Adding new cell at the beginning");
  } else if (index === -1) {
    cell = currentNotebook.content.model.contentFactory.createCodeCell({});
    cell.value.text = code;
    currentNotebook.content.model.cells.push(newCell);
    console.log("Adding new cell");
  } else {
    cell = currentNotebook.content.model.cells.get(index);
    cell.value.text = code;
    console.log("Replacing code in current cell");
  }
};

function getCellContent(cell) {
  var outputText = "";
  const outputJSON = cell.outputArea.model.toJSON();
  if (outputJSON.length > 0) {
    const traceback = outputJSON[0].traceback;
    if (traceback != null) {
      for (var i = 0; i < traceback.length; i++) {
        const escapeRegex = /\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]/g;
        const plainTextString = traceback[i].replace(escapeRegex, '');
        outputText += plainTextString + "\n";
      }
    } else {
      outputText = outputJSON[0].text;
    }
  }
  return {
    "text": cell.model.value.text,
    "output": outputText
  }
}
function getCurrentCellContent(tracker, app) {
  const currentNotebook = tracker.currentWidget;
  if (!currentNotebook) {
    return;
  }
  //get index of currently selected cell
  const index = currentNotebook.content.activeCellIndex;
  if (index === -1) {
    return "";
  } else {
    //retrieve cell text including its kernel output
    const current = app.shell.currentWidget.content.activeCell; 
    return getCellContent(current); 
  }
}

function loadFlutterApp() {
  window.isJupyter = true;
  var serviceWorkerVersion = "124778936";
  const flutter_script = document.createElement('script');
  flutter_script.src = '/roboweb-server-extension/flutter.js';
  document.head.appendChild(flutter_script);
  
  flutter_script.onload = function() {
    console.log('Downloading main.dart.js');
    _flutter.loader.loadEntrypoint({
      serviceWorker: {
        serviceWorkerVersion: serviceWorkerVersion,
      }
    }).then(function(engineInitializer) {
      console.log('Initializing engine');
      waitForNonNullVariable(function() {return document.getElementById("assistant-panel")}, function (target) {
        engineInitializer.initializeEngine({
          hostElement: target,
        }).then(function(appRunner) {
          return appRunner.runApp();
        })
      }); 
      //if target is null sleep for 100 ms 
    });
  };
}
const plugin = {
    id: 'roboweb-extension',
    requires: [INotebookTracker, ICommandPalette],
    activate: (app, tracker, palette) => {
      console.log(
        'Roboweb extension activated v0.1'
      );
      const widget = new AssistantSidebar();
      widget.node.style.minWidth = "450px";
      app.shell.add(widget, 'right', { rank: 0 });

    
      //register function to retrieve current cell text
      window.currentCellText = function () {
        return getCurrentCellContent(tracker, app);
      }

      //register function to edit current cell text
      window.replaceCodeCurrentCell = function(code) {
        replaceCurrentCell(tracker, code);
      }
      
      //track and log executions 
      NotebookActions.executed.connect(async (_, args) => {
        const { cell, notebook, success, error } = args;
        var cellContent = getCellContent(cell); 
        const input = cellContent.text;
        const output = cellContent.output;
        console.log("Logging execution"+input+" "+output);
        window.logCellExecution(cellContent.text, cellContent.output); 
      });

      app.commands.addCommand('fix-cell-extension:fixCell', {
        label: 'Fix',
        execute: () => {
          console.log("Fixing cell");
          const currentNotebook = tracker.currentWidget;
          if (!currentNotebook) {
            console.log("No notebook open");
            return;
          }
          const currentCell = window.currentCellText();
          const errorPrompt = "My code has an error. Ideally give me a quick command to fix it. If that's not available give me python code to fix it. Assume i dont have a credentials or key file. \n\nCode: \n\n" + currentCell.text + "\n\nError: \n\n" + currentCell.output;
          console.log("Pasting prompt "+errorPrompt);
          window.pastePrompt(errorPrompt); 
        }
      });
    
      app.contextMenu.addItem({
        command: 'fix-cell-extension:fixCell',
        selector: '.jp-Notebook',
        rank: 0
      });  

      window.addEventListener('click', function(event) {
        const assistantPanelDiv = document.querySelector('#assistant-panel');
        if (!assistantPanelDiv.contains(event.target)) {
          removeFocus();
        }
      
      }, { passive: true });
            

      //embed flutter app 
      loadFlutterApp();
    },
    autoStart: true
};
export default plugin;




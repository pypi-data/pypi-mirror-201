// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module theme-dark-extension
 */
import { IThemeManager } from '@jupyterlab/apputils';
import { ITranslator } from '@jupyterlab/translation';
import { INotebookTracker } from '@jupyterlab/notebook';
import { Widget } from '@lumino/widgets';
import { ICommandPalette } from '@jupyterlab/apputils';
// import myimage from '../static/test.jpeg';

class AssistantSidebar extends Widget {
  constructor() {
    super();
    this.id = 'assistant-panel';
    this.addClass('assistant-panel');
    this.title.caption = 'Assistant';
    this.title.iconClass = 'fa fa-robot';
  }
}

const plugin = {
    id: 'roboweb-extension',
    requires: [INotebookTracker, ICommandPalette],
    activate: (app, tracker, palette) => {
      console.log(
        'Roboweb extension activated'
      );
      const widget = new AssistantSidebar();
      widget.node.style.minWidth = "500px";
      app.shell.add(widget, 'right', { rank: 0 });
      //set min width of the sidebar

      //register function to retrieve current cell text
      window.currentCellText = function () {
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
          window.current = current; 
          
            
          var outputText = "";
          const outputJSON = current.outputArea.model.toJSON();
          if (outputJSON.length > 0) {
            const traceback = outputJSON[0].traceback;
            for (var i = 0; i < traceback.length; i++) {
              const escapeRegex = /\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]/g;
              const plainTextString = traceback[i].replace(escapeRegex, '');
              outputText += plainTextString + "\n";
            }
          }

          return {
            "text": current.model.value.text,
            "output": outputText
          }
        }
      }
      //register function to edit current cell text
      window.replaceCodeCurrentCell = function (code) {
        const currentNotebook = tracker.currentWidget;
        if (!currentNotebook) {
          return;
        }
        //get index of currently selected cell
        const index = currentNotebook.content.activeCellIndex;
        //if code starts with pip or gcloud add ! at the beginning
        if (code.startsWith("pip") || code.startsWith("gcloud")) {
          code = "!" + code;
          const newCell = currentNotebook.content.model.contentFactory.createCodeCell({});
          newCell.value.text = code;
          //add cell at the beginning of the notebook
          currentNotebook.content.model.cells.insert(0, newCell);
          console.log("Adding new cell at the beginning");
        } else if (index === -1) {
          const newCell = currentNotebook.content.model.contentFactory.createCodeCell({});
          newCell.value.text = code;
          currentNotebook.content.model.cells.push(newCell);
          console.log("Adding new cell");
        } else {
          const cell = currentNotebook.content.model.cells.get(index);
          cell.value.text = code;
          console.log("Replacing code in current cell");
        }
      };



      app.commands.addCommand('fix-cell-extension:fixCell', {
        label: 'Fix',
        execute: () => {
          const currentNotebook = tracker.currentWidget;
          if (!currentNotebook) {
            return;
          }
          const currentCell = window.currentCellText();
          const errorPrompt = "My code has an error. Ideally give me a quick command to fix it. If that's not available give me python code to fix it. Assume i dont have a credentials or key file. \n\nCode: \n\n" + currentCell.text + "\n\nError: \n\n" + currentCell.output;
          window.pastePrompt(errorPrompt); 
        }
      });
    
      app.contextMenu.addItem({
        command: 'fix-cell-extension:fixCell',
        selector: '.jp-Notebook',
        rank: 0
      });      
      var isJupyter = true;
      var serviceWorkerVersion = "124778936";
      const flutter_script = document.createElement('script');
      flutter_script.src = '/roboweb-server-extension/flutter.js';
      document.head.appendChild(flutter_script);
      
      const main_script = document.createElement('script');
      main_script.src = '/roboweb-server-extension/main.js';
      document.head.appendChild(main_script);
      
      flutter_script.onload = function() {
        console.log('Downloading main.dart.js');
        _flutter.loader.loadEntrypoint({
          serviceWorker: {
            serviceWorkerVersion: serviceWorkerVersion,
          }
        }).then(function(engineInitializer) {
          console.log('Initializing engine');
          let target = document.getElementById("assistant-panel");
          return engineInitializer.initializeEngine({
            hostElement: target,
          });
        }).then(function(appRunner) {
          //remove focus from the sidebar when clicking outside of it
          console.log('Running app');
          return appRunner.runApp();
        });
      };


      //add img/test.jpeg to target

      // const testIMG= document.createElement('img');
      // testIMG.src = myimage;
      // target.appendChild(img);

 

    },
    autoStart: true
};
export default plugin;




# Author-Sam Chaney 
# Description-Export multiple sketches as DXF if the sketch name contains 'DXF'
# Edit Kurt Meister: Export from all components and list the sketches
# Script altered with support by rohit.bapat from Autodesk :)

# Online Python - IDE, Editor, Compiler, Interpreter

import adsk.core, adsk.fusion, adsk.cam, traceback, os

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)

        def is_dxf(sketch):
            if 'DXF' in sketch.name:
                return True
            
        myList = []

        folder_dialogue = ui.createFolderDialog()
        folder_dialogue.title = 'Select folder to export all DXFs'
        result = folder_dialogue.showDialog()

        if result == adsk.core.DialogResults.DialogOK: # If the user clicks on the "Select Folder" button
            export_folder = folder_dialogue.folder
            allComponentsInDesign = design.allComponents
            for component in allComponentsInDesign:
                sketches = component.sketches
                for sketch in sketches:
                    if is_dxf(sketch):
                        full_path = os.path.join(export_folder, sketch.name) + '.dxf'
                        sketch.saveAsDXF(full_path)
                        myList.append(sketch.name + ".dxf")

            ui.messageBox("\n".join(myList), "Sketches exported [" + str(len(myList)) + "]:", 0, 2)                
        else: # If the user clicks on the "Cancel" button 
            ui.messageBox(f'No folder selected')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
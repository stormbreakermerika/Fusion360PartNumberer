import os
import adsk.core, adsk.fusion, adsk.cam
import traceback

handlers = []
app = adsk.core.Application.get()
ui  = app.userInterface

class NumbererCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            unitsMgr = app.activeProduct.unitsManager
            command = args.firingEvent.sender
            inputs = command.commandInputs
            selectedFaceInput = inputs.itemById('face')
            selectedFace = selectedFaceInput.selection(0).entity

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
    def extrudeNumbering(self, face):
        return


class NumbererCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # when the command is done, terminate the script
            # this will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class NumbererCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            cmd = args.command
            cmd.isRepeatable = False

            onExecute = NumbererCommandExecuteHandler()
            cmd.execute.add(onExecute)

            onDestroy = NumbererCommandDestroyHandler()
            cmd.destroy.add(onDestroy)

            handlers.append(onExecute)
            handlers.append(onDestroy)

            inputs = cmd.commandInputs
            inputs.addStringValueInput('start', 'Start', str(1))
            faceSelectioninput = inputs.addSelectionInput('face', 'Labeled Face', 'Face To Label')
            faceSelectioninput.addSelectionFilter('Faces')
        except:
            if ui:
                ui.messageBox('Failed: \n{}'.format(traceback.format_exc()))  

def create_text_sketch(sketch, text, position, size, ui):
    """Create a text sketch in the specified position and size."""
    textInput = sketch.sketchTexts.createInput2(str(text), 4.0)
    textInput.textHeight = size
    textInput.text = text
    textInput.setAsMultiLine(adsk.core.Point3D.create(0, 0, 0),
                        adsk.core.Point3D.create(10, 5, 0),
                        adsk.core.HorizontalAlignments.LeftHorizontalAlignment,
                        adsk.core.VerticalAlignments.TopVerticalAlignment, 0)
    sketchText = sketch.sketchTexts.add(textInput)
    return sketchText

def run(context):
    commandDefinitions = ui.commandDefinitions
    cmdDef = commandDefinitions.itemById('Numberer')

    if not cmdDef:
        cmdDef = commandDefinitions.addButtonDefinition('Numberer', 
                                                'Number Parts',
                                                'idk')
    onCommandCreated = NumbererCommandCreatedHandler()
     
    try:
        cmdDef.commandCreated.add(onCommandCreated)
    except Exception as e:
        ui.messageBox(str(e))

    handlers.append(onCommandCreated)
    inputs = adsk.core.NamedValues.create()
    cmdDef.execute(inputs)
    adsk.autoTerminate(False)
    return
    try:
        # Get the active design
        design = app.activeProduct
        if not design:
            ui.messageBox('No active design')
            return

        # Get the root component
        rootComp = design.rootComponent

        # Get the body to be duplicated
        bodies = rootComp.bRepBodies
        if bodies.count == 0:
            ui.messageBox('No bodies found in the root component')
            return

        body = bodies[0]  # Assuming you want the first body
        number_list = list(range(1, 11))  # List of numbers to use

        # Access the components, sketches, and features
        sketches = rootComp.sketches
        extrudeFeatures = rootComp.features.extrudeFeatures

        for number in number_list:
            # Create a new component for each body
            newComp = rootComp#.occurrences.addNewComponent(adsk.core.Matrix3D.create())

            newBody = body.copyToComponent(rootComp)
            newBody.name = f"Body_{number}"

            # Create a new sketch for text
            sketch = sketches.add(newComp.xYConstructionPlane)
            
            # Define text parameters
            text = f"{number}"
            position = adsk.core.Point3D.create(0, 0, 0)
            size = 5  # Adjust text size as needed

            # Create text sketch
            textInput = create_text_sketch(sketch, str(text), position, size, ui)

            # Define profile and extrusion
            extrudeInput = extrudeFeatures.createInput(textInput, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrudeInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(5.0))  # Adjust extrusion height
            extrude = extrudeFeatures.add(extrudeInput)

            # Set the file name
            dirPath = os.path.dirname(os.path.realpath(__file__))

            fileName = dirPath + f"/Body_{number}.stl"
            

            # Set export options
            exportMgr = design.exportManager
            stlOptions = exportMgr.createSTLExportOptions(newBody, fileName)
            stlOptions.sendToPrintUtility = False  # Adjust if you want to print directly

            # Export as STL
            exportMgr.execute(stlOptions)
            # Remove the new component to keep the design clean
            newBody.deleteMe()
            sketch.deleteMe()

        ui.messageBox('STL files with text extrusions generated successfully.')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
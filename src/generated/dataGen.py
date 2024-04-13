import json
import os, shutil

class DataGen:
    #ModID = the sting ID of the mod
    #outputLocation = the sting file path of where the json files will be stored
    #                 for using forge generated file struecture, that is the generated folder
    #resourcesFolder = output location + resources folder
    generatedFileCount = {
        "total": 0,
        "blockstates": 0,
        "blockModels": 0,
        "itemModels": 0,
        "recipes": 0,
        "tags": 0
    }
    
    def __init__(self, ModIDInput, useForgeGenerated=True, clearResources=True, storagePath="./"):
        self.ModID = ModIDInput #save the ModID
        
        if storagePath != "./":  #override useForgeGenerated if storage location is hard set
            useForgeGenerated = False
            
        if useForgeGenerated:  #finds the root directory of a forge mod and sets the generated location
            for dirItem in os.listdir("./"):
                if dirItem == "src":
                    rootFound = 1
                    forgePath = "./"
                else:
                    rootFound = 0
                    forgePath = "../"
            while rootFound == 0:
                dirList = os.listdir(forgePath)
                for dirItem in dirList:
                    if dirItem == "src":
                        rootFound = 1
                    else:
                        forgePath += ("../")
            forgePath += "src/generated/"
            if not os.path.exists(forgePath):
                os.mkdir(forgePath)
            self.outputLocation = forgePath
                
        elif not(useForgeGenerated):
            self.outputLocation = storagePath
            
        if clearResources:
            if os.path.exists(self.outputLocation + "resources"):
                shutil.rmtree(self.outputLocation + "resources")
                
        if not os.path.exists(self.outputLocation + "resources"):
            os.mkdir(self.outputLocation + "resources")
            
        self.resourcesFolder = self.outputLocation + "resources/"
    
    #debug commands
    def printFileCount(self):
        print("Generated File Counts:")
        print(self.generatedFileCount)
        
    def printFilePath(self):
        print(self.outputLocation)
        
    #commands for adding all top level folders
    def makeDataFolder(self):
        if not os.path.exists(self.resourcesFolder + "data"):
            os.mkdir(self.resourcesFolder + "data")
            
    def makeAssetsFolder(self):
        if not os.path.exists(self.resourcesFolder + "assets"):
            os.mkdir(self.resourcesFolder + "assets")
            
    def makeModAssetsFolder(self):
        self.makeAssetsFolder()
        if not os.path.exists(self.resourcesFolder + "assets/" + self.ModID):
            os.mkdir(self.resourcesFolder + "assets/" + self.ModID)
            
    def makeMinecraftAssetsFolder(self):
        self.makeAssetsFolder()
        if not os.path.exists(self.resourcesFolder + "assets/minecraft"):
            os.mkdir(self.resourcesFolder + "assets/minecraft")
            
    def makeForgeAssetsFolder(self):
        self.makeAssetsFolder()
        if not os.path.exists(self.resourcesFolder + "assets/forge"):
            os.mkdir(self.resourcesFolder + "assets/forge")
            
    def makeModDataFolder(self):
        self.makeDataFolder()
        if not os.path.exists(self.resourcesFolder + "data/" + self.ModID):
            os.mkdir(self.resourcesFolder + "data/" + self.ModID)
            
    def makeMinecraftDataFolder(self):
        self.makeDataFolder()
        if not os.path.exists(self.resourcesFolder + "data/minecraft"):
            os.mkdir(self.resourcesFolder + "data/minecraft")
            
    def makeForgeDataFolder(self):
        self.makeDataFolder()
        if not os.path.exists(self.resourcesFolder + "data/forge"):
            os.mkdir(self.resourcesFolder + "data/forge")
            
    #*commands for adding different types of blocks
    def addCubeBlock(self, fullBlockID, renderType=0, usingModNamespace=True):
        dumpLocation = self.resourcesFolder + "assets/"
        workingNamespace = ""
        blockName = ""
        
        if usingModNamespace:
            workingNamespace = self.ModID
            blockName = fullBlockID
            dumpLocation += (workingNamespace + "/")
        else:
            beforeColon = 1
            for letter in fullBlockID:  #pull the namespace and block name
                if letter == ":":
                    beforeColon = 0
                if beforeColon:
                    dumpLocation += letter
                    workingNamespace += letter
                if beforeColon == 0 and letter != ":":
                    blockName += letter
            dumpLocation += "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "assets/" + self.ModID + "/":
            self.makeModAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/minecraft/":
            self.makeMinecraftAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/forge/":
            self.makeForgeAssetsFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "blockstates"):
            os.mkdir(dumpLocation + "blockstates")
        if not os.path.exists(dumpLocation + "models"):
            os.mkdir(dumpLocation + "models")
        if not os.path.exists(dumpLocation + "models/block"):
            os.mkdir(dumpLocation + "models/block")
        if not os.path.exists(dumpLocation + "models/item"):
            os.mkdir(dumpLocation + "models/item")
            
        #make the dicts for all the json files
        blockstatesJson = {
            "variants": {
                "": {
                    "model": workingNamespace + ":block/" + blockName
                }
            }
        }
        blockModelJson = {
            "parent": "minecraft:block/cube_all",
            "textures": {
                "all": workingNamespace + ":block/" + blockName
            }
        }
        itemModelJson = {
            "parent": workingNamespace + ":block/" + blockName
        }
        if renderType != 0:
            blockModelJson["render_type"] = renderType
        
        #dump the json files
        json.dump(blockstatesJson, open(dumpLocation + "blockstates/" + blockName + ".json", "w"), indent=2)
        json.dump(blockModelJson, open(dumpLocation + "models/block/" + blockName + ".json", "w"), indent=2)
        json.dump(itemModelJson, open(dumpLocation + "models/item/" + blockName + ".json", "w"), indent=2)

        #update counts
        self.generatedFileCount["total"] += 3
        self.generatedFileCount["blockstates"] += 1
        self.generatedFileCount["blockModels"] += 1
        self.generatedFileCount["itemModels"] += 1
        
    def addButtonBlock(self, fullBlockID, textureName, renderType=0, usingModNamespace=True):
        dumpLocation = self.resourcesFolder + "assets/"
        workingNamespace = ""
        blockName = ""
        
        if usingModNamespace:
            workingNamespace = self.ModID
            blockName = fullBlockID
            dumpLocation += (workingNamespace + "/")
        else:
            beforeColon = 1
            for letter in fullBlockID:  #pull the namespace and block name
                if letter == ":":
                    beforeColon = 0
                if beforeColon:
                    dumpLocation += letter
                    workingNamespace += letter
                if beforeColon == 0 and letter != ":":
                    blockName += letter
            dumpLocation += "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "assets/" + self.ModID + "/":
            self.makeModAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/minecraft/":
            self.makeMinecraftAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/forge/":
            self.makeForgeAssetsFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "blockstates"):
            os.mkdir(dumpLocation + "blockstates")
        if not os.path.exists(dumpLocation + "models"):
            os.mkdir(dumpLocation + "models")
        if not os.path.exists(dumpLocation + "models/block"):
            os.mkdir(dumpLocation + "models/block")
        if not os.path.exists(dumpLocation + "models/item"):
            os.mkdir(dumpLocation + "models/item")
            
        #make the dicts for the json files
        blockstatesJson = {
            "variants": {
                "face=ceiling,facing=east,powered=false": {
                    "model": workingNamespace + ":block/"  + blockName, "x": 180, "y": 270
                },
                "face=ceiling,facing=east,powered=true": {
                    "model": workingNamespace + ":block/"  + blockName + "_pressed", "x": 180, "y": 270
                },
                "face=ceiling,facing=north,powered=false": {
                    "model": workingNamespace + ":block/"  + blockName, "x": 180, "y": 180
                },
                "face=ceiling,facing=north,powered=true": {
                    "model": workingNamespace + ":block/"  + blockName + "_pressed", "x": 180, "y": 180
                },
                "face=ceiling,facing=south,powered=false": {
                    "model": workingNamespace + ":block/"  + blockName, "x": 180
                },
                "face=ceiling,facing=south,powered=true": {
                    "model": workingNamespace + ":block/"  + blockName + "_pressed", "x": 180
                },
                "face=ceiling,facing=west,powered=false": {
                    "model": workingNamespace + ":block/"  + blockName, "x": 180, "y": 90
                },
                "face=ceiling,facing=west,powered=true": {
                    "model": workingNamespace + ":block/"  + blockName + "_pressed", "x": 180, "y": 90
                },
                "face=floor,facing=east,powered=false": {
                    "model": workingNamespace + ":block/"  + blockName, "y": 90
                },
                "face=floor,facing=east,powered=true": {
                    "model": workingNamespace + ":block/"  + blockName + "_pressed", "y": 90
                },
                "face=floor,facing=north,powered=false": {
                    "model": workingNamespace + ":block/"  + blockName
                },
                "face=floor,facing=north,powered=true": {
                    "model": workingNamespace + ":block/"  + blockName + "_pressed"
                },
                "face=floor,facing=south,powered=false": {
                    "model": workingNamespace + ":block/"  + blockName, "y": 180
                },
                "face=floor,facing=south,powered=true": {
                    "model": workingNamespace + ":block/"  + blockName + "_pressed", "y": 180
                },
                "face=floor,facing=west,powered=false": {
                    "model": workingNamespace + ":block/"  + blockName, "y": 270
                },
                "face=floor,facing=west,powered=true": {
                    "model": workingNamespace + ":block/"  + blockName + "_pressed", "y": 270
                },
                "face=wall,facing=east,powered=false": {
                    "model": workingNamespace + ":block/"  + blockName, "uvlock": True, "x": 90, "y": 90
                },
                "face=wall,facing=east,powered=true": {
                    "model": workingNamespace + ":block/"  + blockName + "_pressed", "uvlock": True, "x": 90, "y": 90
                },
                "face=wall,facing=north,powered=false": {
                    "model": workingNamespace + ":block/"  + blockName, "uvlock": True, "x": 90
                },
                "face=wall,facing=north,powered=true": {
                    "model": workingNamespace + ":block/"  + blockName + "_pressed", "uvlock": True,  "x": 90
                },
                "face=wall,facing=south,powered=false": {
                    "model": workingNamespace + ":block/"  + blockName, "uvlock": True, "x": 90, "y": 180
                },
                "face=wall,facing=south,powered=true": {
                    "model": workingNamespace + ":block/"  + blockName + "_pressed", "uvlock": True, "x": 90, "y": 180
                },
                "face=wall,facing=west,powered=false": {
                    "model": workingNamespace + ":block/"  + blockName, "uvlock": True, "x": 90, "y": 270
                },
                "face=wall,facing=west,powered=true": {
                    "model": workingNamespace + ":block/"  + blockName + "_pressed", "uvlock": True, "x": 90, "y": 270
                }
            }
        }
        buttonModelJson = {
            "parent": "minecraft:block/button",
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        buttonPressedModelJson = {
            "parent": "minecraft:block/button_pressed",
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        itemModelJson = {
            "parent": "minecraft:block/button_inventory",
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        if renderType != 0:
            buttonModelJson["render_type"] = renderType
            buttonPressedModelJson["render_type"] = renderType
            itemModelJson["render_type"] = renderType

        
        #dump the json files
        json.dump(blockstatesJson, open(dumpLocation + "blockstates/" + blockName + ".json", "w"), indent=2)
        json.dump(buttonModelJson, open(dumpLocation + "models/block/" + blockName + ".json", "w"), indent=2)
        json.dump(buttonPressedModelJson, open(dumpLocation + "models/block/" + blockName + "_pressed.json", "w"), indent=2)
        json.dump(itemModelJson, open(dumpLocation + "models/item/" + blockName + ".json", "w"), indent=2)
           
        #update counts
        self.generatedFileCount["total"] += 4
        self.generatedFileCount["blockstates"] += 1
        self.generatedFileCount["blockModels"] += 2
        self.generatedFileCount["itemModels"] += 1
        
    def addDoorBlock(self, fullBlockID, topTextureName, bottomTextureName, itemTextureName, usingModNamespace=True, renderType="cutout"):
        dumpLocation = self.resourcesFolder + "assets/"
        workingNamespace = ""
        blockName = ""
        
        if usingModNamespace:
            workingNamespace = self.ModID
            blockName = fullBlockID
            dumpLocation += (workingNamespace + "/")
        else:
            beforeColon = 1
            for letter in fullBlockID:  #pull the namespace and block name
                if letter == ":":
                    beforeColon = 0
                if beforeColon:
                    dumpLocation += letter
                    workingNamespace += letter
                if beforeColon == 0 and letter != ":":
                    blockName += letter
            dumpLocation += "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "assets/" + self.ModID + "/":
            self.makeModAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/minecraft/":
            self.makeMinecraftAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/forge/":
            self.makeForgeAssetsFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "blockstates"):
            os.mkdir(dumpLocation + "blockstates")
        if not os.path.exists(dumpLocation + "models"):
            os.mkdir(dumpLocation + "models")
        if not os.path.exists(dumpLocation + "models/block"):
            os.mkdir(dumpLocation + "models/block")
        if not os.path.exists(dumpLocation + "models/item"):
            os.mkdir(dumpLocation + "models/item")
            
        #make dicts for json files
        blockstatesJson = {
            "variants": {
                "facing=east,half=lower,hinge=left,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_left"
                },
                "facing=east,half=lower,hinge=left,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_left_open", "y": 90
                },
                "facing=east,half=lower,hinge=right,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_right"
                },
                "facing=east,half=lower,hinge=right,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_right_open", "y": 270
                },
                "facing=east,half=upper,hinge=left,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_top_left"
                },
                "facing=east,half=upper,hinge=left,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_top_left_open", "y": 90
                },
                "facing=east,half=upper,hinge=right,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_top_right"
                },
                "facing=east,half=upper,hinge=right,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_top_right_open", "y": 270
                },
                "facing=north,half=lower,hinge=left,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_left", "y": 270
                },
                "facing=north,half=lower,hinge=left,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_left_open"
                },
                "facing=north,half=lower,hinge=right,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_right", "y": 270
                },
                "facing=north,half=lower,hinge=right,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_right_open", "y": 180
                },
                "facing=north,half=upper,hinge=left,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_top_left", "y": 270
                },
                "facing=north,half=upper,hinge=left,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_top_left_open"
                },
                "facing=north,half=upper,hinge=right,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_top_right", "y": 270
                },
                "facing=north,half=upper,hinge=right,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_top_right_open", "y": 180
                },
                "facing=south,half=lower,hinge=left,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_left", "y": 90
                },
                "facing=south,half=lower,hinge=left,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_left_open", "y": 180
                },
                "facing=south,half=lower,hinge=right,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_right", "y": 90
                },
                "facing=south,half=lower,hinge=right,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_right_open"
                },
                "facing=south,half=upper,hinge=left,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_top_left", "y": 90
                },
                "facing=south,half=upper,hinge=left,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_top_left_open", "y": 180
                },
                "facing=south,half=upper,hinge=right,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_top_right", "y": 90
                },
                "facing=south,half=upper,hinge=right,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_top_right_open"
                },
                "facing=west,half=lower,hinge=left,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_left", "y": 180
                },
                "facing=west,half=lower,hinge=left,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_left_open", "y": 270
                },
                "facing=west,half=lower,hinge=right,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_right", "y": 180
                },
                "facing=west,half=lower,hinge=right,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom_right_open", "y": 90
                },
                "facing=west,half=upper,hinge=left,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_top_left", "y": 180
                },
                "facing=west,half=upper,hinge=left,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_top_left_open", "y": 270
                },
                "facing=west,half=upper,hinge=right,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_top_right", "y": 180
                },
                "facing=west,half=upper,hinge=right,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_top_right_open", "y": 90
                }
            }       
        }
        doorBottomLeft = {
            "parent": "minecraft:block/door_bottom_left",
            "textures": {
                "bottom": workingNamespace + ":block/" + bottomTextureName,
                "top": workingNamespace + ":block/" + topTextureName
            }
        }
        doorBottomLeftOpen = {
            "parent": "minecraft:block/door_bottom_left_open",
            "textures": {
                "bottom": workingNamespace + ":block/" + bottomTextureName,
                "top": workingNamespace + ":block/" + topTextureName
            }
        }
        doorBottomRight = {
            "parent": "minecraft:block/door_bottom_right",
            "textures": {
                "bottom": workingNamespace + ":block/" + bottomTextureName,
                "top": workingNamespace + ":block/" + topTextureName
            }
        }
        doorBottomRightOpen = {
            "parent": "minecraft:block/door_bottom_right_open",
            "textures": {
                "bottom": workingNamespace + ":block/" + bottomTextureName,
                "top": workingNamespace + ":block/" + topTextureName
            }
        }
        doorTopLeft = {
            "parent": "minecraft:block/door_top_left",
            "textures": {
                "bottom": workingNamespace + ":block/" + bottomTextureName,
                "top": workingNamespace + ":block/" + topTextureName
            }
        }
        doorTopLeftOpen = {
            "parent": "minecraft:block/door_top_left_open",
            "textures": {
                "bottom": workingNamespace + ":block/" + bottomTextureName,
                "top": workingNamespace + ":block/" + topTextureName
            }
        }
        doorTopRight = {
            "parent": "minecraft:block/door_top_right",
            "textures": {
                "bottom": workingNamespace + ":block/" + bottomTextureName,
                "top": workingNamespace + ":block/" + topTextureName
            }
        }
        doorTopRightOpen = {
            "parent": "minecraft:block/door_top_right_open",
            "textures": {
                "bottom": workingNamespace + ":block/" + bottomTextureName,
                "top": workingNamespace + ":block/" + topTextureName
            }
        }
        itemModelJson = {
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": workingNamespace + ":item/" + itemTextureName
            }
        }
        doorBottomLeft["render_type"] = renderType
        doorBottomLeftOpen["render_type"] = renderType
        doorBottomRight["render_type"] = renderType
        doorBottomRightOpen["render_type"] = renderType
        doorTopLeft["render_type"] = renderType
        doorTopLeftOpen["render_type"] = renderType
        doorTopRight["render_type"] = renderType
        doorTopRightOpen["render_type"] = renderType
        
        #dump jsons
        json.dump(blockstatesJson, open(dumpLocation + "blockstates/" + blockName + ".json", "w"), indent=2)
        json.dump(doorBottomLeft, open(dumpLocation + "models/block/" + blockName + "_bottom_left.json", "w"), indent=2)
        json.dump(doorBottomLeftOpen, open(dumpLocation + "models/block/" + blockName + "_bottom_left_open.json", "w"), indent=2)
        json.dump(doorBottomRight, open(dumpLocation + "models/block/" + blockName + "_bottom_right.json", "w"), indent=2)
        json.dump(doorBottomRightOpen, open(dumpLocation + "models/block/" + blockName + "_bottom_right_open.json", "w"), indent=2)
        json.dump(doorTopLeft, open(dumpLocation + "models/block/" + blockName + "_top_left.json", "w"), indent=2)
        json.dump(doorTopLeftOpen, open(dumpLocation + "models/block/" + blockName + "_top_left_open.json", "w"), indent=2)
        json.dump(doorTopRight, open(dumpLocation + "models/block/" + blockName + "_top_right.json", "w"), indent=2)
        json.dump(doorTopRightOpen, open(dumpLocation + "models/block/" + blockName + "_top_right_open.json", "w"), indent=2)
        json.dump(itemModelJson, open(dumpLocation + "models/item/" + blockName + ".json", "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 10
        self.generatedFileCount["blockstates"] += 1
        self.generatedFileCount["blockModels"] += 8
        self.generatedFileCount["itemModels"] += 1
        
    def addFenceBlock(self, fullBlockID, textureName, usingModNamespace=True, renderType=0, isWoodenFence=False):
        dumpLocation = self.resourcesFolder + "assets/"
        workingNamespace = ""
        blockName = ""
        
        if usingModNamespace:
            workingNamespace = self.ModID
            blockName = fullBlockID
            dumpLocation += (workingNamespace + "/")
        else:
            beforeColon = 1
            for letter in fullBlockID:  #pull the namespace and block name
                if letter == ":":
                    beforeColon = 0
                if beforeColon:
                    dumpLocation += letter
                    workingNamespace += letter
                if beforeColon == 0 and letter != ":":
                    blockName += letter
            dumpLocation += "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "assets/" + self.ModID + "/":
            self.makeModAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/minecraft/":
            self.makeMinecraftAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/forge/":
            self.makeForgeAssetsFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "blockstates"):
            os.mkdir(dumpLocation + "blockstates")
        if not os.path.exists(dumpLocation + "models"):
            os.mkdir(dumpLocation + "models")
        if not os.path.exists(dumpLocation + "models/block"):
            os.mkdir(dumpLocation + "models/block")
        if not os.path.exists(dumpLocation + "models/item"):
            os.mkdir(dumpLocation + "models/item")
            
        #dict for json files
        blockstatesJson = {
            "multipart": [
                {
                  "apply": { "model": workingNamespace + ":block/" + blockName + "_post" }
                },
                {
                  "apply": { "model": workingNamespace + ":block/" + blockName + "_side", "uvlock": True },
                  "when": { "north": "true" }
                },
                {
                  "apply": { "model": workingNamespace + ":block/" + blockName + "_side", "uvlock": True, "y": 180 },
                  "when": { "south": "true" }
                },
                {
                  "apply": { "model": workingNamespace + ":block/" + blockName + "_side", "uvlock": True, "y": 270 },
                  "when": { "west": "true" }
                },
                {
                  "apply": { "model": workingNamespace + ":block/" + blockName + "_side", "uvlock": True, "y": 90 },
                  "when": { "east": "true" }
                }
            ]
        }
        fencePostJson = {
            "parent": "minecraft:block/fence_post",
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        fenceSideJson = {
            "parent": "minecraft:block/fence_side",
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        itemModelJson = {
            "parent": "minecraft:block/fence_inventory",
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        if not renderType == 0:
            fencePostJson["render_type"] = renderType
            fenceSideJson["render_type"] = renderType
            
        #dump json files
        json.dump(blockstatesJson, open(dumpLocation + "blockstates/" + blockName + ".json", "w"), indent=2)
        json.dump(fencePostJson, open(dumpLocation + "models/block/" + blockName + "_post.json", "w"), indent=2)
        json.dump(fenceSideJson, open(dumpLocation + "models/block/" + blockName + "_side.json", "w"), indent=2)
        json.dump(itemModelJson, open(dumpLocation + "models/item/" + blockName + ".json", "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 4
        self.generatedFileCount["blockstates"] += 1
        self.generatedFileCount["blockModels"] += 2
        self.generatedFileCount["itemModels"] += 1
        
        #add to tag list
        self.makeMinecraftDataFolder()
        if not os.path.exists(self.resourcesFolder + "data/minecraft/tags/blocks/"):
            os.makedirs(self.resourcesFolder + "data/minecraft/tags/blocks/")
        tagFolderLocation = self.resourcesFolder + "data/minecraft/tags/blocks/"
        if isWoodenFence:
            if os.path.exists(tagFolderLocation + "wooden_fences.json"):
                woodenFencesTagJson = json.load(open(tagFolderLocation + "wooden_fences.json", "r"))
            else:
                woodenFencesTagJson = {
                    "values": []
                }
                self.generatedFileCount["tags"] += 1
                self.generatedFileCount["total"] += 1
            if usingModNamespace:
                woodenFencesTagJson["values"].append(workingNamespace + ":" + blockName)
            else:
                woodenFencesTagJson["values"].append(fullBlockID)
            json.dump(woodenFencesTagJson, open(tagFolderLocation + "wooden_fences.json", "w"), indent=2)
        else:
            if os.path.exists(tagFolderLocation + "fences.json"):
                woodenFencesTagJson = json.load(open(tagFolderLocation + "fences.json", "r"))
            else:
                woodenFencesTagJson = {
                    "values": []
                }
                self.generatedFileCount["tags"] += 1
                self.generatedFileCount["total"] += 1
            if usingModNamespace:
                woodenFencesTagJson["values"].append(workingNamespace + ":" + blockName)
            else:
                woodenFencesTagJson["values"].append(fullBlockID)
            json.dump(woodenFencesTagJson, open(tagFolderLocation + "fences.json", "w"), indent=2)
              
    def addFenceGateBlock(self, fullBlockID, textureName, usingModNamespace=True, renderType=0):
        dumpLocation = self.resourcesFolder + "assets/"
        workingNamespace = ""
        blockName = ""
        
        if usingModNamespace:
            workingNamespace = self.ModID
            blockName = fullBlockID
            dumpLocation += (workingNamespace + "/")
        else:
            beforeColon = 1
            for letter in fullBlockID:  #pull the namespace and block name
                if letter == ":":
                    beforeColon = 0
                if beforeColon:
                    dumpLocation += letter
                    workingNamespace += letter
                if beforeColon == 0 and letter != ":":
                    blockName += letter
            dumpLocation += "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "assets/" + self.ModID + "/":
            self.makeModAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/minecraft/":
            self.makeMinecraftAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/forge/":
            self.makeForgeAssetsFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "blockstates"):
            os.mkdir(dumpLocation + "blockstates")
        if not os.path.exists(dumpLocation + "models"):
            os.mkdir(dumpLocation + "models")
        if not os.path.exists(dumpLocation + "models/block"):
            os.mkdir(dumpLocation + "models/block")
        if not os.path.exists(dumpLocation + "models/item"):
            os.mkdir(dumpLocation + "models/item")
            
        #make dicts for json files
        blockstatesJson = {
            "variants": {
                "facing=east,in_wall=false,open=false": {
                    "model": workingNamespace + ":block/" + blockName, "uvlock": True, "y": 270
                },
                "facing=east,in_wall=false,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_open", "uvlock": True, "y": 270
                },
                "facing=east,in_wall=true,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_wall", "uvlock": True, "y": 270
                },
                "facing=east,in_wall=true,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_wall_open", "uvlock": True, "y": 270
                },
                "facing=north,in_wall=false,open=false": {
                    "model": workingNamespace + ":block/" + blockName, "uvlock": True, "y": 180
                },
                "facing=north,in_wall=false,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_open", "uvlock": True, "y": 180
                },
                "facing=north,in_wall=true,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_wall", "uvlock": True, "y": 180
                },
                "facing=north,in_wall=true,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_wall_open", "uvlock": True, "y": 180
                },
                "facing=south,in_wall=false,open=false": {
                    "model": workingNamespace + ":block/" + blockName, "uvlock": True
                },
                "facing=south,in_wall=false,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_open", "uvlock": True
                },
                "facing=south,in_wall=true,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_wall", "uvlock": True
                },
                "facing=south,in_wall=true,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_wall_open", "uvlock": True
                },
                "facing=west,in_wall=false,open=false": {
                    "model": workingNamespace + ":block/" + blockName, "uvlock": True, "y": 90
                },
                "facing=west,in_wall=false,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_open", "uvlock": True, "y": 90
                },
                "facing=west,in_wall=true,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_wall", "uvlock": True, "y": 90
                },
                "facing=west,in_wall=true,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_wall_open", "uvlock": True, "y": 90
                }
            }
        }
        fenceGateJson = {
            "parent": "minecraft:block/template_fence_gate",
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        fenceGateOpenJson = {"parent": "minecraft:block/template_fence_gate_open",
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }}
        fenceGateWallJson = {
            "parent": "minecraft:block/template_fence_gate_wall",
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        fenceGateWallOpenJson = {
            "parent": "minecraft:block/template_fence_gate_wall_open",
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        itemModelJson = {
            "parent": workingNamespace + ":block/" + blockName
        }
        if not renderType == 0:
            fenceGateJson["render_type"] = renderType
            fenceGateOpenJson["render_type"] = renderType
            fenceGateWallJson["render_type"] = renderType
            fenceGateWallOpenJson["render_type"] = renderType
        
            
        #dump json files
        json.dump(blockstatesJson, open(dumpLocation + "blockstates/" + blockName + ".json", "w"), indent=2)
        json.dump(fenceGateJson, open(dumpLocation + "models/block/" + blockName + ".json", "w"), indent=2)
        json.dump(fenceGateOpenJson, open(dumpLocation + "models/block/" + blockName + "_open.json", "w"), indent=2)
        json.dump(fenceGateWallJson, open(dumpLocation + "models/block/" + blockName + "_wall.json", "w"), indent=2)
        json.dump(fenceGateWallOpenJson, open(dumpLocation + "models/block/" + blockName + "_wall_open.json", "w"), indent=2)
        json.dump(itemModelJson, open(dumpLocation + "models/item/" + blockName + ".json", "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 6
        self.generatedFileCount["blockstates"] += 1
        self.generatedFileCount["blockModels"] += 4
        self.generatedFileCount["itemModels"] += 1
        
        #add to tag list
        self.makeMinecraftDataFolder()
        if not os.path.exists(self.resourcesFolder + "data/minecraft/tags/blocks/"):
            os.makedirs(self.resourcesFolder + "data/minecraft/tags/blocks/")
        tagFolderLocation = self.resourcesFolder + "data/minecraft/tags/blocks/"
        if os.path.exists(tagFolderLocation + "fence_gates.json"):
            woodenFencesTagJson = json.load(open(tagFolderLocation + "fence_gates.json", "r"))
        else:
            woodenFencesTagJson = {
                "values": []
            }
            self.generatedFileCount["tags"] += 1
            self.generatedFileCount["total"] += 1
        if usingModNamespace:
            woodenFencesTagJson["values"].append(workingNamespace + ":" + blockName)
        else:
            woodenFencesTagJson["values"].append(fullBlockID)
        json.dump(woodenFencesTagJson, open(tagFolderLocation + "fence_gates.json", "w"), indent=2)
        
    def addPressurePlateBlock(self, fullBlockID, textureName, usingModNamespace=True, renderType=0):
        dumpLocation = self.resourcesFolder + "assets/"
        workingNamespace = ""
        blockName = ""
        
        if usingModNamespace:
            workingNamespace = self.ModID
            blockName = fullBlockID
            dumpLocation += (workingNamespace + "/")
        else:
            beforeColon = 1
            for letter in fullBlockID:  #pull the namespace and block name
                if letter == ":":
                    beforeColon = 0
                if beforeColon:
                    dumpLocation += letter
                    workingNamespace += letter
                if beforeColon == 0 and letter != ":":
                    blockName += letter
            dumpLocation += "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "assets/" + self.ModID + "/":
            self.makeModAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/minecraft/":
            self.makeMinecraftAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/forge/":
            self.makeForgeAssetsFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "blockstates"):
            os.mkdir(dumpLocation + "blockstates")
        if not os.path.exists(dumpLocation + "models"):
            os.mkdir(dumpLocation + "models")
        if not os.path.exists(dumpLocation + "models/block"):
            os.mkdir(dumpLocation + "models/block")
        if not os.path.exists(dumpLocation + "models/item"):
            os.mkdir(dumpLocation + "models/item")
            
        #dicts for json files
        blockstatesJson = {
            "variants": {
                "powered=false": {
                    "model": workingNamespace + ":block/" + blockName
                },
                "powered=true": {
                    "model": workingNamespace + ":block/" + blockName + "_down"
                }
            }
        }
        pressurePlateJson = {
            "parent": "minecraft:block/pressure_plate_up",
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        pressurePlateDownJson = {
            "parent": "minecraft:block/pressure_plate_down",
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        itemModelJson = {
            "parent": workingNamespace + ":block/" + blockName
        }
        if not renderType == 0:
            pressurePlateJson["render_type"] = renderType
            pressurePlateDownJson["render_type"] = renderType
            
        #dump json files
        json.dump(blockstatesJson, open(dumpLocation + "blockstates/" + blockName + ".json", "w"), indent=2)
        json.dump(pressurePlateJson, open(dumpLocation + "models/block/" + blockName + ".json", "w"), indent=2)
        json.dump(pressurePlateDownJson, open(dumpLocation + "models/block/" + blockName + "_down.json", "w"), indent=2)
        json.dump(itemModelJson, open(dumpLocation + "models/item/" + blockName + ".json", "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 4
        self.generatedFileCount["blockstates"] += 1
        self.generatedFileCount["blockModels"] += 2
        self.generatedFileCount["itemModels"] += 1
        
    def addSlabBlock(self, fullBlockID, textureName, fullBlockModelName=0, usingModNamespace=True, renderType=0):
        dumpLocation = self.resourcesFolder + "assets/"
        if fullBlockModelName == 0:
            fullBlockModelName = textureName
        workingNamespace = ""
        blockName = ""
        
        if usingModNamespace:
            workingNamespace = self.ModID
            blockName = fullBlockID
            dumpLocation += (workingNamespace + "/")
        else:
            beforeColon = 1
            for letter in fullBlockID:  #pull the namespace and block name
                if letter == ":":
                    beforeColon = 0
                if beforeColon:
                    dumpLocation += letter
                    workingNamespace += letter
                if beforeColon == 0 and letter != ":":
                    blockName += letter
            dumpLocation += "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "assets/" + self.ModID + "/":
            self.makeModAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/minecraft/":
            self.makeMinecraftAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/forge/":
            self.makeForgeAssetsFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "blockstates"):
            os.mkdir(dumpLocation + "blockstates")
        if not os.path.exists(dumpLocation + "models"):
            os.mkdir(dumpLocation + "models")
        if not os.path.exists(dumpLocation + "models/block"):
            os.mkdir(dumpLocation + "models/block")
        if not os.path.exists(dumpLocation + "models/item"):
            os.mkdir(dumpLocation + "models/item")
        
        #dicts for json files
        blockstatesJson = {
            "variants": {
                "type=bottom": {
                    "model": workingNamespace + ":block/" + blockName
                },
                "type=double": {
                    "model": workingNamespace + ":block/" + fullBlockModelName
                },
                "type=top": {
                    "model": workingNamespace + ":block/" + blockName + "_top"
                }    
            }           
        }
        slabModelJson = {
            "parent": "minecraft:block/slab",
            "textures": {
                "bottom": workingNamespace + ":block/" + textureName,
                "side": workingNamespace + ":block/" + textureName,
                "top": workingNamespace + ":block/" + textureName
            }
        }
        slabTopModelJson = {
            "parent": "minecraft:block/slab_top",
            "textures": {
                "bottom": workingNamespace + ":block/" + textureName,
                "side": workingNamespace + ":block/" + textureName,
                "top": workingNamespace + ":block/" + textureName
            }
        }
        itemModelJson = {
            "parent": workingNamespace + ":block/" + blockName 
        }
        if not renderType == 0:
            slabModelJson["render_type"] = renderType
            slabTopModelJson["render_type"] = renderType
        
        #dump json files
        json.dump(blockstatesJson, open(dumpLocation + "blockstates/" + blockName + ".json", "w"), indent=2)
        json.dump(slabModelJson, open(dumpLocation + "models/block/" + blockName + ".json", "w"), indent=2)
        json.dump(slabTopModelJson, open(dumpLocation + "models/block/" + blockName + "_top.json", "w"), indent=2)
        json.dump(itemModelJson, open(dumpLocation + "models/item/" + blockName + ".json", "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 4
        self.generatedFileCount["blockstates"] += 1
        self.generatedFileCount["blockModels"] += 2
        self.generatedFileCount["itemModels"] += 1
        
    def addStairBlock(self, fullBlockID, textureName, usingModNamespace=True, renderType=0):
        dumpLocation = self.resourcesFolder + "assets/"
        workingNamespace = ""
        blockName = ""
        
        if usingModNamespace:
            workingNamespace = self.ModID
            blockName = fullBlockID
            dumpLocation += (workingNamespace + "/")
        else:
            beforeColon = 1
            for letter in fullBlockID:  #pull the namespace and block name
                if letter == ":":
                    beforeColon = 0
                if beforeColon:
                    dumpLocation += letter
                    workingNamespace += letter
                if beforeColon == 0 and letter != ":":
                    blockName += letter
            dumpLocation += "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "assets/" + self.ModID + "/":
            self.makeModAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/minecraft/":
            self.makeMinecraftAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/forge/":
            self.makeForgeAssetsFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "blockstates"):
            os.mkdir(dumpLocation + "blockstates")
        if not os.path.exists(dumpLocation + "models"):
            os.mkdir(dumpLocation + "models")
        if not os.path.exists(dumpLocation + "models/block"):
            os.mkdir(dumpLocation + "models/block")
        if not os.path.exists(dumpLocation + "models/item"):
            os.mkdir(dumpLocation + "models/item")
            
        #dicts for json files
        blockstatesJson = {
            "variants": {
                "facing=east,half=bottom,shape=inner_left": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "y": 270
                },
                "facing=east,half=bottom,shape=inner_right": {
                    "model": workingNamespace + ":block/" + blockName + "_inner"
                },
                "facing=east,half=bottom,shape=outer_left": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "y": 270
                },
                "facing=east,half=bottom,shape=outer_right": {
                    "model": workingNamespace + ":block/" + blockName + "_outer"
                },
                "facing=east,half=bottom,shape=straight": {
                    "model": workingNamespace + ":block/" + blockName
                },
                "facing=east,half=top,shape=inner_left": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "x": 180
                },
                "facing=east,half=top,shape=inner_right": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "x": 180, "y": 90
                },
                "facing=east,half=top,shape=outer_left": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "x": 180
                },
                "facing=east,half=top,shape=outer_right": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "x": 180, "y": 90
                },
                "facing=east,half=top,shape=straight": {
                    "model": workingNamespace + ":block/" + blockName, "uvlock": True, "x": 180
                },
                "facing=north,half=bottom,shape=inner_left": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "y": 180
                },
                "facing=north,half=bottom,shape=inner_right": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "y": 270
                },
                "facing=north,half=bottom,shape=outer_left": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "y": 180
                },
                "facing=north,half=bottom,shape=outer_right": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "y": 270
                },
                "facing=north,half=bottom,shape=straight": {
                    "model": workingNamespace + ":block/" + blockName, "uvlock": True, "y": 270
                },
                "facing=north,half=top,shape=inner_left": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "x": 180, "y": 270
                },
                "facing=north,half=top,shape=inner_right": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "x": 180
                },
                "facing=north,half=top,shape=outer_left": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "x": 180, "y": 270
                },
                "facing=north,half=top,shape=outer_right": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "x": 180
                },
                "facing=north,half=top,shape=straight": {
                    "model": workingNamespace + ":block/" + blockName, "uvlock": True, "x": 180, "y": 270
                },
                "facing=south,half=bottom,shape=inner_left": {
                    "model": workingNamespace + ":block/" + blockName + "_inner"
                },
                "facing=south,half=bottom,shape=inner_right": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "y": 90
                },
                "facing=south,half=bottom,shape=outer_left": {
                    "model": workingNamespace + ":block/" + blockName + "_outer"
                },
                "facing=south,half=bottom,shape=outer_right": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "y": 90
                },
                "facing=south,half=bottom,shape=straight": {
                    "model": workingNamespace + ":block/" + blockName, "uvlock": True, "y": 90
                },
                "facing=south,half=top,shape=inner_left": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "x": 180, "y": 90
                },
                "facing=south,half=top,shape=inner_right": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "x": 180, "y": 180
                },
                "facing=south,half=top,shape=outer_left": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "x": 180, "y": 90
                },
                "facing=south,half=top,shape=outer_right": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "x": 180, "y": 180
                },
                "facing=south,half=top,shape=straight": {
                    "model": workingNamespace + ":block/" + blockName, "uvlock": True, "x": 180, "y": 90
                },
                "facing=west,half=bottom,shape=inner_left": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "y": 90
                },
                "facing=west,half=bottom,shape=inner_right": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "y": 180
                },
                "facing=west,half=bottom,shape=outer_left": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "y": 90
                },
                "facing=west,half=bottom,shape=outer_right": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "y": 180
                },
                "facing=west,half=bottom,shape=straight": {
                    "model": workingNamespace + ":block/" + blockName, "uvlock": True, "y": 180
                },
                "facing=west,half=top,shape=inner_left": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "x": 180, "y": 180
                },
                "facing=west,half=top,shape=inner_right": {
                    "model": workingNamespace + ":block/" + blockName + "_inner", "uvlock": True, "x": 180, "y": 270
                },
                "facing=west,half=top,shape=outer_left": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "x": 180, "y": 180
                },
                "facing=west,half=top,shape=outer_right": {
                    "model": workingNamespace + ":block/" + blockName + "_outer", "uvlock": True, "x": 180, "y": 270
                },
                "facing=west,half=top,shape=straight": {
                    "model": workingNamespace + ":block/" + blockName, "uvlock": True, "x": 180, "y": 180
                }
            }
        }
        stairModelJson = {
            "parent": "minecraft:block/stairs",
            "textures": {
                "bottom": workingNamespace + ":block/" + textureName,
                "side": workingNamespace + ":block/" + textureName,
                "top": workingNamespace + ":block/" + textureName
            }
        }
        stairInnerModelJson = {
            "parent": "minecraft:block/inner_stairs",
            "textures": {
                "bottom": workingNamespace + ":block/" + textureName,
                "side": workingNamespace + ":block/" + textureName,
                "top": workingNamespace + ":block/" + textureName
            }
        }
        stairOuterModelJson = {
            "parent": "minecraft:block/outer_stairs",
            "textures": {
                "bottom": workingNamespace + ":block/" + textureName,
                "side": workingNamespace + ":block/" + textureName,
                "top": workingNamespace + ":block/" + textureName
            }
        }
        itemModelJson = {
            "parent": workingNamespace + ":block/" + blockName
        }
        if not renderType == 0:
            stairModelJson["render_type"] = renderType
            stairInnerModelJson["render_type"] = renderType
            stairOuterModelJson["render_type"] = renderType
        
        #dump json files
        json.dump(blockstatesJson, open(dumpLocation + "blockstates/" + blockName + ".json", "w"), indent=2)
        json.dump(stairModelJson, open(dumpLocation + "models/block/" + blockName + ".json", "w"), indent=2)
        json.dump(stairInnerModelJson, open(dumpLocation + "models/block/" + blockName + "_inner.json", "w"), indent=2)
        json.dump(stairOuterModelJson, open(dumpLocation + "models/block/" + blockName + "_outer.json", "w"), indent=2)
        json.dump(itemModelJson, open(dumpLocation + "models/item/" + blockName + ".json", "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 5
        self.generatedFileCount["blockstates"] += 1
        self.generatedFileCount["blockModels"] += 3
        self.generatedFileCount["itemModels"] += 1
        
    def addTrapdoorBlock(self, fullBlockID, textureName, usingModNamespace=True, renderType="cutout"):
        dumpLocation = self.resourcesFolder + "assets/"
        workingNamespace = ""
        blockName = ""
        
        if usingModNamespace:
            workingNamespace = self.ModID
            blockName = fullBlockID
            dumpLocation += (workingNamespace + "/")
        else:
            beforeColon = 1
            for letter in fullBlockID:  #pull the namespace and block name
                if letter == ":":
                    beforeColon = 0
                if beforeColon:
                    dumpLocation += letter
                    workingNamespace += letter
                if beforeColon == 0 and letter != ":":
                    blockName += letter
            dumpLocation += "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "assets/" + self.ModID + "/":
            self.makeModAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/minecraft/":
            self.makeMinecraftAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/forge/":
            self.makeForgeAssetsFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "blockstates"):
            os.mkdir(dumpLocation + "blockstates")
        if not os.path.exists(dumpLocation + "models"):
            os.mkdir(dumpLocation + "models")
        if not os.path.exists(dumpLocation + "models/block"):
            os.mkdir(dumpLocation + "models/block")
        if not os.path.exists(dumpLocation + "models/item"):
            os.mkdir(dumpLocation + "models/item")
            
        #dicts for json files
        blockstatesJson = {
            "variants": {
                "facing=east,half=bottom,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom", "y": 90
                },
                "facing=east,half=bottom,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_open", "y": 90
                },
                "facing=east,half=top,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_top", "y": 90
                },
                "facing=east,half=top,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_open", "x": 180, "y": 270
                },
                "facing=north,half=bottom,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom"
                },
                "facing=north,half=bottom,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_open"
                },
                "facing=north,half=top,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_top"
                },
                "facing=north,half=top,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_open", "x": 180, "y": 180
                },
                "facing=south,half=bottom,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom", "y": 180
                },
                "facing=south,half=bottom,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_open", "y": 180
                },
                "facing=south,half=top,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_top", "y": 180
                },
                "facing=south,half=top,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_open", "x": 180
                },
                "facing=west,half=bottom,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_bottom", "y": 270
                },
                "facing=west,half=bottom,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_open", "y": 270
                },
                "facing=west,half=top,open=false": {
                    "model": workingNamespace + ":block/" + blockName + "_top", "y": 270
                },
                "facing=west,half=top,open=true": {
                    "model": workingNamespace + ":block/" + blockName + "_open", "x": 180, "y": 90
                }
            }
        }
        trapdoorBottomModelJson = {
            "parent": "minecraft:block/template_orientable_trapdoor_bottom",
            "render_type": renderType,
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        trapdoorOpenModelJson = {
            "parent": "minecraft:block/template_orientable_trapdoor_open",
            "render_type": renderType,
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        trapdoorTopModelJson = {
            "parent": "minecraft:block/template_orientable_trapdoor_top",
            "render_type": renderType,
            "textures": {
                "texture": workingNamespace + ":block/" + textureName
            }
        }
        itemModelJson = {
            "parent": workingNamespace + ":block/" + blockName + "_bottom"
        }
        
        #dump json files
        json.dump(blockstatesJson, open(dumpLocation + "blockstates/" + blockName + ".json", "w"), indent=2)
        json.dump(trapdoorBottomModelJson, open(dumpLocation + "models/block/" + blockName + "_bottom.json", "w"), indent=2)
        json.dump(trapdoorOpenModelJson, open(dumpLocation + "models/block/" + blockName + "_open.json", "w"), indent=2)
        json.dump(trapdoorTopModelJson, open(dumpLocation + "models/block/" + blockName + "_top.json", "w"), indent=2)
        json.dump(itemModelJson, open(dumpLocation + "models/item/" + blockName + ".json", "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 5
        self.generatedFileCount["blockstates"] += 1
        self.generatedFileCount["blockModels"] += 3
        self.generatedFileCount["itemModels"] += 1
        
    def addWallBlock(self, fullBlockID, textureName, usingModNamespace=True, renderType=0):
        dumpLocation = self.resourcesFolder + "assets/"
        workingNamespace = ""
        blockName = ""
        
        if usingModNamespace:
            workingNamespace = self.ModID
            blockName = fullBlockID
            dumpLocation += (workingNamespace + "/")
        else:
            beforeColon = 1
            for letter in fullBlockID:  #pull the namespace and block name
                if letter == ":":
                    beforeColon = 0
                if beforeColon:
                    dumpLocation += letter
                    workingNamespace += letter
                if beforeColon == 0 and letter != ":":
                    blockName += letter
            dumpLocation += "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "assets/" + self.ModID + "/":
            self.makeModAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/minecraft/":
            self.makeMinecraftAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/forge/":
            self.makeForgeAssetsFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "blockstates"):
            os.mkdir(dumpLocation + "blockstates")
        if not os.path.exists(dumpLocation + "models"):
            os.mkdir(dumpLocation + "models")
        if not os.path.exists(dumpLocation + "models/block"):
            os.mkdir(dumpLocation + "models/block")
        if not os.path.exists(dumpLocation + "models/item"):
            os.mkdir(dumpLocation + "models/item")
            
        #dicts for json files
        blockstatesJson = {
            "multipart": [
                {
                    "apply": { "model": workingNamespace + ":block/" + blockName + "_post" },
                    "when": { "up": "true" }
                },
                {
                    "apply": { "model": workingNamespace + ":block/" + blockName + "_side", "uvlock": True, "y": 90 },
                    "when": { "east": "low" }
                },
                {
                    "apply": { "model": workingNamespace + ":block/" + blockName + "_side_tall", "uvlock": True, "y": 90 },
                    "when": { "east": "tall" }
                },
                {
                    "apply": { "model": workingNamespace + ":block/" + blockName + "_side", "uvlock": True },
                    "when": { "north": "low" }
                },
                {
                    "apply": { "model": workingNamespace + ":block/" + blockName + "_side_tall", "uvlock": True },
                    "when": { "north": "tall" }
                },
                {
                    "apply": { "model": workingNamespace + ":block/" + blockName + "_side", "uvlock": True, "y": 180 },
                    "when": { "south": "low" }
                },  
                {   
                    "apply": { "model": workingNamespace + ":block/" + blockName + "_side_tall", "uvlock": True, "y": 180 },
                    "when": { "south": "tall" }
                },
                {
                    "apply": { "model": workingNamespace + ":block/" + blockName + "_side", "uvlock": True, "y": 270 },
                    "when": { "west": "low" }
                },
                {
                    "apply": { "model": workingNamespace + ":block/" + blockName + "_side_tall", "uvlock": True, "y": 270 },
                    "when": { "west": "tall" }
                }
            ]
        }
        wallPostModelJson = {
            "parent": "minecraft:block/template_wall_post",
            "textures": {
                "wall": workingNamespace + ":block/" + textureName
            }
        }
        wallSideModelJson = {
            "parent": "minecraft:block/template_wall_side",
            "textures": {
                "wall": workingNamespace + ":block/" + textureName
            }
        }
        wallSideTallModelJson = {
            "parent": "minecraft:block/template_wall_side_tall",
            "textures": {
                "wall": workingNamespace + ":block/" + textureName
            }
        }
        itemModelJson = {
            "parent": "minecraft:block/wall_inventory",
            "textures": {
                "wall": workingNamespace + ":block/" + textureName
            }
        }
        if not renderType == 0:
            wallPostModelJson["render_type"] = renderType
            wallSideModelJson["render_type"] = renderType
            wallSideTallModelJson["render_type"] = renderType
        
        #dump json files
        json.dump(blockstatesJson, open(dumpLocation + "blockstates/" + blockName + ".json", "w"), indent=2)
        json.dump(wallPostModelJson, open(dumpLocation + "models/block/" + blockName + "_post.json", "w"), indent=2)
        json.dump(wallSideModelJson, open(dumpLocation + "models/block/" + blockName + "_side.json", "w"), indent=2)
        json.dump(wallSideTallModelJson, open(dumpLocation + "models/block/" + blockName + "_side_tall.json", "w"), indent=2)
        json.dump(itemModelJson, open(dumpLocation + "models/item/" + blockName + ".json", "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 5
        self.generatedFileCount["blockstates"] += 1
        self.generatedFileCount["blockModels"] += 3
        self.generatedFileCount["itemModels"] += 1
        
        #add to tag list
        self.makeMinecraftDataFolder()
        if not os.path.exists(self.resourcesFolder + "data/minecraft/tags/blocks/"):
            os.makedirs(self.resourcesFolder + "data/minecraft/tags/blocks/")
        tagFolderLocation = self.resourcesFolder + "data/minecraft/tags/blocks/"
        if os.path.exists(tagFolderLocation + "walls.json"):
            woodenFencesTagJson = json.load(open(tagFolderLocation + "walls.json", "r"))
        else:
            woodenFencesTagJson = {
                "values": []
            }
            self.generatedFileCount["tags"] += 1
            self.generatedFileCount["total"] += 1
        if usingModNamespace:
            woodenFencesTagJson["values"].append(workingNamespace + ":" + blockName)
        else:
            woodenFencesTagJson["values"].append(fullBlockID)
        json.dump(woodenFencesTagJson, open(tagFolderLocation + "walls.json", "w"), indent=2)
        
    #*commands for adding items
    def addSimpleItem(self, fullItemID, usingModNamespace=True):
        dumpLocation = self.resourcesFolder + "assets/"
        workingNamespace = ""
        itemName = ""
        
        if usingModNamespace:
            workingNamespace = self.ModID
            itemName = fullItemID
            dumpLocation += (workingNamespace + "/")
        else:
            beforeColon = 1
            for letter in fullItemID:  #pull the namespace and block name
                if letter == ":":
                    beforeColon = 0
                if beforeColon:
                    dumpLocation += letter
                    workingNamespace += letter
                if beforeColon == 0 and letter != ":":
                    itemName += letter
            dumpLocation += "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "assets/" + self.ModID + "/":
            self.makeModAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/minecraft/":
            self.makeMinecraftAssetsFolder()
        if dumpLocation == self.resourcesFolder + "assets/forge/":
            self.makeForgeAssetsFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "models"):
            os.mkdir(dumpLocation + "models")
        if not os.path.exists(dumpLocation + "models/item"):
            os.mkdir(dumpLocation + "models/item")
            
        #dict for json file
        itemModelJson = {
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": workingNamespace + ":item/" + itemName
            }
        }
        
        #dump json files
        json.dump(itemModelJson, open(dumpLocation + "models/item/" + itemName + ".json", "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 1
        self.generatedFileCount["itemModels"] += 1
    
    #*commands for adding tags
    def addMinealbeToolTag(self, fullBlockID:str, requiredTool, usingModNamespace=True):
        realTool = False
        for tool in ["pickaxe", "shovel", "hoe", "axe"]:
            if tool == requiredTool:
                realTool = True
        if not realTool:
            return
        
        self.makeMinecraftDataFolder()
        if not os.path.exists(self.resourcesFolder + "data/minecraft/tags/blocks/mineable/"):
            os.makedirs(self.resourcesFolder + "data/minecraft/tags/blocks/mineable/")
        tagFolderLocation = self.resourcesFolder + "data/minecraft/tags/blocks/mineable/"
        
        if os.path.exists(tagFolderLocation + requiredTool + ".json"):
            woodenFencesTagJson = json.load(open(tagFolderLocation + requiredTool + ".json", "r"))
        else:
            woodenFencesTagJson = {
                "values": []
            }
            self.generatedFileCount["tags"] += 1
            self.generatedFileCount["total"] += 1
        if usingModNamespace:
            woodenFencesTagJson["values"].append(self.ModID + ":" + fullBlockID)
        else:
            woodenFencesTagJson["values"].append(fullBlockID)
        json.dump(woodenFencesTagJson, open(tagFolderLocation + requiredTool + ".json", "w"), indent=2)
        
    def addMinealbeToolTagList(self, fullBlockID:list[str], requiredTool, usingModNamespace=True):
        realTool = False
        for tool in ["pickaxe", "shovel", "hoe", "axe"]:
            if tool == requiredTool:
                realTool = True
        if not realTool:
            return
        
        self.makeMinecraftDataFolder()
        if not os.path.exists(self.resourcesFolder + "data/minecraft/tags/blocks/mineable/"):
            os.makedirs(self.resourcesFolder + "data/minecraft/tags/blocks/mineable/")
        tagFolderLocation = self.resourcesFolder + "data/minecraft/tags/blocks/mineable/"
        
        if os.path.exists(tagFolderLocation + requiredTool + ".json"):
            woodenFencesTagJson = json.load(open(tagFolderLocation + requiredTool + ".json", "r"))
        else:
            woodenFencesTagJson = {
                "values": []
            }
            self.generatedFileCount["tags"] += 1
            self.generatedFileCount["total"] += 1
        if usingModNamespace:
            for listItem in range(len(fullBlockID)):
                fullBlockID[listItem] = self.ModID + ":" + fullBlockID[listItem]
            woodenFencesTagJson["values"].extend(fullBlockID)
        else:
            woodenFencesTagJson["values"].extend(fullBlockID)
        json.dump(woodenFencesTagJson, open(tagFolderLocation + requiredTool + ".json", "w"), indent=2)
    
    def addRequireToolMaterialTag(self, fullBlockID:str, toolMaterial, usingModNamespace=True):
        realMaterial = False
        for material in ["stone", "iron", "diamond", "netherite"]:
            if material == toolMaterial:
                realMaterial = True
        if not realMaterial:
            return
        
        if toolMaterial == "netherite":
            self.makeForgeDataFolder()
            tagFolderLocation = self.resourcesFolder + "data/forge/"
        else:
            self.makeMinecraftDataFolder()
            tagFolderLocation = self.resourcesFolder + "data/minecraft/"
        if not os.path.exists(tagFolderLocation + "tags/blocks/"):
            os.makedirs(tagFolderLocation + "tags/blocks/")
        tagFolderLocation += "tags/blocks/"
        
        if os.path.exists(tagFolderLocation + "needs_" + toolMaterial + "_tool.json"):
            woodenFencesTagJson = json.load(open(tagFolderLocation + "needs_" + toolMaterial + "_tool.json", "r"))
        else:
            woodenFencesTagJson = {
                "values": []
            }
            self.generatedFileCount["tags"] += 1
            self.generatedFileCount["total"] += 1
        if usingModNamespace:
            woodenFencesTagJson["values"].append(self.ModID + ":" + fullBlockID)
        else:
            woodenFencesTagJson["values"].append(fullBlockID)
        json.dump(woodenFencesTagJson, open(tagFolderLocation + "needs_" + toolMaterial + "_tool.json", "w"), indent=2)
        
    def addRequireToolMaterialTagList(self, fullBlockID:list[str], toolMaterial, usingModNamespace=True):
        realMaterial = False
        for material in ["stone", "iron", "diamond", "netherite"]:
            if material == toolMaterial:
                realMaterial = True
        if not realMaterial:
            return
        
        if toolMaterial == "netherite":
            self.makeForgeDataFolder()
            tagFolderLocation = self.resourcesFolder + "data/forge/"
        else:
            self.makeMinecraftDataFolder()
            tagFolderLocation = self.resourcesFolder + "data/minecraft/"
        if not os.path.exists(tagFolderLocation + "tags/blocks/"):
            os.makedirs(tagFolderLocation + "tags/blocks/")
        tagFolderLocation += "tags/blocks/"
        
        if os.path.exists(tagFolderLocation + "needs_" + toolMaterial + "_tool.json"):
            woodenFencesTagJson = json.load(open(tagFolderLocation + "needs_" + toolMaterial + "_tool.json", "r"))
        else:
            woodenFencesTagJson = {
                "values": []
            }
            self.generatedFileCount["tags"] += 1
            self.generatedFileCount["total"] += 1
        if usingModNamespace:
            for listItem in range(len(fullBlockID)):
                fullBlockID[listItem] = self.ModID + ":" + fullBlockID[listItem]
            woodenFencesTagJson["values"].extend(fullBlockID)
        else:
            woodenFencesTagJson["values"].extend(fullBlockID)
        json.dump(woodenFencesTagJson, open(tagFolderLocation + "needs_" + toolMaterial + "_tool.json", "w"), indent=2)
    
    #*commands for adding recipes
    def addBasicShapelessRecipe(self, inputItemList: list[str], inputCountList: list[str], outputItem, outputCount: int, filename="", category="misc", recipeNamespace=0, usingModNamespace=True):
        dumpLocation = self.resourcesFolder + "data/"
        if usingModNamespace:
            dumpLocation += self.ModID + "/"
        else:
            dumpLocation += recipeNamespace + "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "data/" + self.ModID + "/":
            self.makeModDataFolder()
        if dumpLocation == self.resourcesFolder + "data/minecraft/":
            self.makeMinecraftDataFolder()
        if dumpLocation == self.resourcesFolder + "data/forge/":
            self.makeForgeDataFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "recipes"):
            os.mkdir(dumpLocation + "recipes")
        if not os.path.exists(dumpLocation + "recipes/crafting"):
            os.mkdir(dumpLocation + "recipes/crafting")
            
        dumpLocation += "recipes/crafting/"
        
        #recipe json dict
        recipeJson = {
            "type": "minecraft:crafting_shapeless",
            "category": category,
            "ingredients": [],
            "result": {
                "item": outputItem,
                "count": outputCount
            }
        }
        
        #add in input items
        for item, count in zip(inputItemList, inputCountList):
            recipeJson["ingredients"].append({
                "item": item,
                "count": count
            })
        
        #make filename
        if filename == "":
            colonFound = 0
            for letter in outputItem:
                if colonFound:
                    filename += letter
                if letter == ":":
                    colonFound = 1
            filename += "_from_"
            colonFound = 0
            for letter in inputItemList[0]:
                if colonFound:
                    filename += letter
                if letter == ":":
                    colonFound = 1
        if filename[-5:] != ".json":
            filename += ".json"
        
        #dump json files
        json.dump(recipeJson, open(dumpLocation + filename, "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 1
        self.generatedFileCount["recipes"] += 1
    
    def addShapedRecipe(self, patternList: list[str], keyList: list[str], keyItemList: list[str], outputItem, outputCount: int, filename="", category="misc", recipeNamespace=0, usingModNamespace=True):
        dumpLocation = self.resourcesFolder + "data/"
        if usingModNamespace:
            dumpLocation += self.ModID + "/"
        else:
            dumpLocation += recipeNamespace + "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "data/" + self.ModID + "/":
            self.makeModDataFolder()
        if dumpLocation == self.resourcesFolder + "data/minecraft/":
            self.makeMinecraftDataFolder()
        if dumpLocation == self.resourcesFolder + "data/forge/":
            self.makeForgeDataFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "recipes"):
            os.mkdir(dumpLocation + "recipes")
        if not os.path.exists(dumpLocation + "recipes/crafting"):
            os.mkdir(dumpLocation + "recipes/crafting")
            
        dumpLocation += "recipes/crafting/"
        
        #recipe json dict
        recipeJson = {
            "type": "minecraft:crafting_shaped",
            "category": "misc",
            "pattern": patternList,
            "key": {},
            "result": {
                "item": outputItem,
                "count": outputCount
            }
        }
        
        #add in input items
        for key, item in zip(keyList, keyItemList):
            recipeJson["key"][key] = {
                "item": item
            }
        
        #make filename
        if filename == "":
            colonFound = 0
            for letter in outputItem:
                if colonFound:
                    filename += letter
                if letter == ":":
                    colonFound = 1
            filename += "_from_"
            colonFound = 0
            for letter in keyItemList[0]:
                if colonFound:
                    filename += letter
                if letter == ":":
                    colonFound = 1
        if filename[-5:] != ".json":
            filename += ".json"
        
        #dump json files
        json.dump(recipeJson, open(dumpLocation + filename, "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 1
        self.generatedFileCount["recipes"] += 1
    
    def add9BlockStorageRecipe(self, smallItem: str, bigItem:str, category="misc", recipeNamespace=0, usingModNamespace=True):
        self.addBasicShapelessRecipe([bigItem], [1], smallItem, 9, recipeNamespace=recipeNamespace, usingModNamespace=usingModNamespace)
        self.addShapedRecipe([
                                "###",
                                "###",
                                "###"], ["#"], [smallItem], bigItem, 1, recipeNamespace=recipeNamespace, usingModNamespace=usingModNamespace)
        
    def add4BlockStorageRecipe(self, smallItem: str, bigItem:str, category="misc", recipeNamespace=0, usingModNamespace=True):
        self.addBasicShapelessRecipe([bigItem], [1], smallItem, 4, recipeNamespace=recipeNamespace, usingModNamespace=usingModNamespace)
        self.addShapedRecipe([
                                "##",
                                "##",], ["#"], [smallItem], bigItem, 1, recipeNamespace=recipeNamespace, usingModNamespace=usingModNamespace)
    
    def addSmeltingRecipe(self, inputItem: str, outputItem, filename="", category="misc", cookingTime=200, experience=.25, group="", recipeNamespace=0, usingModNamespace=True):
        dumpLocation = self.resourcesFolder + "data/"
        if usingModNamespace:
            dumpLocation += self.ModID + "/"
        else:
            dumpLocation += recipeNamespace + "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "data/" + self.ModID + "/":
            self.makeModDataFolder()
        if dumpLocation == self.resourcesFolder + "data/minecraft/":
            self.makeMinecraftDataFolder()
        if dumpLocation == self.resourcesFolder + "data/forge/":
            self.makeForgeDataFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "recipes"):
            os.mkdir(dumpLocation + "recipes")
        if not os.path.exists(dumpLocation + "recipes/smelting"):
            os.mkdir(dumpLocation + "recipes/smelting")
            
        dumpLocation += "recipes/smelting/"
        
        #recipe json dict
        recipeJson = {
            "type": "minecraft:smelting",
            "category": category,
            "cookingtime": cookingTime,
            "experience": experience,
            "ingredient": {
                "item": inputItem
            },
            "result": outputItem
        }
        if group != "":
            recipeJson["group"] = group
        
        #make filename
        if filename == "":
            colonFound = 0
            for letter in outputItem:
                if colonFound:
                    filename += letter
                if letter == ":":
                    colonFound = 1
            filename += "_from_"
            colonFound = 0
            for letter in inputItem:
                if colonFound:
                    filename += letter
                if letter == ":":
                    colonFound = 1
        if filename[-5:] != ".json":
            filename += ".json"
        
        #dump json files
        json.dump(recipeJson, open(dumpLocation + filename, "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 1
        self.generatedFileCount["recipes"] += 1
        
    def addBlastingRecipe(self, inputItem: str, outputItem, filename="", category="misc", cookingTime=100, experience=.25, group="", recipeNamespace=0, usingModNamespace=True):
        dumpLocation = self.resourcesFolder + "data/"
        if usingModNamespace:
            dumpLocation += self.ModID + "/"
        else:
            dumpLocation += recipeNamespace + "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "data/" + self.ModID + "/":
            self.makeModDataFolder()
        if dumpLocation == self.resourcesFolder + "data/minecraft/":
            self.makeMinecraftDataFolder()
        if dumpLocation == self.resourcesFolder + "data/forge/":
            self.makeForgeDataFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "recipes"):
            os.mkdir(dumpLocation + "recipes")
        if not os.path.exists(dumpLocation + "recipes/blasting"):
            os.mkdir(dumpLocation + "recipes/blasting")
            
        dumpLocation += "recipes/blasting/"
        
        #recipe json dict
        recipeJson = {
            "type": "minecraft:blasting",
            "category": category,
            "cookingtime": cookingTime,
            "experience": experience,
            "ingredient": {
                "item": inputItem
            },
            "result": outputItem
        }
        if group != "":
            recipeJson["group"] = group
        
        #make filename
        if filename == "":
            colonFound = 0
            for letter in outputItem:
                if colonFound:
                    filename += letter
                if letter == ":":
                    colonFound = 1
            filename += "_from_"
            colonFound = 0
            for letter in inputItem:
                if colonFound:
                    filename += letter
                if letter == ":":
                    colonFound = 1
        if filename[-5:] != ".json":
            filename += ".json"
        
        #dump json files
        json.dump(recipeJson, open(dumpLocation + filename, "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 1
        self.generatedFileCount["recipes"] += 1
    
    def addSmokingRecipe(self, inputItem: str, outputItem, filename="", category="misc", cookingTime=100, experience=.25, group="", recipeNamespace=0, usingModNamespace=True):
        dumpLocation = self.resourcesFolder + "data/"
        if usingModNamespace:
            dumpLocation += self.ModID + "/"
        else:
            dumpLocation += recipeNamespace + "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "data/" + self.ModID + "/":
            self.makeModDataFolder()
        if dumpLocation == self.resourcesFolder + "data/minecraft/":
            self.makeMinecraftDataFolder()
        if dumpLocation == self.resourcesFolder + "data/forge/":
            self.makeForgeDataFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "recipes"):
            os.mkdir(dumpLocation + "recipes")
        if not os.path.exists(dumpLocation + "recipes/smoking"):
            os.mkdir(dumpLocation + "recipes/smoking")
            
        dumpLocation += "recipes/smoking/"
        
        #recipe json dict
        recipeJson = {
            "type": "minecraft:smoking",
            "category": category,
            "cookingtime": cookingTime,
            "experience": experience,
            "ingredient": {
                "item": inputItem
            },
            "result": outputItem
        }
        if group != "":
            recipeJson["group"] = group
        
        #make filename
        if filename == "":
            colonFound = 0
            for letter in outputItem:
                if colonFound:
                    filename += letter
                if letter == ":":
                    colonFound = 1
            filename += "_from_"
            colonFound = 0
            for letter in inputItem:
                if colonFound:
                    filename += letter
                if letter == ":":
                    colonFound = 1
        if filename[-5:] != ".json":
            filename += ".json"
        
        #dump json files
        json.dump(recipeJson, open(dumpLocation + filename, "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 1
        self.generatedFileCount["recipes"] += 1
    
    def addCampfireRecipe(self, inputItem: str, outputItem, filename="", category="misc", cookingTime=600, experience=.25, group="", recipeNamespace=0, usingModNamespace=True):
        dumpLocation = self.resourcesFolder + "data/"
        if usingModNamespace:
            dumpLocation += self.ModID + "/"
        else:
            dumpLocation += recipeNamespace + "/"
        
        #make folders for namespace
        if dumpLocation == self.resourcesFolder + "data/" + self.ModID + "/":
            self.makeModDataFolder()
        if dumpLocation == self.resourcesFolder + "data/minecraft/":
            self.makeMinecraftDataFolder()
        if dumpLocation == self.resourcesFolder + "data/forge/":
            self.makeForgeDataFolder()
            
        #make inner folders
        if not os.path.exists(dumpLocation + "recipes"):
            os.mkdir(dumpLocation + "recipes")
        if not os.path.exists(dumpLocation + "recipes/campfire_cooking"):
            os.mkdir(dumpLocation + "recipes/campfire_cooking")
            
        dumpLocation += "recipes/campfire_cooking/"
        
        #recipe json dict
        recipeJson = {
            "type": "minecraft:campfire_cooking",
            "category": category,
            "cookingtime": cookingTime,
            "experience": experience,
            "ingredient": {
                "item": inputItem
            },
            "result": outputItem
        }
        if group != "":
            recipeJson["group"] = group
        
        #make filename
        if filename == "":
            colonFound = 0
            for letter in outputItem:
                if colonFound:
                    filename += letter
                if letter == ":":
                    colonFound = 1
            filename += "_from_"
            colonFound = 0
            for letter in inputItem:
                if colonFound:
                    filename += letter
                if letter == ":":
                    colonFound = 1
        if filename[-5:] != ".json":
            filename += ".json"
        
        #dump json files
        json.dump(recipeJson, open(dumpLocation + filename, "w"), indent=2)
        
        #update counts
        self.generatedFileCount["total"] += 1
        self.generatedFileCount["recipes"] += 1
    
    def addSmeltingGroupRecipe(self, inputItemList: list[str], outputItem, category="misc", cookingTime=200, experience=.25, group="", recipeNamespace=0, usingModNamespace=True):
        groupName = ""
        if group == "":
            colonFound = 0
            for letter in outputItem:
                if colonFound:
                    groupName += letter
                if letter == ":":
                    colonFound = 1
        else:
            groupName = group
        for inputItem in inputItemList:
            self.addSmeltingRecipe(inputItem, outputItem, group=groupName, category=category, cookingTime=cookingTime, experience=experience, recipeNamespace=recipeNamespace, usingModNamespace=usingModNamespace)
            
    def addBlastingGroupRecipe(self, inputItemList: list[str], outputItem, category="misc", cookingTime=200, experience=.25, group="", recipeNamespace=0, usingModNamespace=True):
        groupName = ""
        if group == "":
            colonFound = 0
            for letter in outputItem:
                if colonFound:
                    groupName += letter
                if letter == ":":
                    colonFound = 1
        else:
            groupName = group
        for inputItem in inputItemList:
            self.addBlastingRecipe(inputItem, outputItem, group=groupName, category=category, cookingTime=cookingTime, experience=experience, recipeNamespace=recipeNamespace, usingModNamespace=usingModNamespace)
            
    def addSmokingGroupRecipe(self, inputItemList: list[str], outputItem, category="misc", cookingTime=200, experience=.25, group="", recipeNamespace=0, usingModNamespace=True):
        groupName = ""
        if group == "":
            colonFound = 0
            for letter in outputItem:
                if colonFound:
                    groupName += letter
                if letter == ":":
                    colonFound = 1
        else:
            groupName = group
        for inputItem in inputItemList:
            self.addSmokingRecipe(inputItem, outputItem, group=groupName, category=category, cookingTime=cookingTime, experience=experience, recipeNamespace=recipeNamespace, usingModNamespace=usingModNamespace)
    
    #*commands for adding loottables
    
    #*commands for adding lood modifiers
    
#dataGenerator = DataGen("testmod", useForgeGenerated=False)
#dataGenerator.printFileCount()

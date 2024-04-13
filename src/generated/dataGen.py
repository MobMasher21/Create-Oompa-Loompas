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
        "itemModels": 0
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
        
    #*commands for adding items
    
    #*commands for adding tags
    
    #*commands for adding recipies
    
#dataGenerator = DataGen("testmod", useForgeGenerated=False)
#dataGenerator.addCubeBlock("testmod:myblock")
#dataGenerator.addButtonBlock("testmod:myblock_button", "myblock_button")
#dataGenerator.addDoorBlock("testmod:myblock_door", "myblock_door_top", "myblock_door_bottom", "myblock_door", renderType="cutout")

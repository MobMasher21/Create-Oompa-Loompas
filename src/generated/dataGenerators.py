import dataGen

dataGenerator = dataGen.DataGen("create_oompa_loompas")

dataGenerator.addSimpleItem("imagination_essence")
dataGenerator.addSimpleItem("imagination_crystal")
dataGenerator.addSimpleItem("imaginite_bar")

dataGenerator.addSimpleItem("snozzberry")

dataGenerator.addCubeBlock("imaginite_block")
dataGenerator.addCubeBlock("imagination_essence_block", renderType="translucent")

dataGenerator.addSlabBlock("imaginite_slab", "imaginite_block")
dataGenerator.addStairBlock("imaginite_stairs", "imaginite_block")
dataGenerator.addButtonBlock("imaginite_button", "imaginite_block")
dataGenerator.addPressurePlateBlock("imaginite_pressure_plate", "imaginite_block")
dataGenerator.addFenceBlock("imaginite_fence", "imaginite_block")
dataGenerator.addFenceGateBlock("imaginite_fence_gate", "imaginite_block")
dataGenerator.addWallBlock("imaginite_wall", "imaginite_block")
dataGenerator.addDoorBlock("imaginite_door", "imaginite_door_top", "imaginite_door_bottom", "imaginite_door", renderType="cutout")
dataGenerator.addTrapdoorBlock("imaginite_trapdoor", "imaginite_trapdoor")

dataGenerator.add9BlockStorageRecipe("create_oompa_loompas:imaginite_bar", "create_oompa_loompas:imaginite_block")
dataGenerator.add9BlockStorageRecipe("create_oompa_loompas:imagination_essence", "create_oompa_loompas:imagination_essence_block")

mineableWithPickaxe = ["imaginite_block", "imaginite_slab", "imaginite_stairs",
                       "imaginite_pressure_plate", "imaginite_fence", "imaginite_fence_gate",
                       "imaginite_wall", "imaginite_door", "imaginite_trapdoor",
                       "imagination_essence_block"]

needsIronToMine = ["imaginite_block", "imaginite_slab", "imaginite_stairs",
                   "imaginite_pressure_plate", "imaginite_fence", "imaginite_fence_gate",
                   "imaginite_wall", "imaginite_door", "imaginite_trapdoor",
                   "imagination_essence_block"]

dataGenerator.addMinealbeToolTagList(mineableWithPickaxe, "pickaxe")
dataGenerator.addRequireToolMaterialTagList(needsIronToMine, "iron")


dataGenerator.printFileCount()
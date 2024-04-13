import dataGen

dataGenerator = dataGen.DataGen("create_oompa_loompas")
dataGenerator.addCubeBlock("imaginite_block")
dataGenerator.addCubeBlock("imagination_essence_block", renderType="translucent")
dataGenerator.addButtonBlock("imaginite_button", "imaginite_block")
dataGenerator.addDoorBlock("imaginite_door", "imaginite_door_top", "imaginite_door_bottom", "imaginite_door", renderType="cutout")

dataGenerator.printFileCount()
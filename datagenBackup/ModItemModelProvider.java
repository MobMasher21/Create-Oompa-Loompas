package net.mobmasher21.create_oompa_loompas.datagen;

import net.minecraft.data.PackOutput;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraftforge.client.model.generators.ItemModelBuilder;
import net.minecraftforge.client.model.generators.ItemModelProvider;
import net.minecraftforge.common.data.ExistingFileHelper;
import net.minecraftforge.registries.RegistryObject;
import net.mobmasher21.create_oompa_loompas.CreateOompaLoompas;
import net.mobmasher21.create_oompa_loompas.item.ModItems;

public class ModItemModelProvider extends ItemModelProvider {
    public ModItemModelProvider(PackOutput output, ExistingFileHelper existingFileHelper) {
        super(output, CreateOompaLoompas.MOD_ID, existingFileHelper);
    }

    @Override
    protected void registerModels() {
        simpleItem(ModItems.IMAGINATION_CRYSTAL);
        simpleItem(ModItems.IMAGINATION_ESSENCE);
        simpleItem(ModItems.IMAGINITE_BAR);
    }

    private ItemModelBuilder simpleItem(RegistryObject<Item> item) {
        return withExistingParent(item.getId().getPath(),
                new ResourceLocation("item/generated")).texture("layer0",
                new ResourceLocation(CreateOompaLoompas.MOD_ID, "item/" + item.getId().getPath()));
    }
}

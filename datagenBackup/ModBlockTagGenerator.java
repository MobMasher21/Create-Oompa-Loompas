package net.mobmasher21.create_oompa_loompas.datagen;

import net.minecraft.core.HolderLookup;
import net.minecraft.data.PackOutput;
import net.minecraft.tags.BlockTags;
import net.minecraftforge.common.Tags;
import net.minecraftforge.common.data.BlockTagsProvider;
import net.minecraftforge.common.data.ExistingFileHelper;
import net.mobmasher21.create_oompa_loompas.CreateOompaLoompas;
import net.mobmasher21.create_oompa_loompas.block.ModBlocks;
import org.jetbrains.annotations.Nullable;

import java.util.concurrent.CompletableFuture;

public class ModBlockTagGenerator extends BlockTagsProvider {

    public ModBlockTagGenerator(PackOutput output, CompletableFuture<HolderLookup.Provider> lookupProvider, @Nullable ExistingFileHelper existingFileHelper) {
        super(output, lookupProvider, CreateOompaLoompas.MOD_ID, existingFileHelper);
    }

    @Override
    protected void addTags(HolderLookup.Provider pProvider) {
        //this.tag(BlockTags.NEEDS_STONE_TOOL);
        this.tag(BlockTags.NEEDS_IRON_TOOL)
                .add(ModBlocks.IMAGINITE_BLOCK.get(),
                        ModBlocks.IMAGINATION_ESSENCE_BLOCK.get());
        //this.tag(BlockTags.NEEDS_DIAMOND_TOOL);
        //this.tag(Tags.Blocks.NEEDS_NETHERITE_TOOL);

        //this.tag(BlockTags.MINEABLE_WITH_AXE);
        this.tag(BlockTags.MINEABLE_WITH_PICKAXE)
                .add(ModBlocks.IMAGINITE_BLOCK.get(),
                        ModBlocks.IMAGINATION_ESSENCE_BLOCK.get());
        //this.tag(BlockTags.MINEABLE_WITH_SHOVEL);
        //this.tag(BlockTags.MINEABLE_WITH_HOE);
    }
}

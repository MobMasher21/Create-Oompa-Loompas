package net.mobmasher21.create_oompa_loompas.item;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;
import net.mobmasher21.create_oompa_loompas.CreateOompaLoompas;
import net.mobmasher21.create_oompa_loompas.block.ModBlocks;

public class ModCreativeModTabs {
    public static final DeferredRegister<CreativeModeTab>  CREATIVE_MODE_TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, CreateOompaLoompas.MOD_ID);

    public static final RegistryObject<CreativeModeTab> OOMPA_LOOMPA_TAB = CREATIVE_MODE_TABS.register("oompa_loompa_tab",
            () -> CreativeModeTab.builder().icon(() -> new ItemStack(ModItems.IMAGINATION_ESSENCE.get()))
                    .title(Component.translatable("creativetab.oompa_loompa_tab"))
                    .displayItems((pParameters, pOutput) -> {
                        pOutput.accept(ModItems.IMAGINATION_ESSENCE.get());
                        pOutput.accept(ModItems.IMAGINATION_CRYSTAL.get());
                        pOutput.accept(ModItems.IMAGINITE_BAR.get());

                        pOutput.accept(ModBlocks.IMAGINITE_BLOCK.get());
                        pOutput.accept(ModBlocks.IMAGINITE_STAIRS.get());
                        pOutput.accept(ModBlocks.IMAGINITE_SLAB.get());
                        pOutput.accept(ModBlocks.IMAGINITE_BUTTON.get());
                        pOutput.accept(ModBlocks.IMAGINITE_PRESSURE_PLATE.get());
                        pOutput.accept(ModBlocks.IMAGINITE_FENCE.get());
                        pOutput.accept(ModBlocks.IMAGINITE_FENCE_GATE.get());
                        pOutput.accept(ModBlocks.IMAGINITE_WALL.get());
                        pOutput.accept(ModBlocks.IMAGINITE_DOOR.get());
                        pOutput.accept(ModBlocks.IMAGINITE_TRAPDOOR.get());

                        pOutput.accept(ModBlocks.IMAGINATION_ESSENCE_BLOCK.get());

                        pOutput.accept(ModItems.SNOZZBERRY.get());
                    })
                    .build());

    public static void register(IEventBus eventBus) {
        CREATIVE_MODE_TABS.register(eventBus);
    }
}

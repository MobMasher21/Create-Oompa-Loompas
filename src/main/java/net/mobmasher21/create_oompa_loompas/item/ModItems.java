package net.mobmasher21.create_oompa_loompas.item;

import net.minecraft.world.item.Item;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;
import net.mobmasher21.create_oompa_loompas.CreateOompaLoompas;

public class ModItems {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, CreateOompaLoompas.MOD_ID);

    public static final RegistryObject<Item> IMAGINATION_CRYSTAL = ITEMS.register("imagination_crystal", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> IMAGINATION_ESSENCE = ITEMS.register("imagination_essence", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> IMAGINITE_BAR = ITEMS.register("imaginite_bar", () -> new Item(new Item.Properties()));

    public static final RegistryObject<Item> SNOZZBERRY = ITEMS.register("snozzberry", () -> new Item(new Item.Properties().food(ModFoods.SNOZZBERRY)));

    public static void register(IEventBus eventBus) {
        ITEMS.register(eventBus);
    }
}

package net.mobmasher21.create_oompa_loompas.datagen;

import net.minecraft.data.PackOutput;
import net.minecraft.data.recipes.*;
import net.minecraft.world.item.crafting.*;
import net.minecraft.world.level.ItemLike;
import net.minecraftforge.common.crafting.conditions.IConditionBuilder;
import net.mobmasher21.create_oompa_loompas.CreateOompaLoompas;
import net.mobmasher21.create_oompa_loompas.block.ModBlocks;
import net.mobmasher21.create_oompa_loompas.item.ModItems;

import java.util.List;
import java.util.function.Consumer;

public class ModRecipeProvider extends RecipeProvider implements IConditionBuilder {
    public ModRecipeProvider(PackOutput pOutput) {
        super(pOutput);
    }

    private static List<ItemLike> ItemPackingSmallItems = List.of(
            ModItems.IMAGINITE_BAR.get(),
            ModItems.IMAGINATION_ESSENCE.get()
    );
    private static List<ItemLike> ItemPackingPackedItems = List.of(
            ModBlocks.IMAGINITE_BLOCK.get(),
            ModBlocks.IMAGINATION_ESSENCE_BLOCK.get()
    );

    @Override
    protected void buildRecipes(Consumer<FinishedRecipe> pWriter) {
        /*
        ShapedRecipeBuilder.shaped(RecipeCategory.MISC, ModBlocks.IMAGINITE_BLOCK.get())
                .pattern("###")
                .pattern("###")
                .pattern("###")
                .define('#', ModItems.IMAGINITE_BAR.get())
                .unlockedBy(getHasName(ModItems.IMAGINITE_BAR.get()), has(ModItems.IMAGINITE_BAR.get())).save(pWriter);
        ShapedRecipeBuilder.shaped(RecipeCategory.MISC, ModBlocks.IMAGINATION_ESSENCE_BLOCK.get())
                .pattern("###")
                .pattern("###")
                .pattern("###")
                .define('#', ModItems.IMAGINATION_ESSENCE.get())
                .unlockedBy(getHasName(ModItems.IMAGINATION_ESSENCE.get()), has(ModItems.IMAGINATION_ESSENCE.get())).save(pWriter);

        ShapelessRecipeBuilder.shapeless(RecipeCategory.MISC, ModItems.IMAGINITE_BAR.get(), 9)
                .requires(ModBlocks.IMAGINITE_BLOCK.get())
                .unlockedBy(getHasName(ModBlocks.IMAGINITE_BLOCK.get()), has(ModBlocks.IMAGINITE_BLOCK.get())).save(pWriter);
        ShapelessRecipeBuilder.shapeless(RecipeCategory.MISC, ModItems.IMAGINATION_ESSENCE.get(), 9)
                .requires(ModBlocks.IMAGINATION_ESSENCE_BLOCK.get())
                .unlockedBy(getHasName(ModBlocks.IMAGINATION_ESSENCE_BLOCK.get()), has(ModBlocks.IMAGINATION_ESSENCE_BLOCK.get())).save(pWriter);
         */
        createAll9ItemPacking(ItemPackingSmallItems, ItemPackingPackedItems, pWriter);
    }

    protected static void oreSmelting(Consumer<FinishedRecipe> pFinishedRecipeConsumer, List<ItemLike> pIngredients, RecipeCategory pCategory, ItemLike pResult, float pExperience, int pCookingTIme, String pGroup) {
        oreCooking(pFinishedRecipeConsumer, RecipeSerializer.SMELTING_RECIPE, pIngredients, pCategory, pResult, pExperience, pCookingTIme, pGroup, "_from_smelting");
    }

    protected static void oreBlasting(Consumer<FinishedRecipe> pFinishedRecipeConsumer, List<ItemLike> pIngredients, RecipeCategory pCategory, ItemLike pResult, float pExperience, int pCookingTime, String pGroup) {
        oreCooking(pFinishedRecipeConsumer, RecipeSerializer.BLASTING_RECIPE, pIngredients, pCategory, pResult, pExperience, pCookingTime, pGroup, "_from_blasting");
    }

    protected static void foodSmoking(Consumer<FinishedRecipe> pFinishedRecipeConsumer, List<ItemLike> pIngredients, RecipeCategory pCategory, ItemLike pResult, float pExperience, int pCookingTime, String pGroup) {
        oreCooking(pFinishedRecipeConsumer, RecipeSerializer.SMOKING_RECIPE, pIngredients, pCategory, pResult, pExperience, pCookingTime, pGroup, "_from_blasting");
    }

    protected static void oreCooking(Consumer<FinishedRecipe> pFinishedRecipeConsumer, RecipeSerializer<? extends AbstractCookingRecipe> pCookingSerializer, List<ItemLike> pIngredients, RecipeCategory pCategory, ItemLike pResult, float pExperience, int pCookingTime, String pGroup, String pRecipeName) {
        for(ItemLike itemlike : pIngredients) {
            SimpleCookingRecipeBuilder.generic(Ingredient.of(itemlike), pCategory, pResult, pExperience, pCookingTime, pCookingSerializer).group(pGroup)
                    .unlockedBy(RecipeProvider.getHasName(itemlike), RecipeProvider.has(itemlike))
                    .save(pFinishedRecipeConsumer, CreateOompaLoompas.MOD_ID + ":"+ (pResult) + pRecipeName + "_" + RecipeProvider.getItemName(itemlike));
        }

    }

    protected static void createAll9ItemPacking(List<ItemLike> smallItemList, List<ItemLike> packedItemList, Consumer<FinishedRecipe> pWriter) {
        for(int i = 0; i < smallItemList.size(); i++) {
            ItemLike smallItem = smallItemList.get(i);
            ItemLike packedItem = packedItemList.get(i);

            ShapedRecipeBuilder.shaped(RecipeCategory.MISC, packedItem)
                    .pattern("###")
                    .pattern("###")
                    .pattern("###")
                    .define('#', smallItem)
                    .unlockedBy(RecipeProvider.getHasName(smallItem), RecipeProvider.has(smallItem)).save(pWriter);
            ShapelessRecipeBuilder.shapeless(RecipeCategory.MISC, smallItem, 9)
                    .requires(packedItem)
                    .unlockedBy(RecipeProvider.getHasName(packedItem), RecipeProvider.has(packedItem)).save(pWriter);
        }
    }

}

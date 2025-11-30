#Use these test serums to test the MC serum screen.

init 2 python:
    list_of_mc_traits: list[MC_Serum_Trait] = []
    # from game.main_character.mc_serum_trait_ren import list_of_mc_traits
    mc_serum_feat_dick_growth_test = MC_Serum_Trait("Serum: Dick Growth Test", "Human Growth Rebooter", "anatomical", [perk_test_feat_dick_growth_01, perk_test_feat_dick_growth_02, perk_test_feat_dick_growth_03], [perk_feat_dick_growth_test_advance_req_01], "perk_test_label")
#     mc_serum_aura_test = MC_Serum_Trait("Serum: Aura Test", "Mood Enhancer", "aura", [perk_test_aura_01, perk_test_aura_02, perk_test_aura_03], [perk_aura_test_advance_req_01], "perk_test_label")
#     mc_serum_cum_test = MC_Serum_Trait("Serum: Cum Test", "Fertility Enhancement", "cum", [perk_test_cum_01, perk_test_cum_02, perk_test_cum_03], [perk_cum_test_advance_req_01], "perk_test_label")
#     mc_serum_physical_test = MC_Serum_Trait("Serum: Physical Test", "Breast Enhancement", "physical", [perk_test_physical_01, perk_test_physical_02, perk_test_physical_03], [perk_physical_test_advance_req_01], "perk_test_label")
#
    list_of_mc_traits.append(mc_serum_feat_dick_growth_test)
#     list_of_mc_traits.append(mc_serum_aura_test)
#     list_of_mc_traits.append(mc_serum_cum_test)
#     list_of_mc_traits.append(mc_serum_physical_test)
#
init 1 python:
#     def test_mc_serum_01():
#         mc_serum_aura_obedience.apply_trait()
#         mc_serum_cum_obedience.apply_trait()
#         mc_serum_energy_regen.apply_trait()
#         mc_serum_feat_orgasm_control.apply_trait()
#         return
#
#     def perk_test_energy_01():
#         return Ability_Perk(description = "Test Energy Perk 1.")
#
#     def perk_test_energy_02():
#         return Ability_Perk(description = "Test Energy Perk 2.")
#
#     def perk_test_energy_03():
#         return Ability_Perk(description = "Test Energy Perk 3.")
#
#     def perk_energy_test_advance_req_01():
#         return False
#
#     def perk_test_aura_01():
#         return Ability_Perk(description = "Test aura Perk 1.")
#
#     def perk_test_aura_02():
#         return Ability_Perk(description = "Test aura Perk 2.")
#
#     def perk_test_aura_03():
#         return Ability_Perk(description = "Test aura Perk 3.")
#
#     def perk_aura_test_advance_req_01():
#         return False
#
#     def perk_test_cum_01():
#         return Ability_Perk(description = "Test cum Perk 1.")
#
#     def perk_test_cum_02():
#         return Ability_Perk(description = "Test cum Perk 2.")
#
#     def perk_test_cum_03():
#         return Ability_Perk(description = "Test cum Perk 3.")
#
#     def perk_cum_test_advance_req_01():
#         return False
#
    def perk_test_feat_dick_growth_01():
        return Ability_Perk(description = "Test physical Perk 1.")

    def perk_test_feat_dick_growth_02():
        return Ability_Perk(description = "Test physical Perk 2.")

    def perk_test_feat_dick_growth_03():
        return Ability_Perk(description = "Test physical Perk 3.")

    def perk_feat_dick_growth_test_advance_req_01():
        return False
#
label perk_test_label(the_person):
    pass
    return

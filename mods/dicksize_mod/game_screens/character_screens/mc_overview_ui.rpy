screen mc_character_sheet():
    add paper_background_image
    modal True
    zorder 100

    #jes: Add tooltip for dick size
    if mc.dick_size > 2:
        default dick_size_tooltip = "Quite a bit bigger then the average."
    elif mc.dick_size > 4:
        default dick_size_tooltip = "A huge dick."
    elif mc.dick_size > 6:
        default dick_size_tooltip = "A freakishly large."
    else:
        default dick_size_tooltip  = "A perfectly average sized cock. "

    vbox:
        xanchor 0.5
        xalign 0.5
        yalign 0.2
        frame:
            background "#1a45a1aa"
            vbox:
                xsize 1620
                text "[mc.name] [mc.last_name]" style "menu_text_header_style" size 40 xanchor 0.5 xalign 0.5
                text "Owner of: [mc.business.name]" style "menu_text_style" size 30 xanchor 0.5 xalign 0.5
        null height 60
        hbox:
            xanchor 0.5
            xalign 0.5
            yalign 0.4
            spacing 40
            frame:
                background "#1a45a1aa"
                xalign 0.5
                xanchor 0.5
                vbox:
                    frame:
                        background None
                        xsize 500
                        text "Main Stats" style "menu_text_title_style" size 32 xalign 0.5
                    frame:
                        background None
                        xysize (500, 300)
                        xalign 0.5
                        vbox:
                            xalign 0.5
                            hbox:
                                xalign 0.5
                                text "Unspent Points: [mc.free_stat_points]"  style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1 ([mc.buy_point_cost] Clarity)":
                                    xalign 0.5 style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 yanchor 0.5 yalign 0.5
                                    action Function(mc.buy_point, "stat", mc.buy_point_cost) sensitive mc.free_clarity >= mc.buy_point_cost

                            hbox:
                                xalign 0.5
                                text f"Charisma: {mc.charisma}/{max(mc.max_stats, mc.charisma)}" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 xalign 0.5 action Function(mc.improve_stat, "cha") sensitive mc.free_stat_points > 0 and mc.charisma<mc.max_stats yanchor 0.5 yalign 0.5

                            hbox:
                                xalign 0.5
                                text f"Intelligence: {mc.int}/{max(mc.max_stats, mc.int)}" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 xalign 0.5 action Function(mc.improve_stat, "int") sensitive mc.free_stat_points > 0 and mc.int<mc.max_stats yanchor 0.5 yalign 0.5

                            hbox:
                                xalign 0.5
                                text f"Focus: {mc.focus}/{max(mc.max_stats, mc.focus)}" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 xalign 0.5 action Function(mc.improve_stat, "foc") sensitive mc.free_stat_points > 0 and mc.focus<mc.max_stats yanchor 0.5 yalign 0.5

                    use mc_goal_bar(mc.stat_goal)

            frame:
                background "#1a45a1aa"
                xalign 0.5
                xanchor 0.5
                vbox:
                    frame:
                        background None
                        xsize 500
                        text "Work Skills" style "menu_text_title_style" size 32 xalign 0.5
                    frame:
                        background None
                        xysize (500, 300)
                        xalign 0.5
                        vbox:
                            xalign 0.5
                            hbox:
                                xalign 0.5
                                text "Unspent Points: [mc.free_work_points]" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1 ([mc.buy_point_cost] Clarity)":
                                    xalign 0.5 style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 yanchor 0.5 yalign 0.5
                                    action Function(mc.buy_point, "work", mc.buy_point_cost) sensitive mc.free_clarity >= mc.buy_point_cost
                            hbox:
                                xalign 0.5
                                text f"Human Resources: {mc.hr_skill}/{max(mc.max_work_skills, mc.hr_skill)}" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 xalign 0.5 action Function(mc.improve_work_skill, "hr") sensitive mc.free_work_points > 0 and mc.hr_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                            hbox:
                                xalign 0.5
                                text f"Marketing: {mc.market_skill}/{max(mc.max_work_skills, mc.market_skill)}" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 xalign 0.5 action Function(mc.improve_work_skill, "market") sensitive mc.free_work_points > 0 and mc.market_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                            hbox:
                                xalign 0.5
                                text f"Research and Development: {mc.research_skill}/{max(mc.max_work_skills, mc.research_skill)}" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 xalign 0.5 action Function(mc.improve_work_skill, "research") sensitive mc.free_work_points > 0 and mc.research_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                            hbox:
                                xalign 0.5
                                text f"Production: {mc.production_skill}/{max(mc.max_work_skills, mc.production_skill)}" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 xalign 0.5 action Function(mc.improve_work_skill, "production") sensitive mc.free_work_points > 0 and mc.production_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                            hbox:
                                xalign 0.5
                                text f"Supply Procurement: {mc.supply_skill}/{max(mc.max_work_skills, mc.supply_skill)}" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 xalign 0.5 action Function(mc.improve_work_skill, "supply") sensitive mc.free_work_points > 0 and mc.supply_skill < mc.max_work_skills yanchor 0.5 yalign 0.5

                    use mc_goal_bar(mc.work_goal)

            frame:
                background "#1a45a1aa"
                xalign 0.5
                xanchor 0.5
                vbox:
                    frame:
                        background None
                        xsize 500
                        text "Sex Skills" style "menu_text_title_style" size 32 xalign 0.5
                    frame:
                        background None
                        xysize (500, 300)
                        xalign 0.5
                        vbox:
                            xalign 0.5
                            hbox:
                                xalign 0.5
                                text "Unspent Points: [mc.free_sex_points]" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1 ([mc.buy_point_cost] Clarity)":
                                    xalign 0.5 style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 yanchor 0.5 yalign 0.5
                                    action Function(mc.buy_point, "sex", mc.buy_point_cost) sensitive mc.free_clarity >= mc.buy_point_cost
                            hbox:
                                xalign 0.5
                                text f"Stamina: {mc.max_energy}/{mc.max_energy_cap}" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 xalign 0.5 action Function(mc.improve_sex_skill, "stam") sensitive mc.free_sex_points > 0 and mc.max_energy<mc.max_energy_cap yanchor 0.5 yalign 0.5
                            hbox:
                                xalign 0.5
                                text f"Foreplay: {mc.foreplay_sex_skill}/{max(mc.max_sex_skills, mc.foreplay_sex_skill)}" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 xalign 0.5 action Function(mc.improve_sex_skill, "Foreplay") sensitive mc.free_sex_points > 0 and mc.foreplay_sex_skill<mc.max_sex_skills yanchor 0.5 yalign 0.5
                            hbox:
                                xalign 0.5
                                text f"Oral: {mc.oral_sex_skill}/{max(mc.max_sex_skills, mc.oral_sex_skill)}" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 xalign 0.5 action Function(mc.improve_sex_skill, "Oral") sensitive mc.free_sex_points > 0 and mc.oral_sex_skill<mc.max_sex_skills yanchor 0.5 yalign 0.5
                            hbox:
                                xalign 0.5
                                text f"Vaginal: {mc.vaginal_sex_skill}/{max(mc.max_sex_skills, mc.vaginal_sex_skill)}" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 xalign 0.5 action Function(mc.improve_sex_skill, "Vaginal") sensitive mc.free_sex_points > 0 and mc.vaginal_sex_skill<mc.max_sex_skills yanchor 0.5 yalign 0.5
                            hbox:
                                xalign 0.5
                                text f"Anal: {mc.anal_sex_skill}/{max(mc.max_sex_skills, mc.anal_sex_skill)}" style "menu_text_style" xalign 0.5 yalign 0.5
                                textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" text_size 14 yoffset -4 xalign 0.5 action Function(mc.improve_sex_skill, "Anal") sensitive mc.free_sex_points > 0 and mc.anal_sex_skill<mc.max_sex_skills yanchor 0.5 yalign 0.5
                            hbox: #jes: Add info for dick size
                                null:
                                    height 75
                                xalign 0.5
                                if persistent.use_imperial_system:
                                    text f"Dick Size: {4+mc.dick_size}″" style "menu_text_style" xalign 0.5 yalign 0.5
                                else:
                                    text f"Dick Size: {10+mc.dick_size*2.5} cm" style "menu_text_style" xalign 0.5 yalign 0.5
                                null:
                                    height 75
                                textbutton "{image=question_mark_small}":
                                    style "transparent_style"
                                    tooltip dick_size_tooltip
                                    action NullAction()
                                    
                    use mc_goal_bar(mc.sex_goal)
    
    #jes: Add to show tooltips
    use default_tooltip("mc_character_sheet")

    frame:
        background None
        align (0.5, 0.98)
        xysize (300, 150)
        imagebutton:
            align (0.5, 0.5)
            auto "gui/button/choice_%s_background.png"
            focus_mask True
            action Hide("mc_character_sheet")
        textbutton "Return" align (0.5, 0.5) text_style "return_button_style"

screen mc_goal_bar(goal):
    frame:
        background "#0a142688"
        xysize (500, 250)
        vbox:
            xalign 0.5
            if goal:
                text "Goal: [goal.name]" style "menu_text_style" xalign 0.5 size 24
                frame:
                    background None
                    ysize 100
                    xalign 0.5
                    text "[goal.description]" style "menu_text_style" xalign 0.5
                frame:
                    ysize 60
                    xalign 0.5
                    background None
                    bar value goal.progress_fraction range 1.0 xalign 0.5 ysize 50 xfill True
                    textbutton "{color=#fff}[goal.progress_string]{/color}":
                        style "transparent_style"
                        text_style "menu_text_title_style"
                        xfill True
                        yalign 0.5
                if goal.completed:
                    textbutton "Collect Reward" xalign 0.5 action Function(mc.complete_goal, goal) style "textbutton_green_style" text_style "textbutton_text_style"
                else:
                    textbutton "Replace Goal (1/day)" xalign 0.5 action Function(mc.scrap_goal, goal) style "textbutton_style" text_style "textbutton_text_style" sensitive mc.scrap_goal_available
            else:
                text "Goal: No goals available!" style "menu_text_style" xalign 0.5

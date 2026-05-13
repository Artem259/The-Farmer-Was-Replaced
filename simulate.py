sim_items = {Items.Power : 10**6}
run_time = simulate("main", Unlocks, sim_items, {}, 0, 512)
quick_print(run_time)

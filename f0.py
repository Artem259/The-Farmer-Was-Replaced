clear()
sim_items = {Items.Hay: 10**9, Items.Wood: 10**9, Items.Power: 10**6, Items.Water: 10**6, Items.Fertilizer: 10**6}
run_time = simulate("main", Unlocks, sim_items, {}, 0, 1024)
quick_print((run_time - 5) / 5)

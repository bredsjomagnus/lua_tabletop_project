def dijkstra_search(self, start, unit):
        """
        Search out and store all hexes, with its cost, that can be reached with (int) mp movement points from (Hex) start
        """
        movement_type = unit.get_movement_type()
        mp = unit.get_movement_points()
        unit_allegiance = unit.get_allegiance()

        # print("movement_type:", movement_type)
        # print("mp:", mp)

        startHex = self.Hex(start.q, start.r, start.s)
        frontier = PriorityQueue() # fronten som rullar fram över griden och stannar när man uppnått movement cost; cost_so_far
        frontier.put(startHex, 0) # lägger in starten i fronten som första hex att kolla ifrån
        came_from = {} # en dict med info om vilka hexagoner man kommer ifrån; {'gick till denna hex': 'från denna hex'}
        cost_so_far = {} # en dict med vad det kostat så här långt att ta sig; {'till denna hex': 'har det som minst kostat detta'}

        came_from[startHex] = None # Lägger in första rutan i vart man kommit ifrån
        cost_so_far[startHex] = 0 # lägger kostnaden från starthexagonen

        while not frontier.empty(): # så länge det finns hexagoner att kolla av i fronten

            # ta ut en prioriterad hex i fronten där den där de med lägst kostnad, cost_so_far, prioriteras
            currentHex = frontier.get() #currentHex är inte objectet Hex utan collection Hex(q, r, s) (vilket ställer till det något)
            current_q = currentHex.q #tar ut q och r för att kunna hämta objektet Hex
            current_r = currentHex.r
            try: # försök hämta nuvarande hex och kolla dess grannar. Kan hända att man hamnar utanför kartan och då avbryter man
                current = self.getHex(current_q, current_r) # hämta hexobjectet current via q och r från currentHex

                # self.hex_neighbors_prio_roads(current)
                # gå igenom alla grannarna i nuvarande prioriterade hexagon.
                for next in self.hex_neighbors(current):
                    next_q = next.q # på grund av att inte heller next blir objectet Hex utan collection Hex behöver vi ta fram q och r för att fixa det
                    next_r = next.r
                    next_hex = self.getHex(next_q, next_r) # hämtar hexobjectet via q och r från (collection) next

                    next_cost = self.getCost(current, next_hex, unit) # kostnaden att ta sig beroende på vägar, terräng och enhetstyp
                    new_cost = cost_so_far[currentHex] + next_cost # lägg till detta till totala kostnaden

                    actual_mp = mp

                    # try:
                    #     path = self.reconstruct_path(came_from, startHex, currentHex) # så får man path på rad i en lista till currentHex från starthexen

                    #     if self.checkPath(path) and movement_type == 'mechanized': # är pathen fram till den hex man kollar nu enbart roads?
                    #         if self.fromHexEdge(current, next_hex) == 'road': # är hexedgen från nuvarande till nästa en road?
                    #             actual_mp = mp + 1 # Då kan man gå ett steg extra
                    #             # actual_mp = mp
                    # except Exception as e:
                    #     print("path error:", e)

                    actual_mp, new_cost = self.check_for_enemy_zoc(actual_mp, new_cost, current, next_hex, unit_allegiance)
                    actual_mp = self.check_for_enemy_units(actual_mp, next_hex, unit_allegiance)
                    new_cost = self.check_for_river_crossings(current, next_hex, new_cost, actual_mp)

                    # om grannen inte redan är kollad eller om kostnaden till grannen ligger inne men nu är lägre
                    if next not in cost_so_far or new_cost < cost_so_far[next]:

                        if new_cost <= actual_mp:
                            cost_so_far[next] = new_cost # lägg till eller ersätt kostnaden till denna grannen
                            priority = new_cost # prioriteringen bestäms av kostnaden
                            frontier.put(next, priority) # lägg in eller ersätt grannen i fronten med en viss prioritering baserat på vilken kostnad det är att ta sig dit
                            came_from[next] = currentHex # lägg in vart man kom ifrån till denna grannen


            except Exception as e:
                print(e) # hamnade visst utanför kartan

        return came_from, cost_so_far

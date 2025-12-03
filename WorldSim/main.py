from simulation import World, Event

def main():
    world = World()

    print("=== Simulation CLI ===")
    print("Commands:")
    print(" spawn TYPE x y [health]")
    print(" move ENTITY_ID dx dy")
    print(" damage ENTITY_ID amount")
    print(" tick N")
    print(" save filename")
    print(" load filename")
    print(" print")
    print(" quit")
    print("------------------------")

    while True:
        cmd = input("> ").strip().split()

        if not cmd:
            continue

        action = cmd[0]

        # ---------- QUIT ----------
        if action == "quit":
            print("Exiting simulation...")
            break

        # ---------- PRINT ----------
        elif action == "print":
            world.print_state()

        # ---------- SPAWN ----------
        elif action == "spawn":
            # spawn TYPE x y [health]
            if len(cmd) < 4:
                print("Usage: spawn TYPE x y [health]")
                continue

            type = cmd[1]
            x = int(cmd[2])
            y = int(cmd[3])
            health = int(cmd[4]) if len(cmd) > 4 else 100

            world.spawn_entity(type, x, y, health)
            print(f"Spawned {type} at ({x},{y})")

        # ---------- MOVE ----------
        elif action == "move":
            # move ENTITY_ID dx dy
            if len(cmd) != 4:
                print("Usage: move ENTITY_ID dx dy")
                continue

            eid = int(cmd[1])
            dx = int(cmd[2])
            dy = int(cmd[3])

            ev = Event("move", eid, {"dx": dx, "dy": dy})
            world.schedule_event(world.tick, ev)
            print(f"Scheduled move for {eid}: dx={dx}, dy={dy}")

        # ---------- DAMAGE ----------
        elif action == "damage":
            # damage ENTITY_ID amount
            if len(cmd) != 3:
                print("Usage: damage ENTITY_ID amount")
                continue

            eid = int(cmd[1])
            amt = int(cmd[2])

            ev = Event("damage", eid, {"amount": amt})
            world.schedule_event(world.tick, ev)
            print(f"Scheduled damage for {eid}: amount={amt}")

        # ---------- ADVANCE TICKS ----------
        elif action == "tick":
            if len(cmd) != 2:
                print("Usage: tick N")
                continue

            N = int(cmd[1])
            world.run(N)

        # ---------- SAVE ----------
        elif action == "save":
            if len(cmd) != 2:
                print("Usage: save filename")
                continue

            world.save_world(cmd[1])

        # ---------- LOAD ----------
        elif action == "load":
            if len(cmd) != 2:
                print("Usage: load filename")
                continue

            world.load_world(cmd[1])

        else:
            print("Unknown command:", action)



if __name__ == "__main__":
    main()
